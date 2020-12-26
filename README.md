# simple_telegram_bot
This is a basic Telegram Bot template that I use for my projects.  
This bot is currently setup to:
* Mirror user messages
* Store telegram IDs into a local sqlite3 database
* Store all recieved texts into a local sqlite3 database
* Send an image when message 'winrar' is received

Feel free to edit the code to generate customized responses!

Step 1: Load Telegram API Token
-
Create a bot and get the API token from https://core.telegram.org/bots#6-botfather

Open simple_telegram_bot.py and edit line below.

    api_token = '' #Please provide a valid telegram API token

Step 2: Run the Python script
-
    $ python simple_telegram_bot.py
