from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import db as db
import keyboards as kb
import casino

bot = Bot("7006410780:AAG8UqeylJFu-uZMH1sSd5DGtgtt8IGG4ZI")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
ADMIN_ID = '918759409'
admins = [ADMIN_ID]
async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')

class NewOrder(StatesGroup):
    message = State()
    replenish_ID = State()
    replenish_balance = State()

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
        await bot.send_message(ADMIN_ID, 'Новое сообщение!: '+message.text)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await db.cmd_start_db(message.from_user.id, message.from_user.first_name)
        await message.answer(f'{message.from_user.first_name}, Добро пожаловать в казинак!', reply_markup=kb.main_admin)
    else:
        await db.cmd_start_db(message.from_user.id, message.from_user.first_name)
        await message.answer(f'{message.from_user.first_name}, Добро пожаловать в казинак!',reply_markup=kb.main)

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
        await message.answer(f"Успешное пополнение баланса пользователя: {user_id} на: {balance_sum}", reply_markup=kb.main_admin)
        await bot.send_message(user_id, f"Ваш баланс успешно пополнен на: {balance_sum}")
        await state.finish()







@dp.message_handler(text='Играть')
async def game(message: types.Message):
    await message.answer(f'Выберите ставку\nВаш баланс: {db.balance(message.from_user.id)}', reply_markup=kb.game)

@dp.message_handler(text='10')
async def bet10(message: types.Message):

    a = casino.bet(10)
    sum = a[0]
    slots = a[1]
    if db.balance(message.from_user.id)-10>=0:
        if sum>0:
            await db.update_balance(message.from_user.id, sum)
            await message.answer("Аппарат показал: " + slots + "\nВы выиграли: " + str(sum), reply_markup=kb.game)
            await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")


        else:
            await db.update_balance(message.from_user.id, sum)
            await message.answer("Аппарат показал: " + slots + "\nВы проиграли: "+str(sum*(-1)),reply_markup=kb.game)
            await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")
    else:
        await message.answer("Недостаточно денег на балансе: "+str(db.balance(message.from_user.id)))

@dp.message_handler(text='100')
async def bet10(message: types.Message):

    a = casino.bet(100)
    sum = a[0]
    slots = a[1]
    if db.balance(message.from_user.id)-100>=0:
        if sum>0:
            await db.update_balance(message.from_user.id, sum)
            await message.answer("Аппарат показал: " + slots + "\nВы выиграли: " + str(sum), reply_markup=kb.game)
            await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")


        else:
            await db.update_balance(message.from_user.id, sum)
            await message.answer("Аппарат показал: " + slots + "\nВы проиграли: "+str(sum*(-1)),reply_markup=kb.game)
            await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")
    else:
        await message.answer("Недостаточно денег на балансе: "+str(db.balance(message.from_user.id)))

@dp.message_handler(text='1000')
async def bet10(message: types.Message):
    a = casino.bet(1000)
    sum = a[0]
    slots = a[1]
    if db.balance(message.from_user.id)-1000>=0:
        if sum>0:
            await db.update_balance(message.from_user.id, sum)
            await message.answer("Аппарат показал: " + slots + "\nВы выиграли: " + str(sum), reply_markup=kb.game)
            await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")


        else:
            await db.update_balance(message.from_user.id, sum)
            await message.answer("Аппарат показал: " + slots + "\nВы проиграли: "+str(sum*(-1)),reply_markup=kb.game)
            await message.answer(f"Ваш баланс: {db.balance(message.from_user.id)}")
    else:
        await message.answer("Недостаточно денег на балансе: "+str(db.balance(message.from_user.id)))

@dp.message_handler(text='Выйти')
async def game(message: types.Message):
    await message.answer(f'Выберите ставку\nВаш баланс: {db.balance(message.from_user.id)}', reply_markup=kb.main)

@dp.message_handler(text='Рейтинг')
async def rating(message: types.Message):
    await message.answer(db.rating(),reply_markup=kb.main)

@dp.message_handler(commands='replenish')
async def replenish(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        args = message.text.split()
        id = args[1]
        sum = args[2]
        db.replenish(id,sum)
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

