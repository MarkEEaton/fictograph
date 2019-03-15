""" make the plot """
import io
import base64
from math import floor
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from scipy.interpolate import pchip
from adjustText import adjust_text

# import order matters! may break if reordered.



def plot_it(data):
    """ generate a plot of the author's books """

    if len(data) <= 1:
        print("This author does not have enough books to graph")
        return None

    # create a dataframe
    df = pd.DataFrame(data=data)
    df = df.sort_values(["date"])

    # if there's only two books, don't bother smoothing
    if len(df) == 2:
        x = df.date
        y = df.rating
        ax = plt.plot(x, y)

    # otherwise, smooth the line
    else:
        x_smooth = np.linspace(df.date.min(), df.date.max(), num=400)
        pch = pchip(df.date, df.rating)
        plt.plot(x_smooth, pch(x_smooth), "b-", label="pchip")

    # set the ticks and limits
    date_max = floor(df.date.max()) + 2
    date_min = floor(df.date.min()) - 2

    ylim_max = df.rating.max() + 0.2
    ylim_min = df.rating.min() - 0.2

    plt.ylim(ylim_min, ylim_max)
    plt.locator_params(axis="x", nbins=14)
    plt.xlim(date_min, date_max)
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    # set up the labels
    texts1 = []
    texts2 = []
    zipped = zip(df.date, df.rating, df.title)
    sorted_items = sorted(zipped, key=lambda t: t[1], reverse=True)
    top = sorted_items[:5]
    bottom = sorted_items[-5:]
    for x, y, s in top[:5]:
        texts1.append(plt.text(x, y, s, fontsize=8))
    for x, y, s in bottom[:5]:
        texts2.append(plt.text(x, y, s, fontsize=8))

    # make the labels adjust to each other
    adjust_text(
        texts1,
        force_text=10,
        va="top",
        only_move={"text": "y", "points": "y"},
        arrowprops=dict(arrowstyle="-", color="black", lw=0.5),
    )
    adjust_text(
        texts2,
        force_text=10,
        va="top",
        only_move={"text": "y", "points": "y"},
        arrowprops=dict(arrowstyle="-", color="black", lw=0.5),
    )

    plt.ylabel("Awesomeness\n(average Goodreads stars)")

    # to the web!
    fig = plt.gcf()
    fig.set_size_inches(7, 7)
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url


def faux_plot():
    """ this empty plot shows on the index page before a search is run """

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url


if __name__ == "__main__":
    faux_plot()
