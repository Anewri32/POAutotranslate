# POAutotranslate
![icon](icon.ico)

 Translate the '.po' files automatically using translates APIs.

 The program is already configured to support text strings with parameters (which are excluded at the time of translation) and long texts which are split before translation and reunified afterwards to avoid problems with long text strings.

 Error handling and up to 3 retries are also included in the translation in case something goes wrong.

## Use
 Just run the program in the same directory as the '.po' files.
 
The program will automatically detect all files in the directory with .po extension and display them in the console before starting the translation. Once finished, the file will be saved along with a suffix indicating the new language it was translated to.

## Setting
 It is also possible to change the 'lang.config' file to configure the program. The supported languages are the same as those supported by the Google Translate API.

```
{'lang_in': 'en', 'lang_out': 'es', 'provider': 'GoogleTranslate', 'key': 'None'}
```
* lang_in = Input language
* lang_out = Output language
* provider = Translation resource provider
* key = Key required for authentication

### Translators
* GoogleTranslate
* DeepLTranslator (need a key)
* YandexTranslate (need a key)
