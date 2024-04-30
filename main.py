from polib import pofile
from re import findall
from os import getcwd, listdir
from os.path import exists
from ast import literal_eval
from src.Translators import Translators
from src.TextStyler import *


def translate_text(text: str):
    placeholders = {}

    # Use a regular expression to find all the bracketed text
    bracketed_texts = findall(r'\[([^\[\]]*?)]', text)

    # Replace each bracketed text with a unique placeholder
    text = text.replace('\n', '__PPPPPPPPOOOOOOOO_P0__')
    for i, bracketed_text in enumerate(bracketed_texts):
        placeholder = f'__PPPPPPPPOOOOOOOO_{i}__'
        placeholders[placeholder] = f'[{bracketed_text}]'
        text = text.replace(f'[{bracketed_text}]', placeholder)

    # Perform the translation
    text_translated = ''
    i = 0
    while i < 3:
        try:
            if text:
                text_translated = ''
                text_box = split_text(text, '.')
                for tx in text_box:
                    text_translated += translator.translate(tx) + ' '
                text_translated = text_translated.removesuffix(' ')
            break
        except TypeError:
            break
        except Exception as e:
            i += 1
            print(get_text_color('Error: {} : {} ({})'.format(e, text, i), 'red'))
    if not text_translated:
        text_translated = text
    # Replace the placeholders back with the original bracketed text
    for placeholder, bracketed_text in placeholders.items():
        text_translated = text_translated.replace(placeholder, bracketed_text)
    text_translated = text_translated.replace('__PPPPPPPPOOOOOOOO_P0__', '\n')
    return text_translated


def process_file(filename: str):
    print('Translating', filename)
    po = pofile(filename)
    num_max = len(po.translated_entries())
    num_max += len(po.untranslated_entries())
    print('Total entries: #' + str(num_max))
    num_now = 0
    # Charge entries from .po archive
    for entry in po.translated_entries():
        num_now += 1
        if entry.msgid:
            entry.msgstr = translate_text(entry.msgid)
            # We obtain the progress bar by passing the calculated percentage and the colored text as parameters.
            print(get_progress_bar(int((num_now * 100) / num_max),
                                   get_text_color(entry.msgid, 'magenta') + ' -> ' + get_text_color(entry.msgstr,
                                                                                                    'blue')))
    # Charge entries from .po archive, entries not translated
    for entry in po.untranslated_entries():
        num_now += 1
        if entry.msgid:
            entry.msgstr = translate_text(entry.msgid)
            # We obtain the progress bar by passing the calculated percentage and the colored text as parameters.
            print(get_progress_bar(int((num_now * 100) / num_max),
                                   get_text_color(entry.msgid, 'magenta') + ' -> ' + get_text_color(entry.msgstr,
                                                                                                    'blue')))
    file_out = filename.replace('.po', '_' + data['lang_out'] + '.po')
    i = 1
    while exists(file_out):
        file_out = file_out.replace('.po', '({}).po'.format(i))
        i += 1
    po.save(file_out)
    print(get_progress_bar(100, get_text_color('File: ' + file_out + ' saved', 'green')))
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
            # Making sure to extract only text
        for key, value in data.items():
            data[key] = str(value)
        return data
    except:
        try:
            with open(file_config, "w") as file:
                data = {'lang_in': 'en',
                        'lang_out': 'es',
                        'provider': 'GoogleTranslate',
                        'key': 'None'}
                file.write(str(data))
                return data
        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':
    data = charge_file('./lang.config')
    translator = Translators(lang_in=data['lang_in'],
                             lang_out=data['lang_out'],
                             provider=data['provider'],
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
