def split_text(text: str, delimit: str):
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


def get_progress_bar(percent: float, long_bar: float = 25):
    progress_float = percent / 100 * long_bar
    progress = int(progress_float)
    bar_symbols = "=" * progress
    if (progress_float - progress) >= 0.5:
        bar_symbols += '-'
        progress += 1
    bar_symbols += " " * (int(long_bar) - progress)
    bar = "[" + bar_symbols + "]"
    return '\r{} {}%'.format(get_text_color(bar, 'cian'), percent)


def get_text_color(text: str, color: str):
    color = color.lower()
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
    return colors.get(color, '') + text + '\033[0m'
