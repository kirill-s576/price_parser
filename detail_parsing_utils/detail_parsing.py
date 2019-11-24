class DetailParser(object):

    def __init__(self, url):
        self.goose_url = url
        print(self.goose_url)
        if "sigaretnet" in self.goose_url:
            from detail_parsing_utils.sigaretnet import Sigaretnet
            self.shop = Sigaretnet()

        elif "vipmag" in self.goose_url:
            from detail_parsing_utils.vipmag import Vipmag
            self.shop = Vipmag()

        elif "podzemka" in self.goose_url:
            from detail_parsing_utils.podzemka import Podzemka
            self.shop = Podzemka()

        elif "viking" in self.goose_url:
            from detail_parsing_utils.vikingvape import Vikingvape
            self.shop = Vikingvape()

        elif "partut" in self.goose_url:
            from detail_parsing_utils.partut import Partut
            self.shop = Partut()

        elif "vapeart" in self.goose_url:
            from detail_parsing_utils.vapeart import Vapeart
            self.shop = Vapeart()

        elif "novasens" in self.goose_url:
            from detail_parsing_utils.novasens import Novasens
            self.shop = Novasens()

        elif "nekuri" in self.goose_url:
            from detail_parsing_utils.nekuri import Nekuri
            self.shop = Nekuri()

        elif "mvape" in self.goose_url:
            from detail_parsing_utils.mvape import Mvape
            self.shop = Mvape()

        elif "esteamer" in self.goose_url:
            from detail_parsing_utils.esteamer import Esteamer
            self.shop = Esteamer()

        elif "beztabaka" in self.goose_url:
            from detail_parsing_utils.beztabaka import Beztabaka
            self.shop = Beztabaka()

        elif "freevape" in self.goose_url:
            from detail_parsing_utils.freevape import Freevape
            self.shop = Freevape()

        elif "wov" in self.goose_url:
            from detail_parsing_utils.wov import Wov
            self.shop = Wov()

        else:
            self.shop = None

        self.goose = self.shop.set_goose(self.goose_url).parse_all()

        self.dict = self.goose.get_values_dict()
        self.name = self.goose.goose_name
        self.url = self.goose_url
        self.price = self.goose.goose_price
        self.fullprice = self.goose.goose_fullprice
        self.img = self.goose.goose_imageurl
        self.available = self.goose.goose_available
#
# d = DetailParser("https://vapeart.by/products/isparitel-smoant-pasito-pod-mtl-14ohm-kupit-v-minske")
# print(d.dict)