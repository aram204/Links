from nltk.stem.porter import PorterStemmer
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
from nltk.tokenize import word_tokenize
import unicodedata
import sys#
import csv
from model import create_connection,create_table_links,create_table_words,create_link,create_words,select_all_links,select_all_words
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
    with open(f"{path}index({index}).html","w") as f:#try
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

def main():
    conn = create_connection()
    if conn is not None:
        create_table_links(conn)
        create_table_words(conn)
        soup = get_content(SITE_PROTOCOL+SITE_NAME)
        links = get_page_links(soup)
        for data in links:
            o = urlparse(data)
            link_data = (o.scheme,o.netloc,o.path)
            create_link(conn,link_data)
        select_all_links(conn)
        create_diractory("/home/aram/Desktop/links/Links/LinksHtml")
        words = set()
        for i in links:
            wds = get_words(i)
            for j in wds:
                words.add((j,wds.count(j)))
        
        for i in words:
            create_words(conn,i)
        select_all_words(conn)
        
        for link in links:
            ix = links.index(link)+1
            create_html("/home/aram/Desktop/links/Links/LinksHtml/",link,ix)


        
if __name__ == "__main__":
    main()

