import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import unittest

auth_yandex_params = {
    'login': '',
    'passwd': ''
    }


def find_element_by_name_and_input_to(driver, element_name, input_text):
    element = driver.find_element_by_name(element_name)
    element.send_keys(input_text)
    element.send_keys(Keys.RETURN)
    time.sleep(3)
    return element


def get_element_by_class_name(driver, element_name):
    element = driver.find_element_by_class_name(element_name)
    return element


def auth_yandex(login, passwd):
    driver = webdriver.Firefox()
    driver.get("https://passport.yandex.ru/auth/add")

    try:
        find_element_by_name_and_input_to(driver, 'login', login)
        find_element_by_name_and_input_to(driver, 'passwd', passwd)

        # print(driver.page_source)

        element_first_name = get_element_by_class_name(driver, 'personal-info__first')
        element_last_name = get_element_by_class_name(driver, 'personal-info__last')
        person_name = None
        if element_first_name or element_last_name:
            person_name = f"{element_first_name.text} {element_last_name.text}"
    except exceptions.NoSuchElementException:
        raise exceptions.NoSuchElementException
    finally:
        driver.close()

    return person_name


class TestYandexAuth(unittest.TestCase):

    def setUp(self):
        self.login = auth_yandex_params['login']
        self.passwd = auth_yandex_params['passwd']

    def test_auth_yandex(self):
        person_name = auth_yandex(self.login, self.passwd)
        self.assertIsNotNone(person_name)

    def test_auth_yandex_wrong_passwd(self):
        with self.assertRaises(exceptions.NoSuchElementException):
            person_name = auth_yandex(self.login, '********')
            self.assertIsNone(person_name)

    def test_auth_yandex_wrong_login(self):
        with self.assertRaises(exceptions.NoSuchElementException):
            person_name = auth_yandex('****', '****')
            self.assertIsNone(person_name)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestYandexAuth('test_auth_yandex'))
    suite.addTest(TestYandexAuth('test_auth_yandex_wrong_passwd'))
    suite.addTest(TestYandexAuth('test_auth_yandex_wrong_login'))

    return suite


if __name__ == "__main__":
    # Input login and password of real Yandex account
    auth_yandex_params['login'] = input(f"Введите логин в личный кабинет Яндекса:")
    auth_yandex_params['passwd'] = input(f"Введите пароль:")

    runner = unittest.TextTestRunner()
    runner.run(create_suite())
