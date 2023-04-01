from rest_framework.views import APIView
from rest_framework.response import Response

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


class ChartsApi(APIView):
    def get(self, request, *args, **kwargs):
        data = [
            {
                'title': 'Time',
                'type': 'doughnut',
                'labels': ['1', '2', '3', '4', '5', '6', '7'],
                'chart': [
                    {
                        'color': 'red',
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
