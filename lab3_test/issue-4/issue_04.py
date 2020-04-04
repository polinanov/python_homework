from typing import List, Tuple
import pytest


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


def test_str_fit_transformr():
    assert fit_transform(['Moscow', 'New York', 'Moscow', 'London']) == [
        ('Moscow', [0, 0, 1]),
        ('New York', [0, 1, 0]),
        ('Moscow', [0, 0, 1]),
        ('London', [1, 0, 0]),
    ]


def test_int_fit_str_transformr():
    assert fit_transform([1, 2, 1, 3]) == [
        (1, [0, 0, 1]),
        (2, [0, 1, 0]),
        (1, [0, 0, 1]),
        (3, [1, 0, 0]),
    ]


# чтобы проверить, что код вызывает исключение, нужно использовать менеджер контекста pytest.raises
def test_error_type_fit_transformr():
    with pytest.raises(TypeError):
        fit_transform(1)


@pytest.fixture()
def randomize():
    from random import randint
    return [randint(0, 9) for _ in range(randint(0, 10))]


def test_intv2_fit_transformr(randomize):
    print(randomize)
    fit_transform(randomize)
