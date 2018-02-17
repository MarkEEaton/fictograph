import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import linspace
from scipy.interpolate import spline
from pprint import pprint
from adjustText import adjust_text


def plot_it(data):    
    df = pd.DataFrame(data=data)
    df = df.sort_values(['date'])
    
    #x_smooth = linspace(df['date'].min(), df['date'].max(), 200)
    #y_smooth = spline(df['date'], df['rating'], x_smooth)

    sns.set(style='darkgrid')
    
    ax = df.plot.line(x='date', y='rating')
    
    # set the ticks and limits
    date_max = df['date'].max() + 5
    date_min = df['date'].min()
    date_range = range(date_min, date_max, 5)
    
    ylim_max = df['rating'].max() + 0.2
    ylim_min = df['rating'].min() - 0.2
    plt.xticks(date_range, rotation='vertical')
    plt.ylim(ylim_min, ylim_max)
    
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
    with open('data.py', 'r') as data_file:
        read_data = data_file.read()
        json_data = json.loads(read_data)
    plot_it(json_data)
