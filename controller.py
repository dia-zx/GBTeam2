# GBTeam2
# Групповая работа по созданию игры "крестики - нолики" с использованием telegram - bot
# связывающий модуль, обеспечивающий функционирование
import model
import services

def start():
    services.Init()
    
#Ход пользователя. True - корректный ход
def human_move(user_id, user_input : str ) -> bool:
    None
    
#Ход компьютера
def computer_move():
    None

def GetBoard(user_id):
    None

#проверка на выигрышную ситуацию     
def check_win(user_id) -> bool:
    None

def check_nomovs(user_id) -> bool:
    None

#удаляем игру... из словаря
def delete_game(user_id):
    None

#ПАриглашение ходить ("Вы 0(X). Ваш ход.")    
def your_move(user_id) -> str:
    None
    