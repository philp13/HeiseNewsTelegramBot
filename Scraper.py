import os
import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.url_heise = "https://www.heise.de"
        self.url_heise_thema = "https://www.heise.de/thema/"
        self.session = requests.Session()
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
        self.session.headers.update(self.headers)

    # returns current top categories on heise.de
    def get_top_categories(self):
        website = self.session.get(self.url_heise)
        soup = BeautifulSoup(website.content, 'html.parser')
        top_categories = soup.find(class_="topics top-topics__list").text.split()
        return top_categories

    # will return List of Topics in given input category with first value being title and second the url to this topic
    def get_topics_of_category(self, category):
        article_and_links = []
        website = self.session.get(self.url_heise_thema + category)
        soup = BeautifulSoup(website.content, 'html.parser')
        base_content = soup.find(class_="article-index")
        contents = base_content.find_all('article')
        for content in contents:
            title = content.contents[1].attrs['title']
            article_url = self.url_heise + content.contents[1].attrs['href']
            article_and_links.append([title, article_url])
        return article_and_links

    # scrapes newsticker for current day from heise.de/newsticker/, returns List of News with: Time, Title and URL
    def get_newsticker_from_today(self):
        newsticker = []
        url = self.url_heise + "/newsticker/"
        website = self.session.get(url)
        soup = BeautifulSoup(website.content, 'html.parser')
        news_today = soup.find(class_="archive__day")
        current_day = news_today.find('header').text.strip()
        topics = news_today.find_all('li')
        for topic in topics:
            titles = topic.find_all(class_="a-article-teaser__preceded-kicker-container")
            for title in titles:
                url = title.parent.attrs['href']
                if url.startswith('/'):
                    url = self.url_heise + url
                time = title.find(class_="a-datetime__time").text.strip()
                temp_title = title.find(class_="a-article-teaser__title-text").text.strip()
                newsticker.append([time, temp_title, url])
        return newsticker


# temp = Scraper()
# topics = temp.get_topics_of_category('Log4j')
# news = temp.get_newsticker_from_today()

