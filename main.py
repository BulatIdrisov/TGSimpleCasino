import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

import db as db
import keyboards as kb
import casino

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
ADMIN_ID = os.getenv('ADMIN_ID')
admins = [ADMIN_ID]
async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')

class NewOrder(StatesGroup):
    message = State()
    replenish_ID = State()
    replenish_balance = State()
    game = State()

@dp.message_handler(text='Сообщение админу')
async def message(message: types.Message):
    await NewOrder.message.set()
    await message.answer("Напишите сообщение",reply_markup=kb.cancel)

@dp.message_handler(state=NewOrder.message)
async def message_op(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer("Отмена!", reply_markup=kb.main)
        await state.finish()
    else:
        await state.finish()
        await message.answer("Сообщение успешно отправлено!", reply_markup=kb.main)
        await bot.send_message(ADMIN_ID, f'Новое сообщение! {message.text}')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await db.cmd_start_db(message.from_user.id, message.from_user.first_name)
        await message.answer(f'{message.from_user.first_name}, Добро пожаловать в казинак!\n(Если при нажатии на кнопку ставки ничего не происходит, то введите команду /start)', reply_markup=kb.main_admin)
    else:
        await db.cmd_start_db(message.from_user.id, message.from_user.first_name)
        await message.answer(f'{message.from_user.first_name}, Добро пожаловать в казинак!\n(Если при нажатии на кнопку ставки ничего не происходит, то введите команду /start)',reply_markup=kb.main)

@dp.message_handler(text='Пополнение')
async def replenish2(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
            await NewOrder.replenish_ID.set()
            await message.answer("Введите ID", reply_markup=kb.main_admin)
    else:
        await message.answer("У Вас нет прав для этой команды.", reply_markup=kb.main_admin)


@dp.message_handler(state = NewOrder.replenish_ID)
async def replenish_id(message: types.Message,state: FSMContext):
    if message.text == 'Отмена':
        await message.answer("Отмена!", reply_markup=kb.main_admin)
        await state.finish()
    else:
        await state.update_data(id=message.text)
        await NewOrder.replenish_balance.set()
        await message.answer("Введите сумму")

@dp.message_handler(state=NewOrder.replenish_balance)
async def replenish_balance(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer("Отмена!", reply_markup=kb.main_admin)
        await state.finish()
    else:
        user_data = await state.get_data()
        user_id = user_data['id']
        balance_sum = message.text
        db.replenish(user_id, balance_sum)
        await message.answer(f"Успешное пополнение баланса пользователя: {user_id} на {balance_sum}", reply_markup=kb.main_admin)
        await bot.send_message(user_id, f"Ваш баланс успешно пополнен на {balance_sum}")
        await state.finish()


@dp.message_handler(text='Играть')
async def game(message: types.Message):
    await NewOrder.game.set()
    await message.answer(f'Выберите ставку или введите свою! \nВаш баланс: {db.balance(message.from_user.id)}', reply_markup=kb.game)

@dp.message_handler(state=NewOrder.game)
async def bet(message: types.Message, state: FSMContext):
    if message.text == 'Выйти':
        await message.answer("Выход в главное меню!", reply_markup=kb.main)
        await state.finish()
    else:
        try:
            user_bet = int(message.text)
            result = casino.bet(user_bet)
            sum = result[0]
            slots = result[1]
            if db.balance(message.from_user.id)-user_bet>=0:
                if sum>0:
                    await db.update_balance(message.from_user.id, sum)
                    await message.answer("Аппарат показал: " + slots + "\nВы выиграли: " + str(sum), reply_markup=kb.game)
                    await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")


                else:
                    await db.update_balance(message.from_user.id, sum)
                    await message.answer("Аппарат показал: " + slots + "\nВы проиграли: "+str(sum*(-1)),reply_markup=kb.game)
                    await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")
            else:
                await message.answer("Недостаточно денег на балансе: " + str(db.balance(message.from_user.id)))
        except ValueError:
            await message.answer("Пожалуйста, введите целое число.")

@dp.message_handler(text='Рейтинг')
async def rating(message: types.Message):
    await message.answer(db.rating(), reply_markup=kb.main)

@dp.message_handler(commands='replenish')
async def replenish(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        args = message.text.split()
        id = args[1]
        sum = args[2]
        db.replenish(id, sum)
        await message.answer("Успешное пополнение баланса пользователя: "+str(id)+" на: "+str(sum),reply_markup=kb.main)
        await bot.send_message(args[1], "Ваш баланс успешно пополнен на: "+str(sum))
    else:
        await message.answer("У вас недостаточно прав для выполнения данной команды")


@dp.message_handler(commands='list')
async def list(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer(db.list())
    else:
        await message.answer("У вас недостаточно прав для выполнения данной команды",reply_markup=kb.main)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

