# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page

    # search for elements with a specific combination of tag (div) and attribute (list_text)
    # wait one second before searching for components -- useful because sometimes dynamic pages take a while to load, especially if they are image-heavy.
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up HTML parser
    # Convert the browser html to a soup object

    html = browser.html
    news_soup = soup(html,'html.parser')

    # set a variable to look for the <div /> tag and its descendent(the other tags within the <div /> element)
    # Use the . to  select classes. The code 'div.list_text' pinpoints the <div /> tag with the class of list_text.
    # this is our parent element 

    try: 
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()



        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p
    


# ### JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# ### Mars Facts

def mars_facts():
    try: 
        # Use Pandas' .read_html() function to scrape the entire table with instead of scraping each row or the data in each <td />
        # read_html() specifically searches for and returns a list of tables found in the HTML.
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None 
    
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    return df.to_html()


def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # create a html object assigned to the html variable
    html = browser.html
        
    # use beautiful soup to parse the html object 
    image_soup = soup(html, 'html.parser')
        
    # use Beautiful Soup to find all 'span' tags with a class of text 
    try:
        images = image_soup.find_all('div', class_='item')
            
        # prints out the page number and each quote on the page
        index = 0 
        for image in images:
            hemispheres = {}
            full_image_elem = browser.find_by_tag('h3')[index]
            full_image_elem.click()
            html = browser.html
            title_soup = soup(html, 'html.parser')
            title = title_soup.find('h2').text
            img_url = title_soup.find('div', class_='downloads').find('a')['href']
            hemispheres = {'title':title, 'img_url':url+img_url}
            hemisphere_image_urls.append(hemispheres)
            index = index + 1
            browser.back()
    except: 
        return None 



    # 4. Print the list that holds the dictionary of each image url and title.
    return  hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



