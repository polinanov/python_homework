import sqlite3


class SqliteDatabase:
    def __init__(self, database):
        self.model = ''
        self.conn = ''
        if database == ':memory:':
            self.database = database

    def connect(self):
        self.conn = sqlite3.connect(self.database)

    def create_table(self, model):
        self.model = model.__name__
        result_field = []
        for field in model.fields():
            result_field.append(f'{field.name} {field.field_type}')
        sql_result = ', '.join(result_field)
        self.conn.execute(f'CREATE TABLE {self.model} ({sql_result})')

    def create_tables(self, models):
        for model in models:
            self.create_table(model)
