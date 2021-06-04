from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


#setting up chrome control
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


#navigating to the NASA Mars page
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)

#inspect, parse, and find tags for title and sub-title
html = browser.html
soup = bs(html, "html.parser")

top_news = soup.find("div", class_="list_text")
title = top_news.find("div", class_="content_title")
title = title.text.strip()


#inspect, parse, and find tags for sub-title
sub_title = top_news.find('div', class_='article_teaser_body')


#visit Jet Propultion lab 
jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(jpl_url)


#using beautiful soup to parse
jpl_html = browser.html
soup = bs(jpl_html, "html.parser")
top_image = soup.find("img", class_="headerimage fade-in")['src']

#mars Facct
mars_facts_url = 'https://space-facts.com/mars/'

#navigating to mars fact page
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
mars_facts_url = 'https://space-facts.com/mars/'
browser.visit(mars_facts_url)

#reading the data into a dataframe
mars_data = pd.read_html(mars_facts_url)
mars_data = pd.DataFrame(mars_data[0])


#converting the dataframe to HTMl file
mars_facts = mars_data.to_html(header = False, index = False)


#Navigate to Hemispherse site
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)

#inspect, parse,
html = browser.html
soup = bs(html, "html.parser")

#creating a loop to append title and images to list
hemisphere_list = []
category = soup.find("div", class_ = "result-list" )
hemispheres =category.find_all("div", class_="item")
for hemisphere in hemispheres:
    titles = hemisphere.find('h3').text
    titles = titles.strip('Enhanced')
    hemisphere = hemisphere.find("a")["href"]
    pic_link = ('https://astrogeology.usgs.gov/'+hemisphere)
    browser.visit(pic_link)
    hemisphere_html = browser.html
    soup = bs(hemisphere_html, 'html.parser')
    image_pic = soup.find('div', class_="downloads")
    final_pic = image_pic.find('a')['href']
    hemisphere_list.append({"title": titles, "image_url": final_pic})


browser.quit()
