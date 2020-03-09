# Plot the awesomeness of an author's work over time

![Screenshot of the application](img/sample.png?raw=True)

This application charts the awesomeness of an author's work over time, as measured by those works' average Goodreads star ratings. It does a few things:

- Star ratings are drawn from the Goodreads API
- The application does fuzzy matching of the name as input by the user versus the name returned by the Goodreads API to confirm a match
- the five highest ranking and five lowest ranking books are labelled on the chart

Sometimes the Goodreads API returns weird results. I've tried to mitigate against this with the fuzzing string matching, but ultimately there's not much I can do. Sorry!
