import json
import unittest


class ColorizeMixin:
    repr_color_code = 35

    def __repr__(self):
        text = super().__repr__()
        return f'\n\033[{self.repr_color_code}m{text}\n\033[37m'


class Advert(dict):
    def __init__(self, dictionary):
        super(Advert, self).__init__(dictionary)

    def __repr__(self):
        return f'Название: {self.title} | Цена: {self.price} ₽'

    def __getattr__(self, dictionary):
        return self[dictionary] if not isinstance(self[dictionary], dict) \
            else Advert(self[dictionary])


class BaseAdvert(ColorizeMixin, Advert):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        if 'price' in dictionary:
            if dictionary["price"] <= 0:
                raise ValueError("must be >= 0")
        else:
            self.price = 0


class Test(unittest.TestCase):
    def test_init_enclosure_1(self):
        advert_test = Advert({"title": "Вельш-корги", "price": 1000})
        self.assertEqual(advert_test.title, "Вельш-корги")

    def test_init_enclosure_2(self):
        input_test = {"title": "Вельш-корги", "price": 1000,
                      "location": {"address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"}}
        advert_test = Advert(input_test)
        self.assertEqual(advert_test.location.address, "сельское поселение Ельдигинское, поселок санатория Тишково, 25")

    def test_price_value_error(self):
        with self.assertRaises(ValueError):
            assert 'must be >= 0' == BaseAdvert({"title": "Вельш-корги", "price": -1000})

    def test_init_price_not_exist(self):
        advert_test = BaseAdvert({"title": "Вельш-корги"})
        assert advert_test.price == 0

    def test_include_in(self):
        advert_test = BaseAdvert({"title": "Вельш-корги"})
        self.assertIn('price', advert_test.__dict__)


if __name__ == '__main__':
    data_json = """
    {
      "title": "Вельш-корги",
      "price": 1000,
      "class": "dogs",
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }
    """
    lesson_str = """{
    "title": "iPhone",
    "price": 100,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
    }"""

    data_dict = json.loads(data_json)

    advert = BaseAdvert(data_dict)
    print(advert)
    print(f'Название: {advert.title}')
    print(f'Цена: {advert.price}')
    print(f'Адрес: {advert.location.address}')
    print(advert)

    data_dict = json.loads(lesson_str)
    advertv = BaseAdvert(data_dict)
    print(advertv)
