from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Играть','Рейтинг','Сообщение админу')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Играть','Рейтинг','Сообщение админу','Пополнение')

game = ReplyKeyboardMarkup(resize_keyboard=True)
game.add('10','100','1000','Выйти')

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')
