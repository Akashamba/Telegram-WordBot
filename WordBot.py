import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import back


TOKEN = 'token'
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
               InlineKeyboardButton("Retype Word", callback_data="restart"))
    return markup


def new_markup():
    return InlineKeyboardMarkup()


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
    parameter = call.data + " of " + word
    if call.data == "meaning":
        bot.answer_callback_query(call.id, "Fetching " + parameter)
        answer = back.getresult(parameter)
    elif call.data == "synonym":
        bot.answer_callback_query(call.id, "Fetching " + parameter)
        answer = back.getresult(parameter)
    elif call.data == "antonym":
        bot.answer_callback_query(call.id, "Fetching " + parameter)
        answer = back.getresult(parameter)
    else:
        bot.answer_callback_query(call.id, "Processing")
        answer = "Type the word again"
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=new_markup())
    bot.send_message(chat_id, answer)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    global word, chat_id, message_id
    word = message.text
    chat_id = message.chat.id
    #bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    message_id = bot.send_message(chat_id, text="Entered Word: " + word, reply_markup=gen_markup()).message_id


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "working", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='heroku-app/' + TOKEN)
    return back.getresult("what is the meaning of apple"), 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
