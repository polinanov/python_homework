import urllib.request
import json
import unittest
from unittest.mock import patch
import io

API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
        Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год
        Предположим, что currentDateTime может быть в двух форматах:
          * YYYY-MM-DD - 2019-03-01
          * DD.MM.YYYY - 01.03.2019
    """
    resp_json = json.load(urllib.request.urlopen(API_URL))
    # print(resp_json)
    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')
    return int(year_str)


class TestYaer(unittest.TestCase):
    def test_what_is_year_now_v1(self):
        exp = '{"$id": "1", "currentDateTime": "2020-04-08T19:12Z", "utcOffset": "00:00:00"}'
        with patch.object(urllib.request, "urlopen", return_value=io.StringIO(exp)):
            assert what_is_year_now() == 2020

    def test_what_is_year_now_v2(self):
        exp = '{"$id": "1", "currentDateTime": "08.04.2020T23:52Z", "utcOffset": "00:00:00"}'
        with patch.object(urllib.request, "urlopen", return_value=io.StringIO(exp)):
            assert what_is_year_now() == 2020

    def test_what_is_year_now_err(self):
        exp = '{"$id": "1", "currentDateTime": "08-04-20", "utcOffset": "00:00:00"}'
        with patch.object(urllib.request, "urlopen", return_value=io.StringIO(exp)):
            with self.assertRaises(ValueError):
                assert what_is_year_now() == 'Invalid format'
