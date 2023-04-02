from rest_framework.views import APIView
from rest_framework.response import Response

from analysis.api.findSuggestions import find_suggestions
from analysis.models import *
from analysis.api.charts import make_charts_info, get_recommendations
import datetime

REGIONS = ['Москва', 'Санкт-Петербург', 'Московская', 'Краснодарский', 'Пермский', 'Новороссийск', 'Тюменская',
           'Кемеровская область - Кузбасс', 'Горнозаводск', 'Пермь', 'Ямало-Ненецкий', 'Муравленко', 'Березники',
           'Псковская', 'Сургут', 'Иркутская', 'Юрга', 'Ноябрьск', 'Новгородская', 'Ленинградская', 'Шурышкарский',
           'Новосибирская', 'Тазовский', 'Маловишерский', 'Омская', 'Губкинский', 'Орда', 'Мариинск', 'Окуловский',
           'Кемерово', 'Крестецкий', 'Алтайский', 'Чудовский', 'Аксарка', 'Пуровский', 'Шимский', 'Великий Новгород',
           'Салехард', 'Мурманская', 'Новый Уренгой', 'Новгородский', 'Крым', 'Тверская', 'Кинешма', 'Тамбовская',
           'Все регионы', 'Волгоградская', 'Нижегородская', 'Свердловская', 'Белоозерский', 'Красноярский',
           'Ханты-Мансийский АО - Югра', 'Старорусский', 'Иркутск', 'Ярославская', 'Ростовская', 'Брянская',
           'Яхрома', 'Татарстан', 'Белгород', 'Вологодская', 'Саха (Якутия)', 'Челябинская', 'Калининградская',
           'Тульская']

"""
регион, категория, отрезок времени 
    1. прайс закупки по которой купили в контракте и начальный -> закупки 
    2. Даты старты лота
"""


class ChartsApi(APIView):

    def compareDate(self, date1, date2):
        if date1 >= date2:
            return True
        return False

    def get(self, request, *args, **kwargs):
        data_start = datetime.date(*list(map(int, request.query_params['dateStart'].split('-'))))
        data_end = datetime.date(*list(map(int, request.query_params['dateEnd'].split('-'))))
        category = request.query_params['category']
        category = OKPD.objects.filter(name=category).get().no if category != "Все категории" else category
        region = request.query_params['region']
        inn = request.query_params['inn']
        company_tenders = Participants.objects.filter(supplier_inn=inn)
        purchases = []
        for i in range(len(company_tenders)):  #
            purchase = company_tenders[i].part_id
            if (purchase.category == category or category == 'Все категории') \
                    and self.compareDate(purchase.publish_date, data_start) \
                    and self.compareDate(data_end, purchase.publish_date) and \
                    (purchase.delivery_region == region or region == "Все регионы"):
                purchases.append([purchase,
                                  {
                                      'contracts': purchase.contract.all(),
                                      'count': purchase.part.count(),
                                      'is_winner': company_tenders[i].is_winner == "True"
                                  }])
        data = make_charts_info(purchases, inn)
        return Response(data)


class Categories(APIView):
    def get(self, request, *args, **kwargs):
        inn = request.query_params['inn']
        res = set()
        for part in Participants.objects.filter(supplier_inn=inn).all():
            for elem in OKPD.objects.filter(no=part.part_id.category).all():
                res.add(elem.name)
        data = {'categories': list(res)}
        return Response(data)


class Regions(APIView):
    def get(self, request, *args, **kwargs):
        data = {'regions': REGIONS}
        return Response(data)


class Suggestions(APIView):
    def get(self, request, *args, **kwargs):
        # return Response([])
        inn = request.query_params['inn']
        cluster = Companies.objects.get(supplier_inn=inn).cluster
        category = request.query_params['category']
        if category != "Все категории":
            category = OKPD.objects.filter(name=category).get().no
            purchases = Purchases.objects.filter(category)
        else:
            purchases = Purchases.objects
        print(1, purchases.count())
        purchases = purchases.filter(id__in=Participants.objects.filter(is_winner="False").values("part_id"))
        print(2, purchases.count())
        purchases = purchases.filter(id__in=Participants.objects.exclude(supplier_inn=inn).values("part_id"))
        print(3, purchases.count())

        data = find_suggestions(purchases, {
            "inn": inn,
            "cluster": cluster,
        })[:5]

        if purchases.count() == 0:
            return Response([])
        print(data)
        data = list(map(lambda x:
                        {
                            "name": x[0].lot_name,
                            "pk": x[0].id,
                            "cost": x[0].price
                        }
                        , data))
        # data = [{'name': 'sidfisdfgsjkdfgsgfbdsjvbsjvbsbvsdhbvjhbvjhdbvjsdvbh', 'pk': 982735982, 'cost': '23422'},
        #         {'name': 'bsvuhsbvbvxbv,,xvbxc,vnbv', 'pk': 3453433, 'cost': '1222333'}]
        return Response(data)
