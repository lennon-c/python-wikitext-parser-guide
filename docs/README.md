# A Hands-On Guide to Parsing Wikitext with Python

In this tutorial, we will explore how to parse *wikitext* from beginning to end using **Python**. We will cover each step—from fetching data and parsing XML, to directly handling *wikitext* and extracting content like templates, headings, and sections. Throughout the tutorial, we will use the German [Wiktionary](https://de.wiktionary.org/wiki/Haus) as our example. 

## What?

- We will begin by fetching the data, which is detailed in [Fetching XML data](https://lennon-c.github.io/python-wikitext-parser-guide/Fetching%20XML%20data/). The data is retrieved in XML format and includes two methods: 
    * First, we will retrieve *wikitext* online using the Wiki [Special Export tool](https://lennon-c.github.io/python-wikitext-parser-guide/Fetching%20XML%20data/Special%20Exports/) via the `requests` package. 
    * Next, we will locate and download the Wiki [Dump File](https://lennon-c.github.io/python-wikitext-parser-guide/Fetching%20XML%20data/Dump%20files/). 
- Then, using the `lxml` package, we will parse the XML data obtained from both **Special Export** [here](https://lennon-c.github.io/python-wikitext-parser-guide/Parsing%20XML/Parsing%20XML%20from%20Special%20Export/) and **Dump files** [here](https://lennon-c.github.io/python-wikitext-parser-guide/Parsing%20XML/Parsing%20XML%20from%20Dump%20file/) to extract the *wikitext* content.

- In the final part of this tutorial, we will parse the *wikitext* itself. After reviewing key Wiki concepts and *wikitext* syntax in [Wiki Basics](https://lennon-c.github.io/python-wikitext-parser-guide/Parsing%20Wikitext/Wiki%20Basics/), we will use `mwparserfromhell` and some regular expressions to extract elements such as headings, sections, parts of speech, declensions, meanings, and more in [Parsing Wikitext](https://lennon-c.github.io/python-wikitext-parser-guide/Parsing%20Wikitext/Parsing%20Wikitext/).

### Requirements to follow along   
To follow along with this tutorial, you will need to have the following Python packages installed:

- [`requests`](https://pypi.org/project/requests/)
- [`lxml`](https://lxml.de/)
- [`mwparserfromhell`](https://github.com/earwig/mwparserfromhell)

If you do not have these installed, you can install them by running the following command:

```bash
pip install requests lxml mwparserfromhell
```

You can now start with the [hands-on tutorial](https://lennon-c.github.io/python-wikitext-parser-guide/Fetching%20XML%20data/) right away or continue reading below (optional)! 

## Why?

Why would you want to extract content using *wikitext* instead of scraping wiki pages?

- **Webpage layouts change frequently.** If you are scraping the web page, any layout change can break your code. This actually happened to me (see below). However, if your code relies on *wikitext* content, it is less likely to be affected by these changes.
    - *Wikitext* is the source content and contains only minimal formatting. This content then undergoes several transformations for final formatting. One transformation occurs when templates are applied (referred to as “transclusion” in wiki jargon), and another when CSS styles are added.

- **Access to Dump files.** Since dump files store content in *wikitext* format, parsing wikitext is the only option here. Working with dump files has the following advantages:  
    - Dump files are typically downloaded once, so you avoid repeated access to Wikipedia servers. This is respectful of Wikimedia’s resources and helps avoid IP blocking or rate-limit issues.  
    - With the entire database on your computer, you have a broad range of data analysis options available.  
    - No matter how many changes occur on the live site, your code will always work with the dump file.

That being said, parsing *wikitext* does come with its own challenges:

- **Understanding wikitext basics**: To work with *wikitext*, you will need to learn some of its syntax and formatting conventions.

- **Differences from the live web page**: The *wikitext* content you parse is not always identical to what you see on the live web page.


## The Story Behind This Tutorial

Last year, I set up a system of flashcards for learning German, which involved scraping German Wiktionary pages to retrieve word declensions using BeautifulSoup. My code worked well initially, but by the time I wanted to use it again, it was broken because the website layout had changed. So, I fixed the code, but when the layout changed again, I realized that web scraping was not the best approach for the task at hand.

I knew that Wiki projects maintain dump files, so I thought I would give those a try. This was easier said than done.

The dump files do not store content in HTML format, but rather in a markup language called *wikitext*, which is what Wiki contributors use to add content. Additionally, while web scraping requires little knowledge about the structure of Wiki projects, working with dump files does require some understanding of their format. For instance, you need to know what a Wiki namespace is, understand versioning, have a grasp of *wikitext* syntax, and be able to deal with templates. Moreover, dump files are large, and trial-and-error approaches can be time-consuming.

I would have certainly benefited from a tutorial that explains these essential aspects of parsing *wikitext* without becoming a *wikitext* parser expert. Since I am so grateful for the endless tutorials, guides, and open-source projects that have shared their knowledge, writing this tutorial is my way of giving back to the Python community and of saying thanks for the countless hours of joy and learning.

And also because ***<span style="color:blue">open source</span> is <span style="color:red">the Robin Hood</span> of our time</span>***, in my humble opinion :)

Happy coding!  
c-lennon


