# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest

class AccountTest(unittest.TestCase):

    SIGNUP = 'http://localhost:8000/account/signup'
    SIGNIN = 'http://localhost:8000/account/signin'
    LOGOUT = 'http://localhost:8000/account/logout'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_sign_up(self):
        self.browser.get('http://localhost:8000/account/signup_without_captcha')


        # find the element  of form
        username = self.browser.find_element_by_name("username")
        first_name = self.browser.find_element_by_name("first_name")
        last_name = self.browser.find_element_by_name("last_name")
        email = self.browser.find_element_by_name("email")
        password = self.browser.find_element_by_name("password")
        password_confirmation = self.browser.find_element_by_name("password_confirmation")
        submit = self.browser.find_element_by_name("submit")


        # type in the form
        username.send_keys("André")
        first_name.send_keys("Nascimento")
        last_name.send_keys("andrenascimento")
        email.send_keys("andrenascimento@ideiaseo.com")
        password.send_keys("1234")
        password_confirmation.send_keys("1234")

        submit.submit()


    def test_sign_in(self):
        pass

if __name__ == '__main__':  #
    unittest.main(warnings='ignore')