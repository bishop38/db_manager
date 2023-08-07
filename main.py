# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sqlite3
from pathlib import Path

DB_PATH = Path("db.sqlite3")
IS_NEW = not DB_PATH.is_file()
DB_PATH.touch(exist_ok=True)


def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        username STRING PRIMARY KEY,
        fname TEXT,
        lname TEXT,
        gender TEXT);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects(
        id INT PRIMARY KEY,
        name TEXT);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
        id INT PRIMARY KEY,
        user_id INT,
        project_id INT,
        name TEXT,
        type TEXT,
        description TEXT);
    """)


def create_projects(cursor, name):
    cursor.execute(f"""
        INSERT INTO projects( name) 
        VALUES({name});
    """)


def create_users(cursor, connect):
    username = input('Введите username: ')
    fname = input('Введите имя: ')
    lname = input('Введите фамилию: ')
    gender = input('Введите пол: ')
    cursor.execute(f"""
        INSERT INTO users(username, fname, lname, gender) 
        VALUES(?, ?, ?, ?);
    """, (username, fname, lname, gender))
    connect.commit()


def delete_users(cursor, connect):
    username = input('Введите username: ')
    cursor.execute(f"DELETE FROM users WHERE username = '{username}';")
    connect.commit()
    select_users(cursor, connect)


def update_users(cursor, connect):
    field_to_change = input('Введите поле для изменения: ')
    change_from = input('Введите старое значение: ')
    change_to = input('Введите новое значение: ')
    cursor.execute(f"""
            UPDATE users
            SET '{field_to_change}' = '{change_to}'
                'gender'='[[[['
            WHERE '{field_to_change}' = '{change_from}';
        """)
    connect.commit()
    select_users(cursor, connect)


def select_users(cursor, connect):
    cursor.execute(f"""
        SELECT * FROM users; 
    """)
    print(cursor.fetchall())


def filter_users(cursor, connect):
    fname = input('Введите имя: ')
    # lname = input('Введите фамилию: ')
    cursor.execute(f"""
        SELECT * FROM users WHERE fname='{fname}'
    """)


def create_tasks(cursor, name):
    cursor.execute(f"""
        INSERT INTO projects(name) 
        VALUES({name});
    """)


def main():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    if IS_NEW:
        create_tables(cur)
        conn.commit()

    user_actions = {
        'user': {
            'create': create_users,
            'update': update_users,
            'delete': delete_users,
            'select': select_users,
            'filter': filter_users,
        },
        'project': {

        },
        'task': {

        }
    }
    while True:
        table_input = input("Выберите таблицу(user, project, task): ")
        table_action_input = input("Выберите операцию(create, delete, update, select(все записи), filter): ")
        action = user_actions.get(table_input).get(table_action_input)
        action(cur, conn)


if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
