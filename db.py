import sqlite3 as sq

# Устанавливаем соединение с базой данных
db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    global db, cur
    cur.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER,
    first_name TEXT,
    balance INTEGER
    )
    ''')
    db.commit()

async def cmd_start_db(user_id,first_name):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id,balance,first_name) VALUES (?,?,?)", (user_id,10000,first_name))

        db.commit()

async def update_balance(user_id,sum):
    cur.execute('UPDATE accounts SET balance = balance + ? WHERE tg_id = ?', (sum, user_id))
    db.commit()
    print(user_id,sum)

def balance(user_id):
    cur.execute('SELECT balance FROM accounts WHERE tg_id = ?', (user_id,))
    balance_row = cur.fetchone()
    if balance_row:
        balance = balance_row[0]
        return balance

def replenish(user_id, sum):
    cur.execute('UPDATE accounts SET balance = balance + ? WHERE tg_id = ?', (sum, user_id))
    db.commit()

def list():
    cur.execute("SELECT * FROM accounts")
    a = cur.fetchall()
    return a

def rating():
    cur.execute("SELECT first_name, balance FROM accounts")
    data = cur.fetchmany(5)
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)

    result = ""
    for name, balance in sorted_data:
        result += f"{name} - {balance}\n"
    return result

# Сохраняем изменения
db.commit()
rating()
