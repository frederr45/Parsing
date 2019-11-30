import time

from selenium import webdriver

from work_2 import write_csv

if __name__ == "__main__":
    with webdriver.Chrome() as driver:
        driver.get("https://www.list-org.com/company/4868135")
        time.sleep(1)

        #  name - Название предприятия
        name = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/p").text.split(";")
        name = tuple(name[0].split(":"))

        #  table - Таблица данных(директор, дата, статус)
        table = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/table/tbody").text.split("\n")
        director = tuple(table[0].split(":"))
        date = tuple(table[-2].split(":"))
        status = tuple(table[-1].split(":"))

        #  body - Div - данных(ИНН, КПП, ОГРН)
        body = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[8]").text.split("\n")
        inn = tuple(body[0].split(":"))
        kpp = tuple(body[1].split(":"))
        ogrn = tuple(body[3].split(":"))
        dict_ = dict([name, director, date, status, inn, kpp, ogrn])
        write_csv([dict_], "company")
