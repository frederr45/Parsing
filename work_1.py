import csv
import logging

from bs4 import BeautifulSoup
import urllib3


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('logging.log', 'a',
                                                  'utf-8')]
                    )


def info():
    try:
        http = urllib3.PoolManager()
        page = http.request('GET', "https://www.list-org.com/company/4868135")
        page = page.data.decode('utf-8')
        logging.info('Декодирование страницы завершено')
    except Exception:
        print('ConnectionError')
        logging.error('Ошибка сети.')

    soup = BeautifulSoup(page, "html.parser")
    logging.info('Работаю со страницей')

    name = soup.find("p").text.split(":")
    full = soup.select("div > div.content > div:nth-child(3) > table > tr")
    direct = full[0].text.split(":")
    date = full[5].text.split(":")
    stat = full[6].text.split(":")
    req = soup.select("body > div > div.content > div:nth-child(9) > p")
    inn = req[0].text.split(":")
    kpp = req[1].text.split(":")
    ogrn = req[3].text.split(":")

    company, dict_comp = [name, direct, date, stat, inn, kpp, ogrn], {}

    for r in company:
        dict_comp.update({r[0]: r[1]})
    
    logging.info(dict_comp)

    try:
        with open("company.csv", 'a', encoding='utf8') as f:
            writer = csv.DictWriter(f, dict_comp.keys(), delimiter=';')
            writer.writeheader()
            writer.writerow(dict_comp)
            logging.info('Запись завершена, программа выполнена')
    except NameError:
        print('Error')
        logging.error('Ошибка записи')


info()
