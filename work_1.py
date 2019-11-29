import csv
import logging

from bs4 import BeautifulSoup
import urllib3

#  Пишем конфигурации для логгера
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('logging.log', 'a',
                                                  'utf-8')]
                    )


def company_info(link):
    """
        Функция принимает на вход ссылку с сайта
        `https://www.list-org.com/company/IDКОМПАНИИ`,
        где IDКОМПАНИИ - итендификационный номер компании.
        На выходе получаем CSV-файл с полным юр. наименованием,
        руководителем, датой регистрации, статусом, инн, кпп, огрн.
    """
    try:
        http = urllib3.PoolManager()
        page = http.request('GET', link)
        page = page.data.decode('utf-8')
        logging.info('Декодирование страницы завершено')

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

        with open("company.csv", 'a', encoding='utf8') as f:
            writer = csv.DictWriter(f, dict_comp.keys(), delimiter=';')
            writer.writeheader()
            writer.writerow(dict_comp)
            logging.info('Запись завершена, программа выполнена')
    except Exception as e:
        print(e)
        logging.error(e)


company_info("https://www.list-org.com/company/4868135")
