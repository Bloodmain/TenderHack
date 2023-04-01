import sqlite3
import nltk
import spacy
from deep_translator import GoogleTranslator
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from numpy import dot
from numpy.linalg import norm

translator = GoogleTranslator(source='ru', target='en')


# сет токенов
def clear(raw):
    raw = raw.lower()
    tokens = set(word_tokenize(raw))
    tokens = set(filter(lambda x: x not in stops and x.isalpha(), tokens))
    tokens = set(map(lemmatizer.lemmatize, tokens))
    return " ".join(tokens)


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stops = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

COMPANIES_TABLE = "analysis_companies"
CONTRACTS_TABLE = "analysis_contracts"
PURCHASES_TABLE = "analysis_purchases"
PARTICIPANTS_TABLE = "analysis_participants"
OKPD_TABLE = "analysis_okpd"

nlp = spacy.load("en_core_web_sm")

eps = 0.8


def to_eng(rus):
    return translator.translate(rus, source="ru", target="en")

def check_category(purchase_name):
    purchase = nlp(clear(to_eng(purchase_name))).vector
    res = cur.execute(f"SELECT no, name FROM {OKPD_TABLE}")
    categories = res.fetchall()
    for (no, category_name) in categories:
        cat = nlp(clear(to_eng(category_name))).vector
        # print(dot(cat, purchase) / norm(cat) / norm(purchase))
        if dot(cat, purchase) / norm(cat) / norm(purchase) > eps:
            return no[:5].replace(',', '.')
    return "-1"


res = cur.execute(f"SELECT no, name FROM {OKPD_TABLE}")
categories = res.fetchall()
cnt = 0
for (no, category_name) in categories:
    to_eng(category_name)
    if cnt % 10 == 0:
        print(cnt, category_name)
    cnt += 1


# print(check_category("""
# Поставка канцелярских товаров
# """))
