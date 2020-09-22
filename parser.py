import requests
import bs4
from urllib.parse import urlparse
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import unicodedata
import copy
from model import create_connection,create_table_links,create_table_words,create_link,create_words,select_all_links,select_all_words
from config import SITE_NAME,SITE_PROTOCOL

def get_content(url):
    try:
        data = requests.get(url)
    except:
        return None
    soup = bs4.BeautifulSoup(data.text,"html.parser")
    return soup

def get_page_links(soup):
    links = set()
    if type(soup) == bs4.BeautifulSoup:
        for link in soup.find_all("a"):
            href = link.get("href")
            o = urlparse(href)
            if o.path:
                if o.netloc == SITE_NAME or not o.netloc:
                        links.add(SITE_PROTOCOL+SITE_NAME+o.path)
        return list(links)
    return []

def get_all(lst):
    for i in lst:
        print(lst.index(i))
        soup = get_content(i)
        for j in get_page_links(soup):
            if j not in lst:
                lst.append(j)
    return lst
        
def create_html(path,url,index):
    soup = get_content(url)
    if soup != None and os.path.isfile(f"{path}index({index}).html") == False:
        with open(f"{path}index({index}).html","w") as f:
            f.write(str(soup))

def get_words(url):
    soup = get_content(url)
    if soup != None:
        html = soup.get_text()
        text = "".join(i for i in html if not unicodedata.category(i).startswith("P"))
        text = "".join(i for i in text if not unicodedata.category(i).startswith("S"))
        stop_words = stopwords.words("russian") + stopwords.words("english")
        porter = PorterStemmer()
        Words = [porter.stem(i) for i in word_tokenize(text) if i not in stop_words]
        return Words
    return []

def rate_words(links):
    words = set()
    for i in links:
        wds = get_words(i)
        key = links.index(i)+1
        for j in wds:
            words.add((j,wds.count(j),key))
    return words

def create_files_for_html(links):
    if os.path.isdir("/home/aram/Desktop/links/LinksHtml") == False:
        os.mkdir("/home/aram/Desktop/links/LinksHtml")
        for link in links:
            ix = links.index(link)+1
            create_html("/home/aram/Desktop/links/LinksHtml/",link,ix)

def create_table_for_words(conn, rates):
    for i in rates:
        create_words(conn,i)

def insertion_of_links_in_table(conn, links):
    for data in links:
        o = urlparse(data)
        link_data = (o.scheme,o.netloc,o.path)
        create_link(conn,link_data)

def main():
    conn = create_connection()
    if conn is not None:
        soup = get_content(SITE_PROTOCOL+SITE_NAME)
        if soup != None:
            links = get_all(get_page_links(soup))
            
            create_table_links(conn)
            insertion_of_links_in_table(conn,links)
            select_all_links(conn)

            create_table_words(conn)
            create_files_for_html(links)
            
            rates = rate_words(links)
            create_table_for_words(conn,rates)
            select_all_words(conn)
            

if __name__ == "__main__":
    main()
