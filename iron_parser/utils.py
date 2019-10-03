# coding=utf-8
import re
import requests
import urllib
from urllib import request
from urllib.parse import quote
import datetime

class IronParser(object):

    def __init__(self, keys):
        self.keys_string = keys
        self.key_array = self.keys_string.split()

        self.vipmag_url_template = "https://vipmag.by/search/?q=*****&s=%C2%A0"
        self.vipmag_divider = "+"
        self.vipmag_url_full = self.get_full_url(self.vipmag_url_template, "+")

        self.sigaretnet_url_template = "http://www.sigaretnet.by/poisk-tovarov/search.html?keyword=*****&limitstart=0&option=com_virtuemart&view=category"
        self.sigaretnet_divider = "+"
        self.sigaretnet_url_full = self.get_full_url(self.sigaretnet_url_template, self.sigaretnet_divider)

        self.esteamer_url_template = "https://esteamer.by/?s=*****&post_type=product"
        self.esteamer_divider = "+"
        self.esteamer_url_full = self.get_full_url(self.esteamer_url_template, self.esteamer_divider)

        self.nekuri_url_template = "http://nekuri.by/index.php?route=product/search&search=*****"
        self.nekuri_divider = "%20"
        self.nekuri_url_full = self.get_full_url(self.nekuri_url_template, self.nekuri_divider)

        self.vapeart_url_template = "https://vapeart.by/products/search?sort=0&balance=&categoryId=&min_cost=&max_cost=&page=1&text=*****"
        self.vapeart_divider = "+"
        self.vapeart_url_full = self.get_full_url(self.vapeart_url_template, self.vapeart_divider)


    def get_full_url(self, temp, devider):
        pattern = devider.join(self.key_array)
        # Подставляем паттерн в шаблон ссылки поиска
        url = temp.replace("*****", pattern)
        return url

    def get_find_html(self, url):
        print(url)
        resp = urllib.request.urlopen(url)
        try:
            return resp.read().decode('UTF8', errors="ignore")
        except:
            return "Ошибка загрузки HTML страницы"

    # Функция для сортировки данных по цене
    def sort_price(self, val):
        return val["price"]

    #  Образец вывода результатов функции!
    #  [{'name': 'Испаритель ELEAF HW для iJust NexGen, iJust 3, Ello, Ello Duro',
    #  'price': 6.9,
    #  'url': 'https://vipmag.by/2609/isparitel_eleaf_hw_dlya_ijust_nexgen_98554'},...]

    def vipmag_parse(self):
        try:
            html = self.get_find_html(self.vipmag_url_full)  # Получаем страницу с найденными товарами
            gooses = re.findall(r'<div class="liquidprodname"><a href="(.*?)/".*?<figcaption>(.+?)</figcaption>.*?([\d]*.[\d]*)\sBYN', html, flags=re.DOTALL)

            # Запись и вывод результатов
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = float(goose[2])
                url = goose[0]
                if str(self.keys_string).lower() in str(name).lower():
                    new_goose["name"] = name
                    new_goose["price"] = price
                    new_goose["url"] = url.replace('"', '')
                    result.append(new_goose)
                result.sort(key=self.sort_price, reverse=True)
            return result
        except:
            return "Ошибка парсинга ВипМаг."


    def sigaretnet_parse(self):
        try:
            html = self.get_find_html(self.sigaretnet_url_full)
            gooses = re.findall(r'"cat-block-description">.+?<a href=(.+?)>(.+?)</a>.*?<span class="PricesalesPrice" >(.+?)</span>', html, flags=re.DOTALL)

            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = float(goose[2][:-3])
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = price
                new_goose["url"] = "http://www.sigaretnet.by" + str(url.replace('"', ''))
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result

        except:
            return "Ошибка парсинга СигаретНет."


    def nekuri_parse(self):
        try:
            print(datetime.datetime.now())
            html = self.get_find_html(self.nekuri_url_full)
            print(datetime.datetime.now())
            gooses = re.findall(
                r'<div class="name"><a href=(.+?)>(.+?)</a>.*?<div class="price">(.+?)</div>',
                html, flags=re.DOTALL)
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = goose[2]
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = float(re.findall(r'(\d+.\d+)', price)[0])
                new_goose["url"] = url.replace('"', '')
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result

        except:
            return "Ошибка парсинга Некури."


    def esteamer_parse(self):
        try:
            print(datetime.datetime.now())
            html = self.get_find_html(self.esteamer_url_full)
            print(datetime.datetime.now())
            gooses = re.findall(
                r'<h4 class="product-title"><a href=(.+?)>(.+?)</a></h4>.*?<div class="sale_price"><span>(.+?)<span>',
                html, flags=re.DOTALL)

            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = goose[2]
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = float(re.findall(r'(\d+.\d+)', price)[0])
                new_goose["url"] = url.replace('"', '')
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)

            return result

        except:
            return "Ошибка парсинга Esteamer."


    def vape_art_parse(self):
        try:
            html = self.get_find_html(self.vapeart_url_full)
            gooses = re.findall(
                r'<div class="product-item__link"><a href=(.+?)>(.+?)</a></div>.*?<div class="product-item-price">(.+?)</div>',
                html, flags=re.DOTALL)
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = goose[2]
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = float(re.findall(r'(\d+)', price)[0])
                new_goose["url"] = url.replace('"', '')
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result

        except:
            return "Ошибка парсинга VapeArt."


    def get_all_parse(self):
        vipmag = self.vipmag_parse()
        signet = self.sigaretnet_parse()
        nekuri = self.nekuri_parse()
        esteamer = self.esteamer_parse()
        vapeart = self.vape_art_parse()
        all = {}
        all["SigaretNet"] = signet
        all["VipMag"] = vipmag
        all["Esteamer"] = esteamer
        all["Nekuri"] = nekuri
        all["VapeArt"] = vapeart
        return all

    def available_parce(self, url):
        parse_terms = {
            'sigaretnet.by': r'<div class="availability">(.+?)</div>',
            'vipmag.by': r'<div class=.lfttitle left-fl.>(.+?)</div><div class="pl-11 ib lfttitle left-fl fweight-n">(.+?)</div>',
            'esteamer.by': r'<p class="stock out-of-stock">(.+?)</p>',
            'vapeart.by': r'<div class="product__quanity">(.+?)</div>',
            'nekuri.by': ''

        }
        available = []
        return_available = []
        for term in parse_terms:
            if term in url:
                html = self.get_find_html(url)
                available = re.findall(parse_terms[term], html, flags=re.DOTALL)
        for a in available:
            b = ' '.join(a)
            return_available.append(b.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', ''))
        return return_available

a = IronParser('')
av = a.available_parce('https://vipmag.by/cigarettes/veyp_eleaf_ijust_3_s_kliromayzerom_ello_duro_101626/')
print(av)