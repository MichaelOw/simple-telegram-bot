import time
import logging
import telegram
from telegram.error import NetworkError, Unauthorized

logger = logging.getLogger('root')

class Bot:
    def __init__(self, api_token):
        '''Initilizes Bot object with attributes:
            bot (telegram.Bot)
            update_id (int)
            dt_last_message_id (Dictionary): {id: last_message_id}
        '''
        logger.info('Loading bot...')
        self.bot = self.get_bot(api_token)
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None
        self.dt_last_message_id = {}
        logger.info('Bot loaded!')
        
    def send_text(self, id, text):
        '''Does the following:
            - Sends text to telegram id
            - Records message_id of the sent message in self.dt_last_message_id
            - Returns message_id of the message sent
        Args:
            id (int)
            text (str)
        Returns:
            message_id (int)
        '''
        self.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING) #'xxx is typing...' indicator
        message = self.bot.send_message(chat_id=id, text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=1)
        self.dt_last_message_id[id] = message.message_id
        logger.debug(f'Text message sent. (id: {id}, text: {text})')
        return message.message_id

    def send_photo(self, id, f, caption=None):
        '''Sends image to id. Returns message_id of the message sent.
        Args:
            id (int)
            f (str): File name of image file
            caption (str)
        Returns:
            message_id (int)
        '''
        self.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING) #'xxx is typing...' indicator
        message = self.bot.send_photo(chat_id=id, photo=open(f,'rb'), caption = caption)
        self.dt_last_message_id[id] = message.message_id
        logger.debug(f'Photo sent. (id: {id}, f: {f}, caption: {caption})')
        return message.message_id

    def send_file(self, id, f, caption=None):
        '''Sends document to id. Returns message_id of the message sent.
        Args:
            id (int)
            f (str): File name
            caption (str)
        Returns:
            message_id (int)
        '''
        self.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING) #'xxx is typing...' indicator
        message = self.bot.send_document(chat_id=id, document=open(f,'rb'), caption = caption)
        self.dt_last_message_id[id] = message.message_id
        logger.debug(f'Document sent. (id: {id}, f: {f}, caption: {caption})')
        return message.message_id

    def delete_message(self, id, message_id=None):
        '''Deletes message to user with input message_id.
        If no message_id input, tries to delete last message.
        Args:
            id (int)
            message_id (int)
        '''
        if message_id:
            self.bot.delete_message(chat_id=id, message_id=message_id)
        else:
            last_message_id = self.dt_last_message_id.get(id)
            if last_message_id:
                self.bot.delete_message(chat_id=id, message_id=last_message_id)
            else:
                logger.debug('Last message not found.')

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
                logger.debug(f'Message recieved. (id: {m.chat_id}, text: {m.text} ({m.text.encode("raw_unicode_escape")}))')
                ls_updates.append((m.chat_id, m.text))
        return ls_updates
  
    def get_bot(self, api_token):
        '''Returns telegram.Bot object with api_token
        '''
        while 1:
            try:
                bot = telegram.Bot(api_token)
                return bot
            except Exception as e:
                logger.error('exception: ', str(e))
                time.sleep(2)
                return self.get_bot(api_token) #recursive call
                
