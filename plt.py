import json
import clean
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.interpolate import spline
from pprint import pprint
from adjustText import adjust_text


def plot_it(data):    
    df = pd.DataFrame(data=data)
    df = df.sort_values(['date'])
    
    # make it smooth
    x = np.linspace(df['date'].min(), df['date'].max(), num=200)
    y_smooth = spline(df['date'], df['rating'], x, order=2)
    
    sns.set(style='darkgrid')
    ax = plt.plot(x, y_smooth)
    
    # set the ticks and limits
    date_max = df['date'].max() + 5
    date_min = df['date'].min()
    date_range = range(date_min, date_max)
    
    ylim_max = df['rating'].max() + 0.2
    ylim_min = df['rating'].min() - 0.2

    plt.xticks(date_range, date_range, rotation='vertical')
    plt.ylim(ylim_min, ylim_max)
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
    
    plt.ylabel('Average Goodreads Star Rating')
    plt.show()

if __name__ == '__main__':
    with open('black.json', 'r') as data_file:
        read_data = data_file.read()
        json_data = json.loads(read_data)
    pprint(json_data)
    cleaned_data = clean.clean(json_data)
    plot_it(cleaned_data)
