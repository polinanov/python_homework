import sqlite3
from typing import List, Type


class BaseField:
    name = ""
    field_type = ""

    def __set_name__(self, owner, name_field):
        print("BaseField __set_name__")
        """
        Функция для установки имени поля. Например, "title", "price".
        """
        self.name = name_field
        #print("Set name:", name_field)

    def get_value(self, name_insert):
        print("BaseField get_value")
        """
        Функция для возвращения значений (например: "'Iphone X'", "100") для записи строк - INSERT.
        """
        if self.field_type == 'text':
            return f'\'{name_insert.__dict__[self.name]}\''
        return name_insert.__dict__[self.name]


class CharField(BaseField):
    field_type = "text"

    def __init__(self, max_length):
        print("CharField __init__")
        """
        Для CharField установка максимальной и мимнимальной длинны, проверка что пришедшие значения - int.
        """
        if not isinstance(max_length, int):
            raise TypeError(f'Value max_length  must be int')
        self.max_length = max_length
        self.min_length = 0

    def __set__(self, instance, value):
        print("CharField __set__")
        """
            Для CharField проверка при заполнении полей максимальной и мимнимальной длинны str и
            проверка что пришедшие значения - str.
        """
        if not isinstance(value, str):
            raise ValueError(f"Value {self.name} must be {self.field_type}")

        if self.max_length > len(value) > self.min_length:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f"Value {self.name} must be > {self.min_length} and < {self.max_length}")


class IntegerField(BaseField):
    field_type = "int"

    def __init__(self, min_value):
        print("IntegerField __init__")
        """
            Для IntegerField установка мимнимального размера, проверка что пришедшие значения - int.
        """
        if not isinstance(min_value, int):
            raise TypeError(f'Value min_value must be int')
        self.min_value = min_value

    def __set__(self, instance, value):
        print("IntegerField __set__")
        """
            Для IntegerField проверка при заполнении полей минимального значения int и
            проверка что пришедшие значения - int.
        """
        if not isinstance(value, int):
            raise ValueError(f"Value {self.name} must be {self.field_type}")

        if value > self.min_value:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f"Value {self.name} must be > {self.min_value}")


class Model:
    def __init__(self, **fields):
        print("Model __init__")
        """
            Для Model проверка (что поля действительно есть в обьявленных)
            и установка свойств класса(полей) значениями которые пришли из main
            (fields.items() = dict_items([('title', 'iPhone X'), ('price', 100)])) вызываетяся в create
        """
        for field, value in fields.items():
            if field not in [model_field.name for model_field in self.fields()]:
                raise AttributeError(f"The field {field} is not declared")
            setattr(self, field, value)

    @classmethod
    def fields(cls) -> List[BaseField]:
        print("Model fields")
        """
            Возвращает список объектов BaseField (на самом деле IntegerField, CharField),
             для того чтобы по ним итерироваться. Т.е. для
            {'__module__': '__main__', 'title': <__main__.CharField object at 0x012960E8>, 'price': <__main__.IntegerField object at 0x01296130>, '__doc__': None}
            [<__main__.CharField object at 0x012960E8>, <__main__.IntegerField object at 0x01296130>]
        """
        return [
            cls.__dict__[item] for item in cls.__dict__ if isinstance(cls.__dict__[item], BaseField)
        ]

    @classmethod
    def create(cls, **fields):
        print("Model create")
        """
            Заполнения класса Model - (model = cls(**fields)) = (Model.__init__)
            Подготовительные действия - получения названия всех полей и получение форматированных значений
            для Char, потому что не жрет без одинарных ковычек
        """
        conn = cls.Meta.database.conn
        model_name = cls.__name__
        model = cls(**fields)
        result_field = []
        result_value = []
        for model_field in model.fields():
            result_field.append(f"{model_field.name}")
            result_value.append(f"{model_field.get_value(model)}")
        sql_field = ", ".join(result_field)
        sql_value = ", ".join(result_value)
        conn.execute(f'INSERT INTO {model_name} ({sql_field}) VALUES ({sql_value})')
        conn.commit()

    @classmethod
    def select(cls):
        print("Model select")
        """
            Получение значений из БД и привод к нужому формату - str
            cursor.fetchall() - для извлечения строк из таблицы базы данных
            cursor - это специальный объект который делает запросы и получает их результаты
        """
        conn = cls.Meta.database.conn
        model_name = cls.__name__
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {model_name}')
        rows = cursor.fetchall()
        res_string = []
        result_model = []
        for row in rows:
            for string in row:
                res_string.append(str(string))
            result = " | ".join(res_string)
            res_string = []
            result_model.append(result)
        return result_model


class SqliteDatabase:
    def __init__(self, database):
        print("SqliteDatabase __init__")
        if database == ':memory:':
            self.database = database

    def connect(self):
        print("SqliteDatabase connect")
        self.conn = sqlite3.connect(self.database)

    def create_table(self, model: Type[Model]):
        print("SqliteDatabase create_table")
        self.model = model.__name__
        result_field = []
        for field in model.fields():
            result_field.append(f"{field.name} {field.field_type}")
        sql_result = ", ".join(result_field)
        self.conn.execute(f'CREATE TABLE {self.model} ({sql_result})')

    def create_tables(self, models: List[Model]):
        print("SqliteDatabase create_tables")
        for model in models:
            self.create_table(model)


db = SqliteDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = db


class Advert(BaseModel):
    title = CharField(max_length=180)
    price = IntegerField(min_value=0)

"""
class Drink(BaseModel):
    title = CharField(max_length=180)
    price = IntegerField(min_value=0)
    capacity = IntegerField(min_value=0)
"""

if __name__ == '__main__':
    db.connect()
    db.create_tables([Advert])
    #db.create_tables([Advert, Drink])
    Advert.create(title='iPhone X', price=100)
    Advert.create(title='iPod 2', price=1000)
    #Drink.create(title='Pepsi', price=200, capacity=1)
    adverts = Advert.select()
    #drinks = Drink.select()
    #print(drinks[0])
    print(adverts)
    assert str(adverts[0]) == 'iPhone X | 100'
