import pprint
import re
import time

import urllib3
from bs4 import BeautifulSoup

posts = []
dict_ = {}

def get_html(url):
    try:
        http = urllib3.PoolManager()
        result = http.request('GET', url).data.decode('utf-8')
        return result
    except Exception:
        print("Connection Lost")


def get_link():
    page = get_html("https://habr.com/ru/")
    soup = BeautifulSoup(page, "html.parser")
    link = soup.find('a', title="Лучшие публикации за год")["href"]
    return link


def page(link):
    page = get_html(link)
    soup = BeautifulSoup(page, "html.parser")
    posts = soup.find_all("li", class_="content-list__item content-list__item_post shortcuts_item")
    for post in posts:
        try:
            time.sleep(1)
            user_d = post.find("header", class_="post__meta")
            date = user_d.find("span", class_="post__time").text
            user = user_d.find("span", class_="user-info__nickname").text
            
            dict_['user'], dict_['date'] = user, date
            print(dict_)
            post_name = post.find("h2", class_="post__title").text
            print(post_name)
            post_txt = post.find("div", class_="post__body post__body_crop").text
            post_txt = ' '.join(re.sub("^\s+|\n|\r|\s+$", ' ', post_txt).split()[:-3])
            print(post_txt)
            dict_['post_name'], dict_['post_text'] = post_name, post_txt
            posts.append(dict_)
        except AttributeError:
            pass
    print(posts)
        

page(get_link())
