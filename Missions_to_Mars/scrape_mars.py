# import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import datetime as dt
import time

# Set executable path and initialize chrome browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser("chrome", **executable_path, headless=False)

# NASA Mars News and visit the Nasa Mars news site
def mars_news (browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Get first list item
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    # Parse results HTML with BeautifulSoup, <ul class="item_list">, <li class="slide">
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        # Scrape the latest news title and use parent element to find first <a> tag and save it as news_title
        news_title = slide_element.find("div", class_="content_title").get_text()

        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph

# NASA (Jet Propulsion Laboratory) 
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Ask splinter to go to site and click button with class name full_image
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # Parse results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 
   # Use Base URL to Create Absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url

# Mars weather
# Mars weather Twitter account web scraper
def twitter_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    
    # Parse Results HTML with BeautifulSoup
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    
    # Find a Tweet with the data-name `Mars Weather`
    mars_weather_tweet = weather_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
   # Search within Tweet for <p> tag containing tweet text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    return mars_weather

# Mars Facts (Mars Facts Web Scraper)
# Visit the Mars Facts site using Pandas to Read
mars_facts = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_facts)
mars_facts.reset_index(inplace=True)
mars_facts.columns=["ID", "Properties", "Mars", "Earth"]
mars_facts

# Mars Hemispheres
# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology science center site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls = []

    # Get a list of all the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on each loop to avoid exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find sample image tag and extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere title and append hemisphere object to list
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate backwards
        browser.back()
    return hemisphere_image_urls

# Helper function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere

# Main Web Scraping Bot
def scrape_all():
    executable_path = {"executable_path": {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())