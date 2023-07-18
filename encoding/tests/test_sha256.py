from encoding.sha256 import sha256

from unittest import TestCase


class TestSHA256(TestCase):
    @classmethod
    def setUpClass(cls):
        print("Запуск тестов SHA256, написанных в соответствии с документацией центра комп. нац. безопасности США") 

    def test_oneblock(self):
        input_value = "abc"
        expected_output = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        hash_result = sha256(input_value)
        self.assertEqual(hash_result, expected_output, "Одноблочная строка хэшируется неверно")
        print("Тест одноблочной строкой пройден.")
    
    def test_multiblock(self):
        input_value = "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
        expected_output = "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
        hash_result = sha256(input_value)
        self.assertEqual(hash_result, expected_output, "Многоблочная строка хэшируется неверно")
        print("Тест многоблочной строкой пройден.")
    
    def test_long_message(self):
        input_value = "a" * 1_000_000
        expected_output = "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
        hash_result = sha256(input_value)
        self.assertEqual(hash_result, expected_output, "Длинная строка хэшируется неверно")
        print("Тест длинной строкой пройден.")
