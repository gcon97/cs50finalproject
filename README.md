# cs50finalproject
Trending Tracker - 

This site allows you to track trending topics from around the world. 
It works by checking 3 mainstream websites, Twitter, Google and BuzzFeed. 

To collect the Twitter trending topics, I used Twitter's own API to perform a GET api request which allowed me to collect the real time trending topics. These are saved into my own dictionary structure and passed to Flask to be presented in the front end HTML

To collect the Google and Buzzfeed trending topics I used BeatifulSoup4 to scrape their RSS feeds which stores their trending topics, searches or articles. From there I processed the data to remove their HTML tags before passing it back to Flask to display on the front end.

The site does have a user management system, the idea is to progress in the future to allow the user to save trending preferences, for example. Perhaps display US trending, or trending based of their current location. For now it is set to the UK.