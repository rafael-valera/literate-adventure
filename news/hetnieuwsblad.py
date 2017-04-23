# /usr/bin/python3

"""
    Scraps nieuwblad.be news and retrieves a news object

    Copyright (C) 2017 rafael valera

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import bs4
import requests
import re
import datetime
import textwrap


class NewsEvent:
    """ A simple model class of a news event """

    def __init__(self, **kwargs):
        self.headline = kwargs["headline"]
        self.link = kwargs["link"]
        self.date = kwargs["date"]
        self.content = kwargs["content"]
        self.author = ""
        self.location = ""

    def get_headline(self):
        return self.headline

    def get_date(self):
        return self.date

    def get_content(self):
        return self.content

    def __str__(self):
        return "<NewsEvent {} {} >".format(self.date.date(), self.headline)


class SoupMaker:
    """ BeautifulSoup object maker """

    @staticmethod
    def __get(url):
        """ Sends an GET http request and returns the response as string object """

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept_Language": "nl-NL,nl;q=0.8,en-US;q=0.6,en;q=0.4",
            "Accept_Encoding": "gzip, deflate, sdch",
            "Connection": "keep-alive",
        }
        return requests.get(url=url, headers=headers).text

    @staticmethod
    def make_soup(url):
        """Constructs a BeautifulSoup object from a url"""
        response = SoupMaker.__get(url)
        return bs4.BeautifulSoup(response, "html.parser")


class HetNieuwsblad:
    """ Retrieves NewsEvent objects from the website www.nieuwsblad.be """

    # HetNieuwsblad main pages
    MAIN_PAGE_NEWS = "http://www.nieuwsblad.be"
    MAIN_PAGE_SPORTS = "http://www.nieuwsblad.be/sportwereld"
    MAIN_PAGE_REGIO = "http://www.nieuwsblad.be/{regio}"
    MAIN_PAGE_EXTRA = "http://www.nieuwsblad.be/nieuws/extra"
    MAIN_PAGE_SHE = "http://www.nieuwsblad.be/she"
    NEWS_CONTENT_EXAMPLE = "http://www.nieuwsblad.be/cnt/dmf20170423_02846625"

    @staticmethod
    def get_headlines(main_page_url):
        """ Retrieves HetNieuwsblad headlines on the site main pages.
            If it cannot parse the headline, it will return None. """

        # creates a beautifulSoup object
        soup = SoupMaker.make_soup(main_page_url)

        # from each anchor element, retrieve headline, datetime,
        for anchor_element in soup.find_all("a", class_="link-complex"):
            try:
                headline_link = anchor_element["href"]
                date_time = HetNieuwsblad.__parse_headline_datetime(headline_link)
                headline = anchor_element.find_next("h1").string
                headline = headline.strip()
                headline_link = headline_link.strip()
            except AttributeError:
                yield None
            else:
                yield NewsEvent(headline=headline, link=headline_link, date=date_time, content="")

    @staticmethod
    def get_news_content(url):
        """ Collects data from html soup from a HetNieuwsblad url, constructs and returns a NewsEvent object """

        # creates a beautifulSoup object
        soup = SoupMaker.make_soup(url)

        # fetches headline string
        headline = soup.find("h1", {"itemprop": "name"}).string
        div_element_article_body = soup.find("div", class_="article__body")

        # constructs content NewsEvent content from all paragraphs found in the div element
        content = ""
        for p_element in div_element_article_body.find_all_next("p"):
            content += "\n".join(textwrap.wrap(p_element.text, 100)) + "\n\n"

        datetime_string = soup.find("time", {"itemprop": "datePublished"})["datetime"]
        datetime_object = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M+02:00")

        return NewsEvent(headline=headline, link=url, date=datetime_object, content=content)

    @staticmethod
    def __parse_headline_datetime(headline_url):
        """ Fetches a datetime string from HetNieuwsblad url and returns a datetime object
            if it can't retrieve the datetime it returns epoch timestamp 0 """

        regex = "http://www.nieuwsblad.be/cnt/dmf(?P<date>\d+)_\d+"
        pattern = re.compile(regex, re.I)

        match = re.search(pattern, headline_url)
        if match:
            datetime_string = match.group("date")
            datetime_object = datetime.datetime.strptime(datetime_string, "%Y%m%d")
            return datetime_object
        else:
            return datetime.datetime.fromtimestamp(0)


def main():
    headlines = HetNieuwsblad.get_headlines(HetNieuwsblad.MAIN_PAGE_NEWS)
    for headline in headlines:
        print(headline)

    news_event = HetNieuwsblad.get_news_content(HetNieuwsblad.NEWS_CONTENT_EXAMPLE)
    print(news_event.get_content())


if __name__ == "__main__":
    main()
