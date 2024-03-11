import unittest
import string

import password_generator # Import the password_generator module

class TestPasswordGenerator(unittest.TestCase):
    def test_password_length(self):
        # Test the generate_password function with different length parameters
        for length in range(8, 17):
            password = password_generator.generate_password(length)
            self.assertEqual(len(password), length) # Check if the length of the generated password matches the input

    def test_value_error(self):
        # Test if ValueError is raised when the length parameter is out of bounds
        with self.assertRaises(ValueError):
            password_generator.generate_password(7)

        with self.assertRaises(ValueError):
            password_generator.generate_password(17)

    def test_password_content(self):
        # Test if the generated password contains digits and punctuation characters
        password = password_generator.generate_password()
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))


if __name__ == "__main__":
    unittest.defaultTestLoader.testMethodPrefix = "test_"
    unittest.main() # Run the unit tests
