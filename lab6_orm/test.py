from fields import CharField, IntegerField
from model import Model
from sql import SqliteDatabase
import unittest

db = SqliteDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = db


class Advert(BaseModel):
    title = CharField(max_length=10)
    price = IntegerField(min_value=0)


def preparation():
    db.connect()
    db.create_tables([Advert])


class Test(unittest.TestCase):
    def test_select(self):
        preparation()
        Advert.create(title='iPhone X', price=100)
        Advert.create(title='iPod 2', price=1000)
        adverts = Advert.select()
        assert adverts[0] == 'iPhone X | 100'
        assert adverts[1] == 'iPod 2 | 1000'

    def test_fields_int(self):
        preparation()
        with self.assertRaises(ValueError):
            Advert.create(title='iPhone X', price='100p')

    def test_fields_string(self):
        preparation()
        with self.assertRaises(ValueError):
            Advert.create(title=100, price='100')

    def test_fields_int_not_in_range(self):
        preparation()
        with self.assertRaises(ValueError):
            Advert.create(title='iPhone X', price=-20)

    def test_fields_string_not_in_range(self):
        preparation()
        with self.assertRaises(ValueError):
            Advert.create(title='1000000000000000', price=100)

    def test_include(self):
        preparation()
        Advert.create(title='iPhone X', price=100)
        Advert.create(title='iPod 2', price=1000)
        adverts = Advert.select()
        self.assertIn('iPod 2 | 1000', adverts)
