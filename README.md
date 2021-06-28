# MTG scraper


This repo extracts data about Magic The Gathering collectible card game. The initial script extracts data from 2 different websites so that it can scrape
all the info that is necessary for using a card in a deck,its image and its current price. The main idea is to have a database with the price of each card
which I will then use to create playable decks for personal or commercial use.

## Content

There are 3 main scripts in this repo. One, the mtg_scraper.py that extracts the info for every card in the MTG database and then continues by extracting the price for
every card, a second, mtg_img_craper.py that downloads the images for every card and stores them on a bucket in AWS and a third, data_cleaning.py that cleans the data. The chromedriver.exe that is used is also in this
repo and the libraries you will need to run it are:
* selenium
* math
* time
* pandas

## How to use it

It is quite straightforward, you firstly run the mtg_scraper.py to gather all the cards and their prices, then you run the mtg_img_scraper.py to download and store the images and finally the data_cleaning.py.

## Improvements

There are quite a lot of things I want to add to make it more complete. I plan to extract the collector's number for every card, the flavour text and the artist 
so that I can have all the info that is on every card. In addition, I want to gather info that is available online on different decks to check the "popularity" 
of every cardand its correlation with its price. I also want to add a function that, once I download the first database, it will allow the scraper to check 
only for new sets and not run through all of them again. I also want to "decentralise" the card info extraction and the price extraction so that I can only run 
an update on the prices.
Ideas, suggestions, feedback are always welcome.

