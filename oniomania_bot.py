#!/usr/bin/env python2
# with code from @Abbotta4's Pointsbot
import logging,ConfigParser,io
from telegram.ext import Updater,MessageHandler,CommandHandler,Filters,BaseFilter

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

# Load the configuration file
try:
    with open("config.ini") as f:
        sample_config = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_config))
except FileNotFoundError:
    print('Could not find a config file.')

# Main        
updater = Updater(token = config.get('telegram', 'token'))
dispatcher = updater.dispatcher

class FilterUsername(BaseFilter):
    def filter(self, message):
        return config.username in message.text
filter_username = FilterUsername()
    
def respond(bot, update):
    cursor.execute("""SELECT word, freq FROM markov WHERE freq > 0""")
    r = weighted_choice(dict((k[0], k[1]) for k in cursor.fetchall()))
    response = r
    while True:
        cursor.execute("""SELECT next FROM markov WHERE word = %s""", (r, ))
        r = weighted_choice(cursor.fetchall()[0][0])
        if str(r) == 'null':
            break
        else:
            r = str(r)
            response += ' ' + r
    print(response)
    bot.send_message(chat_id = update.message.chat_id, text = response)

response_handler = MessageHandler(filter_username, respond)
dispatcher.add_handler(response_handler)

updater.start_polling()
updater.idle()
