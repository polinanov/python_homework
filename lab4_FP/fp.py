from collections import defaultdict
from itertools import islice
from typing import Iterable
import pytest

def ilenv(iterable: Iterable):
    # return len(list(iterable)))
    return sum(1 for _ in iterable)

def flatten(iterable: Iterable):
    for i in list(iterable):
        if isinstance(i, Iterable):
            yield from flatten(i)
        else:
            yield i

def distinct(iterable: Iterable):
    return list(dict.fromkeys(list(iterable)))

def groupbykey(key, iterable: Iterable):
    result = defaultdict(list)
    for plist in iterable:
        value = plist[key]
        # print('Value: ', value, ':: Partlist: ', plist)
        result[value].append(plist)
    return dict(result)

def chunks(size, iterable: Iterable):
    result = []
    while True:
        if len(list(iterable)) <= size:
            result.append(list(iterable))
            return result
        else:
            result.append(list(iterable)[:size])
            iterable = list(iterable)[size:]

def first(iterable: Iterable, default_=None):
    return next(islice(iterable, 1), default_)

def last(iterable: Iterable, default_=None):
    try:
        return list(iterable)[-1]
    except IndexError:
        return default_

def test_ilenv():
    assert ilenv(x for x in range(10)) == 10

def test_flatten():
    assert list(flatten([0, [1, [2, 3]]])) == [0, 1, 2, 3]

def test_distinct():
    assert list(distinct([1, 1, 2, 0, 1, 3, 0, 2])) == [1, 2, 0, 3]

def test_groupbykey():
    assert groupbykey("gender", [
        {'gender': 'female', 'age': 33},
        {'gender': 'male', 'age': 20},
        {'gender': 'female', 'age': 21},
    ]) == dict(female=[{'age': 33, 'gender': 'female'}, {'age': 21, 'gender': 'female'}],
               male=[{'age': 20, 'gender': 'male'}])

def test_chunks():
    assert chunks(3, [0, 1, 2, 3, 4]) == [[0, 1, 2], [3, 4]]

@pytest.mark.parametrize('test_input,expected', [((x for x in range(3, 10)), 3), (range(0), None)])
def test_first(test_input, expected):
    assert first(test_input) == expected

@pytest.mark.parametrize('test_input,expected', [((x for x in range(5, 10)), 9), (range(0), None)])
def test_last(test_input, expected):
    assert last(test_input) == expected


if __name__ == '__main__':
    users = [
        {'gender': 'female', 'age': 33},
        {'gender': 'male', 'age': 20},
        {'gender': 'female', 'age': 21},
    ]
    foo = (x for x in range(10))
    print(f'Function {ilenv.__name__} :: {ilenv(foo)}')
    print(f'Function {flatten.__name__} :: {list(flatten([0, [1, [2, 3]]]))}')
    print(f'Function {distinct.__name__} :: {list(distinct([1, 1, 2, 0, 1, 3, 0, 2]))}')
    print(f'Function {groupbykey.__name__} :: {groupbykey("gender", users)}')
    print(f'Function {chunks.__name__} :: {chunks(3, [0, 1, 2, 3, 4,5,6,7,8])}')
    foo = (x for x in range(3, 10))
    print(f'Function {first.__name__} :: {first(foo)}')
    print(f'Function {first.__name__} :: {first(range(0))}')
    foo = (x for x in range(5, 10))
    print(f'Function {last.__name__} :: {last(foo)}')
    print(f'Function {last.__name__} :: {last(range(0))}')
