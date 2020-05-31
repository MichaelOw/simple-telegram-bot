import time
import logging
from simple_telegram_bot.bot import Bot
from telegram.error import NetworkError, Unauthorized

try:
    with open ('api_token.txt', 'r') as f:
        api_token = f.readline()
except:
    api_token = '' #Please provide a valid telegram API token
    assert api_token, 'Whoops! Please provide an api_token.'

#functions
def handle_updates(bot):
    '''Gets updates from bot and replies the users with the same text they sent.'''
    ls_updates = bot.get_updates()
    for tup in ls_updates:
        id, text = tup
        bot.send_text(id, text)
        
#main
def main():
    bot = Bot(api_token)
    while 1:
        try:
            handle_updates(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            update_id += 1
        except Exception as e:
            logger.error(f'Exception {str(e)}')
            time.sleep(1)

if __name__ == '__main__':
    #logging
    logger = logging.getLogger('simple_telegram_bot')
    logger.setLevel(logging.INFO)
    c_handler = logging.StreamHandler() #stream log
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(c_handler)
    f_handler = logging.FileHandler('log.log') #file log
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s]: %(message)s'))
    logger.addHandler(f_handler)
    #main
    main()