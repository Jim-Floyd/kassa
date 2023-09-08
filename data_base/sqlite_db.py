import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('kassa.db')
    cur = base.cursor()
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT PRIMARY KEY)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?)', tuple(data.values()))
        base.commit()