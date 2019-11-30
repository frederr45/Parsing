import csv
import logging
import re
import sys
import time

from bs4 import BeautifulSoup
import urllib3

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('log_HABR.log', 'a',
                                                  'utf-8')]
                    )


def get_html(url):
    try:
        http = urllib3.PoolManager()
        result = http.request('GET', url).data.decode('utf-8')
        logging.info(f"HTML({url}) is OK!")
        return result
    except Exception:
        logging.error('Connection lost')
        print("Нет сети. Программа завершена")
        sys.exit()


def get_link():
    """
        Функция выполняет поиск ссылки в HTML- коде,
        в данном случае "Лучшие публикации за год"
    """
    logging.info("Start!")
    print("Программа запущена!")
    page = get_html("https://habr.com/ru/")
    soup = BeautifulSoup(page, "html.parser")
    link = soup.find('a', title="Лучшие публикации за год")["href"]
    logging.info("Link is OK!")
    return link


def page(link):
    """
        Функция принимает на вход ссылку,
        запрашивает нужное количество постов для поиска,
        переходит по страницам(если это требуется)
        На выходе: список словарей с нужными значениями.
    """
    try:
        count = int(input("Введите нужное количество постов:   "))
    except ValueError:
        count = int(input("Ошибка!Вводите только цифры:   "))
    i = 1
    posts = []
    while True and count > 0:
        page = get_html(link + f"page{i}/")
        soup = BeautifulSoup(page, "html.parser")
        posts_all = soup.find_all(
            "li",
            class_="content-list__item content-list__item_post shortcuts_item")
        i += 1
        for post in posts_all:
            try:
                time.sleep(0.3)
                user_d = post.find("header", class_="post__meta")
                date = user_d.find("span", class_="post__time").text
                user = user_d.find("span", class_="user-info__nickname").text

                post_name = post.find("h2", class_="post__title").text
                post_name = ' '.join(
                    re.sub("^\s+|\n|\r|\s+$", ' ', post_name).split())
                post_txt = post.find(
                    "div", class_="post__body post__body_crop").text
                post_txt = ' '.join(
                    re.sub("^\s+|\n|\r|\s+$", ' ', post_txt).split()[:20])

                dict_ = dict([
                    ("post_name", post_name), ("post_text", post_txt + "..."),
                    ("date", date), ("name", user)])

                posts.append(dict_)
                if len(posts) == count:
                    break
            except AttributeError:
                pass
        if len(posts) == count:
            logging.info(f"Posts is full! Amount - {count}! Pages - {i}")
            break
    if len(posts) == 0:
        logging.info("Count error (<= 0). EXIT!")
        print('Пусто, программа завершена!')
        sys.exit()

    return posts


def write_csv(posts, name="habrahabr"):
    """
        Универсальная функция записи полученного списка словарей.
    """
    fields = posts[0].keys()
    with open(f"{name}.csv", "w", encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fields, delimiter=';')
        writer.writeheader()
        writer.writerows(posts)
    logging.info("CSV is OK!")
    logging.info("Succses!")
    print("Программа завершена успешно!")


if __name__ == "__main__":
    write_csv(page(get_link()))
