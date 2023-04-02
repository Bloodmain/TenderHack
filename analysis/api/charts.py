# from analysis.models import *
# import pprint
from analysis.api.findSuggestions import find_suggestions
from analysis.models import *


def get_purchase_charts(purchases):
    ret = [
        {
            'title': 'Максимальная начальная цена',
            'concat': False,
            'ks': True,
            'displayXLabels': False,
        },
        {
            'title': 'Финальная цена',
            'concat': True,
            'ks': True,
            'displayXLabels': False,
        },
        {
            'title': 'Количество поставщиков-участников',
            'concat': True,
            'ks': True,
            'displayXLabels': False,
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
    purchases.sort(key=lambda a: a[0].publish_date)
    ret[0]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[0]['xName'] = "Закупки"
    ret[0]['yName'] = "Рубли"
    ret[0]['chart'][0]['color'] = ['' for _ in range(len(purchases))]
    flag = True
    for i in range(len(purchases)):
        if purchases[i][0].contract_category == "True":
            ret[0]['chart'][0]['color'][i] = 'blue'
        else:
            ret[0]['chart'][0]['color'][i] = 'red'
    ret[0]['chart'][0]['data'] = list(map(lambda a: a[0].price, purchases))

    ret[1]['xName'] = "Закупки"
    ret[1]['yName'] = "Рубли"
    ret[1]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[1]['chart'][0]['color'] = ['' for _ in range(len(purchases))]
    for i in range(len(purchases)):
        if purchases[i][0].contract_category == "True":
            ret[1]['chart'][0]['color'][i] = 'blue'
        else:
            ret[1]['chart'][0]['color'][i] = 'red'
    ret[1]['chart'][0]['data'] = list(
        map(lambda a: sum(map(lambda contract: contract.price, a[1]['contracts'])), purchases))
    ret[2]['xName'] = "Закупки"
    ret[2]['yName'] = "Количество поставщиков"
    for i in purchases:
        ret[2]['labels'].append(i[0].purchase_name)
        if i[0].contract_category == "True":
            ret[2]['chart'][0]['color'].append('blue')
        else:
            ret[2]['chart'][0]['color'].append('red')
        ret[2]['chart'][0]['data'].append(i[1]['count'])
    return ret


def get_region_charts(purchases):
    ret = [
        {
            'title': 'Максимальная начальная цена по регионам',
            'concat': False,
            'ks': False,
            'displayXLabels': True
        },
        {
            'title': 'Финальная цена выигрышных тендеров по регионам',
            'concat': True,
            'ks': False,
            'displayXLabels': True
        }
    ]
    for i in ret:
        i['type'] = 'doughnut'
        i['labels'] = []
        i['chart'] = [
            {
                'color': [],
                'line_label': '',
                'data': [],
                'regression': False
            }
        ]
    region_info = {}
    for i in purchases:
        region = i[0].delivery_region
        if region not in region_info:
            region_info[region] = [0, 0]
        region_info[region][0] += i[0].price
        region_info[region][1] += (1 if i[1]["is_winner"] else 0) * sum(contract.price for contract in i[1]["contracts"])
    ret[0]['labels'] = list(region_info.keys())
    ret[0]['xName'] = "Регионы"
    ret[0]['yName'] = "Рубли"
    ret[0]['chart'][0]['color'] = ['blue'] * len(region_info.keys())
    ret[0]['chart'][0]['data'] = list(map(lambda a: region_info[a][0], region_info.keys()))

    ret[1]['xName'] = "Регионы"
    ret[1]['yName'] = "Рубли"
    ret[1]['labels'] = list(region_info.keys())
    ret[1]['chart'][0]['color'] = ['blue'] * len(region_info.keys())
    ret[1]['chart'][0]['data'] = list(map(lambda a: region_info[a][1], region_info.keys()))
    return ret


def get_year_charts(purchases):
    ret = [
        {
            'title': 'Суммарная максимальная начальная цена по годам',
            'concat': False,
            'ks': False,
            'displayXLabels': True,
        },
        {
            'title': 'Суммарная финальная цена по годам',
            'concat': True,
            'ks': False,
            'displayXLabels': True,
        }
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
    year_info = {}
    for i in purchases:
        year = i[0].publish_date.year
        if year not in year_info:
            year_info[year] = [0, 0]
        year_info[year][0] += i[0].price
        year_info[year][1] += (1 if i[1]["is_winner"] else 0) * sum([contract.price for contract in i[1]["contracts"]])
    ret[0]['labels'] = list(map(lambda a: a, year_info.keys()))
    ret[0]['xName'] = "Годы"
    ret[0]['yName'] = "Рубли"
    ret[0]['chart'][0]['color'] = ['blue' for _ in range(len(year_info.keys()))]
    ret[0]['chart'][0]['data'] = list(map(lambda a: year_info[a][0], year_info.keys()))

    ret[1]['xName'] = "Годы"
    ret[1]['yName'] = "Рубли"
    ret[1]['labels'] = list(map(lambda a: a, year_info.keys()))
    ret[1]['chart'][0]['color'] = ['blue' for _ in range(len(year_info.keys()))]
    ret[1]['chart'][0]['data'] = list(map(lambda a: year_info[a][1], year_info.keys()))
    return ret


# Pred: дата purchase не раньше 1 января текущего года
def get_month_charts(purchases):
    MONTH_CNT = 12
    ret = [{
        'title': '',
        'concat': False,
        'type': 'bar',
        'labels': ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
                   "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        'chart': [{'color': ['blue'] * MONTH_CNT,
                   'line_label': '',
                   'data': [0] * MONTH_CNT,
                   'regression': False
                   }]
    }, {
        'title': '',
        'concat': True,
        'type': 'bar',
        'labels': ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
                   "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        'chart': [{'color': ['blue'] * MONTH_CNT,
                   'line_label': '',
                   'data': [0] * MONTH_CNT,
                   'regression': False
                   }]
    }, {
        'title': 'Количество выигранных и проигрышных тендеров по месяцам',
        'type': 'bar',
        'concat': True,
        'labels': ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
                   "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        'chart': [{'color': ['green'] * MONTH_CNT,
                   'line_label': 'Выигрышные',
                   'data': [0] * MONTH_CNT,
                   'regression': False
                   },
                  {'color': ['red'] * MONTH_CNT,
                   'line_label': 'Проигрышные',
                   'data': [0] * MONTH_CNT,
                   'regression': False
                   }]
    },
    ]
    for purchase in purchases:
        purchase_month = purchase[0].publish_date.month - 1  # because date.month is 1..12 inclusive
        ret[0]['chart'][0]['data'][purchase_month] += purchase[0].price
        ret[1]['chart'][0]['data'][purchase_month] += sum(
            [(1 if purchase[1]["is_winner"] else 0) * contract.price for contract in purchase[1]["contracts"]])

        ret[2]['chart'][0]['data'][purchase_month] += (1 if purchase[1]["is_winner"] else 0)
        ret[2]['chart'][1]['data'][purchase_month] += (1 if not purchase[1]["is_winner"] else 0)
    ret[0]['title'] = 'Суммарная максимальная начальная цена по месяцам'
    ret[1]['title'] = 'Суммарная финальная цена выигранных тендеров по месяцам'
    ret[0]['xName'] = 'Месяцы'
    ret[0]['yName'] = 'Рубли'
    ret[1]['xName'] = 'Месяцы'
    ret[1]['yName'] = 'Рубли'
    ret[2]['xName'] = 'Месяцы'
    ret[2]['yName'] = 'Рубли'

    return ret


def get_recommendations(purchases, args):
    # print({ "inn": inn, "cluster": Companies.objects.get(supplier_inn=inn).cluster })
    # print(find_suggestions(purchases, { "inn": inn, "cluster": Companies.objects.get(supplier_inn=inn).cluster }))
    return find_suggestions(purchases, args)

def make_charts_info(purchases, inn):
    return [*get_purchase_charts(purchases), *get_month_charts(purchases), *get_year_charts(purchases),
            *get_region_charts(purchases)]
    # return [get_day_charts(purchases), get_month_charts(purchases), get_year_charts(purchases),
    #         get_purchase_charts(purchases), get_region_charts(purchases)]
