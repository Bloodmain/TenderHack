from functools import cmp_to_key


def check_cluster(x):
    edges = [5_000, 50_000, 500_000, 5_000_000_000]
    for j in range(4):
        if x < edges[j] or j == 3:
            return j + 1


def cmp(item1, item2):
    # if item1.contr == item2[1]:
        return item2.publish_date - item1.publish_date
    # return item1[1] - item2[1]


# Pred: все purchases в данной категории
#   args['inn'] - инн поставщика
#   args['cluster'] - кластер поставщика (1..4)
def find_suggestions(purchases, args):
    ret = []
    for i in range(len(purchases)):
        if i % 1000 == 0:
            print(i, len(ret))
        purchase = purchases[i]
        if check_cluster(purchase.price) != args['cluster']:
            continue
        ret.append(purchase)
    return sorted(ret, key=cmp_to_key(cmp))
# Желательно выводить в специальных предложениях для каждого тендера конкуренцию в нём, дату и цену
