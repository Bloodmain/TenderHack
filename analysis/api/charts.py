# from analysis.models import *
import pprint


def get_purchase_charts(purchases):
    ret = [
        {
            'title': 'Максимальная начальная цена',
            'concat': False,
        },
        {
            'title': 'Финальная цена',
            'concat': True,
        },
        {
            'title': 'Количество поставщиков-участников',
            'concat': True
         },
    ]
    for i in ret:
        i['type'] = 'bar'
        i['labels'] = []
        i['chart'] = [
            {
                'color': [],
                'line_label': '',
                'data': [],
                'regression': False
            }
        ]

    purchases.sort(key=lambda a: -a[0].price)
    ret[0]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[0]['chart']['color'][i] = ['' for _ in range(len(purchases))]
    for i in range(len(purchases)):
        ret[0]['chart']['color'][i] = 'red' if purchases[i][0].purchase_category else 'blue'
    ret[0]['chart']['data'] = list(map(lambda a: a[0].prices, purchases))

    purchases.sort(key=lambda a: -sum(map(lambda contract: contract.price, a[1]['contracts'])) if a[1]['is_winner'] else 0)
    ret[1]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[1]['chart']['color'][i] = ['' for _ in range(len(purchases))]
    for i in range(len(purchases)):
        ret[1]['chart']['color'][i] = 'red' if purchases[i][0].purchase_category else 'blue'
    ret[1]['chart']['data'] = list(map(lambda a: sum(map(lambda contract: contract.price, a[1]['contracts'])), purchases))

    purchases.sort(key=lambda a: a[1]['count'])
    ret[2]['labels'] = []
    ret[2]['chart']['color'] = []
    ret[2]['chart']['data'] = []
    for i in purchases:
        if not i[0]['purchase_category']:
            continue
        ret[2]['labels'].append(i[0].purchase_name)
        ret[2]['chart']['color'].append('red')
        ret[2]['chart']['data'].append(i[1]['count'])
    return ret


def get_region_charts(purchases):
    ret = {
        'title': 'sex',
        'index': 4,
        'type': 'bar',
        'labels': [],
        'chart': []
    }


def get_year_charts(purchases):
    ret = {
        'title': 'sex',
        'index': 4,
        'type': 'bar',
        'labels': [],
        'chart': []
    }


def get_month_charts(purchases):
    ret = {
        'title': 'sex',
        'index': 4,
        'type': 'bar',
        'labels': [],
        'chart': []
    }


def get_day_charts(purchases):
    ret = {
        'title': 'sex',
        'index': 4,
        'type': 'bar',
        'labels': [],
        'chart': []
    }


def make_charts_info(purchases):
    return [get_day_charts(purchases), get_month_charts(purchases), get_year_charts(purchases),
            get_purchase_charts(purchases), get_region_charts(purchases)]
