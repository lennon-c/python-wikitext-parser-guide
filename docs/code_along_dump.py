import requests
title = 'schön'
url = f'https://raw.githubusercontent.com/lennon-c/python-wikitext-parser-guide/refs/heads/main/docs/data/{title}.txt'
resp = requests.get(url)
wikitext = resp.text

print(wikitext[:500])