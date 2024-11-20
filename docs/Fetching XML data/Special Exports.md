The **Special Export** tool fetches specific pages with their raw content (*wikitext*) in real-time, without needing to download the entire dataset. The content is provided in XML format.

[TOC]

## Using the **Special Export** Tool

You can actually use **Special Export** to retrieve pages from *any* Wiki site. On the German Wiktionary, however, the tool is labelled **Spezial:Exportieren**, but it works the same way.

### Examples

**Exporting Pages from Any Wiki Site**

To access the XML content of the page titled "Austria" from English Wikipedia, you can use the following Python code. When you press `run`, it will open the export link in your default browser:

```pyodide session="webbrowser"
import webbrowser

title = 'Austria'
domain = 'en.wikipedia.org'
url = f'https://{domain}/wiki/Special:Export/{title}'
webbrowser.open_new_tab(url)
```

**Exporting Pages from the German Wiktionary**

For the German Wiktionary, the export tool uses `Spezial:Exportieren` instead of `Special:Export`. You can use similar Python code to open the export link for the page titled "schön" (German for "beautiful"):

```pyodide session="webbrowser"
title = 'schön'
domain = 'de.wiktionary.org'
url = f'https://{domain}/wiki/Spezial:Exportieren/{title}'
webbrowser.open_new_tab(url)
```

## Using the `requests` Library

To programmatically fetch and download XML content, you can use Python's `requests` library. This example shows how to build the URL, make a request, and get the XML content of a Wiktionary page by its title.
 
```python exec="true" source="above"   session="requests"
import requests

def fetch(title):
    # Construct the URL for the XML export of the given page title
    url = f'https://de.wiktionary.org/wiki/Spezial:Exportieren/{title}'
    
    # Send a GET request
    resp = requests.get(url)
    
    # Check if the request was successful, and raise an error if not
    resp.raise_for_status()
    
    # Return the XML content of the requested page
    return resp.content
```

Next, let us attempt to retrieve the XML content for the page titled "hoch" and print the initial 500 bytes for a glimpse of the XML content displayed in the `Result` tab.

 
```python exec="true" source="tabbed-left" result="pycon" session="requests"
page = fetch('hoch')
print(page[:500])
```

<!-- Which will return 
```xml
b'<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.11/ http://www.mediawiki.org/xml/export-0.11.xsd" version="0.11" xml:lang="de">\n  <siteinfo>\n    <sitename>Wiktionary</sitename'
```
   -->
We will continue to use the `fetch` function throughout this tutorial.


