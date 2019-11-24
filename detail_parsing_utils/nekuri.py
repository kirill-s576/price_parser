import requests
import re


class Nekuri(object):
    def __init__(self):
        # Переменные магазина
        self.www = "http://nekuri.by"

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
        self.name_regexp = r'<div class="product-info">.*?<h1>(.*?)</h1>'
        self.price_regexp = r'<div class="price">(.*?)<br'
        self.available_regexp = r'<div class="infoleft">.*?<span>Наличие:</span>(.*?)<br>'
        self.fullprice_regexp = r''
        self.imageurl_regexp = r'<div class="image">.*?<a href="(.*?)" title='


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
        self.goose_price = re.findall(self.price_regexp, self.goose_html, flags=re.DOTALL)
        if "price-new" in str(self.goose_price[0]):
            self.goose_price = float(re.findall(r'<span class="price-new">(.*?) р.</span>', self.goose_price[0], flags=re.DOTALL)[0])
        else:
            self.goose_price = float(re.findall(r'(\d+.\d+) р.', self.goose_price[0], flags=re.DOTALL)[0])
        return self

    def parse_available(self):
        self.goose_available = re.findall(self.available_regexp, self.goose_html, flags=re.DOTALL)[0]
        if "Нет" not in self.goose_available:
            self.goose_available = "В наличии"
        else:
            self.goose_available = "Нет в наличии"
        return self

    def parse_fullprice(self):
        self.goose_fullprice = re.findall(self.price_regexp, self.goose_html, flags=re.DOTALL)
        if "price-old" in str(self.goose_fullprice[0]):
            self.goose_fullprice = float(re.findall(r'<span class="price-old">(.*?) р.</span>', self.goose_fullprice[0], flags=re.DOTALL)[0])
        else:
            self.goose_fullprice = self.goose_price
        return self

    def parse_image(self):
        self.goose_imageurl = re.findall(self.imageurl_regexp, self.goose_html, flags=re.DOTALL)
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
