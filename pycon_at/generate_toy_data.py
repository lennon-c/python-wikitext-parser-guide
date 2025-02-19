# keep only selected pages/titles from the dump 
import lxml.etree as ET
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

date = r'20241020' #  '20250201' # 
XML_FILE  = Path(os.environ.get('XML_PATH')) /f'dewiktionary{date}-pages-articles-multistream.xml'
REPO_CODE = Path(os.environ.get('REPO_CODE'))


titles = """
Welt Zeit Jahr Kind Spiel jetzt über durch klein hoch stark alt kurz jung schön gehen stehen leben bringen kommen sagen """
pages_to_keep = [title for title in titles.split() if title]

tree = ET.parse(XML_FILE)

root = tree.getroot()
NAMESPACES = root.nsmap 
for page in root.findall('page', namespaces=NAMESPACES):
    if page.find('title', namespaces=NAMESPACES).text not in pages_to_keep:
        page.getparent().remove(page)

tree.write( REPO_CODE/ 'data'/ f'playground_dump_{date}.xml')

