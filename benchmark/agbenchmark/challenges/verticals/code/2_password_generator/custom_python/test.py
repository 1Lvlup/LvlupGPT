import unittest

import password_generator  # Importing the password_generator module


class TestPasswordGenerator(unittest.TestCase):
    def test_password_length(self):
        # Testing if the generated password matches the desired length
        for i in range(8, 17):  # Iterating through the range of 8 to 16
            password = password_generator.generate_password(i)  # Generating a password with the given length
            self.assertEqual(len(password), i)  # Checking if the password length matches the desired length

    def test_value_error(self):
        # Testing if ValueError is raised when the length is out of bounds
        with self.assertRaises(ValueError):
            password_generator.generate_password(7)  # Trying to generate a password with a length of 7
        with self.assertRaises(ValueError):
            password_generator.generate_password(17)  # Trying to generate a password with a length of 17

    def test_password_content(self):
        # Testing if the generated password contains digits and punctuation characters
        password = password_generator.generate_password()  # Generating a password with the default length
        self.assertTrue(any(c.isdigit() for c in password))  # Checking if the password contains any digits
        self.assertTrue(any(c in password_generator.string.punctuation for c in password))  # Checking if the password contains any punctuation characters


if __name__ == "__main__":
    unittest.main()  # Running the test suite
