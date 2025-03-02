import csv
import json

with open("csvData/companies.csv", encoding="utf-8") as file:
    with open("csvData/companies3.csv", 'w', encoding="utf-8") as out:
        with open('clasterization.json', 'r', encoding="utf-8") as js_c:
            reader = csv.DictReader(file, delimiter=";")
            fieldnames = ['name', 'supplier_inn', 'supplier_kpp', 'okved', 'status', 'count_managers', 'cluster']
            writer = csv.DictWriter(out, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            clusters = json.load(js_c)
            for row in reader:
                si = str(int(row['supplier_inn']))
                if si in clusters:
                    row['cluster'] = clusters[si]
                else:
                    row['cluster'] = 0
                writer.writerow(row)
            print('Companies preprocessed')

with open("csvData/purchases2.csv", encoding="utf-8") as file:
    with open("csvData/purchases3.csv", 'w', encoding="utf-8") as out:
        with open('categories.json', 'r', encoding="utf-8") as js_c:
            reader = csv.DictReader(file, delimiter=";")
            fieldnames = ['id', 'purchase_name', 'lot_name', 'price', 'customer_inn', 'customer_name', 'delivery_region',
                          'publish_date', 'contract_category', 'category']
            writer = csv.DictWriter(out, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            categories = json.load(js_c)
            for row in reader:
                si = row['id'].split('_')[1]
                row['category'] = categories[si]
                writer.writerow(row)
            print('purchases preprocessed')
