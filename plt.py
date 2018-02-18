import json
import clean
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.interpolate import pchip
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
    
    else:
        x_smooth = np.linspace(df.date.min(), df.date.max(), num=200)
        pch = pchip(df.date, df.rating)
        plt.plot(x_smooth, pch(x_smooth), 'b-', label='pchip')    
    
    # set the ticks and limits
    date_max = df.date.max() + 2 
    date_min = df.date.min() - 2
    date_range = range(date_min, date_max, 4)
    
    ylim_max = df.rating.max() + 0.2
    ylim_min = df.rating.min() - 0.2

    plt.ylim(ylim_min, ylim_max)
    plt.xticks(date_range, date_range, rotation='vertical')
    plt.xlim(date_min, date_max)

    # set up the labels
    texts1 = []
    texts2 = []
    zipped = zip(df.date, df.rating, df.title)
    sorted_items = sorted(zipped, key=lambda t: t[1], reverse=True)
    top = sorted_items[:5]
    bottom = sorted_items[-5:]
    for x, y, s in (top[:5]):
        texts1.append(plt.text(x, y, s, fontsize=6))
    for x, y, s in (bottom[:5]):
        texts2.append(plt.text(x, y, s, fontsize=6))
    
    # make the labels adjust to each other
    adjust_text(texts1,
                force_text=10,
                va='top',
                only_move={'text': 'y', 'points': 'y'},
                arrowprops=dict(arrowstyle='-', color='black', lw=0.5))
    adjust_text(texts2,
                force_text=10,
                va='top',
                only_move={'text': 'y', 'points': 'y'},
                arrowprops=dict(arrowstyle='-', color='black', lw=0.5))
    
    plt.ylabel('Awesomeness\n(average Goodreads stars)')
    plt.show()

if __name__ == '__main__':
    with open('json/irving.json', 'r') as data_file:
        read_data = data_file.read()
        json_data = json.loads(read_data)
    cleaned_data = clean.clean(json_data)
    plot_it(cleaned_data)
