[TOC]

## Importing Packages 
```python exec="1" source="above"  session="requests"
import requests # to fetch info from URLs
import lxml.etree as ET # to parse XML documents
```

We will use the `fetch` function as described in our earlier tutorial on Special Exports, provided here for reference.

```python exec="true" source="above"   session="requests" 
def fetch(title):
    url = f'https://de.wiktionary.org/wiki/Spezial:Exportieren/{title}'
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text
```

Let us fetch the XML content for the page titled `'schön'` as an example. 


```python exec="true" source="tabbed-left" result="xml" session="requests"
xml_content = fetch('schön')
print(xml_content[:500])
print(f'{type(xml_content) = }')
```

## Parsing the XML content

Now that we have retrieved the XML content, we will use `lxml.etree` to parse it. 

In order to parse an XML *string*, which is what `fetch` returns, we will use the  `fromstring` method. Later we will use the `parse` method to parse an XML *file*.
 
 
```python exec="true" source="tabbed-left" result="pycon" session="requests"
# Parse the XML content into an ET Element
root = ET.fromstring(xml_content)

print(type(root)) # Output: <class 'lxml.etree._Element'>
```

`ET.fromstring` returns an `Element` object with several useful properties.  
From an `Element` object, you can extract:

- its tag `<tag_name> ... </tag_name>`, using `Element.tag`
- its attributes `<tag_name attribut1="value1" attrib2="value2"> ...`, using `Element.attrib`
- its text `<tag_name attribut1="value1"> some text </tag_name>`, using `Element.text`

Let us create a dummy XML content to illustrate these:

```python exec="true" source="tabbed-left" result="pycon" session="requests"
xml = """
<tag_name attribut1="value1" attrib2="value2"> some text </tag_name>
"""

element = ET.fromstring(xml)

print('tag'.center(20, '*'))
print(f'{element.tag = }')
print(f'{type(element.tag) = }')

print('attrib'.center(20, '*'))
print(f'{element.attrib = }')
print(f'{type(element.attrib) = }')

print('text'.center(20, '*'))
print(f'{element.text = }')
print(f'{type(element.text) = }')
```

## Displaying XML Structure

XML data can often be large and complex, especially when deeply nested, which makes understanding its structure difficult.

To help with this, let us create a helper function to display the XML tags in a tree-like format. Since we do not know how deep the XML structure might go, the best strategy here is to use *recursion* as follows:
 
 
```python exec="true" source="above"   session="requests"
def print_tags_tree(elem, level=0):
    # print indent, level and tag of the element
    print(' ' * 5 * level, level, elem.tag)
    for child in elem:
        # recursion to go as deep as possible
        print_tags_tree(child, level + 1)
```

Let us try it: 

```python exec="true" source="tabbed-left" result="pycon" session="requests"
print_tags_tree(root)
```

The output of `print_tags_tree` shows tags in a format that combines:

- The **namespace** URI (e.g., `{http://www.mediawiki.org/xml/export-0.11/}`)
- The **tag name** (e.g., `mediawiki`, `page`)

Although knowing the namespace is important, as we will discover later, it makes the tree look very cluttered.

To address this, let us modify the helper function to allow printing only the **tag names** in the tree.

We will use the function `QName`, which splits the tag information of an `element` into its tag name and its namespace. Here is an example code using `QName`:


```python exec="true" source="tabbed-left" result="pycon" session="requests"
print(f'{root.tag=}')

# Using the ET function QName
root_name = ET.QName(root)
# only tag name
print(f'{root_name.localname=}')
# only namespace
print(f'{root_name.namespace=}')
```

Now, let us modify the `print_tags_tree` function to provide the option of printing only tag names when the `only_tagnames` parameter is set to `True`.

```python exec="true" source="tabbed-left" result="pycon" session="requests"

def print_tags_tree(elem, level=0, only_tagnames=False):
    tagname = ET.QName(elem).localname if only_tagnames else elem.tag

    print(' ' * 5 * level, level, tagname)
    for child in elem:
        print_tags_tree(child, level + 1, only_tagnames)

print_tags_tree(root, only_tagnames=True)
```
 
Better! This gives us a clear view of the structure:

The root element is `mediawiki`.

- `mediawiki` has two children:
    - `siteinfo`
        - Contains information about the domain (e.g., its sitename, Wiki namespace).
    - `page`
        - Contains the most important information for this project.
        - `page` has four direct children: `title`, `ns`, `id`, and `revision`.
            - `title` contains the title of the page
                - For example, `schön`, `Flexion:schön`.
            - `ns` contains the Wiki namespace, which should not be confused with XML namespaces!
                - For example, `0`, `108`.
            - `id` is the unique identifier of the page
                - For example, `2930`, `21734`.
            - `revision` contains a revision of the page.
                - Each time a wiki page is modified, a `revision` element is added. In the XML extraction methods covered here, only the latest revision is retrieved, so we have only one `revision` element.
                - The raw *wikitext* is located here in the child element `text`.

The main goal of this section is to extract the `page`, `title`, `ns`, and `text` elements.

But first, let us briefly discuss XML namespaces. If you are already familiar with XML namespaces, feel free to skip this part.

## XML Namespaces Overview

In XML, tag names and attributes are user-defined, which can lead to name conflicts when combining data from different XML files. To avoid these conflicts, XML uses a system of namespaces and prefixes. Each namespace is typically defined using a URI.

Namespaces are often declared in the **root element** of the XML (but not always, they can also be declared in children elements).  To identify namespaces in an XML document, look for attributes beginning with `xmlns` and/or  `xmlns:prefix`. 

- *`xmlns` without a prefix*: This denotes the default namespace, applying to the element where it appears and all its descendants (unless overridden).
- *`xmlns:prefix`*: This is a prefixed namespace. It applies only to elements that explicitly use the prefix.

For example, in our Wiki XML, we see two namespaces defined at the root element:

```xml
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
```

This gives us:

- **Default Namespace**: `xmlns="http://www.mediawiki.org/xml/export-0.11/"`, which applies to all elements without prefixes.
- **Prefixed Namespace**: `xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"` with the prefix `xsi`.

An even simpler approach is to use the `nsmap` method, which provides a dictionary mapping prefixes to their respective URIs.

```python exec="true" source="tabbed-left" result="pycon" session="requests"
NAMESPACES = root.nsmap
for key, namespace in NAMESPACES.items():
    print('prefix:', key,'=> namespace-URI:', namespace)
```

## Extracting Data

### `element.find` 

To extract elements from the XML, we will use the `find` method, which searches for the **first child element** with a specified **tag name** or **path**.

Note that the following code will fail to find the `page` element and will return `None`. This is because `lxml` requires the correct namespace to be specified if the XML we are working with has declared any namespaces.

```python exec="true" source="tabbed-left" result="pycon" session="requests"
# This will not work, because it lacks the required namespace
page = root.find('page')
print(page) # None
```

You can specify the namespace in two ways:

- Using the full `{namespace}tagname` notation
- Passing a **namespace dictionary** as an argument to `find`

The following code will successfully retrieve the `page` element using each method:

```python exec="true" source="tabbed-left" result="pycon" session="requests"
# Full notation 
page = root.find('{http://www.mediawiki.org/xml/export-0.11/}page')
print('Full notation:',page) 

# Namespace dictionary
# NAMESPACES = {None: 'http://www.mediawiki.org/xml/export-0.11/'}
NAMESPACES = root.nsmap
page = root.find('page', NAMESPACES)
print('Namespace dictionary:', page)  
```

We will stick to the **namespace dictionary** to avoid writing the URL each time we need to use the `find` method.

Now that we have successfully located the `page` element, we can retrieve its child elements `ns` and `title`.
 

```python exec="true" source="tabbed-left" result="pycon" session="requests"
# Accessing Wiki namespace
ns = page.find('ns', NAMESPACES)
print(ns)
print(ns.text) # '0'

# Accessing the title of the page
title = page.find('title', NAMESPACES)
print(title)
print(title.text) # schön
```

Finally, we want to retrieve the main content, or **wikitext**, which is stored in the `text` element.

Note that we cannot use `page.find('text', NAMESPACES)` directly because `text` is not a direct child of `page`; it is nested under `revision`.

```python exec="true" source="tabbed-left" result="pycon" session="requests"
# Print the tree of page, to find the path 
print_tags_tree(page, only_tagnames=True)
```

Fortunately, the `find` method allows us to specify the path to a nested tag. In this case, we specify the path `revision/text` from `page` to `text`:

```python exec="true" source="tabbed-left" result="pycon" session="requests"
wikitext = page.find('revision/text', NAMESPACES)
print(wikitext)
# Let's print the first 300 characters of the wikitext
print(wikitext.text[:300])
```

We are done; we have just retrieved the **wikitext** content from the XML string.


Before moving on to the next section, let us quickly recap what we have learned by using functions.

```python exec="true" source="tabbed-left" result="pycon" session="requests"
import requests
import lxml.etree as ET

def fetch(title):
    url = f'https://de.wiktionary.org/wiki/Spezial:Exportieren/{title}'
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def fetch_wikitext(title):
    xml_content = fetch(title)
    root = ET.fromstring(xml_content)
    namespaces  = root.nsmap
    page = root.find('page', namespaces)
    wikitext = page.find('revision/text', namespaces)
    return wikitext.text 

# let us try it 
print(fetch_wikitext('schön')[:5000])
```

