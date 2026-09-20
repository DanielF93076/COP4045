"""Homework 2, Problem 1: parsing Python source files.

Daniel Farafonov
"""

import re


def line_number(source_filename: str, dest_filename: str) -> None:
    """Writes source_filename's lines, each prefixed by its number, to dest_filename."""
    try:
        with open(source_filename, 'r', encoding='utf-8') as source_file:
            lines = source_file.readlines()
        with open(dest_filename, 'w', encoding='utf-8') as dest_file:
            for i, line in enumerate(lines, start=1):
                stripped = line.rstrip('\n')
                dest_file.write(f'{i}. {stripped}\n')
    except OSError as error:
        print(f'Error: could not number lines from "{source_filename}" '
              f'into "{dest_filename}": {error}')
        raise


def _remove_comments_and_blanks(code: str) -> str:
    """Removes "#" comments and blank lines from code, ignoring "#" inside strings."""
    kept_chars = []
    quote = ''
    i = 0
    length = len(code)
    while i < length:
        char = code[i]

        if quote:
            if char == '\\' and quote in ("'", '"'):
                kept_chars.append(code[i:i + 2])
                i += 2
                continue
            if code.startswith(quote, i):
                kept_chars.append(quote)
                i += len(quote)
                quote = ''
                continue
            kept_chars.append(char)
            i += 1
            continue

        if code.startswith('"""', i) or code.startswith("'''", i):
            quote = code[i:i + 3]
            kept_chars.append(quote)
            i += 3
            continue
        if char in ('"', "'"):
            quote = char
            kept_chars.append(char)
            i += 1
            continue
        if char == '#':
            while i < length and code[i] != '\n':
                i += 1
            continue

        kept_chars.append(char)
        i += 1

    result_lines = [line.rstrip() for line in ''.join(kept_chars).split('\n')
                     if line.strip() != '']
    return '\n'.join(result_lines) + ('\n' if result_lines else '')


def parse_functions(filename: str) -> tuple:
    """Returns (line_number, name, args, code) for each top-level function in filename, sorted by name."""
    try:
        with open(filename, 'r', encoding='utf-8') as source_file:
            lines = source_file.readlines()
    except OSError as error:
        print(f'Error: could not read file "{filename}": {error}')
        raise

    def_pattern = re.compile(r'^def\s+(\w+)\s*\(([^)]*)\)[^:]*:')
    functions = []
    total_lines = len(lines)
    index = 0
    while index < total_lines:
        match = def_pattern.match(lines[index])
        if match:
            start = index
            name = match.group(1)
            args = match.group(2).strip()
            index += 1
            while index < total_lines and (
                    lines[index].strip() == '' or lines[index][0] in ' \t'):
                index += 1
            code = _remove_comments_and_blanks(''.join(lines[start:index]))
            functions.append((start + 1, name, args, code))
        else:
            index += 1

    functions.sort(key=lambda item: item[1])
    return tuple(functions)


def main() -> None:
    """Tests line_number and parse_functions on this file."""
    this_file = 'p1_Farafonov_Daniel.py'
    numbered_file = 'p1_Farafonov_Daniel_numbered.txt'

    print(f'Numbering lines of {this_file} into {numbered_file}...')
    line_number(this_file, numbered_file)
    print(f'Done, see {numbered_file}.\n')

    print(f'Parsing functions defined in {this_file}:\n')
    functions = parse_functions(this_file)
    for line_no, name, args, code in functions:
        print(f'Line {line_no}: {name}({args})')
        print(code)
        print('-' * 40)


if __name__ == '__main__':
    main()
