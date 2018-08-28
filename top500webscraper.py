#import libraries for scraping, processing and data formatting

from lxml import html
import grequests  
from bs4 import BeautifulSoup
import pandas as pd

#read csv and convert URLs to list with http:// preceeding url to work with grequests
top500_df = pd.read_csv('top500.domains.05.18.csv')
top500_clean_df = top500_df.loc[:,["Rank","URL"]]
pages = top500_clean_df["URL"].tolist()
h = 'http://'
http_pages = [h + page for page in pages]

#scrape and gather results
unsent_request = (grequests.get(url) for url in http_pages)

results = grequests.map(unsent_request) 

#set empty list of pages with src in script tag(inline JS), iterate through result's for script tags
#containing src and append to list, print pages with inline JS.

srcPages = []

for r in results[:]:
    for n in BeautifulSoup(r.text,'html.parser').find_all('script'):
        if 'src' in n.attrs:
            js = n['src']
            if r.url not in srcPages:
                srcPages.append(r.url)
                print(srcPages)
                