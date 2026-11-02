"""Homework 3, Problem 6: storage size of files and folders.

Daniel Farafonov
"""

from typing import List, Optional, Tuple


class Entry:
    """An entry (file or folder) in a storage system."""

    def __init__(self, name: str, parent: Optional['Folder'] = None) -> None:
        """Creates an entry with the given name."""
        if not name:
            raise ValueError('name must not be empty')
        self.name = name
        self._parent = None
        if parent is not None:
            parent.add(self)

    def parent(self) -> Optional['Folder']:
        """Returns the folder containing this entry, or None for a root."""
        return self._parent

    def size(self) -> int:
        """Returns the number of bytes used by this entry."""
        raise NotImplementedError('size() must be overridden')

    def absolute_path(self) -> List['Entry']:
        """Returns [self, parent, ..., root], computed recursively."""
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()

    def __str__(self) -> str:
        """Returns the entry's name."""
        return self.name

    def __repr__(self) -> str:
        """Returns a short description of the entry."""
        return f'{type(self).__name__}({self.name!r})'


class File(Entry):
    """A file that uses a fixed number of bytes."""

    def __init__(self, name: str, bytes_used: int,
                 parent: Optional['Folder'] = None) -> None:
        """Creates a file using bytes_used bytes."""
        if bytes_used < 0:
            raise ValueError('bytes_used must be nonnegative')
        self.bytes_used = bytes_used
        super().__init__(name, parent)

    def size(self) -> int:
        """Returns the number of bytes used by the file."""
        return self.bytes_used


class Folder(Entry):
    """A folder that contains files and other folders."""

    def __init__(self, name: str, parent: Optional['Folder'] = None) -> None:
        """Creates an empty folder."""
        self._children: List[Entry] = []
        super().__init__(name, parent)

    def add(self, entry: Entry) -> None:
        """Adds entry to the children and becomes its parent."""
        if entry.parent() is not None:
            raise ValueError(f'{entry.name} already has a parent')
        entry._parent = self
        self._children.append(entry)

    def children(self) -> Tuple[Entry, ...]:
        """Returns a tuple with this folder's children."""
        return tuple(self._children)

    def size(self) -> int:
        """Returns the total size of all children, nested ones included."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> List[File]:
    """Returns the files under entry of at least minimum_size bytes."""
    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []
    large_files = []
    for child in entry.children():
        large_files.extend(find_large_files(child, minimum_size))
    return large_files


def path_string(entry: Entry) -> str:
    """Returns entry's absolute path as text, e.g. /university/cs/a.txt."""
    names = [e.name for e in reversed(entry.absolute_path())]
    return '/' + '/'.join(names)


def main() -> None:
    """Builds a folder tree and demonstrates the classes and functions."""
    university = Folder('university')
    File('budget.xlsx', 40_000, university)
    engineering = Folder('engineering', university)
    File('syllabus.pdf', 250_000, engineering)
    cs = Folder('cs', engineering)
    File('grades.csv', 12_000, cs)
    cop4045 = Folder('cop4045', cs)
    File('lecture.mp4', 900_000, cop4045)
    File('notes.txt', 3_000, cop4045)
    Folder('empty', cop4045)

    print('Entries (polymorphic size() calls):')
    for entry in (university, engineering, cs, cop4045,
                  *cop4045.children()):
        print(f'  {type(entry).__name__:6s} {path_string(entry):50s} '
              f'{entry.size():>9,d} bytes')

    print()
    print(f'university.size() = {university.size():,d} bytes')

    for minimum in (10_000, 300_000):
        found = find_large_files(university, minimum)
        print(f'Files of at least {minimum:,d} bytes: '
              f'{[str(f) for f in found]}')

    print()
    lecture = cop4045.children()[0]
    print('lecture.absolute_path() =', lecture.absolute_path())
    print('As a path string:', path_string(lecture))
    print('university.absolute_path() =', university.absolute_path())


if __name__ == '__main__':
    main()
