# Twitter-Web-Scraper

This scraper is coded using python to scrape through 200 recent tweets regarding the brand Tesla. It uses the library Selenium to mannually go through each tweet post and extract the necessary details and then stores these information into a CSV file.

# Instructions
1. Before running the codes, please ensure that you have the required packages installed. 
	- `pip install selenium`
	- `pip install webdriver-manager`
	- `pip install pandas`
	- `pip install time`
	- `pip install tdsm`
	- `pip install datetime`
	- `pip install psutil`
2. After installation of packages, modify the parameter input of 
  - `twitter_login` function: with a **valid email address, username and password** that will able to access and log into Twitter
  - `twitter_search` function: with the **search URL, and the number of tweets to scrape**.
4. Lastly change the **file path** in `tweets.to_csv('C:/Users/user/desktop/tweets.csv')` to the directory that you would like the csv file to be stored in.
