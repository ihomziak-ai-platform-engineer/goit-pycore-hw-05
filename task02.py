"""Command-line log analyzer for the homework task 2."""

import re
from collections.abc import Callable, Iterator


def generator_numbers(text: str) -> Iterator[float]:
    # Знаходимо числа, відокремлені пробілами
    pattern = r"(?<!\S)[+-]?\d+(?:\.\d+)?(?!\S)"

    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(
    text: str,
    func: Callable[[str], Iterator[float]]
) -> float:
    # Отримуємо числа з генератора та підсумовуємо
    return sum(func(text))


if "__main__" == __name__:
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими "
        "надходженнями 27.45 і 324.00 доларів."
    )

    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income:.2f}")
