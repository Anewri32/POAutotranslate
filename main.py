import sys
from polib import pofile
from re import findall
from os import getcwd, listdir
from os.path import exists
from ast import literal_eval
from src.Translators import Translators
from src.TextStyler import *


def translate_text(text: str):
    placeholders = {}
    bracketed_texts = findall(r'\[([^\[\]]*?)]', text)
    text = text.replace('\n', '__PPPPOOOO_P0__')
    for i, bracketed_text in enumerate(bracketed_texts):
        placeholder = f'__kkkk5555_{i}__'
        placeholders[placeholder] = f'[{bracketed_text}]'
        text = text.replace(f'[{bracketed_text}]', placeholder)

    text_translated = ''
    i = 0
    while i < 3:
        try:
            if text:
                text_box = split_text(text, '.')
                for tx in text_box:
                    text_translated += translator.translate(tx) + ' '
                text_translated = text_translated.strip()
            break
        except TypeError:
            break
        except Exception as e:
            i += 1
            print(get_text_color(f'Error: {e} : {text} ({i})', 'red'))
    if not text_translated:
        text_translated = text
    for placeholder, bracketed_text in placeholders.items():
        text_translated = text_translated.replace(placeholder, bracketed_text)
    text_translated = text_translated.replace('__PPPPOOOO_P0__', '\n')
    return text_translated


def print_status(txt: str, num_now: float, num_max: float):
    progress_bar = get_progress_bar(num_now * 100 / num_max)
    print(progress_bar, txt)


def process_file(filename: str):
    print('Translating', filename)
    try:
        po = pofile(filename)
    except Exception as e:
        print(f"Error loading file {filename}: {e}")
        return

    num_max = len(po.translated_entries()) + len(po.untranslated_entries())
    print('Total entries: #' + str(num_max))
    num_now = 0
    for entry in po.translated_entries():
        num_now += 1
        if entry.msgid:
            entry.msgstr = translate_text(entry.msgid)
            text = get_text_color(entry.msgid, 'magenta') + ' -> ' + get_text_color(entry.msgstr, 'blue')
            print_status(text, num_now, num_max)

    for entry in po.untranslated_entries():
        num_now += 1
        if entry.msgid:
            entry.msgstr = translate_text(entry.msgid)
            text = get_text_color(entry.msgid, 'magenta') + ' -> ' + get_text_color(entry.msgstr, 'blue')
            print_status(text, num_now, num_max)

    file_out = filename.replace('.po', '_' + data['lang_out'] + '.po')
    i = 1
    while exists(file_out):
        file_out = file_out.replace('.po', f'({i}).po')
        i += 1
    try:
        po.save(file_out)
        print(get_progress_bar(100, get_text_color('File: ' + file_out + ' saved', 'green')))
    except Exception as e:
        print(f"Error saving file {file_out}: {e}")
    print('\n\n')


def po_files_list():
    po_files = []
    dir = getcwd()
    for file in listdir(dir):
        if file.endswith('.po'):
            po_files.append(file)
    return po_files


def charge_file(file_config: str):
    try:
        with open(file_config, "r") as file:
            data = literal_eval(file.read())
            for key, value in data.items():
                data[key] = str(value)
            return data
    except Exception as e:
        print(f"Error reading config file {file_config}: {e}")
        try:
            with open(file_config, "w") as file:
                data = {'lang_in': 'en', 'lang_out': 'es', 'provider': 'GoogleTranslate', 'key': 'None'}
                file.write(str(data))
                return data
        except Exception as e:
            raise Exception(f"Error writing default config file {file_config}: {e}")


if __name__ == '__main__':
    data = charge_file('./lang.config')
    translator = Translators(lang_in=data['lang_in'], lang_out=data['lang_out'], provider=data['provider'],
                             key=data['key'])
    po_files = po_files_list()
    if po_files:
        print(get_text_color('Detected files: ' + str(po_files), 'cian'))
        input('Press enter to start...')
        for file_name in po_files:
            process_file(file_name)
        input('All process has been finalized, press enter to exit.')
    else:
        input('No files with .po extension were detected, press enter to exit.')
