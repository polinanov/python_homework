import json
import unittest


class ColorizeMixin:
    def __call__(self, color_repr, color_err):
        self.repr_color_code = color_repr
        self.repr_color_code_error = color_err

class Advert(ColorizeMixin, dict):
    def __init__(self, dictionary):
        check = False
        if not check:
            ColorizeMixin.__call__(self, 35, 31)
            if 'price' in dictionary:
                if dictionary["price"] <= 0:
                    print(f'\n\033[{self.repr_color_code_error}mValueError: must be >= 0')
                    exit()
            else:
                self.price = 0
        super(Advert, self).__init__(dictionary, check=True)

    def __repr__(self):
        return f'\n\033[{self.repr_color_code}mНазвание: {self.title} | Цена: {self.price} ₽\n \033[37m'

    def __getattr__(self, dictionary):
        return self[dictionary] if not isinstance(self[dictionary], dict) \
            else Advert(self[dictionary])

class TestAdvert(unittest.TestCase):
    def test_init_(self):
        advert_test = Advert({"title": "Вельш-корги", "price": 1000})
        self.assertEqual(advert_test.title, "Вельш-корги")

    def test_init_type_error(self):
        with self.assertRaises(ValueError):
            assert 'dictionary update sequence element #0 has length 1; 2 is required' == Advert("Привет")

    def test_isubclass(self):
        assert issubclass(Advert, ColorizeMixin)

    def test_init_price_negative(self):
        with self.assertRaises(SystemExit):
            assert Advert({"title": "Вельш-корги", "price": -1000})

    def test_init_price_not_exist(self):
        advert_test = Advert({"title": "Вельш-корги"})
        assert advert_test.price == 0


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

    advert = Advert(data_dict)
    print(advert)
    print(f'Название: {advert.title}')
    print(f'Цена: {advert.price}')
    print(f'Адрес: {advert.location.address}')
    advert.repr_color_code = 32
    print(advert)

    data_dict = json.loads(lesson_str)
    advertv = Advert(data_dict)
    advertv.repr_color_code = 33
    print(advertv)
