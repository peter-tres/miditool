import urllib3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



web_url = "https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}



http = urllib3.PoolManager()
response = http.request('GET', web_url)
page = response.data


soup = BeautifulSoup(page, 'html.parser')

table_entries = soup.tbody

site_data = []
for entry in table_entries:
    columns = [tag for tag in entry if tag != '\n' and tag]
    if not columns:
        continue
    midi_note, piano_note, note_name = columns[0].contents[0], columns[2].contents[0],columns[3].contents[0]
    
    site_data.append([midi_note,piano_note,note_name])


filter_out = '\xa0'

site_data = [data for data in site_data if not filter_out in data]


for row in site_data:
    for k,v in enumerate(row):
        row[k] = v.get_text()


with open("out.txt", "w") as f:
    f.write("MIDI NOTE\tPIANO NOTE\tNOTE NAME\t\n")
    for row in site_data:
        for col in row:
            f.write(col + "\t")
        
        f.write('\n')

        