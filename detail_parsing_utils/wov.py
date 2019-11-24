import requests
import re


class Wov(object):
    def __init__(self):
        # Переменные магазина
        self.www = "http://wov.by"

        # Переменные товара
        self.goose_url = None
        self.goose_html = None

        # Параметры товара, которые должны быть найдены.
        self.goose_name = ""
        self.goose_price = ""
        self.goose_available = ""
        self.goose_fullprice = ""
        self.goose_imageurl = ""

        # Регулярные выражения для парсинга параметров товара.
        self.name_regexp = r''
        self.price_regexp = r''
        self.available_regexp = r''
        self.fullprice_regexp = r''
        self.imageurl_regexp = r''


    def set_goose(self, url):
        self.goose_url = url
        self.get_goose_html()
        return self

    def get_goose_html(self):
        resp = requests.get(self.goose_url)
        try:
            self.goose_html = resp.text
        except Exception as e:
            print("Ошибка загрузки HTML страницы товара Wov.by")
            print(e)
            self.goose_html = None

    def parse_name(self):
        self.goose_name = ""
        return self

    def parse_price(self):
        self.goose_price = 0.00
        return self

    def parse_available(self):
        self.goose_available = "Нет в наличии"
        return self

    def parse_fullprice(self):
        self.goose_fullprice = 0.00
        return self

    def parse_image(self):
        self.goose_imageurl = ""
        return self

    def parse_all(self):
        self.parse_name()
        self.parse_price()
        self.parse_available()
        self.parse_fullprice()
        self.parse_image()
        # Просто запускаем по порядку все функции, описанные выше.
        return self

    def get_values_dict(self):
        dict = {}
        dict["name"] = self.goose_name
        dict["price"] = self.goose_price
        dict["fullprice"] = self.goose_fullprice
        dict["available"] = self.goose_available
        dict["url"] = self.goose_url
        dict["imageurl"] = self.goose_imageurl
        return dict

