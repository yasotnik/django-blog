# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest


# Test class is inherit from unittest.TestCase
class NewVisitorTest(unittest.TestCase):

    # Run before each test
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    # Run after each test
    def tearDown(self):
        self.browser.quit()

    # Test starts with test (CAP!)
    def test_it_worked(self):
        self.browser.get('http://localhost:8000')
        # assertEquals etc.
        self.assertIn('Welcome to Django', self.browser.title)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
