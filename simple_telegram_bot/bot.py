import logging
import telegram
from telegram.error import NetworkError, Unauthorized

logger = logging.getLogger('simple_telegram_bot.bot')

class Bot:
    def __init__(self, api_token):
        '''Initilizes bot object with attributes:
            api_token (str)
            bot (telegram.Bot)
            update_id (int)            
        '''
        logger.info('Loading bot...')
        self.api_token = api_token
        self.bot = self.get_bot()
        self.update_id = self.get_update_id()
        logger.info('Bot loaded!')
        
    def send_text(self, id, text):
        '''Sends text to telegram id'''
        self.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING) #user will see 'bot is typing...' indicator
        self.bot.send_message(chat_id=id, text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=1)
        logger.info(f'Message sent. (id: {id}, text: {text})')

    def get_updates(self):
        '''Returns list of tuples:
            1. id int - id of user
            2. text str - message sent by user
        '''
        ls_updates = []
        for update in self.bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1
            if update.message:
                m = update.message
            elif update.edited_message:
                m = update.edited_message
            else:
                m = None
            if m:
                logger.info(f'Message recieved. (id: {m.chat_id}, text: {m.text})')
                ls_updates.append((m.chat_id, m.text))
        return ls_updates

    def get_update_id(self):
        '''Returns update_id from Bot object
            update_id (int)
        '''
        try:
            update_id = self.bot.get_updates()[0].update_id
            return update_id
        except IndexError:
            return None
  
    def get_bot(self):
        '''Returns telegram.Bot object with self.api_token
        '''
        while 1:
            try:
                bot = telegram.Bot(self.api_token)
                return bot
            except Exception as e:
                logger.error('exception: ', str(e))
                time.sleep(2)
                return self.get_bot(self.api_token) #recursive call
                
