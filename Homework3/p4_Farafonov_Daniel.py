"""Homework 3, Problem 4: non-interactive text editor.

Daniel Farafonov

File I/O errors (e.g. FileNotFoundError, OSError) are not caught by these
functions; they are passed to the caller. Files are read entirely into
memory and only written back after the new content has been computed, so
a file is not changed when an error occurs.
"""

import os
from typing import List

from testif import testif


def _read_all(filename: str) -> str:
    """Returns the whole content of the utf-8 file filename."""
    with open(filename, 'r', encoding='utf-8') as text_file:
        return text_file.read()


def _write_all(filename: str, content: str) -> None:
    """Overwrites the utf-8 file filename with content."""
    with open(filename, 'w', encoding='utf-8') as text_file:
        text_file.write(content)


def _check_str(value: str, name: str) -> None:
    """Raises TypeError if value is not a str."""
    if not isinstance(value, str):
        raise TypeError(f'{name} must be a str')


def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Returns the file content between positions from_ and to.

    The range is half-open: [from_, to). If to == -1, returns from from_
    to the end of the file. (from_ has a trailing underscore because from
    is a Python keyword.)
    Precondition: 0 <= from_ <= to <= file length, or to == -1.
    Raises IndexError if to exceeds the file length or the range is
    invalid, FileNotFoundError if the file does not exist.
    """
    content = _read_all(filename)
    if to == -1:
        to = len(content)
    if to > len(content):
        raise IndexError(f'to={to} exceeds file length {len(content)}')
    if not 0 <= from_ <= to:
        raise IndexError(f'invalid range [{from_}, {to})')
    return content[from_:to]


def ed_find(filename: str, search_str: str) -> List[int]:
    """Returns the positions in the file where search_str starts.

    Overlapping occurrences are all reported. Returns [] if search_str is
    not found.
    Precondition: search_str is a non-empty str.
    Raises ValueError if search_str is empty, FileNotFoundError if the
    file does not exist.
    """
    _check_str(search_str, 'search_str')
    if not search_str:
        raise ValueError('search_str must not be empty')
    content = _read_all(filename)
    positions = []
    index = content.find(search_str)
    while index != -1:
        positions.append(index)
        index = content.find(search_str, index + 1)
    return positions


def ed_replace(filename: str, search_str: str, replace_with: str,
               occurrence: int = -1) -> int:
    """Replaces search_str with replace_with in the file.

    If occurrence == -1, replaces all (non-overlapping) occurrences.
    If occurrence >= 0, replaces only the occurrence with that index
    (0 is the first); nothing is replaced if there are fewer occurrences.
    Returns the number of replacements made.
    Precondition: search_str is a non-empty str, occurrence >= -1.
    Postcondition: the file is only rewritten if something was replaced.
    Raises ValueError for an empty search_str or occurrence < -1,
    FileNotFoundError if the file does not exist.
    """
    _check_str(search_str, 'search_str')
    _check_str(replace_with, 'replace_with')
    if not search_str:
        raise ValueError('search_str must not be empty')
    if occurrence < -1:
        raise ValueError('occurrence must be -1 or >= 0')
    content = _read_all(filename)

    if occurrence == -1:
        count = content.count(search_str)
        new_content = content.replace(search_str, replace_with)
    else:
        index = content.find(search_str)
        for _ in range(occurrence):
            if index == -1:
                break
            index = content.find(search_str, index + len(search_str))
        if index == -1:
            return 0
        count = 1
        new_content = (content[:index] + replace_with
                       + content[index + len(search_str):])

    if count:
        _write_all(filename, new_content)
    return count


def ed_append(filename: str, string: str) -> int:
    """Appends string to the end of the file, creating it if needed.

    Returns the number of characters written.
    Precondition: string is a str.
    Raises TypeError if string is not a str.
    """
    _check_str(string, 'string')
    with open(filename, 'a', encoding='utf-8') as text_file:
        return text_file.write(string)


def test_ed_find() -> None:
    """Unit tests for ed_find."""
    fn = 'test_ed_find.txt'
    _write_all(fn, '01234567890123456789')
    testif(ed_find(fn, '345') == [3, 13], 'ed_find two matches')
    testif(ed_find(fn, '356') == [], 'ed_find no match')
    testif(ed_find(fn, '0') == [0, 10], 'ed_find single char')
    _write_all(fn, 'aaaa')
    testif(ed_find(fn, 'aa') == [0, 1, 2], 'ed_find overlapping matches')
    try:
        ed_find(fn, '')
        testif(False, 'ed_find empty string raises ValueError')
    except ValueError:
        testif(True, 'ed_find empty string raises ValueError')
    try:
        ed_find('no_such_file.txt', 'a')
        testif(False, 'ed_find missing file raises FileNotFoundError')
    except FileNotFoundError:
        testif(True, 'ed_find missing file raises FileNotFoundError')
    os.remove(fn)


def test_ed_replace() -> None:
    """Unit tests for ed_replace."""
    fn = 'test_ed_replace.txt'
    original = '01234567890123456789'

    _write_all(fn, original)
    count = ed_replace(fn, '345', 'ABCDE', 1)
    testif(count == 1 and _read_all(fn) == '0123456789012ABCDE6789',
           'ed_replace second occurrence', _read_all(fn))

    _write_all(fn, original)
    count = ed_replace(fn, '345', 'ABCDE')
    testif(count == 2 and _read_all(fn) == '012ABCDE6789012ABCDE6789',
           'ed_replace all occurrences', _read_all(fn))

    _write_all(fn, original)
    count = ed_replace(fn, '345', 'ABCDE', 0)
    testif(count == 1 and _read_all(fn) == '012ABCDE67890123456789',
           'ed_replace first occurrence', _read_all(fn))

    _write_all(fn, original)
    count = ed_replace(fn, '345', 'ABCDE', 5)
    testif(count == 0 and _read_all(fn) == original,
           'ed_replace occurrence too large leaves file unchanged')

    count = ed_replace(fn, 'xyz', 'ABCDE')
    testif(count == 0 and _read_all(fn) == original,
           'ed_replace no match leaves file unchanged')

    try:
        ed_replace(fn, '345', 'ABCDE', -2)
        testif(False, 'ed_replace invalid occurrence raises ValueError')
    except ValueError:
        testif(_read_all(fn) == original,
               'ed_replace invalid occurrence raises ValueError')
    os.remove(fn)


def main() -> None:
    """Shows how to use the ed_ functions, then runs the unit tests."""
    fn = 'file1.txt'
    if os.path.exists(fn):
        os.remove(fn)

    print('ed_append returned', ed_append(fn, '0123456789'))
    print('ed_append returned', ed_append(fn, '0123456789'))
    print('ed_read(fn):', ed_read(fn))
    print('ed_read(fn, 3, 9):', ed_read(fn, 3, 9))
    print('ed_read(fn, 3):', ed_read(fn, 3))
    try:
        ed_read(fn, 0, 100)
    except IndexError as error:
        print('ed_read(fn, 0, 100) raised IndexError:', error)
    print('ed_find(fn, "345"):', ed_find(fn, '345'))
    print('ed_find(fn, "356"):', ed_find(fn, '356'))

    print('ed_replace(fn, "345", "ABCDE", 1) returned',
          ed_replace(fn, '345', 'ABCDE', 1))
    print('  file content:', ed_read(fn))
    print('ed_replace(fn, "ABCDE", "345") returned',
          ed_replace(fn, 'ABCDE', '345'))
    print('ed_replace(fn, "345", "ABCDE") returned',
          ed_replace(fn, '345', 'ABCDE'))
    print('  file content:', ed_read(fn))

    try:
        ed_read('no_such_file.txt')
    except FileNotFoundError as error:
        print('ed_read on a missing file raised FileNotFoundError:', error)
    os.remove(fn)

    print()
    print('Unit tests:')
    test_ed_find()
    test_ed_replace()


if __name__ == '__main__':
    main()
