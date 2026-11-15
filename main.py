import sys
from http.client import HTTPException
from pathlib import Path

from postal_codes import find_postal_codes, is_postal_code
from sources import read_file, read_url


MENU = """
1. Проверить почтовый индекс
2. Найти индексы во введённом тексте
3. Найти индексы в файле
4. Найти индексы на веб-странице
0. Выйти
"""


def print_matches(text: str) -> None:
    matches = find_postal_codes(text)
    if matches:
        print(*matches, sep="\n")
    else:
        print("Почтовые индексы не найдены.")


def main() -> None:
    try:
        while True:
            print(MENU, end="")
            choice = input("Выберите действие: ").strip()

            try:
                if choice == "0":
                    return
                if choice == "1":
                    value = input("Введите почтовый индекс: ")
                    if is_postal_code(value):
                        print("Формат индекса корректен.")
                    else:
                        print("Формат индекса некорректен.")
                elif choice == "2":
                    print_matches(input("Введите текст: "))
                elif choice == "3":
                    path = input("Введите путь к файлу: ").strip()
                    print_matches(read_file(Path(path).expanduser()))
                elif choice == "4":
                    url = input("Введите URL страницы: ").strip()
                    print_matches(read_url(url))
                else:
                    print("Выберите пункт от 0 до 4.")
            except (OSError, ValueError, LookupError, RuntimeError, HTTPException) as error:
                print(f"Ошибка: {error}", file=sys.stderr)
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
