# Plot the awesomeness of an author's work over time

## *** This project is no longer being maintained, as Goodreads retired their API in December 2020 ***

![Screenshot of the application](img/sample.png?raw=True)

This application charts the awesomeness of an author's work over time, as measured by those works' average Goodreads star ratings. It does a few things:

- Star ratings are drawn from the Goodreads API
- Charting is done with matplotlib
- The application does fuzzy matching of the name as input by the user versus the name returned by the Goodreads API to confirm a match
- The five highest ranking and five lowest ranking books are labelled on the chart

Sometimes the Goodreads API returns weird results. I've tried to mitigate against this with the fuzzy string matching, but in some cases, there's not much I can do. Sorry!
