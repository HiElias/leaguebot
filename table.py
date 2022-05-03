import os
import sqlite3

class Table():
    def __init__(self) -> None:
        if 'table.db' in os.listdir():
            self.con = sqlite3.connect('table.db', check_same_thread=False)
            self.cur = self.con.cursor()
        else:
            self.con = sqlite3.connect('table.db', check_same_thread=False)
            self.cur = self.con.cursor()
            self.cur.execute('''CREATE TABLE instas
               (date text, urls text, name text primary key, whose text, place int)''')
            self.con.commit()

    def add(self, data):
        date, urls, name, whose, place = data
        query = """
                    INSERT INTO 
                        instas 
                    VALUES (?, ?, ?, ?, ?)
                    """ 
        self.cur.execute(query, (date, urls, name, whose, place))
        self.con.commit()