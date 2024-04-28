import polib
import re
import sys
import os
from googletrans import Translator

translator = Translator()
num_max = 0
num_now = 0


def translate(text, lang_in, lang_out):
    global num_max, num_now
    # Define a dictionary to hold the mappings of bracketed text to placeholders
    placeholders = {}
    origin_text = text

    # Use a regular expression to find all the bracketed text
    bracketed_texts = re.findall(r'\{[(.*?)]}', text)

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
                text = translator.translate(text, dest=lang_out, src=lang_in, timeout=10).text
                break
        except Exception as e:
            i += 1
            print_bar(get_percent(), str(e) + ' : ' + text + ' ' + '(' + str(i) + ')')
    # Replace the placeholders back with the original bracketed text
    for placeholder, bracketed_text in placeholders.items():
        text = text.replace(placeholder, bracketed_text)
    num_now += 1
    print_bar(get_percent(), origin_text + ' : ' + text)
    return text


def process_file(filename, lang_in, lang_out):
    global num_max, num_now
    po = polib.pofile(filename)

    num_max = len(po.translated_entries())
    num_max += len(po.untranslated_entries())
    num_now = 0

    # Charge entries from .po archive
    for entry in po.translated_entries():
        if entry.msgstr:
            entry.msgstr = translate(entry.msgid, lang_in, lang_out)

    # Charge entries from .po archive, entries not translated
    for entry in po.untranslated_entries():
        if not entry.msgstr:
            entry.msgstr = translate(entry.msgid, lang_in, lang_out)
    file_out = filename.replace('.po', '_' + lang_out + '.po')
    po.save(file_out)
    print_bar( 100, 'File: ' + file_out + ' saved')
    print('\n')


def print_bar(percent, text_out):
    long_bar = 50
    progress = int(percent / 100 * long_bar)
    bar = '[' + '#' * progress + ' ' * (long_bar - progress) + ']'
    sys.stdout.write('\r{} {}% {}'.format(bar, percent, text_out))
    sys.stdout.flush()


def get_percent():
    return int((num_now * 100) / num_max)


def po_files_list():
    po_files = []
    dir = os.getcwd()
    for file in os.listdir(dir):
        if file.endswith('.po'):
            po_files.append(file)
    return po_files


if __name__ == '__main__':
    file_config = './lang.config'
    try:
        with open(file_config, "r") as file:
            data = eval(file.read())
    except:
        try:
            with open(file_config, "w") as file:
                data = {'lang_in': 'en', 'lang_out': 'es'}
                file.write(str(data))
        except Exception as e:
            print(e)

    po_files = po_files_list()
    for file_name in po_files:
        process_file(file_name, data['lang_in'], data['lang_out'])
