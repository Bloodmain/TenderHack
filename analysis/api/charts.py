# from analysis.models import *
# import pprint


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
    purchases.sort(key=lambda a: a[0].publish_date )
    ret[0]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[0]['xName'] = "Закупки"
    ret[0]['yName'] = "Рубли"
    ret[0]['chart'][0]['color'] = ['' for _ in range(len(purchases))]
    for i in range(len(purchases)):
        ret[0]['chart'][0]['color'][i] = 'red' if purchases[i][0].contract_category else 'blue'
    ret[0]['chart'][0]['data'] = list(map(lambda a: a[0].price, purchases))

    ret[1]['xName'] = "Закупки"
    ret[1]['yName'] = "Рубли"
    ret[1]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[1]['chart'][0]['color'] = ['' for _ in range(len(purchases))]
    for i in range(len(purchases)):
        ret[1]['chart'][0]['color'][i] = 'red' if purchases[i][0].contract_category else 'blue'
    ret[1]['chart'][0]['data'] = list(map(lambda a: sum(map(lambda contract: contract.price, a[1]['contracts'])), purchases))

    ret[2]['xName'] = "Закупки"
    ret[2]['yName'] = "Количество поставщиков"
    for i in purchases:
        ret[2]['labels'].append(i[0].purchase_name)
        ret[2]['chart'][0]['color'].append('red')
        ret[2]['chart'][0]['data'].append(i[1]['count'])
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
    return [get_purchase_charts(purchases)]
    # return [get_day_charts(purchases), get_month_charts(purchases), get_year_charts(purchases),
    #         get_purchase_charts(purchases), get_region_charts(purchases)]
