import csv
import sqlite3
import datetime


def get_purch_id(id):
    return id.split('_')[1]


def company_from_companies(companies):
    res = companies[0]
    for company in companies:
        if 'филиал' not in company['name'] and len(company['name']) > len(res['name']):
            res = company
    return res


def loadCompanies(loadToDatabase):
    with open("csvData/companies.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            if len(row['name'].strip()) != 0:
                COMPANIES[row['supplier_inn']] = [row] + COMPANIES.get(row['supplier_inn'], [])

        if not loadToDatabase:
            return
        request = f""" INSERT INTO {COMPANIES_TABLE} (name, supplier_inn, status, count_managers, okved) VALUES """
        vals = []
        for inn, companies in COMPANIES.items():
            company = company_from_companies(companies)
            company['status'] = "active" if company['status'] == "Активная" else 'blocked'
            company['name'] = company['name'].replace('"', '')
            vals.append(
                f"""(\"{company['name']}\", \"{company['supplier_inn']}\", \"{company['status']}\", \"{company['count_managers']}\", \"{company['okved']}\")""")
        request = request + ',\n'.join(vals)
        cursor.execute(request)


def loadPurchases(loadToDatabase):
    with open("csvData/purchases.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        vals = []
        for row in reader:
            if row['customer_inn'] not in COMPANIES:
                continue
            row['id'] = int(get_purch_id(row['id']))

            PURCHASES[row['id']] = row

            if not loadToDatabase:
                continue

            row['publish_date'] = row['publish_date'].strip().split(' ')[0]
            row['contract_category'] = True if row['contract_category'] == "КС" else False
            row['price'] = int(float(row['price']))
            row['lot_name'] = row['lot_name'].replace('"', '')
            row['purchase_name'] = row['purchase_name'].replace('"', '')
            row['customer_inn'] = int(row['customer_inn'])
            vals.append(
                f"""(\"{row['id']}\", \"{row['purchase_name']}\", \"{row['lot_name']}\", \"{row['price']}\", 
                \"{row['delivery_region']}\", \"{row['customer_inn']}\", \"{row['publish_date']}\", 
                \"{row['contract_category']}\")""")
        if loadToDatabase:
            request = f"""
                    INSERT INTO {PURCHASES_TABLE} (id, purchase_name, lot_name, price, delivery_region, customer_inn_id, publish_date, contract_category)
                    VALUES
                    """
            request = request + ',\n'.join(vals)
            cursor.execute(request)


def loadContracts(loadToDatabase):
    with open("csvData/contracts.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        vals = []
        for row in reader:
            row['id'] = int(get_purch_id(row['id']))
            if row['id'] not in PURCHASES:
                continue
            date1 = datetime.date(*list(map(int, row['contract_conclusion_date'].split('-'))))
            date2 = datetime.date(*list(map(int, PURCHASES[row['id']]['publish_date'].split(' ')[0].split('-'))))
            if date1 < date2:
                row['contract_conclusion_date'] = PURCHASES[row['id']]['publish_date'].split(' ')[0]
            row['price'] = int(float(row['price']))
            vals.append(f"""(\"{row['contract_reg_number']}\", \"{row['id']}\", \"{row['price']}\",
            \"{row['contract_conclusion_date']}\")""")
        if loadToDatabase:
            request = f"""
                        INSERT INTO {CONTRACTS_TABLE} (contract_reg_number, contract_id_id, price, contract_conclusion_date)
                        VALUES
                        """
            request = request + ',\n'.join(vals)
            cursor.execute(request)


def loadParticipants(loadToDatabase):
    with open("csvData/participants.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        vals = []
        for row in reader:
            row['supplier_inn'] = row['supplier_inn']
            row['id'] = int(get_purch_id(row['id']))
            if row['supplier_inn'] not in COMPANIES or row['id'] not in PURCHASES:
                continue
            row['is_winner'] = True if row['is_winner'] == "Да" else False
            vals.append(f"(\"{row['supplier_inn']}\", \"{row['id']}\", \"{row['is_winner']}\")")
        if loadToDatabase:
            request = f"""
                        INSERT INTO {PARTICIPANTS_TABLE} (supplier_inn_id, part_id_id, is_winner)
                        VALUES
                        """
            request = request + ',\n'.join(vals)
            cursor.execute(request)


def loadOKPD(loadToDatabase):
    with open("csvData/okpd.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        vals = []
        trash_chars = ['"', '-', ':', '(', ')', '_', '.']
        for row in reader:
            row_name = row['Название'].lower()
            for trash_char in trash_chars:
                row_name = row_name.replace(trash_char, '')
            row['Название'] = row_name
            vals.append(f"""(\"{row['Код']}\", \"{row['Название']}\")""")
        if loadToDatabase:
            request = f"""INSERT INTO {OKPD_TABLES} (no, name)
                            VALUES """ + ',\n'.join(vals)
            cursor.execute(request)


COMPANIES = {}
PURCHASES = {}
OKPD_TABLES = "analysis_okpd"
COMPANIES_TABLE = "analysis_companies"
CONTRACTS_TABLE = "analysis_contracts"
PURCHASES_TABLE = "analysis_purchases"
PARTICIPANTS_TABLE = "analysis_participants"


if __name__ == '__main__':
    con = sqlite3.connect("db.sqlite3")
    cursor = con.cursor()
    loadToDatabase = True
    loadCompanies(loadToDatabase)
    print('Companies load: success')
    loadPurchases(loadToDatabase)
    print('Purchases load: success')
    loadContracts(loadToDatabase)
    print('Contracts load: success')
    loadParticipants(loadToDatabase)
    print('Participants load: success')
    loadOKPD(loadToDatabase)
    print('OKPD load: success')
    con.commit()
    con.close()
    print('All success')
