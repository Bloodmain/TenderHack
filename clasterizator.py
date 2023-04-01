import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from pymorphy3 import *
import sqlite3
import json

stops = set(stopwords.words('russian'))
lemmatizer = MorphAnalyzer(lang='ru')

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

COMPANIES_TABLE = "analysis_companies"
CONTRACTS_TABLE = "analysis_contracts"
PURCHASES_TABLE = "analysis_purchases"
PARTICIPANTS_TABLE = "analysis_participants"
OKPD_TABLE = "analysis_okpd"

def count_meds():
    req = f"SELECT part_id_id, supplier_inn_id, is_winner FROM {PARTICIPANTS_TABLE}"
    participant_tuples = cur.execute(req).fetchall()
    participant_contract_prices = dict()
    ind = 0
    for purchase_id, supplier_inn, is_winner in participant_tuples:
        if ind % 1000 == 0:
            print(ind, len(participant_tuples))
        ind += 1
        if is_winner:
            if supplier_inn not in participant_contract_prices:
                participant_contract_prices[supplier_inn] = []
            req = f"SELECT price FROM {CONTRACTS_TABLE} WHERE contract_id_id = {purchase_id}"
            resp = cur.execute(req).fetchone()
            # print(resp)
            if resp is not None:
                participant_contract_prices[supplier_inn].append(resp[0])
    participant_map = dict()
    ind = 0
    for supplier_inn in participant_contract_prices:
        if ind % 1000 == 0:
            print(ind, len(participant_contract_prices))
        ind += 1
        participant_contract_prices[supplier_inn].sort()
        median = 0
        if len(participant_contract_prices[supplier_inn]) > 0:
            median = participant_contract_prices[supplier_inn][len(participant_contract_prices[supplier_inn]) // 2]
        participant_map[supplier_inn] = median

    with open("medians.json", "w") as cls:
        json.dump(participant_map, cls)

if __name__ == "__main__":
    count_meds()
