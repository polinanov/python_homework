from typing import List
from fields import BaseField


class Model:
    Meta = None

    def __init__(self, **fields):
        for field, value in fields.items():
            if field not in [model_field.name for model_field in self.fields()]:
                raise AttributeError(f'The field {field} is not declared')
            setattr(self, field, value)

    @classmethod
    def fields(cls) -> List[BaseField]:
        return [
            cls.__dict__[item] for item in cls.__dict__ if isinstance(cls.__dict__[item], BaseField)
        ]

    @classmethod
    def create(cls, **fields):
        conn = cls.Meta.database.conn
        model_name = cls.__name__
        model = cls(**fields)
        result_field = []
        result_value = []
        for model_field in model.fields():
            result_field.append(f"{model_field.name}")
            result_value.append(f'{model_field.get_value(model)}')
        sql_field = ', '.join(result_field)
        sql_value = ', '.join(result_value)
        conn.execute(f'INSERT INTO {model_name} ({sql_field}) VALUES ({sql_value})')
        conn.commit()

    @classmethod
    def select(cls):
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
