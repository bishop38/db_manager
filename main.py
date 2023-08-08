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
        username INT,
        project_id INT,
        name TEXT,
        type TEXT,
        description TEXT);
    """)

class SqlRequests:
    table_name = None
    columns = []
    cursor = None
    connect = None

    def __init__(self, table_name, columns, connect, cursor):
        self.table_name = table_name
        self.columns = columns
        self.connect = connect
        self.cursor = cursor

    def create_record(self):
        values = [input(f'Введите значение для {key}: ') for key in self.columns]
        self.cursor.execute(f"""
            INSERT INTO {self.table_name} ({','.join(self.columns)}) 
            VALUES({", ".join(['?' for i in values])});
        """, values)
        self.connect.commit()
        self.select_record()

    def delete_record(self):
        username = input('Введите username: ')
        self.cursor.execute(f"DELETE FROM users WHERE username = '{username}';")
        self.connect.commit()
        self.select_record()

    def update_record(self):
        identifier_field = input(f'Введите поле идентификатор ({self.columns}): ')
        identifier_value = input('Введите текущее значение идентификатора: ')
        values = {}
        print('Доступные поля: ', ', '.join(self.columns))
        while True:
            field = input('Введите поле для изменения(пустое поле, если хотите сохранить изменения): ')
            if not field:
                break
            value = input('Введите значение: ')
            values[field] = value

        self.cursor.execute(f"""
                UPDATE {self.table_name}
                SET {', '.join([key + '=' + f"'{value}'" for key, value in values.items()])}
                WHERE {identifier_field} = '{identifier_value}';
            """)
        self.connect.commit()
        self.select_record()

    def select_record(self):
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name}; 
        """)
        print(self.cursor.fetchall())

    def filter_record(self):
        values = {}
        print('Доступные поля: ', ', '.join(self.columns))
        while True:
            field = input('Введите поле для фильтрации(пустое поле - получение результатов): ')
            if not field:
                break
            value = input('Введите значение: ')
            values[field] = value
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name} 
            WHERE {', '.join([key + '=' + f"'{value}'" for key, value in values.items()])}
        """)
        print(self.cursor.fetchall())


def main():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    if IS_NEW:
        create_tables(cur)
        conn.commit()

    user_request = SqlRequests('users', ['username', 'fname', 'lname', 'gender'], conn, cur)
    project_request = SqlRequests('projects', ['id', 'name'], conn, cur)
    task_request = SqlRequests('tasks', ['id', 'username', 'project_id', 'name', 'type', 'description'], conn, cur)

    user_actions = {
        'user': {
            'create': user_request.create_record,
            'update': user_request.update_record,
            'delete': user_request.delete_record,
            'select': user_request.select_record,
            'filter': user_request.filter_record,
        },
        'project': {
            'create': project_request.create_record,
            'update': project_request.update_record,
            'delete': project_request.delete_record,
            'select': project_request.select_record,
            'filter': project_request.filter_record,
        },
        'task': {
            'create': task_request.create_record,
            'update': task_request.update_record,
            'delete': task_request.delete_record,
            'select': task_request.select_record,
            'filter': task_request.filter_record,
        }
    }
    while True:
        table_input = input("Выберите таблицу(user, project, task): ")
        table_action_input = input("Выберите операцию(create, delete, update, select(все записи), filter): ")
        action = user_actions.get(table_input).get(table_action_input)
        action()


if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
