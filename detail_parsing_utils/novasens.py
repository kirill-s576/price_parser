import requests
import re


class Novasens(object):
    def __init__(self):
        # Переменные магазина
        self.www = "https://www.novasens.by/"

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
        self.name_regexp = r'<h1 itemprop="name">(.*?)</h1>'
        self.price_regexp = r'<span><span class=\'autocalc-product-special\'>(.*?) руб.</span></span>'
        self.available_regexp = r'<div class="stock[\sin_stock]*?">[\n\t]+(.*?)[\n\t]*?</div>'
        self.fullprice_regexp = r'<span class="price-old">&nbsp;<span class=\'autocalc-product-price\'>(.*?) руб.</span>&nbsp;</span>'
        self.imageurl_regexp = r'<img itemprop="image" src="(.*?)" title='


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
        self.goose_price = float(re.findall(self.price_regexp, self.goose_html, flags=re.DOTALL)[0])
        return self

    def parse_available(self):
        self.goose_available = re.findall(self.available_regexp, self.goose_html, flags=re.DOTALL)[0]
        if "Нет" not in self.goose_available:
            self.goose_available = "В наличии"
        else:
            self.goose_available = "Нет в наличии"
        return self

    def parse_fullprice(self):
        self.goose_fullprice = float(re.findall(self.fullprice_regexp, self.goose_html, flags=re.DOTALL)[0])
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
