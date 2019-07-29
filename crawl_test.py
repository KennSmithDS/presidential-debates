import pandas as pd
import requests
import re
import datetime as dt
from bs4 import BeautifulSoup

base_url = 'http://www.debates.org'
debate_archive_url = 'http://www.debates.org/voter-education/debate-transcripts/'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
# <div id="content-sm">

def get_content_div(url):
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    found = soup.find('div', {'id': 'content-sm'})
    return found

archive_list = []
archive_soup = get_content_div(debate_archive_url)
for link in archive_soup.findAll('a', attrs={'href': re.compile("^/voter-education/debate-transcripts/")}):
    archive_dict = {}
    href = link.get('href')
    text = link.text
    archive_dict['debate_name'] = text
    archive_dict['debate_url'] = base_url + href
    archive_list.append(archive_dict)

archive_df = pd.DataFrame(archive_list)
archive_df['debate_text'] = archive_df.apply(lambda row: get_content_div(row['debate_url']), axis=1)
# archive_df.to_csv('debate_archive.csv', index=False)