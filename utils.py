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

def gather_books(soup):
    urls = []

    for book in soup.find_all('book'): 
        # use the book.show api to get original publication year
        url = 'https://www.goodreads.com/book/show.xml?key=' + key.token + '&id=' + book.id.string
        urls.append(url)
    return urls

async def fetch(session, url):
    with aiohttp.Timeout(10):
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
