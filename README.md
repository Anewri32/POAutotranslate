# POAutotranslate
 Translate the '.po' files automatically using the Google Translate API.

## Use
 Just run the program in the same directory as the '.po' files.

## Setting
 It is also possible to change the 'lang.config' file to configure the languages. The supported languages are the same as those supported by the Google Translate API.

```
{'lang_in': 'en', 'lang_out': 'es'}
```

* lang_ing = Input language
* lang_out = Output language

### Translators

* GoogleTranslate
* DeepLTranslator (need a key)
* YandexTranslate (need a key)