import os
import logging
import sqlite3
logger = logging.getLogger('root')

class DataBase:
    def __init__(self, dir_db, init_query = None):
        '''Initilizes DataBase object with attributes:
        Args:
            ls_db_init_str (List): List of init strings (Optional)
            dir_db (str): Directory the database is in (Optional) e.g. 'D:\\Program Files\\simple_telegram_bot\\'
        '''
        assert dir_db, 'Please provide a valid directory...'
        logger.info('Loading db...')
        self.conn = sqlite3.connect(os.path.join(dir_db, 'db.db'))
        c = self.conn.cursor()
        if init_query:
            c.executescript(init_query)
        logger.info('db loaded!')

    def execute(self, query, input_tuple = None):
        '''Executes query, uses input_tuple if given
        Args:
            query (str): SQLite query
            input_tuple (Tuple): input parameters for the query if required
        '''
        assert query
        c = self.conn.cursor()
        if input_tuple:
            c.execute(query, input_tuple)
        else:
            c.executescript(query)
        self.conn.commit()

    def get_ls_rows(self, query, input_tuple = None):
        '''Executes query, uses input_tuple if given, returns rows fetched
        Args:
            query (str): SQLite query
            input_tuple (Tuple): input parameters for the query if required
        Returns:
            ls_rows (List):
                tup (Tuple)
        '''
        ls_rows = []
        c = self.conn.cursor()
        if input_tuple:
            c.execute(query, input_tuple)
        else:
            c.execute(query)
        for row in c.fetchall():
            ls_rows.append(row)
        return ls_rows

    def close(self):
        '''Closes connection'''
        self.conn.close()