import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from pymorphy3 import *
import sqlite3


# сет токенов
def clear(raw):
    raw = raw.lower()
    tokens = set(word_tokenize(raw))
    tokens = set(filter(lambda x: x not in stops and x.isalpha(), tokens))
    tokens = set(map(lambda x: lemmatizer.normal_forms(x)[0], tokens))
    return tokens


# nltk.download('punkt')
# nltk.download('stopwords')
stops = set(stopwords.words('russian'))
lemmatizer = MorphAnalyzer(lang='ru')

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

COMPANIES_TABLE = "analysis_companies"
CONTRACTS_TABLE = "analysis_contracts"
PURCHASES_TABLE = "analysis_purchases"
PARTICIPANTS_TABLE = "analysis_participants"
OKPD_TABLE = "analysis_okpd"
trash_words = ["поставка", "закупка", "оказание", "выполнение"]
trash_chars = ['"', '-', ':', '(', ')', '_', '.']

def check_category(purchase_name):
    purchase_tokens = clear(purchase_name)
    for trash_word in trash_words:
        if trash_word in purchase_tokens:
            purchase_tokens.remove(trash_word)
    print(purchase_tokens)
    res = cur.execute(f"SELECT no, name FROM {OKPD_TABLE}")
    categories = res.fetchall()
    best_result = 0
    ans = "-1"
    for (no, category_name) in categories:
        category_tokens = clear(category_name)
        matches = 0
        for purchase_token in purchase_tokens:
            if purchase_token in category_tokens:
                matches += 1
        if matches > best_result:
            best_result = matches
            ans = no[:5].replace(',', '.')
            if matches == len(purchase_tokens):
                break
    return ans


ask = cur.execute(f"SELECT id, lot_name FROM {PURCHASES_TABLE}")
purchases_tuple = ask.fetchall()
cnt = 0
ind = 0
req = f"SELECT no, name FROM {OKPD_TABLE}"
resp = cur.execute(req).fetchall()
fast_table = dict()
for i in resp:
    fast_table[i[1]] = i[0]
for purchase_id, lot_name in purchases_tuple:
    if ind % 1000 == 0:
        print(ind, cnt, len(purchases_tuple))
    lot_name = lot_name.lower()
    for trash_char in trash_chars:
        lot_name = lot_name.replace(trash_char, '')
    resp = fast_table.get(lot_name, None)
    if resp is not None:
        cnt += 1
        req = f"""
            UPDATE {PURCHASES_TABLE}
            SET category = \"{resp[:5]}\"
            WHERE id = {purchase_id}
        """
        cur.execute(req)
    ind += 1

con.commit()
con.close()
