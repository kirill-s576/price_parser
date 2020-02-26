# coding=utf-8
import re
import requests
import urllib
from urllib import request
from urllib.parse import quote
import datetime
import requests
class IronParser(object):

    def __init__(self, keys):
        self.keys_string = keys
        self.key_array = self.keys_string.split()

        self.vipmag_url_template = "https://vipmag.by/search/?q={0}"
        self.vipmag_divider = " "
        self.vipmag_url_full = self.get_full_url(self.vipmag_url_template, self.vipmag_divider).replace("%20","+")
        # print(self.vipmag_url_full)

        self.sigaretnet_url_template = "http://www.sigaretnet.by/poisk-tovarov/search.html?keyword={0}"
        self.sigaretnet_divider = " "
        self.sigaretnet_url_full = self.get_full_url(self.sigaretnet_url_template, self.sigaretnet_divider)
        # print(self.sigaretnet_url_full)

        self.esteamer_url_template = "https://esteamer.by/?s={0}&post_type=product"
        self.esteamer_divider = " "
        self.esteamer_url_full = self.get_full_url(self.esteamer_url_template, self.esteamer_divider)
        # print(self.esteamer_url_full)

        self.nekuri_url_template = "http://nekuri.by/index.php?route=product/search&search={0}"
        self.nekuri_divider = " "
        self.nekuri_url_full = self.get_full_url(self.nekuri_url_template, self.nekuri_divider)
        # print(self.nekuri_url_full)

        self.vapeart_url_template = "https://vapeart.by/products/search?page=1&text={0}"
        self.vapeart_divider = " "
        self.vapeart_url_full = self.get_full_url(self.vapeart_url_template, self.vapeart_divider)
        # print(self.vapeart_url_full)

        self.viking_url_template = "http://vikingvape.by/search/?search={0}"
        self.viking_divider = " "
        self.viking_url_full = self.get_full_url(self.viking_url_template, self.viking_divider)
        # print(self.viking_url_full)

        self.wov_url_template = "https://wov.by/search/?search={0}&sub_category=true&description=true"
        self.wov_divider = " "
        self.wov_url_full = self.get_full_url(self.wov_url_template, self.wov_divider)
        # print(self.wov_url_full)

        self.podzemka_url_template = "http://podzemka-minsk.by/search?q={0}"
        self.podzemka_divider = " "
        self.podzemka_url_full = self.get_full_url(self.podzemka_url_template, self.podzemka_divider).replace("%20", "+")
        # print(self.podzemka_url_full)

        self.mvape_url_template = "https://mvape.by/index.php?route=product/search&search={0}&description=true"
        self.mvape_divider = " "
        self.mvape_url_full = self.get_full_url(self.mvape_url_template, self.mvape_divider)
        # print(self.mvape_url_full)

        self.novasens_url_template = "https://www.novasens.by/index.php?route=product/search&search={0}"
        self.novasens_divider = " "
        self.novasens_url_full = self.get_full_url(self.novasens_url_template, self.novasens_divider)
        # print(self.novasens_url_full)

        self.partut_url_template = "https://partut.by/?s={0}"
        self.partut_divider = " "
        self.partut_url_full = self.get_full_url(self.partut_url_template, self.partut_divider).replace("%20", "+")
        # print(self.partut_url_full)

        self.beztabaka_url_template = "http://beztabaka.by/index.php?route=product/search&search={0}"
        self.beztabaka_divider = " "
        self.beztabaka_url_full = self.get_full_url(self.beztabaka_url_template, self.beztabaka_divider)
        # print(self.beztabaka_url_full)

        self.freevape_url_template = "https://freevape.by/?s={0}&post_type=product"
        self.freevape_divider = " "
        self.freevape_url_full = self.get_full_url(self.freevape_url_template, self.freevape_divider)

        self.pgvg_url_template = "https://pgvg.by/site_search?search_term={0}"
        self.pgvg_divider = " "
        self.pgvg_url_full = self.get_full_url(self.pgvg_url_template, self.pgvg_divider)

    def get_full_url(self, temp, devider):
        pattern = devider.join(self.key_array)
        # Подставляем паттерн в шаблон ссылки поиска
        url = temp.format(quote(pattern))
        url1 = request.unquote(url)
        return url

    def get_find_html(self, url):
        # resp = urllib.request.urlopen(url)
        resp = requests.get(url)
        try:
            return resp.text
        except:
            return "Ошибка загрузки HTML страницы"

    # Функция для сортировки данных по цене
    def sort_price(self, val):
        return val["price"]

    def sort_key(self, val):
        return val[0]
    #  Образец вывода результатов функции!
    #  [{'name': 'Испаритель ELEAF HW для iJust NexGen, iJust 3, Ello, Ello Duro',
    #  'price': 6.9,
    #  'url': 'https://vipmag.by/2609/isparitel_eleaf_hw_dlya_ijust_nexgen_98554'},...]

    def vipmag_parse(self):
        try:
            html = self.get_find_html(self.vipmag_url_full)  # Получаем страницу с найденными товарами
            gooses = re.findall(r'<div class="liquidprodname"><a href="(.*?)" title=".*?" itemprop="name"><figcaption>(.+?)</figcaption>.*?([\d]*.[\d]*)\sBYN', html, flags=re.DOTALL)

            # Запись и вывод результатов
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = float(goose[2])
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = price
                new_goose["url"] = url.replace('"', '')
                result.append(new_goose)
                result.sort(key=self.sort_price, reverse=True)
            return result
        except:
            return []


    def sigaretnet_parse(self):
        try:
            html = self.get_find_html(self.sigaretnet_url_full)

            gooses = re.findall(r'"cat-block-description">.+?<a href=(.+?)>(.+?)</a>.*?<span class="PricesalesPrice" >(.+?)</span>', html, flags=re.DOTALL)

            result = []
            for goose in gooses:
                print(goose)
                new_goose = {}
                name = goose[1]
                try:
                    price = float(goose[2][:-3])
                except:
                    price = 0
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = price
                new_goose["url"] = "http://www.sigaretnet.by" + str(url.replace('"', ''))
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result

        except:
            return []


    def nekuri_parse(self):
        try:
            html = self.get_find_html(self.nekuri_url_full)
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
            return []


    def esteamer_parse(self):
        try:
            html = self.get_find_html(self.esteamer_url_full)
            gooses = re.findall(
                r'<h4 class="product-title"><a href=(.+?)>(.+?)</a></h4>.*?<div class="product-price-container prices clearfix">(.+?)</div>',
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
            return []


    def vape_art_parse(self):
        try:
            html = self.get_find_html(self.vapeart_url_full)
            gooses = re.findall(
                r'<div class="product-item__link"><a href=(.+?)>(.+?)</a></div>.*?<div class="product-item-price.*?">(.+?)</div>',
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
            return []

    def viking_parse(self):
        try:
            html = self.get_find_html(self.viking_url_full)
            gooses = re.findall(
                r'<div class="caption">.*?<h4><a href=(.+?)>(.+?)</a></h4>.*?<p class="price">(.+?)</p>', html, flags=re.DOTALL)
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
            return []

    def wov_parse(self):
        try:
            html = self.get_find_html(self.wov_url_full)
            gooses = re.findall(
                r'<div class="name"><a href=(.+?)>(.+?)</a></div>.*?<div class="price">(.+?)<i> руб.</i>', html, flags=re.DOTALL)
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
            return []

    def podzemka_parse(self):
        try:
            html = self.get_find_html(self.podzemka_url_full)
            gooses = re.findall(
                r'<article class="product"><a href=(.+?)><p class="h2">(.+?)</p><img src=.*?<span class="price"><span>(.+?) руб.</span>', html, flags=re.DOTALL)
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = goose[2]
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = float(re.findall(r'(\d+.\d+)', price)[0])
                new_goose["url"] = "http://www.podzemka-minsk.by" + str(url.replace('"', ''))
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result

        except:
            return []


    def mvape_parse(self):
        try:
            html = self.get_find_html(self.mvape_url_full)
            gooses = re.findall(
                r'<h4 class="name"><a href="(.+?)">(.+?)</a></h4>.*?<p class="price">(.+?) р..*?</p>', html, flags=re.DOTALL)
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
            return []


    def novasens_parse(self):
        try:
            html = self.get_find_html(self.novasens_url_full)
            gooses = re.findall(
                r'<div class="caption">.*?<div class="h4new"><a href=(.+?)>(.+?)</a></div>.*?<span class="price-new">(.+?) руб.</span>', html, flags=re.DOTALL)
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
            return []


    def partut_parse(self):
        try:
            html = self.get_find_html(self.partut_url_full)
            gooses = re.findall(
                r'<a class="post-title" href="(.+?)"><span class="cell">(.+?)</span></a>.*?<span class="product-price">(.+?)&nbsp;руб.</span>', html, flags=re.DOTALL)
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = goose[2]
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = float(re.findall(r'(\d+.\d+)', price)[0].replace(",", "."))
                new_goose["url"] = url.replace('"', '')
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result

        except Exception as e:
            print(e)
            return []


    def beztabaka_parse(self):
        try:
            html = self.get_find_html(self.beztabaka_url_full)
            gooses = re.findall(
                r'<div class="name"><a href="(.+?)">(.+?)</a></div>.*?<div class="price">(.+?)руб.*?</div>', html, flags=re.DOTALL)
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = goose[2]
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = float(re.findall(r'(\d+.)', price)[0])
                new_goose["url"] = url.replace('"', '')
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result


        except Exception as e:
            print(e)
            return []

    def freevape_parse(self):
        try:
            html = self.get_find_html(self.freevape_url_full)
            gooses = re.findall(
                r'<h4 class="entry-title"> <a href="(.+?)" title="(.+?)" rel="bookmark">.*?class="woocommerce-Price-amount amount">(.+?)&nbsp;<span', html, flags=re.DOTALL)
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


        except Exception as e:
            print(e)
            return []

    def pgvg_parse(self):
        try:
            html = self.get_find_html(self.pgvg_url_full)
            gooses = re.findall(
                r'<div class="b-product-line__product-name"><a href="(.+?)".+?title="(.+?)".+?<div class="b-product-line__price">(.+?) руб.</div>', html, flags=re.DOTALL)
            result = []
            for goose in gooses:
                new_goose = {}
                name = goose[1]
                price = goose[2]
                url = goose[0]
                new_goose["name"] = name
                new_goose["price"] = float(re.findall(r'[\d,]+', price)[0].replace(",", "."))
                new_goose["url"] = url.replace('"', '')
                result.append(new_goose)
            result.sort(key=self.sort_price, reverse=True)
            return result


        except Exception as e:
            print(e)
            return []


    def get_all_parse(self):
        vipmag = self.vipmag_parse()
        signet = self.sigaretnet_parse()
        nekuri = self.nekuri_parse()
        esteamer = self.esteamer_parse()
        vapeart = self.vape_art_parse()
        viking = self.viking_parse()
        wov = self.wov_parse()
        podzemka = self.podzemka_parse()
        mvape = self.mvape_parse()
        novasens = self.novasens_parse()
        partut = self.partut_parse()
        beztabaka = self.beztabaka_parse()
        freevape = self.freevape_parse()
        pgvg = self.pgvg_parse()
        all = {}
        all["SigaretNet"] = signet
        all["VipMag"] = vipmag
        all["VikingVape"] = viking
        all["Esteamer"] = esteamer
        all["Nekuri"] = nekuri
        all["VapeArt"] = vapeart
        all['Wov'] = wov
        all["Podzemka"] = podzemka
        all["Mvape"] = mvape
        all["Novasens"] = novasens
        all["Partut"] = partut
        all["BezTabaka"] = beztabaka
        all["FreeVape"] = freevape
        all["PgVg"] = pgvg
        return all


p = IronParser("boost")
print(p.sigaretnet_parse())