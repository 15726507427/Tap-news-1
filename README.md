# Tap-news
Single web application providing a customized news list for the users. The news are scraped from media sources like CNN, Bloomberg, etc. A machine learning service is designed to model news topics for the ease of news preference recommendation model.

There are two bash script that can easily try the application on localhost.
To start the news pipeline that grab latest news from media sources to the local database, run
``` $ ./news_pipline_laucher.sh ```

To start the application, run
``` $ ./app_launcher.sh ```
To start the application, the news_pipline is not necessarily started.
