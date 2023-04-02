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
trash_words = ["поставка", "закупка", "оказание", "выполнение"]
trash_chars = ['"', '-', ':', '(', ')', '_', '.']


def fix_name(arg_name):
    arg_name = arg_name.lower()
    for trash_char in trash_chars:
        arg_name = arg_name.replace(trash_char, '')
    return arg_name


def clear(raw):
    raw = fix_name(raw)
    tokens = set(word_tokenize(raw))
    tokens = set(filter(lambda x: x not in stops and x.isalpha(), tokens))
    tokens = set(map(lambda x: lemmatizer.normal_forms(x)[0], tokens))
    return tokens


def dump_category_map():
    ind = 0
    global words_category, names_category
    number_set = set()
    for no, name in okpd_pairs:
        if ind % 1000 == 0:
            print(ind)
        no.replace(',', '.')
        if no in number_set:
            continue
        number_set.add(no)
        words = clear(name)
        names_category[no] = len(words)
        for word in words:
            if word not in words_category:
                words_category[word] = []
            words_category[word].append(no)
        ind += 1
    with open("words_category.json", "w") as wc:
        json.dump(words_category, wc)
    with open("names_category.json", "w") as nc:
        json.dump(names_category, nc)


def load_words_category():
    global words_category, names_category
    with open("words_category.json", "r") as wc:
        words_category = json.load(wc)
    with open("names_category.json", "r") as nc:
        names_category = json.load(nc)


#   can return None
def find_category(lot_name):
    global words_category
    lot_name = fix_name(lot_name)
    tokens = clear(lot_name)
    for trash_word in trash_words:
        if trash_word in tokens:
            tokens.remove(trash_word)
    potential_categories = dict()
    for token in tokens:
        matching_categories = words_category.get(token, [])
        for category in matching_categories:
            if category not in potential_categories:
                potential_categories[category] = 0
            potential_categories[category] += 1
    bestie = None
    best_res = 0
    for category_num, entries in potential_categories.items():
        expr = entries / names_category[category_num]
        if expr > best_res:
            best_res = expr
            bestie = category_num
    return bestie


if __name__ == "__main__":
    req = f"SELECT no, name FROM {OKPD_TABLE}"
    okpd_pairs = cur.execute(req).fetchall()
    words_category = dict()
    names_category = dict()
    # dump_category_map()
    # exit(0)
    load_words_category()

    req = f"SELECT id, lot_name FROM {PURCHASES_TABLE}"
    purchase_pairs = cur.execute(req).fetchall()
    categories_map = dict()
    ind = 0
    for purchase_id, lot_name in purchase_pairs:
        if ind % 1000 == 0:
            print(ind, len(purchase_pairs))
        categories_map[purchase_id] = find_category(lot_name)
        ind += 1
    with open("categories.json", "w") as categories_file:
        json.dump(categories_map, categories_file)
