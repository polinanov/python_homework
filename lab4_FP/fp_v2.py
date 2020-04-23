from collections import defaultdict
from itertools import islice
from typing import Iterable
import pytest


def ilen(iterable: Iterable):
    return sum(1 for _ in iterable)


def flatten(iterable: Iterable):
    for i in iterable:
        if isinstance(i, Iterable):
            yield from flatten(i)
        else:
            yield i


def distinct(iterable: Iterable):
    return dict.fromkeys(list(iterable))


def group_by(key, iterable: Iterable):
    result = defaultdict(list)
    for plist in iterable:
        value = plist[key]
        result[value].append(plist)
    return dict(result)


def chunks(size: int, iterable: Iterable):
    """
    The first version of the chunks function. Does not work correctly with Iterable
    """
    result = []
    while True:
        if ilen(iterable) <= size:
            result.append(list(iterable))
            return result
        else:
            result.append(list(iterable)[:size])
            iterable = list(iterable)[size:]


def chunks_v2(size: int, iterable: Iterable):
    piece = tuple(islice(iterable, size))
    while piece:
        yield piece
        piece = tuple(islice(iterable, size))


def first(iterable: Iterable, default_=None):
    return next(islice(iterable, 1), default_)


def last(iterable: Iterable, default_=None):
    try:
        return list(iterable)[-1]
    except IndexError:
        return default_


def test_ilen():
    assert ilen(x for x in range(10)) == 10


def test_flatten():
    assert list(flatten([0, [1, [2, 3]]])) == [0, 1, 2, 3]


def test_distinct():
    assert list(distinct([1, 1, 2, 0, 1, 3, 0, 2])) == [1, 2, 0, 3]


def test_group_by():
    input_test = [{'gender': 'female', 'age': 33},
                  {'gender': 'male', 'age': 20},
                  {'gender': 'female', 'age': 21}]
    expected = {'female': [{'age': 33, 'gender': 'female'}, {'age': 21, 'gender': 'female'}],
                'male': [{'age': 20, 'gender': 'male'}]}
    assert group_by("gender", input_test) == expected


def test_chunks():
    assert chunks(3, [0, 1, 2, 3, 4]) == [[0, 1, 2], [3, 4]]


@pytest.mark.parametrize('test_input,expected',
                         [((x for x in range(10)), [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]),
                          ([], [])])
def test_chunks_v2(test_input, expected):
    assert (list(chunks_v2(3, test_input))) == expected


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
    print(f'Function {ilen.__name__} :: {ilen(foo)}')
    print(f'Function {flatten.__name__} :: {list(flatten([0, [1, [2, 3]]]))}')
    print(f'Function {distinct.__name__} :: {list(distinct([1, 1, 2, 0, 1, 3, 0, 2]))}')
    print(f'Function {group_by.__name__} :: {group_by("gender", users)}')
    print(f'Function {chunks.__name__} :: {chunks(3, [0, 1, 2, 3, 4, 5, 6, 7, 8])}')
    print(f'Function {chunks_v2.__name__} :: {list(chunks_v2(3, (x for x in range(10))))}')
    foo = (x for x in range(3, 10))
    print(f'Function {first.__name__} :: {first(foo)}')
    print(f'Function {first.__name__} :: {first(range(0))}')
    foo = (x for x in range(5, 10))
    print(f'Function {last.__name__} :: {last(foo)}')
    print(f'Function {last.__name__} :: {last(range(0))}')
