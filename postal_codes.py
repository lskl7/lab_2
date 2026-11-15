# Проверка и поиск российских почтовых индексов

import re

POSTAL_CODE_PATTERN = re.compile(r"\b[0-9]{6}\b")


# Проверяет, что вся строка соответствует формату почтового индекса
def is_postal_code(value: str) -> bool:
    return POSTAL_CODE_PATTERN.fullmatch(value) is not None


# Возвращает все найденные индексы в порядке появления, включая повторы
def find_postal_codes(text: str) -> list[str]:
    return POSTAL_CODE_PATTERN.findall(text)
