import requests
import lxml
import key
import utils
import plt
from bs4 import BeautifulSoup
from wtforms import Form, StringField, validators
from flask import Flask, render_template, request, url_for

app = Flask(__name__)


class SearchForm(Form):
    """ set up wtforms class """
    keywords = StringField('query', [
        validators.Length(max=200, message='You cannot enter more than 200 characters.'),
        validators.Regexp('^[\-\+a-zA-Z]*$', message='Invalid characters in your search string. Use only A-Z, -, and space.'),
        validators.DataRequired(message='You must type in something.')])


@app.route('/')
def index():
    """ display the index page"""

    plot_url = plt.faux_plot()
    return render_template('index.html', error_message='', plot_url=plot_url)


@app.route('/getPlot', methods=['POST'])
def getPlot():
    """ make the plot """

    # get the author's name
    name = request.form['authorname']
    name = name.replace(' ', '+')

    form = SearchForm(keywords=name)
    if form.validate():
        # search the author name and get the author id
        req1 = requests.get('https://www.goodreads.com/api/author_url/'
                            + name + '?key=' + key.token)
        soup1 = BeautifulSoup(req1.text, 'xml')
        if soup1.author == None:
            plot_url = plt.faux_plot()
            return render_template('index.html', error_message='<div class="alert alert-danger" role="alert">Author not found.</div>', plot_url=plot_url)
        auth_id = soup1.author['id']

        # get the author's books based on the author id
        req2 = requests.get('https://www.goodreads.com/author/list.xml?key='
                            + key.token + '&page=1-10&id=' + auth_id)
        soup2 = BeautifulSoup(req2.text, 'xml')
        if int(soup2.author.books['total']) <= 1:
            plot_url = plt.faux_plot()
            return render_template('index.html', error_message='<div class="alert alert-danger" role="alert">This author does not have enough books to graph.</div>', plot_url=plot_url)

        # create the data list
        works = []
        book_urls = utils.gather_books(soup2)
        works = utils.run_asy(book_urls)

        # clean up the data and plot it
        cleaned_data = utils.clean(works)
        plot_url = plt.plot_it(cleaned_data)
        return render_template("index.html", error_message='',
                               plot_url=plot_url)

    else:
        plot_url = plt.faux_plot()
        return render_template('index.html', error_message='<div class="alert alert-danger" role="alert">' + form.errors['keywords'][0] + '</div>', plot_url=plot_url)


app.secret_key = key.key

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)
