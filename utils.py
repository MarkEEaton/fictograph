import requests
import aiohttp
import asyncio
import key
from random import uniform
from bs4 import BeautifulSoup

def clean(data):
    sorted_data = sorted(data, key=lambda k: k['date'])

    cleaned = []
    for i, item in enumerate(sorted_data):
        try:
            if item['date'] ==  sorted_data[i+1]['date']:
                cleaned.append({'title': item['title'],
                                'date': item['date'] + uniform(0, 1),
                                'rating': item['rating'],
                                'id': item['id']
                                })
            else:
                cleaned.append(item)
        except IndexError:
            cleaned.append(item)
    return cleaned

def gather_books(soup):
    urls = []

    for book in soup.find_all('book'): 
        # use the book.show api to get original publication year
        url = 'https://www.goodreads.com/book/show.xml?key=' + key.token + '&id=' + book.id.string
        urls.append(url)
    return urls

async def fetch(session, url):
    with aiohttp.Timeout(40):
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.text()


async def fetch_all(session, urls, loop):
    results = await asyncio.gather(*[loop.create_task(fetch(session, url)) for url in urls])
    return results

def run_asy(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with aiohttp.ClientSession(loop=loop) as session:
        htmls = loop.run_until_complete(
            fetch_all(session, urls, loop))
    
    works = []
    for page in htmls:
        soup3 = BeautifulSoup(page, 'xml')
        try:
            year = soup3.book.work.original_publication_year.string

            # truncate long titles
            if len(soup3.book.title.string) > 20:
                title = soup3.book.title.string[:20] + '...'
            else:
                title = soup3.book.title.string
       
            if year != None:
                work = {
                   'title': title,
                   'date': int(year),
                   'rating': float(soup3.book.average_rating.string),
                   'id': soup3.book.id.string
                }
                works.append(work)
            else: pass 
        except Exception as e:
            print(e)
    return works
