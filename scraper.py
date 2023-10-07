import os
from xata.client import XataClient
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

#Authenticates Xata.
api_key = os.environ['XATA_API_KEY']
db_url = os.environ['EGW_DB_URL']
xata = XataClient(api_key=api_key, db_url=db_url)

## Functions

#Adds a record to Xata
def insert_xata(content, book, ref, ref_url):
  record = xata.records().insert("egw_writings", {
  "content": content,
  "book": book,
  "ref": ref,
  "ref_url": ref_url
  })
  return None

#Takes URL and retrieves book title
def get_title(url, soup):
  title = soup.findAll("h1")
  title = title[0]
  title = title.text.strip()
  return title

#Receives URL of EGW content page and adds data to Xata. URL MUST BE STRING!
def url2xata(url):
   page = requests.get(url)
   soup = BeautifulSoup(page.content, 'html.parser')
   book = get_title(url, soup)
   paragraphs = soup.findAll("p", class_="egw_content_wrapper")
   for paragraph in paragraphs:
    content = paragraph.find("span", class_="egw_content")
    content = content.text.strip()
    ref = paragraph.find("span", class_="egw_refcode")
    if ref is None:
      continue
    else:
      ref = ref.text.strip()
      insert_xata(content, book, ref, url)
    

#Give TOC URL and returns list of URL's of pages
def get_urls_on_page(url, soup):
  url_list = []
  links = soup.findAll('a', class_="enable")
  for link in links:
    url_list.append("https://m.egwwritings.org/" + link.get('href'))
  return url_list


#Takes TOC url and adds all to Xata
def toc_to_xata(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  url_list = get_urls_on_page(url, soup)
  for i in url_list:
    url2xata(i)
    


#STC Table of Contents URL
url = 'https://m.egwwritings.org/en/book/108.21/toc'

#Calling the function - disabled to avoid accidents
#toc_to_xata(url)
