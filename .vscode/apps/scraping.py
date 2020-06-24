# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    hem_title, hem_img = mars_hemi()

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "title": hem_title,
        "img_url": hem_img
    }

    browser.quit()

    return data

### Featured Article

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    # Set up HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    # Find title of articles
    slide_elem.find("div", class_='content_title')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_p

### Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url


# ### Facts

def mars_facts():

    # Read html page with Pandas
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)


    # Convert DataFrame back to html
    return df.to_html()


def mars_hemi():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Visit the mars hemisphere site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up HTML parser
    html = browser.html
    hem_soup = BeautifulSoup(html, 'html.parser')

    # Find all h3 headings
    hem_title = hem_soup.find_all('h3')
    hem_title

    # Put titles in a list
    hem_list = []
    for title in hem_title:
        word = title.text
        hem_list.append(word)

    url_list = []
    for index in [0,1,2,3]:
        
        # Visit the mars hemisphere site
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
        
        # Find the title button and click that
        more_info_elem = browser.find_link_by_partial_text(hem_list[index])
        more_info_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        # Find the relative image url
        hem_url_rel = img_soup.find('img', class_ = "wide-image").get("src")

        # Use the base URL to create an absolute URL
        hem_url = f'https://astrogeology.usgs.gov/{hem_url_rel}'

        url_list.append(hem_url)

    return hem_list, url_list

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())