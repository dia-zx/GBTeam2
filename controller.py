# GBTeam2
# Групповая работа по созданию игры "крестики - нолики" с использованием telegram - bot
# связывающий модуль, обеспечивающий функционирование

from encodings import utf_8
import model as model
import services


def start():
    """ получение токена Бота из файла и инициализация Telegram бота """
    bot = []
    with open("bot.txt", "r", encoding="utf_8") as f:
        while True:
            st = f.readline()
            _st = st.replace(" ", "")
            if len(_st) == 0 or _st[0] == "#":
                continue
            bot = st.split()
            break

    if len(bot) != 2:
        print("Неверный формат файла bot.txt.")
        print("Bot_user_name Bot_token")
        return
    services.Init(bot)


def newgame(user_id: int):
    """ Начало новой игры """
    model.newgame(user_id)


def move(user_id, user_input: list) -> str:
    """ обработка хода человеки и ответа компьютера с проверками на конец игры """
    if not model.check_human(user_id):
        return "Сначала нужно начать новую игру (/start)"
    if not model.human_move(user_id, user_input):
        return """<b>Неверное значение!</b>
        Поле занято или не существует. Чтобы продолжить введите '[номер столбца (0..2)] [номер строки (0..2)]'.
        Например, /move 1 2        
        """
    st = ""
    st = model.get_board(user_id)  # отрисовка поля после хода игрока
    (res_str, endgame) = _check_position(user_id, human=True)
    st += res_str
    if endgame:
        return st

    model.computer_move(user_id)
    st += "\n\nХод компьютера:\n"
    st += model.get_board(user_id)
    (res_str, endgame) = _check_position(user_id, human=False)
    return st + res_str


def _check_position(user_id: int, human: bool):
    """ Проверка достижения конца игры с выдачей соответствующего сообщения
    human == True последний ход - игрока человека
    human == False последний ход - компьютера
    """
    if model.check_win(user_id):  # проверка на выигрыш
        model.delete_game(user_id)
        if human:
            return ("\nПоздравляю! Вы выиграли! Сыграем еще раз? /start", True)
        else:
            return ("\nУвы..! Вы проиграли! Сыграем еще раз? /start", True)

    if model.check_nomovs(user_id):  # проверка на отсутствие свободных ходов
        model.delete_game(user_id)
        return ("\nНичья! Сыграем еще раз? /start", True)
    return ("", False)


def get_board(user_id) -> str:
    """ Формирование игровой доски для отрисовки"""
    return model.get_board(user_id)
