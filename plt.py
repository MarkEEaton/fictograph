import json
import clean
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.interpolate import spline
from adjustText import adjust_text


def plot_it(data):    
    """ generate a plot of the author's books """

    if len(data) <= 1:
        print('This author does not have enough books to graph')
        return

    df = pd.DataFrame(data=data)
    df = df.sort_values(['date'])
    
    sns.set(style='darkgrid')

    # if there's only two books, don't bother smoothing
    if len(df) == 2:
        x = df.date
        y = df.rating
        ax = plt.plot(x, y)
    
    # otherwise make it smooth
    else:
        x_smooth = np.linspace(df.date.min(), df.date.max(), num=200)
        y_smooth = spline(df.date, df.rating, x_smooth, order=2)
        ax = plt.plot(x_smooth, y_smooth)
    
    # set the ticks and limits
    date_max = df.date.max() + 2 
    date_min = df.date.min() - 2
    date_range = range(date_min, date_max, 4)
    
    plt.xticks(date_range, date_range, rotation='vertical')
    plt.tick_params(axis='y',
                    which='both',
                    left='off',
                    right='off',
                    labelleft='off')
    plt.xlim(date_min, date_max)
    
    # set up the labels
    texts = []
    for x, y, s in zip(df.date, df.rating, df.title):
        texts.append(plt.text(x, y, s, fontsize=6))
    
    # make the labels adjust to each other
    adjust_text(texts,
                force_text=10,
                va='top',
                only_move={'text': 'y', 'points': 'y'},
                arrowprops=dict(arrowstyle='-', color='black', lw=0.5))
    
    plt.ylabel('Awesomeness')
    plt.show()

if __name__ == '__main__':
    with open('auster.json', 'r') as data_file:
        read_data = data_file.read()
        json_data = json.loads(read_data)
    cleaned_data = clean.clean(json_data)
    plot_it(cleaned_data)
