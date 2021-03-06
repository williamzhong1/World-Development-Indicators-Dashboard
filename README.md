# World Development Indicators Dashboard

**Please view 'Demo' video** accessible [here](https://youtu.be/1wybdaavOPU) or downloadable from the repository

## Description
Simple data dashboard built in Python, based on Dash & Flask. The app serves a single web-page with a scatter plot, showing GDP against life expectancy. Underneath is a bar-chart of C02 emissions over time.

Plots are interactive, allowing the user to filter the displayed data based on different countries and year. Data is pulled in from a SQLite database, and handled using Pandas.



## Dependencies
This app relies on external modules and the database file. To run this app yourself you will need to install Dash, Plotly, Pandas and sqlite3 via pip. Dash includes multiple dependencies which may have to be installed in addition to the main Dash package. Check the top lines of 'App.py' to confirm all dependencies. Database file available on request.
