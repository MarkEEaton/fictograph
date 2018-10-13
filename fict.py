""" run the fictograph flask application """
import requests
import lxml
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from wtforms import Form, StringField, validators
from fuzzywuzzy import fuzz
import key
import utils
import plt

app = Flask(__name__)

class SearchForm(Form):
    """ set up wtforms class """
    keywords = StringField('query', [
        validators.Length(max=200, message='You cannot enter more than 200 characters.'),
        validators.Regexp(r'^[\-a-zA-Z ]*$',
                          message='Invalid characters in your search string. \
                                   Use only A-Z, -, and space.'),
        validators.DataRequired(message='You must type in something.')])


@app.route('/')
def index():
    """ display the index page"""

    plot_url = plt.faux_plot()
    return render_template('index.html', error_message='', plot_url=plot_url)


@app.route('/get_plot', methods=['POST'])
def get_plot():
    """ make the plot """

    # get the author's name
    untrusted_name = request.form['authorname']

    form = SearchForm(keywords=untrusted_name)
    if form.validate():
        name = untrusted_name.replace(' ', '+')
        # search the author name and get the author id
        req1 = requests.get('https://www.goodreads.com/api/author_url/'
                            + name + '?key=' + key.token)
        soup1 = BeautifulSoup(req1.text, 'xml')

        if soup1.author is not None:
            soup_author = soup1.find('name').contents[0].lower()
            user_author = name.replace('+', ' ').lower()
            fuzz_value = fuzz.ratio(soup_author, user_author)
            print(fuzz_value, user_author, soup_author)

        if (soup1.author is None or fuzz_value < 60):
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
        if len(cleaned_data) <= 1:
            plot_url = plt.faux_plot()
            return render_template('index.html', error_message='<div class="alert alert-danger" role="alert">This author does not have enough books to graph.</div>', plot_url=plot_url)

        plot_url = plt.plot_it(cleaned_data)
        return render_template("index.html", error_message='<div class="alert alert-dark" role="alert">Showing results for: <strong>' + soup2.find('name').string + '</strong></div>',
                               plot_url=plot_url)

    else:
        plot_url = plt.faux_plot()
        return render_template('index.html', error_message='<div class="alert alert-danger" role="alert">' + form.errors['keywords'][0] + '</div>', plot_url=plot_url)


app.secret_key = key.key

#if __name__ == '__main__':
#    app.run(port=8000, host='127.0.0.1', debug=True)
