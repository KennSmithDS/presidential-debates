import pandas as pd
import requests
import re
import sys
import traceback
import datetime as dt
import os
from bs4 import BeautifulSoup

base_url = 'http://www.debates.org'
debate_archive_url = 'http://www.debates.org/voter-education/debate-transcripts/'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
# <div id="content-sm">

def get_archive_df(archive_url):
    archive_list = []
    archive_soup = get_content_div(archive_url)
    for link in archive_soup.findAll('a', attrs={'href': re.compile("^/voter-education/debate-transcripts/")}):
        archive_dict = {}
        href = link.get('href')
        text = link.text
        archive_dict['debate_name'] = text
        archive_dict['debate_url'] = base_url + href
        archive_list.append(archive_dict)
    archive_df = pd.DataFrame(archive_list)
    return archive_df

def get_content_div(url):
    try:
        print(f'Fetching response from: \n {url}')
        response = requests.get(url=url, headers=headers)
        html = response.text
        print(f'Found {len(html)} characters of html content')
        soup = BeautifulSoup(html, 'lxml') #.encode("utf-8")
        found = soup.find('div', {'id': 'content-sm'})
        return found
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return None   

def write_content_to_file(debate_url, debate_content):
    try:
        pattern = re.compile(r'/debate-transcripts/(.*?)/')
        matches = pattern.findall(debate_url)
        file_name = matches[0]
        print(f'Writing {file_name} to text file')
        save_path = 'C://Users//Kendall//Documents//presidential_debates//debate_texts'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        complete_file_path = os.path.join(save_path, file_name+".txt") 
        text_file = open(f'{complete_file_path}.txt', 'w', encoding="utf-8")
        text_file.write(str(debate_content))
        text_file.close()
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        pass

if __name__ == "__main__":
    try:
        archive_df = get_archive_df(debate_archive_url)
        archive_df['debate_text'] = archive_df.apply(lambda row: get_content_div(row['debate_url']), axis=1)
        archive_df[['debate_name', 'debate_url']].to_csv('debate_header.csv', index=False)
        archive_df.apply(lambda row: write_content_to_file(row['debate_url'], row['debate_text']), axis=1)
    except Exception as e:
        print(e)