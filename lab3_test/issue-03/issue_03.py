from typing import List, Tuple
import unittest


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


class TestFitTransform(unittest.TestCase):
    def test_str_fit_transformr(self):
        self.assertEqual(fit_transform(['Moscow', 'New York', 'Moscow', 'London']), [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ])

    def test_int_fit_transformr(self):
        self.assertEqual(fit_transform([1, 2, 1, 3]), [
            (1, [0, 0, 1]),
            (2, [0, 1, 0]),
            (1, [0, 0, 1]),
            (3, [1, 0, 0]),
        ])

    def test_error_fit_transformr(self):
        with self.assertRaises(TypeError):
            fit_transform(1)

    def test_not_include_in_fit_transformr(self):
        self.assertNotIn(('1', [0, 0, 1]), fit_transform([1, 2, 1, 3]))

    def test_include_in_fit_transformr(self):
        self.assertIn((1, [0, 0, 1]), fit_transform([1, 2, 1, 3]))


if __name__ == '__main__':
    unittest.main()
