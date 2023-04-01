from rest_framework.views import APIView
from rest_framework.response import Response
from analysis.models import *
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
        region = request.query_params['region']
        inn = request.query_params['inn']
        company_tenders = Participants.objects.filter(supplier_inn=inn)
        purchases = []
        other_data = []
        for i in range(len(company_tenders)):
            purchas = company_tenders[i].part_id
            if (purchas.category == category or category == 'Все категории') \
                    and self.compareDate(purchas.publish_date, data_start) \
                    and self.compareDate(data_end, purchas.publish_date) and \
                    (purchas.delivery_region == region or region == "Все регионы"):
                purchases.append(purchas)
                if not purchas.contract_category:
                    print(purchas.part.count())
                other_data.append({'contracts': purchas.contract.all(), 'count': purchas.part.count()})

        data = [
            {
                'title': 'Time',
                'concat': False,
                'type': 'doughnut',
                'labels': ['1', '2', '3', '4', '5', 'long dick', 'ttt'],
                'chart': [
                    {
                        'color': ['red'],
                        'line_label': 'time_label',
                        'data': [123, 3, 12, 33, 98, 100, 23],
                        'regression': False
                    }
                ]
            },
            {
                'title': 'Segments',
                'type': 'bar',
                'labels': ['1', '2', '3', '4', '5', '6', '7'],
                'chart': [
                    {
                        'color': 'blue',
                        'line_label': 'seg1_label',
                        'data': [1, 2, 3, 4, 5, 6, 1],
                        'regression': False
                    },
                    {
                        'color': 'green',
                        'line_label': 'seg2_label',
                        'data': [10, 3, 12, 39, 48, 55, 10],
                        'regression': False
                    }
                ]
            }
        ]
        return Response(data)


class Categories(APIView):
    def get(self, request, *args, **kwargs):
        data = {'categories': ["Seeds", "melons", "weapons", "nuclear"]}
        return Response(data)


class Regions(APIView):
    def get(self, request, *args, **kwargs):
        data = {'regions': REGIONS}
        return Response(data)
