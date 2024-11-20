[TOC]

## Get the Wikitext Data

We already know how to extract *wikitext* from dump files and the special exports tool. In this section, we will parse this *wikitext*.

We will use the word `stark` as an example ([link to the wiktionary page](https://de.wiktionary.org/wiki/stark)). We will retrieve the *wikitext* for the page `stark` from my GitHub repository so that we have the same version of the page. However, you can use either of the two methods we have learned so far to retrieve the *wikitext*. 


```python exec="1" source="tabbed-left" result="pycon" session="wiki"
import requests
title = 'stark'
url = f'https://raw.githubusercontent.com/lennon-c/python-wikitext-parser-guide/refs/heads/main/docs/data/{title}.txt'
resp = requests.get(url)
wikitext = resp.text

print(wikitext[:500])
```

## Parsing Wikitext 

First, we need to import `mwparserfromhell`. Then, we use the `parse` function and pass in our wikitext, which will return a `Wikicode` object.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
import mwparserfromhell
parsed = mwparserfromhell.parse(wikitext)
print(type(parsed)) # <class 'mwparserfromhell.wikicode.Wikicode'>
```

## Retrieving Headings and Sectioning

`Wikicode` objects have several capabilities. You can obtain lists of different components of the *wikitext* by using a set of `filter` methods. For instance, you can use the `filter_headings` method to retrieve a list of all headings as follows:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
headings = parsed.filter_headings()
print(type(headings)) # <class 'list'>
print(len(headings)) # 11
```

We found 11 headings. Each element of the list is a `Heading` object. We can extract the `title` and the `level` of the heading objects.

Let us inspect the first heading in the list:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
heading = headings[0]

print(f'{heading = }\n{type(heading) = }\n')

print(f'{heading.level = }\n{type(heading.level) = }\n')

print(f'{heading.title = }\n{type(heading.title) = }\n')

```

The first heading is a **second-level** heading with the title `stark ({{Sprache|Deutsch}})`. Notice that we did not find any **first-level** headings. This is because the **first-level** heading is reserved for internal use, and wiki contributors can only begin creating headings from the **second level** onwards.

Let us use this information to create a helper function that prints the headings tree of the text.

```python exec="1" source="above" session="wiki"
def print_headings_tree(parsed):
    headings = parsed.filter_headings()
    for heading in headings:
        print(' ' * 5 *(heading.level - 2), heading.level, heading.title)
```

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
print_headings_tree(parsed)
```

- The first thing to notice when looking at the **second-level** headings is that the `Sprache` includes not only `Deutsch`, but also `Englisch` and `Schwedisch`.

    - Indeed, wiktionaries are multilingual. Thus, the German Wiktionary does not only cover information related to the *German-to-German* dictionary, but also includes bilingual dictionaries for several languages to German, such as *English to German* in this example.

- Notice as well that the **third-level** headings refer to the word forms (`Wortart`). A word can have one or more word forms. For instance, in English, `stark` is both an *adjective* and an *adverb*.

- Finally, the **fourth-level** headings contain information on the translation of the word into different languages (`Übersetzungen`).

For my project, I only need the *German-to-German* dictionary. So, let us extract the *wikitext* for that heading. We can use the method `get_sections()`, which accepts a heading level as an argument. Passing **level 2** will split the text into sections based on the second-level headings.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
sections = parsed.get_sections(levels=[2])
print(len(sections)) # 3
```

We obtained a list of 3 sections, one for each of the languages.

We could use `sections_DE = sections.pop(0)` to obtain the *German* section. Alternatively, we can use the `matches` parameter to retrieve sections whose heading title matches `Deutsch`, as follows:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
sections_DE = parsed.get_sections(levels=[2], matches="Deutsch")

# get_section() retreives always a list!
print(type(sections_DE)) # <class 'list'>
print(len(sections_DE)) # 1

# Get the first element.
sections_DE = sections_DE[0]
print(type(sections_DE)) # <class 'mwparserfromhell.wikicode.Wikicode'>
```

Let us have a look inside the *German* section.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
print(sections_DE[:450])
```

Sections include all of their subheadings by default.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
print_headings_tree(sections_DE)
```
If you want to retrieve a section but not its subsections, set the `flat` parameter to `True`.

For instance, if we want to retrieve `Wortart` sections (level 3) without including the translation sections `Übersetzungen` (level 4), we can use the following code:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
# flat = True
wordforms_DE = sections_DE.get_sections(levels=[3]
                                        , matches="Wortart"
                                        , flat=True)

# Get the first element
wordforms_DE = wordforms_DE[0]

# Check 
print_headings_tree(wordforms_DE) 
```

The most important information one might be interested in extracting is contained in the *Wortart* section. Here, you can find definitions, example phrases, synonyms, antonyms, rhymes, proverbs, translations, and more.

Since most of this information is related in one way or another to templates, let us learn how to use `mwparserfromhell` to extract wiki templates.

## Extracting Templates

You can use the `filter_templates` method to obtain a list of templates. Each element in the returned list will be a `Template` object.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
wordforms_tpls = wordforms_DE.filter_templates()
print(len(wordforms_tpls)) # 49
tpl = wordforms_tpls[0]
print(type(tpl)) # <class 'mwparserfromhell.nodes.template.Template'>
```

The wikicode `wordforms_DE` contains 49 templates. Let us print the first 3 templates.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
for tpl in wordforms_tpls[:3]:
    print(tpl,'\n')
```

There are two important templates worth examining: the `Wortart` template and the `Übersicht` template. These are the first and second templates in the template list `wordforms_tpls`.


### `Wortart` Template

From the `Wortart` template, you can extract the *Part of Speech* (POS), which indicates the type of word, such as nouns, verbs, and adjectives.

You can extract this template using `wortart_tpl = wortart_tpls[0]` or, alternatively, by using the `matches` parameter.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
wortart_tpls = wordforms_DE.filter_templates(matches='Wortart')
wortart_tpl = wortart_tpls[0]
print(wortart_tpl) # {{Wortart|Adjektiv|Deutsch}}
```

Let us get the `name` and parameters (`params`) of the template:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
print(wortart_tpl.name) # Wortart
print(wortart_tpl.params) # ['Adjektiv', 'Deutsch']
print(type(wortart_tpl.params)) # <class 'list'>
```

The `wortart_tpl` template has two unnamed parameters. The first is assigned the name `'1'` and contains information about the POS of the word (here, `'Adjektiv'`). The second is assigned the name `'2'` and relates to the language (here, `'Deutsch'`).

Since `wortart_tpl.params` is simply a list, you can use list **indexes** to extract any parameter. For instance, you can use `wortart_tpl.params[1]` to extract the second parameter.

You can also extract a parameter by its **name** using the `get` method.

Let us extract the POS parameter by name (`'1'`).

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
pos = wortart_tpl.get('1')
print(f'{type(pos) = }\n')
 
print(f'{pos.name = }')
print(f'{type(pos.name) = }\n')

print(f'{pos.value = }')
print(f'{type(pos.value) = }\n')
```

Note that the parameter `pos` is a `Parameter` object with `name` and `value` attributes. Also, notice that the `name` and `value` attributes are not strings but `Wikicode` objects!

If you need the string representation of these objects, you can use the `str()` function. For instance, let us create a helper function that will transform the parameters of a `Template` into a dictionary of strings:


```python exec="1" source="above" session="wiki"
def template_to_dict(template):
    """Get dictionary from template object."""
    params = {str(p.name).strip():str(p.value).strip() 
                for p in template.params}
    return params
```

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
params = template_to_dict(wortart_tpl)
for key, value in params.items():
    print(key, '=' , value)

```

### Conjugation or Declension Templates

The "conjugation or declension table," referred to as "Flexionstabelle" in the German Wiktionary, is constructed from templates whose names end with `Übersicht`:

- `Deutsch Adjektiv Übersicht`
- `Deutsch Substantiv Übersicht`
- `Deutsch Verb Übersicht`, etc.

Therefore, we can obtain these templates by matching the word `Übersicht`.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
übersichts_tpls = wordforms_DE.filter_templates(matches='Übersicht')

# Check length
print(len(übersichts_tpls)) # 1

# Extract template
übersichts_tpl = übersichts_tpls[0]

# Print name
print(f'{übersichts_tpl.name = }')
```

Let us print it using our helper function:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
for key, value in template_to_dict(übersichts_tpl).items():
    print(key, '=' , value)
```

This is more information than I need. I will exclude keys that contain `Bild` and all unnamed parameters (those with numeric names). These parameters relate to the images and their formatting that appear at the bottom of the declension table on the wiki page.


```python exec="1" source="above"  session="wiki"
übersichts_dict = {k:v for k,v in template_to_dict(übersichts_tpl).items() 
                if 'Bild' not in k  
                and not k.isnumeric()}
```

Let us see what we have obtained:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
for key, value in übersichts_dict.items():
    print(key, '=' , value)
```
That is exactly what I need. :fontawesome-regular-face-smile:


## Extracting Other Important Content

Although `mwparserfromhell` is an excellent tool, not all tasks can be accomplished using only this tool. Sometimes, it is necessary to incorporate regular expressions here and there.

If you want to extract, for instance, the `Bedeutungen` (Meanings), the `Beispiele` (Phrase Examples), the `Synonyme` (Synonyms), or the `Sprichwörter` (Proverbs), among others, you may notice that they all follow the same pattern.

We can take advantage of this pattern and begin writing the blocks for our regular expression right away.

For all of them:

- Their content is located in separate paragraphs:
    - They start and end with two new lines `\n\n ... \n\n`.
- The **first line** of the paragraph contains only a template without parameters, whose `name` indicates the type of content in the paragraph:
    - For example, `{{Bedeutungen}}\n` or `{{Beispiele}}\n`.
    - Note that `{` are special characters in regular expressions, so we must escape them using `\`:
        - `\{\{Bedeutungen\}\}\n`.
- From the **second line** onward, the content we want to extract begins:
    - It includes at least one or more characters `.+`.
    - It can span several lines.
        - Note that `.` matches any character except new lines. Since we want the content to span multiple lines, we need to add the flag `re.DOTALL` so that `.` can match new lines (`\n`) as well.
    - It should stop when a new paragraph starts:
        - To ensure this, we add the non-greedy qualifier `?`, making it `.+?`.
    - Finally, we want to retrieve the content starting from the second line onward:
        - To do this, we create a capturing group by enclosing it in parentheses:
            - `(.+?)`.

Putting everything together, we get the following pattern:

`r'\n\n\{\{Bedeutungen\}\}\n(.+?)\n\n'`, which should be used with the `re.DOTALL` flag. 

Let us try it using the `re.search` method:

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
import re
# Define the pattern 
pattern = r'\n\n\{\{Bedeutungen\}\}\n(.+?)\n\n'

# Get your text (convert Wikicode to string)
text = str(wordforms_DE)  

# Perform the search
search = re.search(pattern, text, re.DOTALL)

# Extract the content from the capturing group
bedeutungen_text = search.group(1)

# Print some characters of the text
print(bedeutungen_text[:300])
```
 
We have obtained the content of `Bedeutungen`, but it is difficult to read because it contains many Wiki links `[[link]]` and indentation syntax `:`.

To improve readability, we can use the `strip_code` method from `mwparserfromhell` to convert the Wikicode into plain text.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
# Parse the found text into Wikicode
bedeutungen = mwparserfromhell.parse(bedeutungen_text)

# Strip Wiki links, templates, and any special Wiki code
bedeutungen_plain = bedeutungen.strip_code()

# Print the start of the text 
print(bedeutungen_plain[:300])
```
 

Finally, we will wrap this code into a function, allowing us to parse any content type by providing the content's `name`. We will also include an option to retrieve plain text when the `strip_code` option is set to `True`.

```python exec="1" source="above"   session="wiki"
def content_extract(name, text, strip_code=True):
    # Adjust the pattern to accept the content name
    pattern = r'\n\n\{\{' + name + r'\}\}\n(.+?)\n\n'
    search = re.search(pattern, text, re.DOTALL)
    content = search.group(1)
    # Return plain text if strip_code is True
    if strip_code:
        return mwparserfromhell.parse(content).strip_code()
    # Return raw wikitext if strip_code is False
    else:
        return content
```

Let us try it using the content types: 'Bedeutungen', 'Beispiele', 'Synonyme', 'Sprichwörter' and print the first 150 characters of each content.

```python exec="1" source="tabbed-left" result="pycon" session="wiki"
# Get your text (convert Wikicode to string)
text = str(wordforms_DE) 

# Get different content types
for name in ['Bedeutungen', 'Beispiele', 'Synonyme', 'Sprichwörter']:
    print(name.center(20, '-'))
    content = content_extract(name, text)
    print(content[:150], '\n')
```
 
What a fitting proverb (*Sprichwort*) to conclude this tutorial—it was not planned at all!  

> *Was dich nicht umbringt, macht dich stärker*  

A reminder that:  

> *What does not kill you makes you stronger.*  

We have now reached the end of this hands-on guide!  

You can use this code to create your own **DerDieDas** game or to perform linguistic analyses.  

If you are interested, feel free to explore the [`de_wiktio`](https://github.com/lennon-c/de_wiktio) project, which implements all the steps covered in this tutorial in one package.  
 



