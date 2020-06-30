import time
import logging
from simple_telegram_bot.bot import Bot
from simple_telegram_bot.db import DataBase
from telegram.error import NetworkError, Unauthorized

api_token = '' #enter your api token

#editable functions
def handle_updates(bot, db):
    '''Gets updates from bot and replies the users with the same text they sent.'''
    ls_updates = bot.get_updates()
    for tup in ls_updates:
        id, text = tup
        add_id_to_db(id, db)
        db.execute('INSERT INTO texts(id, text) VALUES(?, ?)', (id, text))
        bot.send_text(id, text)
        if text.lower()=='winrar': bot.send_photo(id, 'winrar.jpg')

#core
def main():
    global api_token
    ls_db_init_str = ['CREATE TABLE IF NOT EXISTS users(id INTEGER)'
                        ,'CREATE TABLE IF NOT EXISTS texts(id INTEGER, text TEXT)']
    db = DataBase(ls_db_init_str)
    if not api_token: api_token = get_api_token()
    bot = Bot(api_token)
    while 1:
        try:
            handle_updates(bot, db)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            update_id += 1
        except Exception as e:
            logger.error(f'Exception: {str(e)}')
            time.sleep(1)

def add_id_to_db(id, db):
    '''Adds id to db if it is new
    Args:
        id (int) - telegram id of user
        db (DataBase) - DataBase object
    '''
    ls_rows = db.get_ls_rows('SELECT id FROM users WHERE id=(?)', (id,))
    if id not in [x[0] for x in ls_rows]:
        db.execute('INSERT INTO users(id) VALUES(?)', (id,))
        logger.info(f'New user {id} added.')

def get_api_token():
    try:
        with open ('api_token.txt', 'r') as f:
            api_token = f.readline()
        return api_token
    except:
        assert api_token, 'Whoops! Please provide an api_token.'

if __name__ == '__main__':
    #logging
    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler() #stream log
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(c_handler)
    f_handler = logging.FileHandler('log.log', 'w', 'utf-8') #file log
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s]: %(message)s'))
    logger.addHandler(f_handler)
    #main
    main()