import sqlite3
import requests


def get_set_of_existing_currencies():
    with sqlite3.connect('forex.sqlite3') as conn:
        cursor = conn.cursor()
        currencies_set = set()
        cursor.execute('SELECT * FROM rates')
        for row in cursor.fetchall():
            currencies_set.add(row[0])
        return currencies_set


def update_currencies(currencies_set, rates):
    with sqlite3.connect('forex.sqlite3') as conn:
        cursor = conn.cursor()
        for currency in currencies_set:
            cursor.execute("UPDATE rates SET rate = %s WHERE currency_code = '%s'" % (rates[currency], currency))


def delete_currencies(currencies_set):
    with sqlite3.connect('forex.sqlite3') as conn:
        cursor = conn.cursor()
        for currency in currencies_set:
            cursor.execute("DELETE FROM rates WHERE currency_code = '%s'" % currency)


def insert_currencies(currencies_set, rates):
    with sqlite3.connect('forex.sqlite3') as conn:
        cursor = conn.cursor()
        for currency in currencies_set:
            cursor.execute('INSERT INTO rates VALUES (?, NULL, ?)', (currency, rates[currency]))


response = requests.get(
    'https://api.exchangeratesapi.io/latest')

json_response = response.json()
print(json_response)

input_rates = json_response['rates']
input_currencies = set(input_rates.keys())

existing_currencies = get_set_of_existing_currencies()
currencies_to_update = existing_currencies & input_currencies
currencies_to_delete = existing_currencies - input_currencies
currencies_to_insert = input_currencies - existing_currencies

update_currencies(currencies_to_update,input_rates)
delete_currencies(currencies_to_delete)
insert_currencies(currencies_to_insert,input_rates)
