**Dump File Fetching:** This is a static snapshot of all wiki pages, which is stored in a single compressed file (e.g., dewiktionary-latest-pages-articles.xml.bz2). 

[TOC]

## German Wiktionary Dump Files

### Latest Version

- To download the latest dump file of the German Wiktionary, click [here](https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-articles-multistream.xml.bz2).
    - This will download the compressed file: `dewiktionary-latest-pages-articles-multistream.xml.bz2`.
    - The file is stored in this directory: [https://dumps.wikimedia.org/dewiktionary/latest/](https://dumps.wikimedia.org/dewiktionary/latest/).

### Latest (alternative way) and Older Versions

- If you need an older version of the Wiktionary dump, visit this directory: [https://dumps.wikimedia.org/dewiktionary/](https://dumps.wikimedia.org/dewiktionary/).
    - To download a specific version:
        - Navigate to the folder for the desired date.
        - A new window will open.
        - Look for the section titled **Articles, templates, media/file descriptions, and primary meta-pages**.
        - Select the file. The file name will follow the pattern: `dewiktionary-YYYYMMDD-pages-articles.xml.bz2`, where `YYYYMMDD` represents the dump date.
    - **Notes**:
        - Older dumps are only retained for a few months.
        - You can also fetch the latest version from this directory by choosing the most recent date.

## Any Wiki Dump File

- Click on **[Database backup dumps](https://dumps.wikimedia.org/backup-index.html)**.
- Scroll down the page to find the domain of interest.
    - For example, use `enwiktionary` for the English Wiktionary.
- Click on the domain link, then look for the section titled **Articles, templates, media/file descriptions, and primary meta-pages**.
    - The file you are looking for should end with `-pages-articles.xml.bz2`.
 
## Should I download a multistream dump file or not?

The files `-pages-articles.xml.bz2` and `multistream-pages-articles.xml.bz2` contain the same information. For our purposes here, either option will work just fine because we are working with a relatively small wiki database.

However, if you plan to work with a larger dump file in the future that exceeds your computer's memory capacity, you could download the `multistream-pages-articles.xml.bz2` version. This would allow you to adjust your parsing strategy to process the data in smaller chunks.