"""Unit tests for find_large_files and absolute_path (Homework 3, Problem 6).

Daniel Farafonov
"""

import unittest

from p6_Farafonov_Daniel import Entry, File, Folder, find_large_files


class StorageTest(unittest.TestCase):
    """Tests for find_large_files and Entry.absolute_path."""

    def setUp(self) -> None:
        """Builds root/{a.txt, docs/{b.txt, deep/{c.bin}}, empty/}."""
        self.root = Folder('root')
        self.a = File('a.txt', 100, self.root)
        self.docs = Folder('docs', self.root)
        self.b = File('b.txt', 500, self.docs)
        self.deep = Folder('deep', self.docs)
        self.c = File('c.bin', 1000, self.deep)
        self.empty = Folder('empty', self.root)

    def test_find_large_files_from_folder(self) -> None:
        self.assertEqual(find_large_files(self.root, 500), [self.b, self.c])

    def test_find_large_files_all(self) -> None:
        self.assertEqual(find_large_files(self.root, 0),
                         [self.a, self.b, self.c])

    def test_find_large_files_none(self) -> None:
        self.assertEqual(find_large_files(self.root, 1001), [])

    def test_find_large_files_nested_folder(self) -> None:
        self.assertEqual(find_large_files(self.docs, 1), [self.b, self.c])

    def test_find_large_files_empty_folder(self) -> None:
        self.assertEqual(find_large_files(self.empty, 0), [])

    def test_find_large_files_on_file(self) -> None:
        self.assertEqual(find_large_files(self.c, 1000), [self.c])
        self.assertEqual(find_large_files(self.a, 101), [])

    def test_absolute_path_root(self) -> None:
        self.assertEqual(self.root.absolute_path(), [self.root])

    def test_absolute_path_deep_file(self) -> None:
        self.assertEqual(self.c.absolute_path(),
                         [self.c, self.deep, self.docs, self.root])

    def test_absolute_path_folder(self) -> None:
        self.assertEqual(self.deep.absolute_path(),
                         [self.deep, self.docs, self.root])

    def test_absolute_path_detached_file(self) -> None:
        lone = File('lone.txt', 5)
        self.assertEqual(lone.absolute_path(), [lone])

    def test_size_handles_files_and_folders(self) -> None:
        self.assertEqual(self.root.size(), 1600)
        self.assertEqual(self.empty.size(), 0)

    def test_invalid_entries(self) -> None:
        with self.assertRaises(ValueError):
            File('bad.txt', -1)
        with self.assertRaises(ValueError):
            self.root.add(self.a)  # already has a parent
        with self.assertRaises(NotImplementedError):
            Entry('plain').size()


if __name__ == '__main__':
    unittest.main(verbosity=2)
