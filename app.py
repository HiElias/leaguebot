import re
import telebot # pyTelegramBotAPI 
from telebot import types 
import re
import table 
import os
import requests as r
import urllib.parse as ur

TOKEN = str(open('TOKEN', 'r').read())
table = table.Table()
url_reg = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
regexp_arg = r"(?:(?:http|https):\/\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/(\w+)"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	but1 = types.KeyboardButton("Tournament") 
	but2 = types.KeyboardButton("Vote") 
	but3 = types.KeyboardButton("Add url") 
	markup.add(but1, but2, but3)

	bot.reply_to(message, "Hi {0.first_name}\n".format(message.from_user)
  ,parse_mode='html',reply_markup=markup)



@bot.message_handler(func=lambda message: re.search(url_reg, message.text))
def insta_url(message): # ONLY INSTA URLS
	date = message.date
	url = message.text
	whose = message.from_user.username
	place = 0
	try:
		validator_reg = re.search(regexp_arg, message.text)
		url_path = ur.urlparse(message.text).path
		first_path = re.findall(r'/\w*', url_path)[0][1:]
		#print(first_path)
		if validator_reg is None and \
			first_path != 'stories' and \
				len(first_path) > 1: #and r.get(message.text).ok:
			bot.reply_to(message, "Invalid link, send link to profile")
		else:
			name = re.findall(r'(?:.om|.am)/[A-Za-z0-9-_\.]+', message.text)[0][4:]
			data = (date, url, name, whose, place)
			table.add(data)
			bot.reply_to(message, "Done!")
		
	except BaseException as ex:
		if 'UNIQUE constraint failed: instas.name' in str(ex):
			bot.reply_to(message, f"Nickname: {first_path} already added")
		else:
			bot.reply_to(message, "Invalid link, send a new one")
	

@bot.message_handler(func=lambda message: True)
def menu(message):
	#print(message.text)
	if message.chat.type == 'private':
		if message.text == "Tournament":
			bot.reply_to(message, "There is no tournament")
			#bot.send_message(message.chat.id, row)
		
		elif message.text == "Vote":
			bot.reply_to(message, "There is no vote")

		elif message.text == "Add url":
			bot.reply_to(message, "Just send a link")
bot.polling(none_stop=True)