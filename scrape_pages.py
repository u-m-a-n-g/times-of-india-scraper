import requests
import csv
from bs4 import BeautifulSoup
import lazynlp
import progressbar
import pickle
import json
import sys

def load_article(url):
    '''
    Loads an article and returns the title,text
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title_html = soup.find_all('h1', class_='_23498')[0]
    title_txt = lazynlp.clean_html(str(title_html))
    content_html = soup.find_all('div', class_='_1_Akb')[0]
    content_txt = lazynlp.clean_html(str(content_html))

    return title_txt,content_txt

def load_csv(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [row for row in csv_reader]
            

url_list = load_csv('covid_links.csv')

# Now create new list of dicts with fields: title,url,date,text

start_idx = int(sys.argv[1])
end_idx = min(int(sys.argv[2]),len(url_list))

articles = []
for ctr in progressbar.progressbar(range(start_idx,end_idx)):
    row = url_list[ctr]
    try:
        obj = row.copy()
        obj["title"], obj["text"] = load_article(obj["url"])
        articles.append(obj)
    except IndexError as e:
        print("Index error: " + str(e) + str(row))

filename = "articles_" + str(start_idx) + "_" + str(end_idx) + ".json";
with open(filename, 'w') as f:
    json.dump(articles,f)
