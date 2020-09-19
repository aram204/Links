from nltk.stem.porter import PorterStemmer
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
from nltk.tokenize import word_tokenize
import unicodedata
import sys
import csv
from model import create_connection,create_table,create_link,select_all_links
from config import SITE_NAME,SITE_PROTOCOL

def get_content(url):
    try:
        data = requests.get(url)
    except:
        return None
    soup = BeautifulSoup(data.text,"html.parser")
    return soup

def get_page_links(soup):
    links = set()
    for link in soup.find_all("a"):
        href = link.get("href")
        o = urlparse(href)
        if o.path:
            if o.netloc == SITE_NAME or not o.netloc:
                    links.add(SITE_PROTOCOL+SITE_NAME+o.path)
    return list(links)

def get_all(lst):
    links = []
    def in_links(lst):
        nonlocal links
        if len(lst) == 0:
            return
        for url in lst:
            if url not in links:
                soup = get_content(url)
                if soup != None:
                    links.append(url)
                    in_links(get_page_links(soup))
    in_links(lst)
    return list(set(links))
        
def create_html(path,url,index):
    soup = get_content(url)
    with open(f"{path}index({index}).html","w") as f:
        f.write(str(soup))

def create_diractory(path):
    os.mkdir(path)

def get_words(url):
    html = get_content(url)
    txt = ""
    for i in html.find_all("div"):
        txt += i.text
    symbols = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith("P") or unicodedata.category(chr(i)).startswith("N"))
    Words = [string.translate(symbols) for string in word_tokenize(txt) if len(string.translate(symbols))>1]
    return Words

def create_csv(path,words,index):
    wds = set()
    for i in words:
        wds.add((i,words.count(i)))
    with open(f"{path}indexWords({index}).csv","w") as f:
        writer = csv.writer(f,quotechar='|',delimiter='|')
        for i in wds:
            writer.writerow([i[0],i[1]])

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        soup = get_content(SITE_PROTOCOL+SITE_NAME)
        links = get_all(get_page_links(soup))
        for data in links:
            o = urlparse(data)
            link_data = (o.scheme,o.netloc,o.path)
            create_link(conn,link_data)
        select_all_links(conn)
        create_diractory("/home/aram/Desktop/links/LinksHtml")
        create_diractory("/home/aram/Desktop/links/WordAnalize")
        for link in links:
            ix = links.index(link)+1
            create_csv("/home/aram/Desktop/links/WordAnalize/",get_words(link),ix)
            create_html("/home/aram/Desktop/links/LinksHtml/",link,ix)


        
if __name__ == "__main__":
    main()
