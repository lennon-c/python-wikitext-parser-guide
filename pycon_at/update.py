#%%
from generate_notebooks import render_workshop, create_index_md

import os
from pathlib import Path
import subprocess
from dotenv import load_dotenv, find_dotenv
load_dotenv()

REPO_GUIDE = Path(os.environ.get('REPO_GUIDE'))
REPO_CODE = Path(os.environ.get('REPO_CODE'))

def update_and_commit(path, commit_msg):
    os.chdir(path)
    subprocess.run("git add .", shell=True)
    subprocess.run(f'git commit -m "{commit_msg}"', shell=True)
    subprocess.run("git push origin main", shell=True)

def deploy_mkdocs():
    subprocess.run("mkdocs gh-deploy", shell=True)
 
def update_notebooks(commit_msg = "Update pycon_at"):
    render_workshop()
    update_and_commit(REPO_CODE, commit_msg)

def update_workshop_index(commit_msg = "Update workshop index"):
    # update workshop index pycon_at.md
    # manual modifications are done in pycon_template.md
    # index is based on get_table_of_content() function in `generate_notebooks`
    create_index_md()
    update_and_commit(REPO_GUIDE, commit_msg)
    deploy_mkdocs()

#%% 
if __name__ == "__main__":
    render_workshop()
    create_index_md()

    update_notebooks(commit_msg = "Update pycon_at - fixing 403 error")
    update_workshop_index()


 
