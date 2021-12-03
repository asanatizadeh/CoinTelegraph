import time
import pandas as pd
from selenium import webdriver as wd
from selenium.webdriver import ActionChains
from tqdm import tqdm

# https://chromedriver.chromium.org/downloads

chrome_driver_path = '/Users/hamid/PycharmProjects/cointelegraph/chromedriver'

chrome_options = wd.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')

browser = wd.Chrome(chrome_driver_path, options=chrome_options)

url: str = input("enter the link to scrape: \n")
file_name: str = input("enter the name of the file name: \n")
num_pages: int = input("number of pages to scrape: \n")

def get_title(element):
    return element.find_element_by_class_name("post-card-inline__title").text


def get_date(element):
    return element.find_element_by_tag_name("time").get_attribute("datetime")


def get_author_profile(element):
    return element.find_element_by_class_name("post-card-inline__author").find_element_by_tag_name(
        "a").get_attribute("href")


def get_author(element):
    return element.find_element_by_class_name("post-card-inline__author").find_element_by_tag_name(
        "a").text


def summary_text(element):
    return element.find_element_by_class_name("post-card-inline__text").text


def get_views(element):
    return element.find_element_by_class_name("post-card-inline__stats").text


def get_news_url(element):
    return element.find_element_by_tag_name("a").get_attribute("href")


if __name__ == '__main__':

    browser.get(url)

    for i in tqdm(range(0, int(num_pages))):
        time.sleep(3)
        browser.execute_script("scrollBy(0,10000);")
        button = browser.find_element_by_class_name("posts-listing__more-wrp")
        ActionChains(browser).click(button).perform()

    time.sleep(3)
    news_titles = browser.find_elements_by_class_name("post-card-inline__content")

    news = []
    for item in tqdm(news_titles):
        title_text = get_title(item)
        article_date = get_date(item)
        author_profile = get_author_profile(item)
        author_name = get_author(item)
        summary = summary_text(item)
        views = get_views(item)
        url = get_news_url(item)
        info = [title_text,
                article_date,
                author_profile,
                author_name,
                summary,
                views,
                url]

        news.append(info)

    news_df = pd.DataFrame(news,
                           columns=["title_text", "article_date", "author_profile", "author_name", "summary", "views",
                                    "url"])

    news_df.to_csv(f"Output/{file_name}", index=False)

    browser.close()