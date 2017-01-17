import datetime
import os
import sqlite3
import time


DB_NAME = 'numbers.db'
SCHEMA = 'create table numbers (id integer primary key autoincrement not null,number text not null,text integer not null)'


def init_db():
    exists = os.path.exists(DB_NAME)
    with sqlite3.connect(DB_NAME) as conn:
        if not exists:
            conn.executescript(SCHEMA)
            conn.commit()


def insert_to_db(number: str, text: bool):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM numbers WHERE number = ?', (number,))
        data = cursor.fetchone()
        if not data:
            text = 1 if text else 0
            cursor.execute('INSERT INTO numbers (number, text) values (?,?)', (number, text))
            conn.commit()


def get_all_numbers():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT number, text FROM numbers')
        numbers = cursor.fetchall()
        return numbers


def make_recordings_directory():
    if not os.path.exists('recordings'):
        os.mkdir('recordings')

