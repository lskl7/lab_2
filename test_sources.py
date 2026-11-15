from email.message import Message
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from postal_codes import find_postal_codes
from sources import read_file, read_url


# Проверяет чтение файлов и получение текста с веб-страниц.
class SourceTests(unittest.TestCase):
    # Проверяет чтение файла в UTF-8 с меткой порядка байтов.
    def test_utf8_file_with_bom(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "адреса.txt"
            path.write_text("Индекс 101000", encoding="utf-8-sig")
            self.assertEqual(read_file(path), "Индекс 101000")

    # Проверяет извлечение индексов из соседних абзацев HTML-файла.
    def test_html_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "адреса.html"
            path.write_text("<p>101000</p><p>190000</p>", encoding="utf-8")
            self.assertEqual(find_postal_codes(read_file(path)), ["101000", "190000"])

    # Проверяет декодирование страницы и поиск индексов в её тексте.
    @patch("sources.urlopen")
    def test_html_page(self, urlopen):
        html = (
            '<head><title>999999</title></head>'
            '<p data-id="123456">Москва: <b>101</b>000</p>'
            '<p>&#49;90000</p><script>123456</script><style>234567</style>'
        )
        response = BytesIO(html.encode("windows-1251"))
        response.headers = Message()
        response.headers["Content-Type"] = "text/html; charset=windows-1251"
        urlopen.return_value = response
        text = read_url("https://example.com")
        self.assertIn("Москва", text)
        self.assertEqual(find_postal_codes(text), ["101000", "190000"])
        urlopen.assert_called_once_with("https://example.com", timeout=10)

    # Проверяет, что неподдерживаемый URL отклоняется до сетевого запроса.
    @patch("sources.urlopen")
    def test_invalid_url_is_rejected_before_request(self, urlopen):
        with self.assertRaises(ValueError):
            read_url("file:///tmp/address.txt")
        urlopen.assert_not_called()
