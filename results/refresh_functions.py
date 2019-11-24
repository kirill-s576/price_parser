from iron_parser.models import *
from iron_parser.utils import IronParser
from news.models import PotentialGoose
from detail_parsing_utils.detail_parsing import DetailParser



def new_refresh(**data):
    if 'id' in data.keys():
        gooses = GooseBase.objects.filter(id=data['id'])
    else:
        gooses = GooseBase.objects.all()

    for goose in gooses:

        # Поиск потенциальных оппонентов при первом парсинге
        checks = Check.objects.filter(goose=goose)
        if len(checks) < 1:
            refresh_potential_gooses(id=goose.id, first=True)
        ###

        check = Check(goose=goose)
        check.save()
        op_gooses = OpponentGoose.objects.filter(goose=goose)
        for op_goose in op_gooses:
            url = op_goose.url
            try:
                parse = DetailParser(url)
                if "sigaretnet" in url:
                    try:
                        goose.image = parse.img
                        goose.price = parse.price
                        goose.save()
                    except Exception as e:
                        print(e)
                        print(parse.img)

                op_goose.img = parse.img
                # op_goose.available = parse.available
                op_goose.save()

                sub = SubCheck(check_name=check, price=parse.price, full_price=parse.fullprice, available=parse.available,
                               opponent_goose=op_goose)
                sub.save()
            except Exception as e:
                print(e)
                print("Не удалось спарсить страницу с товарами по URL " + str(url))

def refresh_potential_gooses(**data):
    print("Ищем новые потенциальные товары.")
    if 'id' in data.keys():
        gooses = GooseBase.objects.filter(id=data['id'])
    else:
        gooses = GooseBase.objects.all()

    for goose in gooses:
        print(goose.name)
        temp = goose.keys
        parse = IronParser(temp)
        parse_results = parse.get_all_parse()
        for shop in parse_results:
            for parse_goose in parse_results[shop]:
                name = parse_goose["name"]
                url = parse_goose["url"]
                price = parse_goose["price"]
                try:
                    pot_goose = PotentialGoose.objects.filter(url=url, opponent__name=shop, goose=goose)[0]
                    pot_goose.price = price
                    pot_goose.save()
                except Exception as e:
                    print(e)
                    pot_goose = PotentialGoose()
                    pot_goose.name = name
                    pot_goose.url = url
                    pot_goose.template = temp
                    pot_goose.opponent = Opponent.objects.get(name__icontains=shop)
                    pot_goose.goose = goose
                    pot_goose.price = price
                    if 'first' in data.keys():
                        pot_goose.confirmed = data["first"]
                        pot_goose.viewed = data["first"]
                        pot_goose.removed = data["first"]
                    pot_goose.save()
                    print("Создан потенциальный товар для" + str(shop))