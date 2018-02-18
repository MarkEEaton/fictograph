import requests
import lxml
import json
import key
import clean
from plt import plot_it
from bs4 import BeautifulSoup
from wtforms import Form, StringField, validators
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

class SearchForm(Form):
    """ set up wtforms class """
    keywords = StringField('query', [
        validators.Length(max=200, message="length"),
        validators.Regexp('^[\-\+a-zA-Z]*$', message='regex')])


@app.route('/')
def index():
    return render_template('index.html', plot_url='')

@app.route('/getPlot', methods=['POST'])
def getPlot():
    # get the author's name
    name = request.form['authorname'] 
    name = name.replace(' ', '+')
    
    form = SearchForm(keywords=name)
    if form.validate():
        # search the author name and get the author id
        req1 = requests.get('https://www.goodreads.com/api/author_url/' + name + '?key=' + key.token)
        soup1 = BeautifulSoup(req1.text, 'xml')
        auth_id = soup1.author['id']
        
        # get the author's books based on the author id
        req2 = requests.get('https://www.goodreads.com/author/list.xml?key='+ key.token + '&page=1-10&id=' + auth_id)
        soup2 = BeautifulSoup(req2.text, 'xml')
        
        # create the data list
        works = []
        print("Number of books found: " + str(len(soup2.find_all('book'))))
        for book in soup2.find_all('book'):
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

        cleaned_data = clean.clean(works)
        plot_url = plot_it(cleaned_data)
        return render_template("index.html", plot_url=plot_url)
        
    else:
        print('failed regex')

app.secret_key = key.key

if __name__ == '__main__':
     app.run(port=8000, host='127.0.0.1', debug=True)
