# A Hands-On Guide to Parsing Wikitext

In this a hands-on guide on how to parse *wikitext* from beginning to end using *Python*. 

## What?

Throughout the tutorial, we will use the [German Wiktionary](https://de.wiktionary.org) as our example. 

This hands-on guide is divided into three parts:

1. **Fetching the Data**: Learn two ways to retrieve wiki data — by using the *Special Export* tool or by downloading wiki dump files. [Learn more about fetching XML data.](https://lennon-c.github.io/python-wikitext-parser-guide/Fetching%20XML%20data/)

2. **Parsing the XML Files**: Once the data is retrieved in XML format, this section explains how to parse the files to extract the *wikitext*. [Learn more about parsing XML files.](https://lennon-c.github.io/python-wikitext-parser-guide/Parsing%20XML/)

3. **Parsing the Wikitext**: In the final part, we will parse the *wikitext* and extract elements such as headings, sections, word forms, meanings, inflections and more. [Learn more about parsing wikitext.](https://lennon-c.github.io/python-wikitext-parser-guide/Parsing%20Wikitext/)

### Requirements to follow along   
To follow along with this tutorial, you will need to have the following Python packages installed:

- [`requests`](https://pypi.org/project/requests/)
- [`lxml`](https://lxml.de/)
- [`mwparserfromhell`](https://github.com/earwig/mwparserfromhell)

You can install them by running the following command:

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

Last year, I set up a system of flashcards for learning German, which involved scraping German Wiktionary pages to retrieve word inflections using BeautifulSoup. My code worked well initially, but by the time I wanted to use it again, it was broken because the website layout had changed. So, I fixed the code, but when the layout changed again, I realized that web scraping was not the best approach for the task at hand.

I knew that Wiki projects maintain dump files, so I thought I would give those a try. This was easier said than done.

The dump files do not store content in HTML format, but rather in a markup language called *wikitext*, which is what Wiki contributors use to add content. Additionally, while web scraping requires little knowledge about the structure of Wiki projects, working with dump files does require some understanding of their format. For instance, you need to know what a Wiki namespace is, understand versioning, have a grasp of *wikitext* syntax, and be able to deal with templates. Moreover, dump files are large, and trial-and-error approaches can be time-consuming.

I would have certainly benefited from a tutorial that explains these essential aspects of parsing wikitext without needing to become a wikitext parsing expert myself. Writing this tutorial is my way of giving back to the Python and open-source community for the countless hours of joy and learning.

And also because ***<span style="color:blue">open source</span> is <span style="color:red">the Robin Hood</span> of our time</span>***, in my humble opinion :)

Happy coding!  
c-lennon


