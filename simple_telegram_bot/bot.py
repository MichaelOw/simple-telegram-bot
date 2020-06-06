import time
import logging
import telegram
from telegram.error import NetworkError, Unauthorized

logger = logging.getLogger('simple_telegram_bot.bot')

class Bot:
    def __init__(self, api_token):
        '''Initilizes Bot object with attributes:
            api_token (str)
            bot (telegram.Bot)
            update_id (int)            
        '''
        logger.info('Loading bot...')
        self.api_token = api_token
        self.bot = self.get_bot()
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None
        self.dt_last_message_id = {}
        logger.info('Bot loaded!')
        
    def send_text(self, id, text, delete_last=0):
        '''Does the following:
            1. Sends text to telegram id
            2. If delete_last is True, bot will try to delete the last message it sent 
            3. Records message_id of the sent message in self.dt_last_message_id
        Args:
            id (int)
            text (str)
        '''
        if delete_last:
            last_message_id = self.dt_last_message_id.get(id)
            if last_message_id: message = self.bot.delete_message(chat_id=id, message_id=last_message_id)
        self.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING) #user will see 'bot is typing...' indicator
        message = self.bot.send_message(chat_id=id, text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=1)
        self.dt_last_message_id[id] = message.message_id
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
                return self.get_bot() #recursive call
                
