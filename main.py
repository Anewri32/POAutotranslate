import polib
import re
import os
import ast
from src.Translators import Translators

num_max = 0
num_now = 0


def translate_text(text):
    global num_max, num_now
    # Define a dictionary to hold the mappings of bracketed text to placeholders
    placeholders = {}
    origin_text = text

    # Use a regular expression to find all the bracketed text
    bracketed_texts = re.findall(r'\[([^\[\]]*?)\]', text)

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
            else:
                text_translated = text
            break
        except Exception as e:
            i += 1
            print_bar(get_percent(), get_text_color('Error: ' + str(e) + ' : ' + text + ' ' + '(' + str(i) + ')', 'red'))
    # Replace the placeholders back with the original bracketed text
    for placeholder, bracketed_text in placeholders.items():
        text_translated = text_translated.replace(placeholder, bracketed_text)
    text_translated = text_translated.replace('__PPPPPPPPOOOOOOOO_P0__', '\n')

    num_now += 1
    print_bar(get_percent(), get_text_color(origin_text, 'magenta') + ' -> ' + get_text_color(text_translated, 'blue'))
    return text_translated


def process_file(filename):
    global num_max, num_now
    print('Translating', filename)
    po = polib.pofile(filename)

    num_max = len(po.translated_entries())
    num_max += len(po.untranslated_entries())
    print('Total entries:', str(num_max))
    num_now = 0

    # Charge entries from .po archive
    for entry in po.translated_entries():
        if entry.msgid:
            entry.msgstr = translate_text(entry.msgid)

    # Charge entries from .po archive, entries not translated
    for entry in po.untranslated_entries():
        if entry.msgid:
            entry.msgstr = translate_text(entry.msgid)
    file_out = filename.replace('.po', '_' + data['lang_out'] + '.po')
    po.save(file_out)
    print_bar( 100, get_text_color('File: ' + file_out + ' saved', 'green'))
    print('\n\n')


def split_text(text, delimit):
    lines = []
    line_now = ''
    for character in text:
        if character in delimit:
            if line_now:
                lines.append(line_now)
            line_now = ''
        else:
            line_now += character
    if line_now:
        lines.append(line_now)
    return lines


def print_bar(percent, text_out):
    long_bar = 25
    progress = int(percent / 100 * long_bar)
    if percent % 2 == 0:
        bar_symbols = "=" * progress
    elif percent == 1:
        bar_symbols = '-'
        progress += 1
    elif percent == 0:
        bar_symbols = ''
    else:
        bar_symbols = "=" * progress
        bar_symbols += '-'
        progress += 1
    bar_symbols += " " * (long_bar - progress)
    bar = "[" + bar_symbols + "]"
    output = '\r{} {}% {}'.format(bar, percent, text_out)
    print(output)
    # sys.stdout.write(output)
    # sys.stdout.flush()


def get_text_color(text, color):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cian': '\033[36m',
        'white': '\033[37m'
    }
    color_reset = '\033[0m'

    if color.lower() in colors:
        return colors[color.lower()] + text + color_reset
    else:
        print("Color invalid.")
        return text


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
            data = ast.literal_eval(file.read())
            # Making sure to extract only text
        for key, value in data.items():
            data[key] = str(value)
    except:
        try:
            with open(file_config, "w") as file:
                data = {'lang_in': 'en',
                        'lang_out': 'es',
                        'provider': 'GoogleTranslate',
                        'key': 'None'}
                file.write(str(data))
        except Exception as e:
            raise Exception(e)
    translator = Translators(lang_in=data['lang_in'],
                             lang_out=data['lang_out'],
                             provider=data['provider'],
                             key=data['key'])
    input('Press enter to start...')
    po_files = po_files_list()
    for file_name in po_files:
        process_file(file_name)
    input('All process has been finalized, press enter to exit.')

