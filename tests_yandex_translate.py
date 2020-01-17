import unittest
import requests
from unittest.mock import patch

# all what we need to ask Yandex Translate
api_key = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

params = {
    "key": api_key,
    "text": "",
    "lang": "en-ru",
    }


def translate(text):
    if len(text) <= 0:
        return

    params["text"] = text
    response = requests.get(url, params=params)
    json_result = response.json()
    return json_result


class TestYandexTranslate(unittest.TestCase):

    def test_translate_correct(self):
        json_result = translate("hello")
        text_result = "".join(json_result["text"])
        self.assertEqual(text_result, 'привет')

    def test_translate_reply200(self):
        json_result = translate("hello")
        self.assertEqual(json_result['code'], 200)

    def test_translate_empty_text(self):
        json_result = translate("")
        self.assertIsNone(json_result)

    @patch.dict(params, params.copy())
    def test_translate_wrong_apikey(self):
        params['key'] = ""
        json_result = translate("привет")
        self.assertEqual(json_result['code'], 401)

    @patch.dict(params, params.copy())
    def test_translate_wrong_language(self):
        params['lang'] = ""
        json_result = translate("привет")
        self.assertEqual(json_result['code'], 502)

    @patch('__main__.url', 'wrong url')
    def test_translate_wrong_url(self):
        with self.assertRaises(requests.exceptions.MissingSchema):
            translate('hello')


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestYandexTranslate('test_translate_wrong_apikey'))
    suite.addTest(TestYandexTranslate('test_translate_correct'))
    suite.addTest(TestYandexTranslate('test_translate_reply200'))
    suite.addTest(TestYandexTranslate('test_translate_wrong_language'))
    suite.addTest(TestYandexTranslate('test_translate_empty_text'))
    suite.addTest(TestYandexTranslate('test_translate_wrong_url'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(create_suite())
