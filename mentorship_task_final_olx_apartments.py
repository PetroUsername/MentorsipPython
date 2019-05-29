import sqlite3
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def create_table():
    with sqlite3.connect('olx_apartments.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE posts (
                        id integer,
                        price_usd real,
                        title text,
                        text text,
                        total_area real,
                        kitchen_area real,
                        living_area real,
                        location text,
                        number_of_rooms integer,
                        added_on text)""")
        conn.commit()


def populate_table():
    start_date = "2017-01-01"
    stop_date = "2018-01-01"
    row_id = 1

    start = datetime.strptime(start_date, "%Y-%m-%d")
    stop = datetime.strptime(stop_date, "%Y-%m-%d")

    while start < stop:

        response = requests.get(
            'https://35.204.204.210/' + datetime.strftime(start, "%Y-%m-%d") + '/',
            verify=False)

        json_response = response.json()

        for post in json_response['postings']:
            row = (
            str(row_id), post['price_usd'], post['title'], post['text'], post['total_area'], post['kitchen_area'],
            post['living_area'], post['location'], post['number_of_rooms'], post['added_on'])

            with sqlite3.connect('olx_apartments.sqlite3') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO posts VALUES (?,?,?,?,?,?,?,?,?,?)", row)
                conn.commit()
                row_id += 1

        print('Saved data for', datetime.strftime(start, "%Y-%m-%d"), 'into DB')
        start = start + timedelta(days=1)


try:
    create_table()
    populate_table()
except:
    print('Looks like the table "posts" was already created. Trying to build the graph with it.')

objects = []
performance = []

with sqlite3.connect('olx_apartments.sqlite3') as conn:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT strftime('%m',added_on) as month, count(*) as count FROM posts GROUP BY strftime('%m',added_on) ORDER BY month")
    for row in cursor.fetchall():
        objects.append(row[0])
        performance.append(row[1])


y_pos = np.arange(len(objects))

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Count')
plt.title('Number of posts per month in 2017')

plt.show()
