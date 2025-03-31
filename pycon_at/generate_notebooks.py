#%%
import nbformat
import re 
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()
from urllib.parse import quote


PATH_GUIDE = Path(os.environ.get('PATH_GUIDE_DOCS'))
PATH_NOTEBOOKS = Path(os.environ.get('PATH_NOTEBOOKS'))
PATH_PYFILES = Path(os.environ.get('PATH_PYFILES'))
REPO="lennon-c/pycon_at/" 
COLAB = "https://colab.research.google.com/github/"
GUIDE_URL = "https://lennon-c.github.io/python-wikitext-parser-guide/"

# RE patterns 
PATTERN = r'(\n\s*```(?:pyodide|python).*?\n.+?\n\s*```)'
EXTRACT = r'(\n\s*```(?:pyodide|python).*?\n(.+?)\n\s*```)'
PYCON = r'(\n\s*```(?:pycon).*?\n.+?\n\s*```)'
LINKS = r'\[([^\]]+?)\]\((\.\./.+?)\)'
 

# define order of the files for the workshop
FOLDER_FILES_ORDER = [
('docs', 'README.md'),
('Fetching XML data', 'index.md'),
('Fetching XML data', 'Special Exports.md'),
('Fetching XML data', 'Dump files.md'),
('Parsing XML', 'index.md'),
('Parsing XML', 'Parsing XML from Special Export.md'),
('Parsing XML', 'Parsing XML from Dump file.md'),
('Parsing Wikitext', 'index.md'),
('Parsing Wikitext', 'Wiki Basics.md'),
('Parsing Wikitext', 'Parsing Wikitext.md'),
]
 
# subset of md with python code
CODE_MD_FILENAMES = ['Special Exports.md',
                'Parsing XML from Special Export.md',
                'Parsing XML from Dump file.md',
                'Parsing Wikitext.md',
                ]

CHAPTERS = list()
for item in FOLDER_FILES_ORDER: 
    if item[0] not in CHAPTERS: 
        CHAPTERS.append(item[0])


def get_md_path(parent, name):
    "return Path object of the file for a given folder in docs and file name"
    for f in PATH_GUIDE.glob('**/*.md'):
        if f.parent.name == parent and f.name == name:
            return f
        
# Get all `Path` objects from the md files in the order of FOLDER_FILES_ORDER
MD_PATHS = [ get_md_path(parent, name) for parent,name in FOLDER_FILES_ORDER]
# Get the subset of md files with python code
CODE_MD_PATHS = [ file for file in MD_PATHS if file.name in CODE_MD_FILENAMES]
 

def split_code_text(file):
    """check if the md file has python code and split into text and code blocks
    
    return content as an ordered list of text blocks using tuples, e.g.('text', some text) and ('code', python code)
    if no code if found, it returns a list with only one tuple ('text', 'some text')
    """
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    split = re.split(PATTERN, text, flags=re.DOTALL)

    code_list = list()
    for s in split: 
        if re.search(PATTERN, s, flags=re.DOTALL):
            search = re.search(EXTRACT, s, flags=re.DOTALL)
            code = search.group(2)
            if code.startswith('    '):
                code = '\n'.join([ line.replace('    ', '', 1)  for line in code.split('\n')])
            code_list.append(('code', code))
        else:
            text = s.replace('[TOC]', '')
            text = text.replace(':fontawesome-regular-face-smile:', '')
            text = text.replace('=== "Source"', '')
            text = text.replace('=== "Result"', '')
            text = re.sub(PYCON, '', text, flags=re.DOTALL)
            links = re.findall(LINKS, text)
            for link in links:
                old_link = link[1]
                link_filename = old_link.split('/')[-1]
                link_filepath = [file for file in MD_PATHS if file.name == link_filename][0]
                new_link =  get_guide_url(link_filepath)
                text = text.replace(old_link, new_link)
           
            code_list.append(('text',text))

    return code_list

def render_notebook(file):
    """return notebook object for a given md file"""
    # code_text = split_code_text(file)
    code_text = modified_code_text(file) 
    nb = nbformat.v4.new_notebook()
    for key, value in code_text:
        if key == 'code':
            nb.cells.append(nbformat.v4.new_code_cell(value))
        else:
            nb.cells.append(nbformat.v4.new_markdown_cell(value))
    return nb

def modified_code_text(file):
    """return code_text with some modifications to make it work in colab"""

    code_list = split_code_text(file)

    # 'Parsing XML from Dump file.md'
    name = 'Parsing XML from Dump file.md'
    markdown ="""
## Setting Up Paths in Google Colab 

- In Google Colab we are going to work with a toy version of the dump file that you can find in my github repo. 
- We will set `DICT_PATH` to the current working directory and set the file name in `XML_FILE` to "playground_dump_20241020.xml"  
- The following code will download the xml file and save it as "playground_dump_20241020.xml" in the current working directory.

"""
    code ="""import urllib
XML_FILE = Path("playground_dump_20241020.xml")
DICT_PATH = Path("")

url =  "https://raw.githubusercontent.com/lennon-c/pycon_at/refs/heads/main/data/playground_dump_20241020.xml"

urllib.request.urlretrieve(url, XML_FILE)"""

    if  file.name == name:
        code_list.insert(4, ('code', code))
        code_list.insert(4, ('text', markdown))
        # code_list = [('text', markdown), ('code', code)] + code_list 
    
    name = 'Parsing Wikitext.md'
    markdown="""## Installing `mwparserfromhell` in Google Colab"""
    code="""!pip install mwparserfromhell"""

    if  file.name == name:
        code_list.insert(0, ('code', code))
        code_list.insert(0, ('text', markdown))

    return code_list

  
def render_py(file):
    """return python code based on the given md file"""
    code_text = split_code_text(file)
    py_text = ''
    for key, value in code_text:
        if key == 'code':
            py_text += value
        else:
            py_text += '\n\n"""'+value+'\n"""\n\n'
    return py_text

def python_name(file):
    """return python file name based on the given md file"""
    if file in CODE_MD_PATHS:
        n = CODE_MD_PATHS.index(file)
        return f'{n}-{file.stem.replace(" ", "_")}.py'
 

def ipynb_name(file):
    """return notebook file name based on the given md file"""
    if file in CODE_MD_PATHS:
        n = CODE_MD_PATHS.index(file)
        return f'{n}-{file.stem.replace(" ", "_")}.ipynb'


def render_workshop():
    """Translate all markdown files with python code into ipynb and py files and save in their corresponding workshop folders"""
    for file in CODE_MD_PATHS:
        # ipynb
        nb = render_notebook(file)
        nbformat.write(nb, PATH_NOTEBOOKS/ipynb_name(file))
        # py
        py = render_py(file)
        with open(PATH_PYFILES/ python_name(file), 'w', encoding='utf-8') as f:
            f.write(py)

link_open_new_tab = lambda text, url: f'<a href="{url}" target="_blank">{text}</a>'

def get_table_of_content():
    markdown=''
    keep = [md for md in MD_PATHS if md.stem not in ['index', 'README']]
    for group in CHAPTERS:
        if group == 'docs':
            continue

        markdown+=f'\n**{group}**\n\n'
        for md in keep:
            if md.parent.name == group:
                if md in CODE_MD_PATHS:
                    nb = PATH_NOTEBOOKS/ipynb_name(md)
                    text = "go to Google Colab" 
                    url = get_google_colab_url(nb)
                    # markdown+=f'- {md.stem}   {google_colab_badge(url, text)}\n'
                else:
                    text = f'go to guide' 
                    url = get_guide_url(md)
                markdown+=f'- {md.stem} - {link_open_new_tab(text, url)}\n'
    return markdown

def create_index_md():
    """Currently saving this in the guide docs.
    
    This should be part of the home page of the workshop. 
    """
    template_path = PATH_GUIDE/'pycon_template.md'
    template = template_path.read_text('utf-8')
    markdown = get_table_of_content()
    template = template.replace('[INSERT]', markdown)

    # md_path = Path(__file__).parent.parent/'README.md'
    md_path = PATH_GUIDE/'pycon_at.md'
    md_path.write_text(template, encoding='utf-8')
  
def get_google_colab_url(file):
    colab = f'{COLAB}{REPO}blob/main/notebooks/{file.name}'
    return colab

def google_colab_badge(url, text):
    text = f"""<a href="{url}" target="_blank">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>"""
    return text

def get_guide_url(file):
    if 'README' in file.name:
        file_url = ""
    elif 'index' in file.name:
        file_url = quote(f'{file.parent.name}/')
    else:
        file_url = quote(f'{file.parent.name}/{file.stem}/')
    url = f'{GUIDE_URL}/'
    return url+file_url
 
#%%
if __name__ == '__main__':
    create_index_md()

#%%


    name = 'Parsing XML from Dump file.md'  
    file = [file for file in MD_PATHS if file.name == name][0]
    code_text = split_code_text(file)
    for n, (key, value) in enumerate(code_text):
        print(n)
        print(key, value)
 
    render_workshop()   
    print(get_table_of_content())
