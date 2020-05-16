from fields import CharField, IntegerField
from model import Model
from sql import SqliteDatabase

db = SqliteDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = db


class Advert(BaseModel):
    title = CharField(max_length=180)
    price = IntegerField(min_value=0)


class Drink(BaseModel):
    title = CharField(max_length=180)
    price = IntegerField(min_value=0)
    capacity = IntegerField(min_value=0)


if __name__ == '__main__':
    db.connect()
    db.create_tables([Advert])
    Advert.create(title='iPhone X', price=100)
    Advert.create(title='iPod 2', price=1000)
    adverts = Advert.select()
    print(adverts)
    assert str(adverts[0]) == 'iPhone X | 100'
