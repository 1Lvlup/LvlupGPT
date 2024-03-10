import unittest
import string

import password_generator


class TestPasswordGenerator(unittest.TestCase):
    def test_password_length(self):
        for length in range(8, 17):
            password = password_generator.generate_password(length)
            self.assertEqual(len(password), length)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            password_generator.generate_password(7)

        with self.assertRaises(ValueError):
            password_generator.generate_password(17)

    def test_password_content(self):
        password = password_generator.generate_password()
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))


if __name__ == "__main__":
    unittest.defaultTestLoader.testMethodPrefix = "test_"
    unittest.main()
