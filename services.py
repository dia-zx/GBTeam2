# GBTeam2
# Групповая работа по созданию игры "крестики - нолики" с использованием telegram - bot

import controller

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

def Init():
    application = ApplicationBuilder().token('5665588710:AAF41tF61xNX7XKc-vmkvwfKswBbeGW62sw').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    # application.add_handler(inline_caps_handler)
        
    application.run_polling()


#/start
#/help - выводит список и описание команд
#/move 0 1          x[0..2] y[0..2]
#/draw - отрисовка доски


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    controller.newgame(user_id)
    await context.bot.send_message(chat_id=update.effective_user.id, text = controller.get_board(user_id), parse_mode= "html")    

async def move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not controller.move(user_id, user_input):
        await context.bot.send_message(chat_id=update.effective_user.id, text = "Неверно....", parse_mode= "html")
        return
    
    await context.bot.send_message(chat_id=update.effective_user.id, text = controller.get_board(user_id), parse_mode= "html")    
    
    if controller.check_win(user_id):
        await context.bot.send_message(chat_id=update.effective_user.id, text = "Поздравляю Вы выиграли....", parse_mode= "html")
        controller.delete_game(user_id)
        return
    
    if controller.check_nomovs(user_id):
        await context.bot.send_message(chat_id=update.effective_user.id, text = "Ничья ....", parse_mode= "html")
        controller.delete_game(user_id)
        return        
    
    controller.computer_move()
    #.....
    
async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=update.effective_user.id, text = controller.get_board(user_id), parse_mode= "html")
  #Ваш ход 0(Х)




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



