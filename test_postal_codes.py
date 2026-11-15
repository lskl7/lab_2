import unittest

from postal_codes import find_postal_codes, is_postal_code


# Проверяет правила проверки и поиска почтовых индексов
class PostalCodeTests(unittest.TestCase):
    # Проверяет, что шестизначные строки проходят проверку формата
    def test_valid_format(self):
        for value in ("101000", "190000", "012345", "000000"):
            with self.subTest(value=value):
                self.assertTrue(is_postal_code(value))

    # Проверяет отклонение строк с неверной длиной или недопустимыми символами
    def test_invalid_format(self):
        for value in (
            "", "12345", "1234567", " 123456", "123456 ", "123456\n",
            "123 456", "123-456", "A123456", "123456Б", "１２３４５６",
            "١٢٣٤٥٦", "12345６",
        ):
            with self.subTest(value=value):
                self.assertFalse(is_postal_code(value))

    # Проверяет порядок найденных индексов и сохранение повторов
    def test_search_preserves_order_and_repetitions(self):
        text = "Москва (101000), Санкт-Петербург: 190000.\nПовтор: 101000."
        self.assertEqual(find_postal_codes(text), ["101000", "190000", "101000"])

    # Проверяет, что поиск пропускает части слов и длинных чисел
    def test_search_excludes_parts_of_words_and_long_numbers(self):
        text = "1234567 0123456 A123456 123456Б _123456 123456_ １123456 12345"
        self.assertEqual(find_postal_codes(text), [])

    # Проверяет, что поиск в пустом тексте возвращает пустой список
    def test_search_empty_text(self):
        self.assertEqual(find_postal_codes(""), [])


if __name__ == "__main__":
    unittest.main()
