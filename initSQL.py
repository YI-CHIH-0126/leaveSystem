import sqlite3
def setUpSQL():
    connection = sqlite3.connect("employees.db") #連接資料庫
    cursor = connection.cursor() #創建游標對象，使我們能控制資料庫對象
    #員工列表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        key INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        idNumber TEXT NOT NULL,
        department TEXT NOT NULL
    )
    ''')
    #請假列表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave (
        key INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        proof BLOB,
        agent TEXT NOT NULL,
        verify INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()