#!/usr/bin/env python
# coding: utf-8

# # <center>Web Scraping</center>

# <div class="alert alert-block alert-warning">Each assignment needs to be completed independently. Never ever copy others' work or let someone copy your solution (even with minor modification, e.g. changing variable names). Anti-Plagiarism software will be used to check all submissions. No last minute extension of due date. Be sure to start working on it ASAP! </div>

# ##  Collecting Movie Reviews
# 
# Writing a function `getReviews(url)` to scrape all **reviews on the first page**, including, 
# - **title** (see (1) in Figure)
# - **reviewer's name** (see (2) in Figure)
# - **date** (see (3) in Figure)
# - **rating** (see (4) in Figure)
# - **review content** (see (5) in Figure. For each review text, need to get the **complete text**.)
# - **helpful** (see (6) in Figure). 
# 
# 
# Requirements:
# - `Function Input`: book page URL
# - `Function Output`: save all reviews as a DataFrame of columns (`title, reviewer, rating, date, review, helpful`). For the given URL, you can get 24 reviews.
# - If a field, e.g. rating, is missing, use `None` to indicate it. 
# 
#     


# In[1]:


import requests

from bs4 import BeautifulSoup   
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# Add your import statements


# In[2]:



def getReviews(page_url):
    page = requests.get(page_url)
    final=[]
   
    if page.status_code==200:
        soup = BeautifulSoup(page.content,'html.parser')
        divs = soup.select("div.lister-list div.lister-item.mode-detail.imdb-user-review ")
        
        title = []
        reviewer_name = []
        date = []
        rating = []
        review_content = []
        helpful = []
        for idx,div in enumerate(divs):
            page_title = div.select("a.title")
            if page_title != []:
                title.append(page_title[0].get_text(strip=True))
            else:
                title.append("None")
            page_r_name = div.select("span.display-name-link")
            if page_r_name != []:
                reviewer_name.append(page_r_name[0].get_text())
            else:
                reviewer_name.append("None")
            page_date = div.select("span.review-date")
            if page_date != []:
                date.append(page_date[0].get_text())
            else:
                date.append("None")
            page_rating = div.select("span span")
            if page_rating != []:
                rating.append(page_rating[0].get_text())
            else:
                rating.append("None")
            page_review_content = div.select("div.text.show-more__control")
            if page_review_content!=[]:
                review_content.append(page_review_content[0].get_text())
            else:
                review_content.append("None")
            page_helpful =div.select("div.actions.text-muted")
            text=page_helpful[0].get_text(strip=True).split(".")
            if page_helpful!=[]:
                helpful.append(text[0])
            else:
                helpful.append("None")
  
        data = {'title':title,'reviewer_name':reviewer_name,'date':date,'rating':rating,'review_content':review_content,'helpful':helpful}    
        df = pd.DataFrame(data)
            
    
    
   
    
    
    return df


# In[3]:


# Testing the function

page_url = 'https://www.imdb.com/title/tt1745960/reviews?sort=totalVotes&dir=desc&ratingFilter=0'
reviews = getReviews(page_url)

print(len(reviews))
reviews.head()


# ## Collecting Dynamic Content
# 
# Writing a function `get_N_review(url, webdriver)` to scrape **at least 100 reviews** by clicking "Load More" button 5 times through Selenium WebDrive, 
# 
# 
# Requirements:
# - `Function Input`: book page `url` and a Selenium `webdriver`
# - `Function Output`: save all reviews as a DataFrame of columns (`title, reviewer, rating, date, review, helpful`). For the given URL, you can get 24 reviews.
# - If a field, e.g. rating, is missing, use `None` to indicate it. 
# 
# 

# In[4]:


def get_N_Reviews(page_url,driver):
    driver.get(page_url)
    driver.implicitly_wait(10)
    for i in range(6):
        more=driver.        find_element(By.CSS_SELECTOR,"div.ipl-load-more.ipl-load-more--loaded")
        more.click()
   
    soup = BeautifulSoup(driver.page_source,'html.parser')
    divs = soup.select("div.lister-list div.lister-item.mode-detail.imdb-user-review ")
        
    title = []
    reviewer_name = []
    date = []
    rating = []
    review_content = []
    helpful = []
    for idx,div in enumerate(divs):
        page_title = div.select("a.title")
        if page_title != []:
            title.append(page_title[0].get_text(strip=True))
        else:
            title.append("None")
        page_r_name = div.select("span.display-name-link")
        if page_r_name != []:
            reviewer_name.append(page_r_name[0].get_text())
        else:
            reviewer_name.append("None")
        page_date = div.select("span.review-date")
        if page_date != []:
            date.append(page_date[0].get_text())
        else:
            date.append("None")
        page_rating = div.select("span span")
        if page_rating != []:
            rating.append(page_rating[0].get_text())
        else:
            rating.append("None")
        page_review_content = div.select("div.text.show-more__control")
        if page_review_content!=[]:
            review_content.append(page_review_content[0].get_text())
        else:
            review_content.append("None")
        page_helpful =div.select("div.actions.text-muted")
        text = page_helpful[0].get_text(strip=True).split(".")   
        if page_helpful!=[]:
            helpful.append(text[0])
        else:
            helpful.append("None")
  
        data = {'title':title,'reviewer_name':reviewer_name,'date':date,'rating':rating,'review_content':review_content,'helpful':helpful}    
        df = pd.DataFrame(data)
    return df


# In[5]:


# Test the function

executable_path = 'C:/Users/Admin/Downloads/Drive/chromedriver.exe'

driver = webdriver.Chrome(executable_path=executable_path)

page_url = 'https://www.imdb.com/title/tt1745960/reviews?sort=totalVotes&dir=desc&ratingFilter=0'
reviews = get_N_Reviews(page_url, driver)

driver.quit()

print(len(reviews))
reviews.head()


# In[ ]:




