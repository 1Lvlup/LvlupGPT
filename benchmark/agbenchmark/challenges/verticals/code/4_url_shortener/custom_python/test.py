import unittest
import pytest
from unittest.mock import patch
from url_shortener import retrieve_url, shorten_url

# The following lines import the necessary modules for running unit tests.
# unittest and pytest are both popular testing frameworks in Python, and
# unittest.mock is used for creating mock objects. The url_shortener module
# is being tested, and its retrieve_url and shorten_url functions are being
# imported.


class TestUrlShortener(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.original_retrieve_url = retrieve_url
        cls.original_shorten_url = shorten_url

        cls.retrieve_url_mock = patch('url_shortener.retrieve_url').start()
        cls.shorten_url_mock = patch('url_shortener.shorten_url').start()

        cls.retrieve_url_mock.return_value = 'original_url'
        cls.shorten_url_mock.return_value = 'short_url'

    @classmethod
    def teardown_class(cls):
        patch.stopall()

        retrieve_url = cls.original_retrieve_url
        shorten_url = cls.original_shorten_url

    # The following code block defines a TestCase class for running unit tests
    # on the url_shortener module. The setup_class and teardown_class methods
    # are used to create mock objects for the retrieve_url and shorten_url
    # functions and restore the original functions after the tests have run.


    def test_retrieve_url(self):
        self.assertEqual(retrieve_url('short_url'), 'original_url')

        self.retrieve_url_mock.assert_called_once_with('short_url')

    def test_shorten_url(self):
        self.assertEqual(shorten_url('original_url'), 'short_url')

        self
