import sqlite3 as sq



base = sq.connect('kassa.db')
cur = base.cursor()

async def sql_add_income_type_command(state):
    
    data = await state.get_data()
    
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS income_types(type_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, user_id INTEGER)')
    base.commit()
    cur.execute('INSERT INTO income_types (name, user_id) VALUES (?,?)', tuple(data.values()))
    base.commit()


async def sql_add_cost_type_command(state):
    
    data = await state.get_data()
    
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS cost_types(type_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, user_id INTEGER)')
    base.commit()
    cur.execute('INSERT INTO cost_types (name, user_id) VALUES (?,?)', tuple(data.values()))
    base.commit()



async def sql_add_transaction_command(state):
    data = await state.get_data()
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS transactions(transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, income_type TEXT, income_amount INTEGER, date TEXT, cost_type TEXT, cost_amount INTEGER, user_id INTEGER)')
    base.commit()
    cur.execute('INSERT INTO transactions (income_type, income_amount, date, cost_type, cost_amount, user_id) VALUES (?,?,?,?,?,?)', tuple(data.values()))
    base.commit()


async def income_types(message):
    list_of_tuples = cur.execute('SELECT name FROM income_types').fetchall()
    list_of_str = []
    for tup in list_of_tuples:
        str_tuple = str(tup[0])
        list_of_str.append(str_tuple)
    return list_of_str


async def cost_types(message):
    list_of_tuples = cur.execute('SELECT name FROM cost_types').fetchall()
    list_of_str = []
    for tup in list_of_tuples:
        str_tuple = str(tup[0])
        list_of_str.append(str_tuple)
    return list_of_str


async def all_transactions(message):
    transactions_tuples = cur.execute('SELECT income_type, income_amount, date, cost_type, cost_amount, user_id FROM transactions').fetchall()
    list_of_list = []
    print(list_of_list)
    for tup in transactions_tuples:
        print(tup)
        list_tuple = list(tup)
        print(list_tuple)
        list_of_list.append(list_tuple)
    return list_of_list


async def all_years(message):
    transactions_tuples = cur.execute('SELECT income_type, income_amount, date, cost_type, cost_amount, user_id FROM transactions').fetchall()
    list_of_list = []
    print(list_of_list)
    for tup in transactions_tuples:
        print(tup)
        list_tuple = list(tup)
        print(list_tuple)
        list_of_list.append(list_tuple)
    return list_of_list