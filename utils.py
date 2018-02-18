import requests
import aiohttp
import asyncio
import key
from bs4 import BeautifulSoup

def clean(data):
    cleaned = []
    for i in range(len(data)):
        try:
            if data[i]['date'] != data[i+1]['date']:
                cleaned.append(data[i])
        except IndexError:
            cleaned.append(data[i])
    return cleaned

def asy(soup):
    works = []

    for book in soup.find_all('book'): 
        print(book.title.string)
        # use the book.show api to get original publication year
        req3 = requests.get('https://www.goodreads.com/book/show.xml?key=' + key.token + '&id=' + book.id.string)

        soup3 = BeautifulSoup(req3.text, 'xml')
        try:
            year = soup3.book.work.original_publication_year.string

            # truncate long titles
            if len(book.title.string) > 20:
                title = book.title.string[:20] + '...'
            else:
                title = book.title.string
       
            if year != None:
                work = {
                   'title': title,
                   'date': int(year),
                   'rating': float(book.average_rating.string),
                   'id': book.id.string
                }
                works.append(work)
            else: pass 
        except Exception as e:
            print(e)
    return works
