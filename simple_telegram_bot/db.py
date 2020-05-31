import logging
import sqlite3
logger = logging.getLogger('simple_telegram_bot.db')

class DataBase:
    def __init__(self, db_init_string):
        '''Initilizes DataBase object with attributes:
            conn
        '''
        logger.info('Loading db...')
        self.conn = sqlite3.connect('db.db')
        c = self.conn.cursor()
        c.execute(db_init_string)
        logger.info('db loaded!')

    def insert_id(self, id):
        '''Inserts new id into DataBase object'''
        c = self.conn.cursor()
        c.execute(
            '''
            INSERT INTO users(id)
            VALUES(?)
            '''
            ,(id,)
        )
        self.conn.commit()
        
    def get_ls_rows(self):
        '''Returns list of tuples
            1. id (int) - id of user
        '''
        ls_rows = []
        c = self.conn.cursor()
        c.execute(
            '''
            SELECT *
            FROM users
            '''
        )  
        for row in c.fetchall():
            ls_rows.append(row)
        return ls_rows