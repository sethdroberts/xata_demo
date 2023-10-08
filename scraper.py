import os
import time
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
def insert_xata(content, book, ref, ref_url, chapter):
  record = xata.records().insert("egw_cota", {
  "content": content,
  "book": book,
  "ref": ref,
  "ref_url": ref_url,
  "chapter": chapter
  })
  return None

#Takes URL and retrieves book title
def get_title(url, soup):
  title = soup.findAll("h1")
  title = title[0]
  title = title.text.strip()
  return title

#Receives URL of EGW content page and adds data to Xata. URL MUST BE STRING!
def url2xata(url, title):
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
      ref = ref.split(" ")
      ref = float(ref[1])
      insert_xata(content, book, ref, url, title)
    

#Give TOC URL and returns list of URL's of pages. WORKS FOR ALL WITHOUT SECTIONS
def get_urls_on_page(soup):
  url_list = []
  excluded_titles = ["preface", "introduction", "foreword", "appendix"]
  title_list = []
  links = soup.findAll('a', class_="enable")
  for link in links:
    title = link.text.strip()
    if title.lower() in excluded_titles:
      continue
    title_list.append(title)
    url_list.append("https://m.egwwritings.org" + link.get('href'))
  return url_list, title_list

#Give TOL URL and returns list of URL's of pages
#THIS ONE SPECIFICALLY FOR SECTIONED. IT STARTS AT FIRST PAGE AND MOVES FROM PAGE TO PAGE
def get_sectioned_urls(soup):
  url_list = []
  title_list = []
  excluded_titles = ["preface", "introduction", "foreword", "appendix"]
  links = soup.findAll('a', class_="enable")
  link = links[0]
  title = link.text.strip()
  url = "https://m.egwwritings.org" + link.get('href')
  if title.lower() not in excluded_titles:
    title_list.append(title)
    url_list.append(url)
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  next_url = soup.find_all('a', class_='btn-large')
  next_url = "https://m.egwwritings.org" + next_url[1].get('href')
  while True:
    page = requests.get(next_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find_all('span', class_="egw_content")
    if len(title) == 0:
      break
    title = title[0]
    title = title.text.strip()
    print(title)
    if title.lower() not in excluded_titles:
      title_list.append(title)
      url_list.append(next_url)
    next_url = soup.find_all('a', class_='btn-large')
    next_url = "https://m.egwwritings.org" + next_url[1].get('href')
  return url_list, title_list
  

#Takes TOC url and adds all to Xata
def toc_to_xata(url):
  starttime = time.time()
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  url_list, title_list = get_sectioned_urls(soup)
  url_list = enumerate(url_list)
  endtime = time.time()
  print("Time taken to get URL's:", endtime - starttime)
  starttime = time.time()
  for i in url_list:
    num = i[0]
    title = title_list[num]
    url2xata(i[1], title)
    print('Completed chapter: ' + title)
  endtime = time.time()
  print("Time taken to scrape content:", endtime - starttime)
    


#Table of Contents URL's for STC and COTA series
stc_url = 'https://m.egwwritings.org/en/book/108.21/toc'
pp_url = 'https://m.egwwritings.org/en/book/84.4/toc'
pk_url = 'https://m.egwwritings.org/en/book/88.8/toc'
da_url = 'https://m.egwwritings.org/en/book/130.4/toc'
aa_url = 'https://m.egwwritings.org/en/book/127/toc'
gc_url = 'https://m.egwwritings.org/en/book/132.2/toc'

#Calling the function - disabled to avoid accidents
#toc_to_xata(pk_url)

#Next, build a function that gets all the urls/list of books printed before 1915. So I can start working on it. 