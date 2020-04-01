import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Timer
import time
import back

import os
from flask import Flask, request

TOKEN = 'toekn'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

word = ''
chat_id = 0
message_id = 0


def gen_markup():
    markup = InlineKeyboardMarkup()

    markup.row_width = 1
    markup.add(InlineKeyboardButton("Meaning", callback_data="meaning"),
               InlineKeyboardButton("Synonym", callback_data="synonym"),
               InlineKeyboardButton("Antonym", callback_data="antonym"),
               InlineKeyboardButton("Retype Word", callback_data="retype"),
               InlineKeyboardButton("Done", callback_data="done"))
    return markup


def new_markup():
    return InlineKeyboardMarkup()


def close_markup():
    global chat_id, message_id
    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Entered Word: " + word + "\n" 
                                                    + "Session terminated due to inactivity", reply_markup=new_markup())
        message_id = 0


end_chat = None


@bot.message_handler(commands=['start'])
def start(message):
    chatid = message.chat.id
    text = 'Hello. Ask me the meaning of any word. Just type the word to get started.'
    bot.send_message(chatid, text)


@bot.message_handler(commands=['help'])
def help_text(message):
    chatid = message.chat.id
    text = 'To find the meaning of a word, just type it in.'
    bot.send_message(chatid, text)


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    global word, chat_id, message_id, end_chat
    answer = None
    parameter = call.data + " of " + word

    end_chat.cancel()

    if call.data == "meaning":
        bot.answer_callback_query(call.id, "Fetching " + parameter)
        answer = back.getresult(parameter)
    elif call.data == "synonym":
        bot.answer_callback_query(call.id, "Fetching " + parameter)
        answer = back.getresult(parameter)
    elif call.data == "antonym":
        bot.answer_callback_query(call.id, "Fetching " + parameter)
        answer = back.getresult(parameter)
    elif call.data == "retype":
        bot.answer_callback_query(call.id, "Processing")
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=new_markup())
        message_id = 0
        answer = "Type the word again"
    elif call.data == "done":
        bot.answer_callback_query(call.id, "Processing")
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=new_markup())
        message_id = 0

    if answer:
        bot.send_message(chat_id, answer)
        end_chat = Timer(120.0, close_markup)
        end_chat.start()


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    global word, chat_id, message_id, end_chat

    word = message.text
    chat_id = message.chat.id
    end_chat = Timer(120.0, close_markup)

    if message_id:
        time.sleep(1)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=new_markup())
        message_id = 0
    message_id = bot.send_message(chat_id=chat_id, text="Entered Word: " + word, reply_markup=gen_markup()).message_id
    end_chat.start()

    
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "working", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='heroku-app-url/' + TOKEN)
    return "working", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
