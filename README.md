# Twitter-Web-Scraper

This scraper is coded using python to scrape through 200 recent tweets regarding the brand Tesla. It uses the library Selenium to mannually go through each tweet post and extract the necessary details and then stores these information into a CSV file.

## Instructions
1. Before running the codes, please ensure that you have the required packages installed. 
	- `pip install -r requirements.txt`
2. After installation of packages, modify the parameter input of 
  - `twitter_login` function: with a **valid email address, username and password** that will able to access and log into Twitter
  - `twitter_search` function: with the **search URL, and the number of tweets to scrape**.
3. Lastly change the **file path** in `tweets.to_csv('<dir>/tweets.csv')` to the directory that you would like the csv file to be stored in.
