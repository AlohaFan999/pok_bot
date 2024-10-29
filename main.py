import telebot
from config import token
from random import randint

from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["aba"])
def aba(message):
    bot.send_message(
        message.chat.id, "Добрый день! 23 ноября в клубе состоятся соревнования"
    )
    bot.send_message(
        message.chat.id,
        "Доброе утро! Участники соревнований в Динамо, по возможности отправьте видео заплыва",
    )
    bot.send_message(message.chat.id, "Старшая группа сегодня к 18:30")
    bot.send_message(
        message.chat.id,
        "Добрый вечер! Тренировка у старшей группы отменяется, младшие будут готовиться к соревнованиям 23.11.2024",
    )


@bot.message_handler(commands=["go"])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        x = randint(1, 3)
        if x == 1:
            pokemon = Pokemon(message.from_user.username)
            bot.send_message(message.chat.id, "Вам выпал обычный покемон")

        elif x == 2:
            pokemon = Wizard(message.from_user.username)
            bot.send_message(message.chat.id, "Вам выпал покемон-волшебник")

        else:
            pokemon = Fighter(message.from_user.username)
            bot.send_message(message.chat.id, "Вам выпал покемон-боец")

        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=["info"])
def cmd_info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        return bot.send_message(message.chat.id, pok.info())
    else:
        return bot.send_message(essage.chat.id, "у тебя еще нет покемона")


@bot.message_handler(commands=["attack"])
def cmd_attack(message: telebot.types.Message):
    if not message.reply_to_message:
        bot.send_message(message.chat.id, "А кого атакуешь?")
        return
    if message.from_user.username not in Pokemon.pokemons.keys():
        bot.send_message(message.chat.id, "Сначала создай себе покемона")
        return
    if message.reply_to_message.from_user.username not in Pokemon.pokemons.keys():
        bot.send_message(message.chat.id, "У твоего противника нет покемона")
        return
    pok = Pokemon.pokemons.get(message.from_user.username)
    enemy_pok = Pokemon.pokemons.get(message.reply_to_message.from_user.username)
    bot.send_message(message.chat.id, pok.attack(enemy_pok))


@bot.message_handler(commands=["feed"])
def cmd_feed(message: telebot.types.Message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        bot.send_message(message.chat.id, "Сначала создай себе покемона")
        return
    pok: Pokemon = Pokemon.pokemons.get(message.from_user.username)
    if pok.hp >= pok.max_hp:
        bot.send_message(message.chat.id, "У вас и так много здоровья")
        return
    bot.send_message(message.chat.id, pok.feed())


bot.infinity_polling(none_stop=True)
