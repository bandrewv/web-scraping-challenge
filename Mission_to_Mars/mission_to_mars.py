#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Insert dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd


# In[ ]:


# Creating path to NASA's Mars Exploration Program url
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
response = requests.get(url)
html = response.text


# In[ ]:


# Creating a Beautiful Soup object for Latest News
soup = bs(html, 'html.parser')


# In[ ]:


# Pulling the first instance of 'div', class_='content_title' to pull the latest news story
# from 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Pulling the headline from latest news story
news_title = soup.find('div',class_='content_title').text

# Pulling the teaser paragraph for the latest news story
news_p = soup.find('div', class_='rollover_description_inner').text


# In[ ]:


# Setting executable path for chromedriver & opening browser window
executable_path = {'executable_path': 'Resources/chromedriver/chromedriver.exe'}
browser = Browser("chrome", **executable_path, headless=False)

# Pointing Splinter to url
splinter_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit"
browser.visit(splinter_url)
browser.click_link_by_partial_text('FULL IMAGE')


# In[ ]:


# Using current, clicked in Splinter url to grab url for featured image, storing in 'featured_image_url'
image_html = browser.html
soup = bs(image_html,'html.parser')
featured_image_url = 'https://www.jpl.nasa.gov/' + soup.find('img', class_='fancybox-image')['src']


# In[ ]:


# Using Pandas to pull facts table from Mars facts url
tables_url = 'https://space-facts.com/mars/'
tables = pd.read_html(tables_url)
tables_df = tables[0]
tables_df.columns = ['Description','Mars']
tables_df.set_index('Description', inplace=True)

# Pandas converts table to HTML format for use in flask app
facts_html_table = tables_df.to_html()


# In[ ]:


# Navigated to the url 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
# To obtain the image urls and titles of Mars hemisphere images
hemisphere_image_urls = [
    {'title':'Valles Marineris Hemisphere','img_url':'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'},
    {'title':'Cerberus Hemisphere','img_url':'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'},
    {'title':'Schiaparelli Hemisphere','img_url':'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'},
    {'title':'Syrtis Major Hemisphere','img_url':'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'},
]

