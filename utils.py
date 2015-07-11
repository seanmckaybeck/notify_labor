import datetime
import os
import sqlite3
import time


DB_NAME = 'numbers.db'
SCHEMA = 'create table numbers (id integer primary key autoincrement not null,number text not null)'


def init_db():
    exists = os.path.exists(DB_NAME)
    with sqlite3.connect(DB_NAME) as conn:
        if not exists:
            conn.executescript(SCHEMA)
            conn.commit()


def insert_to_db(number):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM numbers WHERE number = ?', (number,))
        data = cursor.fetchone()
        if not data:
            cursor.execute('INSERT INTO numbers (number) values (?)', (number,))
            conn.commit()


def get_all_numbers():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT number FROM numbers')
        numbers = cursor.fetchall()
        return [row[0] for row in numbers]


def get_timestamp():
    dt = datetime.datetime.now()
    stamp = time.mktime(dt.timetuple())
    return stamp
