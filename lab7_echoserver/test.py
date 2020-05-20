import unittest


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