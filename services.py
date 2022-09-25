# GBTeam2
# Групповая работа по созданию игры "крестики - нолики" с использованием telegram - bot

from tabnanny import check
from turtle import update
import controller

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

bot = Updater('5665588710:AAF41tF61xNX7XKc-vmkvwfKswBbeGW62sw')


def Init():
    app = ApplicationBuilder().token(
        '5665588710:AAF41tF61xNX7XKc-vmkvwfKswBbeGW62sw').build()

    start_handler = CommandHandler('start', start)
    move_handler = CommandHandler('move', move)
    draw_handler = CommandHandler('draw', draw)
    help_handler = CommandHandler('help', help)
    app.add_handler(move_handler)
    app.add_handler(draw_handler)
    app.add_handler(help_handler)
    app.add_handler(start_handler)

    # inline_caps_handler = InlineQueryHandler(inline_caps)
    # application.add_handler(inline_caps_handler)

    app.run_polling()


# /start
# /help - выводит список и описание команд
# /move 0 1          x[0..2] y[0..2]
# /draw - отрисовка доски


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    controller.newgame(user_id)
    await context.bot.send_message(chat_id=update.effective_user.id, text=controller.get_board(user_id), parse_mode="html")


async def move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = context[:-2]
    if not controller.move(user_id, user_input):
        await context.bot.send_message(chat_id=update.effective_user.id, text="Неверно! Поле занято или не существует. Чтобы продолжить введите '/move <номер строки> <номер столбца>'.\nНапример, /move 1 2", parse_mode="html")
        return

    await context.bot.send_message(chat_id=update.effective_user.id, text=controller.get_board(user_id), parse_mode="html")
    if not check(user_id, person=1):
        return

    controller.computer_move()
    if not check(user_id, person=2):
        return


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id, person):
    if controller.check_win(user_id):
        if person == 1:
            await context.bot.send_message(chat_id=update.effective_user.id, text="Поздравляю! Вы выиграли! Сыграем еще раз?\start", parse_mode="html")
        else:
            await context.bot.send_message(chat_id=update.effective_user.id, text="Вы проиграли. Сыграем еще раз?\start", parse_mode="html")
        controller.delete_game(user_id)
        return 0

    if controller.check_nomovs(user_id):
        await context.bot.send_message(chat_id=update.effective_user.id, text="Ничья! Сыграем еще раз?\start", parse_mode="html")
        controller.delete_game(user_id)
        return 0
    return 1


async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=update.effective_user.id, text=controller.get_board(user_id)+'\nВаш ход', parse_mode="html")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_user.id, text='<b>Правила игры</b>\nИгроки по очереди ставят на свободные клетки поля 3×3 знаки. Первый, выстроивший в ряд 3 своих фигуры по вертикали, горизонтали или диагонали, выигрывает. Первый ход делает игрок, ставящий крестики.\n /start - \n/move - сделать ход.\n/help - помощь\n<b>Формат ввода</b>: /move <номер строки> <номер столбца>.\nНапример, /move 1 2\n/draw - показать доску\n', parse_mode="html")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     await context.bot.answer_inline_query(update.inline_query.id, results)
