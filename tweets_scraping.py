from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm

import pandas as pd
import datetime
import psutil

# Login 
def twitter_login(driver, email, username, password):
    driver.implicitly_wait(5)
    
    # Email
    login_email = driver.find_element_by_css_selector("input[autocomplete='username']")
    login_email.clear()
    login_email.send_keys(email)
    login_email.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    
    # Username
    try:
        login_username = driver.find_element_by_css_selector("input[autocomplete='on']")
        login_username.send_keys(username)
        login_username.send_keys(Keys.RETURN)
        driver.implicitly_wait(5)
    except: 
        driver.implicitly_wait(5)
        
    # Password
    login_password = driver.find_element_by_css_selector("input[autocomplete='current-password']")
    login_password.clear()
    login_password.send_keys(password)
    login_password.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)

# Explore/Search Top hashtag
def twitter_search(driver, search_link, num_of_tweets):
    driver.get(search_link)
    try:
        driver.maximize_window()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']")))     
    except:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']")))     
    
    tweet_url_list = reaction_list = []
    tweets_data = pd.DataFrame(columns=['Tweets','ID','Date','Likes','Retweets','Quote_Tweets','Replies','Source','Location','Tweet_URL','Display_Name','Username','Profile_URL','Verified'])
    while len(tweet_url_list) < num_of_tweets:
        # From Main Page
        tweet_url_list = tweet_url_list + [i.get_attribute('href') for i in driver.find_elements_by_css_selector("a[class='css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0']:not(div[class='css-1dbjc4n r-1ets6dv r-1867qdf r-rs99b7 r-1loqt21 r-adacv r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg'])")]
        reaction_list = reaction_list + [[i.get_attribute('aria-label')] for i in driver.find_elements_by_css_selector("div[class='css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws']")]
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)
        
    if len(tweet_url_list) != len(reaction_list):
        driver.close()
        raise ValueError("tweet_url and reaction list not equal length")
    retrieve_dict = dict(zip(tweet_url_list, reaction_list))
    
    # Individual Page
    for key in tqdm(retrieve_dict):
        temp_store = tweets_data.copy().to_dict()
        
        try:
            driver.get(key)
            time.sleep(5) # let page load
            
            temp_store['Tweets'] = driver.find_element_by_css_selector("div[class='css-901oao r-18jsvk2 r-37j5jr r-1blvdjr r-16dba41 r-vrz42v r-bcqeeo r-bnwqim r-qvutc0']").text
            temp_store['ID'] = key.split('status/',1)[1]
            temp_store['Date'] = driver.find_element_by_css_selector("a[class='css-4rbku5 css-18t94o4 css-901oao css-16my406 r-14j79pv r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0']").text
            temp_store['Location'] = None
            temp_store['Source'] = driver.find_element_by_css_selector("a[class='css-4rbku5 css-18t94o4 css-901oao css-16my406 r-14j79pv r-1loqt21 r-poiln3 r-bcqeeo r-1jeg54m r-qvutc0']").text
            temp_store['Tweet_URL'] = key
            temp_store['Display_Name'] = driver.find_element_by_css_selector("div[class='css-1dbjc4n r-18u37iz r-15zivkp'] div[class='css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0']").text
            temp_store['Username'] = driver.find_element_by_css_selector("div[class='css-1dbjc4n r-18u37iz r-15zivkp'] a[class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l']").text
            temp_store['Profile_URL'] = driver.find_element_by_css_selector("div[class='css-1dbjc4n r-18u37iz r-15zivkp'] a[class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l']").get_attribute('href')
            
            try:
                temp_store['Replies'] = int([int(s) for s in [i.split() for i in retrieve_dict[key][0].split(",") if 'repl' in i][0] if s.isdigit()][0])
            except:
                temp_store['Replies'] = 0
            
            try:
                temp_store['Likes'] = int([int(s) for s in [i.split() for i in retrieve_dict[key][0].split(",") if 'like' in i][0] if s.isdigit()][0])
            except:
                temp_store['Likes'] = 0
        
            if 'Retweet' in retrieve_dict[key][0]:
                rt = [i.text for i in driver.find_elements_by_css_selector("a[class='css-4rbku5 css-18t94o4 css-901oao r-18jsvk2 r-1loqt21 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']")]
                try: 
                    temp_store['Quote_Tweets'] = int([int(s) for s in [i.replace(",","").split() for i in rt if 'Quote Tweet' in i][0] if s.isdigit()][0])
                except:
                    temp_store['Quote_Tweets'] = 0
                try:
                    temp_store['Retweets'] = int([int(s) for s in [i.replace(",","").split() for i in rt if 'Retweet' in i][0] if s.isdigit()][0])
                except:
                    temp_store['Retweets'] = 0
            else:
                temp_store['Quote_Tweets'] = 0
                temp_store['Retweets'] = 0

            try:
                driver.find_element_by_css_selector("div[class='css-1dbjc4n r-18u37iz r-15zivkp'] svg[class='r-1cvl2hr r-4qtqp9 r-yyyyoo r-1xvli5t r-9cviqr r-f9ja8p r-og9te1 r-bnwqim r-1plcrui r-lrvibr']")
                temp_store['Verified'] = True
            except:
                temp_store['Verified'] = False
        
            tweets_data = tweets_data.append(temp_store, ignore_index=True)    
        
        except:  
            time.sleep(2)
            
    return tweets_data

if __name__ == '__main__':
    # initialize driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.wait = WebDriverWait(driver, 5)

    email = input('twitter email address -> ')
    username = input('twitter username -> ')
    password = input('twitter password -> ')

    start_time = datetime.datetime.now()
    driver.get("https://twitter.com/login")
    twitter_login(driver, email, username, password)

    tweets = twitter_search(driver, 'https://twitter.com/search?q=tesla%20-nikola%20lang%3Aen&src=typed_query&f=live', 200)
    tweets.to_csv('tweets.csv')

    end_time = datetime.datetime.now()
    print('elapsed time: ', end_time-start_time)

    print('', psutil.cpu_percent())
    print(psutil.virtual_memory())
    print('memory % used:', psutil.virtual_memory()[2])

    driver.quit()