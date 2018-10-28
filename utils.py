""" some tools to work with the data """
import asks
import trio
import multio
from random import uniform
import aiohttp  # use version 2.3.10
from bs4 import BeautifulSoup
import key


def clean(data):
    """ clean the data """

    # sort the data by date
    sorted_data = sorted(data, key=lambda k: k['date'])

    cleaned = []

    # if there are duplicate dates, add some randomness so that they are not
    # exact duplicates
    for i, item in enumerate(sorted_data):
        try:
            if item['date'] == sorted_data[i+1]['date']:
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
    """ assemble the urls for all of the author's books """

    urls = []
    for book in soup.find_all('book'):
        # use the book.show api to get original publication year
        url = 'https://www.goodreads.com/book/show.xml?key='\
              + key.token + '&id=' + book.id.string
        urls.append(url)
    return urls


htmls = []

async def fetch(url: str):
    response = await asks.get(url)
    htmls.append(response.content)


def run_asy(urls: list):
    multio.init('trio')
    return trio.run(nurs, urls)


async def nurs(urls: list):
    async with trio.open_nursery() as nursery:
        for url in urls:
            nursery.start_soon(fetch, url, name=url)

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

            if year is not None:
                work = {
                    'title': title,
                    'date': int(year),
                    'rating': float(soup3.book.average_rating.string),
                    'id': soup3.book.id.string
                       }
                works.append(work)
            else:
                pass
        except Exception as e:
            print(e)
    return works
