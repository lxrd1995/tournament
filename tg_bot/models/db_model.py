import sqlite3
import logging


class DBModel:
    def __init__(self, path: str):
        self.connect = sqlite3.connect(path, check_same_thread=True)
        self.cursor = self.connect.cursor()

    def func(self):
        try:
            with self.connect:
                self.cursor.execute('')
        except Exception as ex:
            logging.info(f'Ошибка БД: {ex}')
