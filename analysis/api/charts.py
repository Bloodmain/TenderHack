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
    purchases.sort(key=lambda a: a[0].publish_date)
    ret[0]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[0]['xName'] = "Закупки"
    ret[0]['yName'] = "Рубли"
    ret[0]['chart'][0]['color'] = ['' for _ in range(len(purchases))]
    for i in range(len(purchases)):
        if purchases[i][0].contract_category:
            ret[0]['chart'][0]['color'][i] = 'blue'
        else:
            ret[0]['chart'][0]['color'][i] = 'red'
    ret[0]['chart'][0]['data'] = list(map(lambda a: a[0].price, purchases))

    ret[1]['xName'] = "Закупки"
    ret[1]['yName'] = "Рубли"
    ret[1]['labels'] = list(map(lambda a: a[0].purchase_name, purchases))
    ret[1]['chart'][0]['color'] = ['' for _ in range(len(purchases))]
    for i in range(len(purchases)):
        if purchases[i][0].contract_category:
            ret[0]['chart'][0]['color'][i] = 'blue'
        else:
            ret[0]['chart'][0]['color'][i] = 'red'
    ret[1]['chart'][0]['data'] = list(
        map(lambda a: sum(map(lambda contract: contract.price, a[1]['contracts'])), purchases))

    ret[2]['xName'] = "Закупки"
    ret[2]['yName'] = "Количество поставщиков"
    for i in purchases:
        ret[2]['labels'].append(i[0].purchase_name)
        ret[2]['chart'][0]['color'].append('red')
        ret[2]['chart'][0]['data'].append(i[1]['count'])
    return ret


def get_region_charts(purchases):
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
            'title': 'Количество выигрышных и проигрышных тендеров',
            'type': 'bar',
            'concat': True,
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
        region_info[region][1] += sum([contract.price for contract in i[1]["contracts"]])
    ret[0]['labels'] = list(map(lambda a: a, region_info.keys()))
    ret[0]['xName'] = "Регионы"
    ret[0]['yName'] = "Рубли"
    ret[0]['chart'][0]['color'] = ['blue' for _ in range(len(purchases))]
    ret[0]['chart'][0]['data'] = list(map(lambda a: region_info[a][0], region_info.keys()))

    ret[1]['xName'] = "Регионы"
    ret[1]['yName'] = "Рубли"
    ret[1]['labels'] = list(map(lambda a: a, region_info.keys()))
    ret[1]['chart'][0]['color'] = ['blue' for _ in range(len(purchases))]
    ret[1]['chart'][0]['data'] = list(map(lambda a: region_info[a][1], region_info.keys()))

    ret[2]['xName'] = "Регионы"
    ret[2]['yName'] = "Рубли"
    ret[2]['labels'] = list(map(lambda a: a, region_info.keys()))
    ret[2]['chart'][0]['color'] = ['blue' for _ in range(len(purchases))]
    ret[2]['chart'][0]['data'] = list(map(lambda a: region_info[a][1], region_info.keys()))
    ret[2]['chart'][1]['color'] = ['blue' for _ in range(len(purchases))]
    ret[2]['chart'][1]['data'] = list(map(lambda a: region_info[a][1], region_info.keys()))
    return ret


def get_year_charts(purchases):
    ret = [
        {
            'title': 'Максимальная начальная цена',
            'concat': False,
        },
        {
            'title': 'Финальная цена',
            'concat': True,
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
        year_info[year][1] += sum([contract.price for contract in i[1]["contracts"]])
    ret[0]['labels'] = list(map(lambda a: a, year_info.keys()))
    ret[0]['xName'] = "Года"
    ret[0]['yName'] = "Рубли"
    ret[0]['chart'][0]['color'] = ['blue' for _ in range(len(purchases))]
    ret[0]['chart'][0]['data'] = list(map(lambda a: year_info[a][0], year_info.keys()))

    ret[1]['xName'] = "Года"
    ret[1]['yName'] = "Рубли"
    ret[1]['labels'] = list(map(lambda a: a, year_info.keys()))
    ret[1]['chart'][0]['color'] = ['blue' for _ in range(len(purchases))]
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
        'title': 'Количество выигрышных и проигрышных тендеров',
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
    ret[0]['title'] = 'Максимальная начальная цена'
    ret[1]['title'] = 'Финальная цена'
    ret[0]['xName'] = 'Месяцы'
    ret[0]['yName'] = 'Рубли'
    ret[1]['xName'] = 'Месяцы'
    ret[1]['yName'] = 'Рубли'
    ret[2]['xName'] = 'Месяцы'
    ret[2]['yName'] = 'Рубли'

    return ret


def make_charts_info(purchases):
    return [*get_purchase_charts(purchases), *get_month_charts(purchases), *get_year_charts(purchases),
            *get_region_charts(purchases)]
    # return [get_day_charts(purchases), get_month_charts(purchases), get_year_charts(purchases),
    #         get_purchase_charts(purchases), get_region_charts(purchases)]
