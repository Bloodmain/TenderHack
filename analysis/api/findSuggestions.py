from clasterizator import check_cluster
from functools import cmp_to_key


def cmp(item1, item2):
    if len(item1[1]['contracts']) == len(item2[1]['contracts']):
        return item2[0].publish_date - item1[0].publish_date
    return len(item1[1]['contracts']) - len(item2[1]['contracts'])


# Pred: все purchases в данной категории
#   args['inn'] - инн поставщика
#   args['cluster'] - кластер поставщика (1..4)
def find_suggestions(purchases, args):
    ret = []
    for purchase_pair in purchases:
        purchase = purchase_pair[0]
        purchase_dict = purchase_pair[1]
        participants = purchase_dict['participants']
        flag = False
        for participant in participants:
            if participant.is_winner or participant.supplier_inn == args['inn']:
                flag = True
                break
        if flag or check_cluster(purchase.price) != args['cluster']:
            continue
        ret.append(purchase_pair)
    sorted(ret, key=cmp_to_key(cmp))
    return ret
# Желательно выводить в специальных предложениях для каждого тендера конкуренцию в нём, дату и цену
