# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest

"""
These tests cover all completed functions.
These tests need selenium webdriver and Mozilla Firefox

For run these testes you need start selenium server with
    $ java -jar selenium-version
After of you run command, you need run
    $ python directory/rede_gsti/apps/account/tests/function.py
"""


class AccountTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # def test_register_user(self):
    #     self.browser.get('http://localhost:8000/account/signup_without_captcha')
    #
    #     # find the elements of form
    #     username = self.browser.find_element_by_name("username")
    #     first_name = self.browser.find_element_by_name("first_name")
    #     last_name = self.browser.find_element_by_name("last_name")
    #     email = self.browser.find_element_by_name("email")
    #     password = self.browser.find_element_by_name("password")
    #     password_confirmation = self.browser.find_element_by_name("password_confirmation")
    #     submit = self.browser.find_element_by_name("submit")
    #
    #
    #     # type in the form
    #     username.send_keys("Andre")
    #     first_name.send_keys("Nascimento")
    #     last_name.send_keys("andrenascimento")
    #     email.send_keys("andrenascimento@ideiaseo.com")
    #     password.send_keys("1234")
    #     password_confirmation.send_keys("1234")
    #
    #     submit.submit()
    #
    #     self.assertEqual(self.browser.title.lower(), 'Registered Successfully'.lower())

    # def test_sign_in(self):
    #     self.browser.get('http://localhost:8000/account/signin')
    #
    # def test_logout(self):
    #     self.browser.get('http://localhost:8000/account/logout')

if __name__ == '__main__':
    unittest.main()