# MTG scraper


This repo extracts data about Magic The Gathering collectible card game. The initial script extracts data from 2 different websites so that it can scrape
all the info that is necessary for using a card in a deck,its image and its current price. The main idea is to have a database with the price of each card
which I will then use to create playable decks for personal or commercial use.

## Content

There are 5 scripts in this repo. 
1. scraper_classes.py contains the classes used to scrape the info of every card.
2. card_data.py scrapes the info from every card in the sets chosen (all or part).
3. mtg_prices_scraper_function.py scrapes the prices of every card in the game.
4. combine_data.py combines info and prices.
5. data_cleaning.py cleans the data and saves everything in a .csv file
in the repo there are also the chromedriver.exe that is used to run those files. The libraries needed are:
* selenium
* math
* time
* pandas

## How to use it

The steps are quite straightforward:
1. card_data.py
2. mtg_prices_scraper_function.py
3. combine_data.py
4. data_cleaning.py

Once you run card_data.py for all the sets and you get all the cards, then you only need to run 2, 3, 4 regularly (or when needed) to get a recent update on the card values. card_data.py needs to be run again only when Wizards releases a new set of cards.

## Improvements

There are quite a lot of things I want to add to make it more complete. 
1. I plan to extract the collector's number for every card, the flavour text and the artist 
so that I can have all the info that is on every card. (Done) 
2. I want to gather info that is available online on different decks to check the "popularity" of every card and its correlation with its price. 
3. I also want to add a function that, once I download the first database, it will allow the scraper to check 
only for new sets and not run through all of them again. #
4. I also want to "decentralise" the card info extraction and the price extraction so that I can only run an update on the prices. (Done)
Ideas, suggestions, feedback are always welcome.

