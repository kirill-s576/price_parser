import requests
import re


class Partut(object):
    def __init__(self):
        # Переменные магазина
        self.www = "http://partut.by"

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
        self.name_regexp = r'<header class="page-header">.*?<h1>(.*?)</h1>'
        self.price_regexp = r'<div class="product-price"><span>Цена:</span><strong>(.*?)&nbsp;руб.</strong></div>'
        self.available_regexp = r''
        self.fullprice_regexp = r''
        self.imageurl_regexp = r'<a class="thumb-container" rel="product-gallery-\d+" href="(.*?)" title='


    def set_goose(self, url):
        self.goose_url = url
        self.get_goose_html()
        return self

    def get_goose_html(self):
        resp = requests.get(self.goose_url)
        try:
            self.goose_html = resp.text
        except Exception as e:
            print("Ошибка загрузки HTML страницы товара Sigaretnet.by")
            print(e)
            self.goose_html = None

    def parse_name(self):
        self.goose_name = re.findall(self.name_regexp, self.goose_html, flags=re.DOTALL)[0]
        return self

    def parse_price(self):
        self.goose_price = float(str(re.findall(self.price_regexp, self.goose_html, flags=re.DOTALL)[0]).replace(",", "."))
        return self

    def parse_available(self):
        self.goose_available = "Не указано"
        return self

    def parse_fullprice(self):
        self.goose_fullprice = self.goose_price
        return self

    def parse_image(self):
        self.goose_imageurl = re.findall(self.imageurl_regexp, self.goose_html, flags=re.DOTALL)[0]
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

# p = Partut().set_goose("https://partut.by/catalog/parogenerator-joyetech-evic-vtwo-mini-75w/").parse_all()
# print(p.get_values_dict())