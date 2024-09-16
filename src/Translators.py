import requests


class Translators:
    def __init__(self, lang_out, lang_in='auto', key='None', provider='GoogleTranslate'):
        self.lang_in = lang_in
        self.lang_out = lang_out
        self.__key = key
        self.provider = provider

    def translate(self, text):
        if self.provider.lower() == 'googletranslate':
            return str(self.google_translate(text))
        elif self.provider.lower() == 'deepltranslator':
            if self.__key:
                return str(self.deepl_translator(text))
            else:
                raise Exception('Key needed for DeepL Translator')
        elif self.provider.lower() == 'yandextranslate':
            if self.__key:
                return str(self.yandex_translate(text))
            else:
                raise Exception('Key needed for Yandex Translator')
        else:
            raise Exception('Translator not found')

    def google_translate(self, text):
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format(
                self.lang_in, self.lang_out, text))
        if response.status_code == 200:
            data = response.json()
            return data[0][0][0]  # The translation is in the first item of the first list
        else:
            raise Exception("Error with the request: {}: status code: {}".format(response.text, response.status_code))

    def deepl_translator(self, text):
        response = requests.get(
            'https://api-free.deepl.com/v2/translate?auth_key={}&text={}&source_lang={}&target_lang={}'.format(
                self.__key, text, self.lang_in, self.lang_out))
        if response.status_code == 200:
            return response.json()["translations"][0]["text"]
        else:
            raise Exception("Error with the request: {}: status code: {}".format(response.text, response.status_code))

    def yandex_translate(self, text):
        response = requests.get(
            'https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}-{}'.format(
                self.__key, text, self.lang_in, self.lang_out))
        if response.status_code == 200:
            return response.json()["text"][0]
        else:
            raise Exception("Error with the request: {}: status code: {}".format(response.text, response.status_code))

    def test_providers(self):
        # Preview the tests
        temp_text = 'egg'
        preview_lang_in = self.lang_in
        preview_lang_out = self.lang_out
        self.lang_in = 'en'
        self.lang_out = 'es'

        # Start test with Google Translate
        try:
            result = self.google_translate(temp_text)
            if result == 'huevo':
                print('Google Translate: pass')
            else:
                print('Google Translate: error with the translation', result)
        except:
            pass

        # Start test with DeepL Translator
        try:
            result = self.deepl_translator(temp_text)
            if result == 'huevo':
                print('DeepL Translator: pass')
            else:
                print('DeepL Translator: error with the translation', result)
        except:
            pass

        # Start test with Yandex Translate
        try:
            result = self.yandex_translate(temp_text)
            if result == 'huevo':
                print('Yandex Translate: pass')
            else:
                print('Yandex Translate: error with the translation', result)
        except:
            pass

        # After the tests
        self.lang_in = preview_lang_in
        self.lang_out = preview_lang_out
