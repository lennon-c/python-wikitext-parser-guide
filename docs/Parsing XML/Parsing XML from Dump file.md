[TOC]

## Importing Packages
```python  
from pathlib import Path 
import lxml.etree as ET # to parse XML documents
import pickle # to store the dictionary locally 
```

## Setting Up Paths Local Machine

To follow along in this section:

1. You will need to download and decompress the Wiktionary dump file.  
    - You can download the latest version [here](https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-articles-multistream.xml.bz2) or refer to instructions for downloading specific versions [here](../Fetching XML data/Dump files.md).
2. Once you have done that, specify the path to the decompressed file in `XML_FILE`.
3. By the end of this section, we will save our result as a dictionary and store it locally.  
    - Therefore, do not forget to specify in which folder the dictionary should be saved in `DICT_PATH`.

```python  
# Specify your own paths
XML_FILE = Path(r'path\to\xml\dewiktionary-20241020-pages-articles-multistream.xml')
DICT_PATH = Path(r'path\to\dict')
```

## Parsing the XML File
Since we are working with a file, we cannot use the `ET.fromstring` function to parse the XML content. Instead, we must use the `ET.parse` function.

Note that this process can take some time. On my computer, it takes approximately 42 seconds to load the entire XML tree.

=== "Source"
    ```python  
    # ET.parse for a xml file
    tree = ET.parse(XML_FILE)
    print(type(tree)) # lxml.etree._ElementTree

    root = tree.getroot()
    print(type(root)) # <class 'lxml.etree._Element'>
    ```
=== "Result"
    ```pycon
    <class 'lxml.etree._ElementTree'>
    <class 'lxml.etree._Element'>
    ```


The parser returns an `ElementTree` object. We use the `getroot()` method to access the root `Element`.


## Displaying the XML Structure

The XML structure of the dump file is quite large, so printing the entire tree would not only be inefficient but also quite overwhelming. To make it more manageable, let us modify our `print_tags_tree` function.

We will add options to limit the number of children displayed for the root element and to control the depth of the tree.

Here is our updated `print_tags_tree` function:

```python
def print_tags_tree(elem, level=0, only_tagnames=False, max_children=5, max_level=5):

    tagname = ET.QName(elem).localname if only_tagnames else elem.tag
    print(" " * 5 * level, level, tagname)

    # Restrict depth
    if level + 1 <= max_level:
        for child_index, child in enumerate(elem):
            print_tags_tree(child, level + 1, only_tagnames, max_children, max_level)
            # Limit number of children of the root element
            if level == 0 and child_index == max_children - 1:
                break
```

To display only the first 5 direct children of the root element and limit the tree to the first level:

=== "Source"
    ```python
    print_tags_tree(root, only_tagnames=True, max_children=5, max_level=1)
    ```
=== "Result"
    ```pycon
    0 mediawiki
        1 siteinfo
        1 page
        1 page
        1 page
        1 page
    ```


To view the first 3 children of the root element and display two levels of the tree:

=== "Source"
    ```python
    print_tags_tree(root, only_tagnames=True, max_children=3, max_level=2)
    ```
=== "Result"
    ```pycon
    0 mediawiki
        1 siteinfo
            2 sitename
            2 dbname
            2 base
            2 generator
            2 case
            2 namespaces
        1 page
            2 title
            2 ns
            2 id
            2 revision
        1 page
            2 title
            2 ns
            2 id
            2 revision
    ```
 
## Extracting Data

### `element.findall` 

As with the previous section, we are interested in extracting the `page`, `title`, `ns`, and `text` tags.

The main difference in structure here is that we now have multiple `page` elements, and we want to extract all of them.

We cannot use `find`, because it will return only the first `page`. However, we can use the `findall` method instead, which will return a list of all `page` elements.

=== "Source"
    ```python
    NAMESPACES = root.nsmap 
    pages = root.findall('page', namespaces=NAMESPACES)
    print(len(pages)) # as of today 1281638
    ```
=== "Result"
    ```pycon
    1281638
    ```

Notice that the latest dump file version contains more than one million pages, and retrieving them all takes approximately 45 seconds.

Since retrieving all pages is time-consuming, we will store the relevant information locally in a dictionary and save it as a pickle file for quicker access in the future.

We will create a dictionary, `dict_0`, using page titles as keys and their *wikitext* as values. Additionally, we will restrict the pages we store to those within the main Wiki namespace (`'0'`). We will discuss Wiki namespaces further when we parse *wikitext*.

This process may take a couple of minutes!

 
```python
ns = '0'
dict_0 = dict()
for page in pages:
    ns_elem = page.find('ns', namespaces=NAMESPACES)
    if ns_elem.text == ns: 
        title = page.find('title', namespaces=NAMESPACES)
        wikitext = page.find('revision/text', namespaces=NAMESPACES)
        dict_0[title.text] = wikitext.text
```

To check that our dictionary is correctly populated, let us print out part of the *wikitext* for a sample page:

=== "Source"
    ```python
    print(dict_0['schön'][:300])
    ```
=== "Result"
    ```pycon
    {{Siehe auch|[[schon]]}}
    {{Wort der Woche|26|2007}}
    == schön ({{Sprache|Deutsch}}) ==
    === {{Wortart|Adjektiv|Deutsch}} ===

    {{Deutsch Adjektiv Übersicht
    |Positiv=schön
    |Komparativ=schöner
    |Superlativ=schönsten
    |Bild 1=Jaguar E-type (serie III).jpg|mini|1|ein ''schönes'' [[Auto]]
    |Bild 2=12er Anitra

    ```

## Saving the Dictionary Locally

Once the dictionary is built, we save it locally using the `pickle` module, which allows us to store the dictionary in a serialized format. This way, we will not need to parse the XML file again in the future.

```python
dict_file = DICT_PATH / f'wikidict_{ns}.pkl'
        
with open(dict_file, 'wb') as f:
    pickle.dump(dict_0, f)
```

## Loading Dictionary

The next time you need to retrieve *wikitext*, simply load the dictionary from the pickle file and select the title page you need!
  
=== "Source"
    ```python
    import pickle
    from pathlib import Path

    ns = '0'
    dict_file = DICT_PATH / f'wikidict_{ns}.pkl'

    with open(dict_file, 'rb') as f:
        dict_0 = pickle.load(f)
    # 9 secs

    wikitext = dict_0['schön']
    print(wikitext[:300])
    ```
=== "Result"
    ```pycon
    {{Siehe auch|[[schon]]}}
    {{Wort der Woche|26|2007}}
    == schön ({{Sprache|Deutsch}}) ==
    === {{Wortart|Adjektiv|Deutsch}} ===

    {{Deutsch Adjektiv Übersicht
    |Positiv=schön
    |Komparativ=schöner
    |Superlativ=schönsten
    |Bild 1=Jaguar E-type (serie III).jpg|mini|1|ein ''schönes'' [[Auto]]
    |Bild 2=12er Anitra
    ```

And we are done! Now we can retrieve any *wikitext* by the page title.  
Next, we can cover how to parse *wikitext*.