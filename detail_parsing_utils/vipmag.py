import requests
import re


class Vipmag(object):
    def __init__(self):
        # Переменные магазина
        self.www = "https://vipmag.by"

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
        self.name_regexp = r'<h1 itemprop="name">\r\n\s+(.*?)\s+</h1>'
        self.price_regexp = r'<span class=\'cena priceValue\'>(.*?) BYN</span>'
        self.available_regexp = r'В наличии:</div><div class="pl-11 ib lfttitle left-fl fweight-n">(.*?)\s+</div>'
        self.fullprice_regexp = r'<div class="oldcena">(.*?) BYN</div>'
        self.imageurl_regexp = r'<meta itemprop="image" content=".*?"/><img src="(.*?)" width="515"'


    def set_goose(self, url):
        self.goose_url = url
        self.get_goose_html()
        return self

    def get_goose_html(self):
        resp = requests.get(self.goose_url)
        try:
            self.goose_html = resp.text
        except Exception as e:
            print("Ошибка загрузки HTML страницы товара Vipmag.by")
            print(e)
            self.goose_html = None

    def parse_name(self):
        self.goose_name = re.findall(self.name_regexp, self.goose_html, flags=re.DOTALL)[0]
        return self

    def parse_price(self):
        try:
            self.goose_price = float(re.findall(self.price_regexp, self.goose_html, flags=re.DOTALL)[0])
        except:
            self.goose_price = 0
        return self

    def parse_available(self):
        self.goose_available = re.findall(self.available_regexp, self.goose_html, flags=re.DOTALL)[0]
        if "Нет" not in self.goose_available:
            self.goose_available = "В наличии"
        else:
            self.goose_available = "Нет в наличии"
        return self

    def parse_fullprice(self):
        try:
            self.goose_fullprice = float(re.findall(self.fullprice_regexp, self.goose_html, flags=re.DOTALL)[0])
        except:
            self.goose_fullprice = self.goose_price
        return self

    def parse_image(self):
        try:
            self.goose_imageurl = "https:"+re.findall(self.imageurl_regexp, self.goose_html, flags=re.DOTALL)[0]
        except:
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

# v = Vipmag().set_goose("https://vipmag.by/other/steklo_eleaf_dlya_melo_5_117120/").parse_all()
# print(v.get_values_dict())