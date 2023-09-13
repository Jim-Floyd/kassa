import sqlite3 as sq



base = sq.connect('kassa.db')
cur = base.cursor()

async def sql_add_income_type_command(state):
    
    data = await state.get_data()
    
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS income_types(name TEXT PRIMARY KEY)')
    base.commit()
    cur.execute('INSERT INTO income_types VALUES (?)', tuple(data.values()))
    base.commit()




async def sql_add_income_command(state):
    data = await state.get_data()
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS income(type TEXT PRIMARY KEY, amount INTEGER, date TEXT)')
    base.commit()
    cur.execute('INSERT INTO income VALUES (?,?,?)', tuple(data.values()))
    base.commit()


async def type_read(message):
    list_of_tuples = cur.execute('SELECT name FROM income_types').fetchall()
    list_of_str = []
    for tuple in list_of_tuples:
        str_tuple = str(tuple[0])
        list_of_str.append(str_tuple)
    return list_of_str
    