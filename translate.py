import polib
from googletrans import Translator
import re


translator = Translator()

def translate(text, lang):
    # Define a dictionary to hold the mappings of bracketed text to placeholders
    placeholders = {}

    # Use a regular expression to find all the bracketed text
    bracketed_texts = re.findall(r'\[(.*?)\]', text)

    # Replace each bracketed text with a unique placeholder
    for i, bracketed_text in enumerate(bracketed_texts):
        placeholder = f'__BRACKET_{i}__'
        placeholders[placeholder] = f'[{bracketed_text}]'
        text = text.replace(f'[{bracketed_text}]', placeholder)

    # Perform the translation
    i = 0
    while i < 3:
        try:
            if text:
                text = translator.translate(text, dest=lang, src="en", timeout=10).text
                break
        except Exception as e:
            i += 1
            print(e + " (" + str(i) + ")")

    # Replace the placeholders back with the original bracketed text
    for placeholder, bracketed_text in placeholders.items():
        text = text.replace(placeholder, bracketed_text)

    return text


def process_file():
    lang = "es"
    filename = "./de.PO"
    po = polib.pofile(filename)
    
    for entry in po.translated_entries():
        if entry.msgstr:
            print(entry.msgid)
            print('translating...')
            translated_text = translate(entry.msgid, lang)
            entry.msgstr = translated_text
            print(entry.msgstr)
            print('\n')
            
    for entry in po.untranslated_entries():
        if not entry.msgstr:
            print(entry.msgid)
            print('translating...')
            translated_text = translate(entry.msgid, lang)
            entry.msgstr = translated_text
            print(entry.msgstr)
            print('\n')
    po.save(filename+".translated")
    print('File .po saved')

if __name__ == '__main__':
    process_file()
