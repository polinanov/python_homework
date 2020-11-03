def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def enter_data():
    salary = int(input('Введите зп инженера - целое число от 70000 до 750000: '))
    level = int(input('Введите уровень инженера - целое число от 7 до 17: '))
    performance_review = float(input('Введите Performance Review  инженера -  число от 1 до 5: '))
    if not (isinstance(salary, int)):
        print(f'ЗП - {salary} - должна быть в верном формате')
        return TypeError, level, performance_review
    elif (salary < 70000) or (salary > 750000):
        print(f'ЗП - {salary} - должна быть в заданном диапозоне')
        return ValueError, level, performance_review
    return salary, performance_review, level


# def handler(salary, performance_review, level):
#     if (salary < 70000 or salary > 750000) or (performance_review < 1 or performance_review > 5) or (
#                     level < 7 or level > 17):
#         print('Проверьте диапозон введенных данных ')
#         print('...')
#         enter_data()


def calculation_bonus_level(level):
    if not (isinstance(level, int)):
        print(f'Уровень инженера - {level} - должен быть в верном формате')
        return TypeError
    if (level < 7) or (level > 17):
        print(f'Уровень инженера - {level} - должен быть в заданном диапозоне')
        return ValueError
    else:
        bonus_level = 0
        if level < 10:
            bonus_level = 0.05
        elif 10 <= level < 13:
            bonus_level = 0.1
        elif 13 <= level < 15:
            bonus_level = 0.15
        elif level >= 15:
            bonus_level = 0.2
    return bonus_level


def calculation_bonus_performance_review(performance_review):
    if not ((isinstance(performance_review, int)) or (isinstance(performance_review, float))):
        print(f'Performance review - {performance_review} - должно быть в верном формате')
        return TypeError
    elif (performance_review < 1) or (performance_review > 5):
        print(f'Performance review - {performance_review} - должно быть в заданном диапозоне')
        return ValueError
    else:
        performance_review = performance_review
        bonus_performance_review = 0
        if performance_review < 2:
            bonus_performance_review = 0
        elif 2 <= performance_review < 2.5:
            bonus_performance_review = 0.25
        elif 2.5 <= performance_review < 3:
            bonus_performance_review = 0.5
        elif 3 <= performance_review < 3.5:
            bonus_performance_review = 1
        elif 3.5 <= performance_review < 4:
            bonus_performance_review = 1.5
        elif performance_review >= 4:
            bonus_performance_review = 2
    return bonus_performance_review


def quarterly_bonus(salary, level,
                    performance_review):  # проверка на отрицательные значения, добавить в тесты
    bonus_level = calculation_bonus_level(level)
    bonus_performance_review = calculation_bonus_performance_review(performance_review)
    # print(bonus_level, bonus_performance_review)
    if (bonus_level is TypeError) or (bonus_performance_review is TypeError) or (salary is TypeError):
        return TypeError
    elif (bonus_level is ValueError) or (bonus_performance_review is ValueError) or (salary is ValueError):
        return ValueError
    else:
        bonus = (3 * int(salary)) * float(bonus_level) * float(bonus_performance_review)
        print('Квартальная премия инженера', bonus)
    return bonus


if __name__ == '__main__':
    salary_, performance_review_, level_ = enter_data()
    bonus_ = quarterly_bonus(salary_, level_, performance_review_)
    if (bonus_ is TypeError) or (bonus_ is ValueError):
        print('Выход из программы')
        raise SystemExit

# Нам необходимо создать механизм расчета премии по результатам Performance Review программиста,
# какие у нас есть входные данные:
# 1. ЗП инженера – [70 000... 750 000]
# 2. Результат квартального Performance Review [1…5]
# 3. Уровень инженера – [7..17]
# 4. Размер премии от квартальной ЗП:
# 1. 5% если lvl < 10,
# 2. 10% если 10 =< lvl < 13,
# 3. 15% если 13 =< lvl < 15,
# 4. 20% если lvl >= 15
# 5. Модификатор премии:
# 1. 0% – если результат perf-review < 2
# 2. 25% – если результат 2 =< perf-review < 2.5
# 3. 50% – если результат 2.5 =< perf-review < 3
# 4. 100% – если результат 3 =< perf-review < 3.5
# 5. 150% – если результат 3.5 =< perf-review < 4
# 6. 200% – если результат perf-review >= 4
