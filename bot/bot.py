import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import baza 
import random
 
bot = telebot.TeleBot("7407665532:AAF1Ipaa0YO9TtKZDoIIatcEfGDL9jdr53o")
@bot.message_handler(commands=["start"])
def start(msg):
    Keyboard = InlineKeyboardMarkup()
    Keyboard.add(InlineKeyboardButton("help",callback_data="help"))
    bot.send_message(msg.chat.id,"hi,i cool bot list of movies",reply_markup=Keyboard)
@bot.message_handler(commands=["help"])
def help(msg):
    Keyboard = InlineKeyboardMarkup()
    Keyboard.add(InlineKeyboardButton("movie",callback_data="movie"))
    bot.send_message(msg.chat.id,"u can",reply_markup=Keyboard)

@bot.message_handler(commands=["movie"])
def movie(msg):
    Keyboard = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(movie,callback_data=F"movie:{movie}")for movie in baza.films]
    Keyboard.add(*buttons)
    bot.send_message(msg.chat.id,"what do u gonna?,ja razreshaju",reply_markup=Keyboard)
@bot.callback_query_handler(func=lambda call: True)
def otwtnabaton(call):
    if call.data == "help":
            Keyboard = InlineKeyboardMarkup()
            Keyboard.add(InlineKeyboardButton("movie",callback_data="movie"))
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id,"u can",reply_markup=Keyboard)
    elif call.data == "movie":
            Keyboard = InlineKeyboardMarkup()
            buttons = [InlineKeyboardButton(movie,callback_data=F"movie:{movie}")for movie in baza.films]
            Keyboard.add(*buttons)
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id,"shoose a movei",reply_markup=Keyboard)
    else:
        title = call.data.replace("movie:","")
        if title in baza.films:
            info = baza.films[title]
            foto = info.get("foto","")
            text = f"{title}({info["year"]})\nregiser:{info["regiser"]}\njanr:{info["janr"]}"
            if foto:
                bot.send_photo(call.message.chat.id,foto,caption=text)
            else:
               bot.send_message(call.message.chat.id,text)
        else:
            bot.send_message(call.message.chat.id,"filma netu(hotheh kupit u menja?---da---da---)")
        # message.texs  
@bot.message_handler(commands=["addmovie"])
def add_movie(message):
    bot.reply_to(message,"enter name of movie:")
    bot.register_next_step_handler(message, add_movie_director)
def add_movie_director(message):
    user_data = {}
    user_data["name"] = message.text 
    bot.reply_to(message,F"enter regiser of movie")
    bot.register_next_step_handler(message, add_movie_year, user_data)

def add_movie_year(message,user_data):
    user_data["regiser"] = message.text 
    bot.reply_to(message,F"enter year of movie")
    bot.register_next_step_handler(message, add_movie_genre, user_data)  

def add_movie_genre(message,user_data):
    user_data["year"] = message.text 
    bot.reply_to(message,F"enter genre of movie")
    bot.register_next_step_handler(message, add_movie_foto, user_data) 

def add_movie_foto(message,user_data):
    user_data["genre"] = message.text 
    bot.reply_to(message,F"enter foto of movie")
    bot.register_next_step_handler(message, save_movie, user_data) 

def save_movie(message,user_data):
    baza.films[user_data["name"]] = {
        "regiser":user_data["regiser"],
        "year":user_data["year"],
        "janr":user_data["genre"],
        "foto":message.text
    }
    bot.reply_to(message,"film added")
@bot.message_handler(commands=["random_movie"])
def random_movie(message):
    random_movie = random.choice(list(baza.films.keys()))
    info = baza.films[random_movie]
    photo = info.get("foto","")
    text = f"{random_movie}({info["year"]})\nregiser:{info["regiser"]}\njanr:{info["janr"]}"
    if photo: 
        bot.send_photo(message.chat.id,photo,caption=text)
    else:
        bot.send_message(message.chat.id,text)






















bot.polling()
