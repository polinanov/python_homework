import pytest
import lab1


@pytest.mark.parametrize('test_input,expected', [(7, 0.05), (10, 0.1), (11, 0.1), (13, 0.15), (14, 0.15), (15, 0.2),
                                                 (17, 0.2)])  # переходные границы 10 13 15 17
def test_calculation_bonus_level(test_input, expected):
    assert lab1.calculation_bonus_level(test_input) == expected


@pytest.mark.parametrize('test_input,expected', [(6, ValueError), (18, ValueError)])
def test_calculation_bonus_level_errorV(test_input, expected):
    assert lab1.calculation_bonus_level(test_input) == expected


@pytest.mark.parametrize('test_input,expected', [('string', TypeError), (None, TypeError)])
def test_calculation_bonus_level_errorT(test_input, expected):
    assert lab1.calculation_bonus_performance_review(test_input) == expected


@pytest.mark.parametrize('test_input,expected', [(1, 0), (2, 0.25), (2.3, 0.25), (2.5, 0.5), (2.6, 0.5), (3, 1),
                                                 (3.1, 1), (3.5, 1.5), (3.6, 1.5), (4, 2), (5, 2)])  # границы
def test_calculation_bonus_performance_review(test_input, expected):
    assert lab1.calculation_bonus_performance_review(test_input) == expected


@pytest.mark.parametrize('test_input,expected', [(0.9, ValueError), (5.1, ValueError)])
def test_calculation_bonus_performance_review_errorV(test_input, expected):
    assert lab1.calculation_bonus_performance_review(test_input) == expected


@pytest.mark.parametrize('test_input,expected', [('string', TypeError), (None, TypeError)])
def test_calculation_bonus_performance_review_errorT(test_input, expected):
    assert lab1.calculation_bonus_performance_review(test_input) == expected


@pytest.mark.parametrize('salary,bonus_level,bonus_performance_review,expected',
                         [(70000, 9, 1, 0), (700000, 17, 5, 840000),
                          (200000, 14, 2.9, 45000)])  # расширить значения входящие
def test_quarterly_bonus(salary, bonus_level, bonus_performance_review, expected):
    assert lab1.quarterly_bonus(salary, bonus_level, bonus_performance_review) == expected


@pytest.mark.parametrize('salary,bonus_level,bonus_performance_review,expected',
                         [(-70000, -9, -1, ValueError), (-700000, 17, -5, ValueError),
                          (200000, 14, -2.9, ValueError)])  # расширить значения входящие
def test_quarterly_bonus_error(salary, bonus_level, bonus_performance_review, expected):
    assert lab1.quarterly_bonus(salary, bonus_level, bonus_performance_review) == expected


@pytest.mark.parametrize('salary,bonus_level,bonus_performance_review,expected',
                         [(None, 'string', None, TypeError), ('srting', 'string', 'string', TypeError),
                          (None, None, None, TypeError)])  # расширить значения входящие
def test_quarterly_bonus_error(salary, bonus_level, bonus_performance_review, expected):
    assert lab1.quarterly_bonus(salary, bonus_level, bonus_performance_review) == expected
