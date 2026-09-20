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


def _strip_comment(line: str) -> str:
    """Returns line with everything after an unquoted hash mark removed."""
    trimmed = line.strip()
    if trimmed.startswith('"""') and trimmed.endswith('"""'):
        return line
    quote = ''
    for i, char in enumerate(line):
        if quote:
            if char == quote:
                quote = ''
        elif char in ('"', "'"):
            quote = char
        elif char == '#':
            return line[:i]
    return line


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
            body_lines = [_strip_comment(line).rstrip()
                          for line in lines[start:index]]
            code = '\n'.join(line for line in body_lines if line.strip())
            functions.append((start + 1, name, args, code + '\n'))
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
