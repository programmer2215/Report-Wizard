import sqlite3 as sql


def connect(func, *args, **kwargs):

    conn = sql.connect("Data.db")
    cur = conn.cursor()
    data = func(cur, *args, **kwargs)
    conn.commit()
    conn.close()
    return data

def valid_date(cur, date: str, db_table: str) -> bool:
    SQL = f"SELECT * FROM {db_table} WHERE DATE = \"{date}\";"
    for i in cur.execute(SQL):
        if i[0] == date:
            return False
    return True

def add_capital(cur, date: str, capital: str, override=False) -> bool:
    if not connect(valid_date, date, 'Capital'): return False
    SQL = f"INSERT INTO Capital VALUES (\"{date}\", {int(capital)});" 
    cur.execute(SQL)
    return True

def add_profit(cur, date: str, profit: str, override=False) -> bool:
    if not connect(valid_date, date, 'DailyProfit'): return False
    SQL = f"INSERT INTO DailyProfit VALUES (\"{date}\", {int(profit)});" 
    cur.execute(SQL)
    return True

