"""Homework 3, Problem 1: N-dimensional vector class.

Daniel Farafonov
"""

from numbers import Number
from typing import Sequence, Union

from testif import testif


class NVector:
    """An N-dimensional vector of real numbers stored in a list."""

    def __init__(self, *args: Union[Number, Sequence[Number]]) -> None:
        """Creates a vector from one sequence or from two or more numbers.

        Precondition: either one argument that is a sequence of numbers,
            or two or more number arguments.
        Postcondition: the vector owns a new list with the given elements.
        Raises TypeError if called with no arguments, with a single
            argument that is not a sequence, or with non-number elements.
        """
        if not args:
            raise TypeError('NVector needs at least one argument')
        if len(args) == 1:
            self.elements = list(args[0])
        else:
            self.elements = list(args)
        if not all(isinstance(e, Number) for e in self.elements):
            raise TypeError('NVector elements must be numbers')

    def __len__(self) -> int:
        """Returns the number of elements (the vector's dimension)."""
        return len(self.elements)

    def __getitem__(self, index: int) -> Number:
        """Returns the element at index; negative indices work like lists.

        Raises IndexError if index is out of range, TypeError if index is
        not an int.
        """
        if not isinstance(index, int):
            raise TypeError('NVector index must be an int')
        return self.elements[index]

    def __setitem__(self, index: int, value: Number) -> None:
        """Sets the element at index to value.

        Precondition: index is an int in range, value is a number.
        Postcondition: self[index] == value.
        Raises IndexError if index is out of range, TypeError if index is
        not an int or value is not a number.
        """
        if not isinstance(index, int):
            raise TypeError('NVector index must be an int')
        if not isinstance(value, Number):
            raise TypeError('NVector elements must be numbers')
        self.elements[index] = value

    def __str__(self) -> str:
        """Returns the vector as a string, e.g. [3, 0, 1, -1]."""
        return str(self.elements)

    def __repr__(self) -> str:
        """Returns a string that recreates the vector when evaluated."""
        return f'NVector({self.elements})'

    def __eq__(self, other: object) -> bool:
        """Returns True if other is an NVector with equal elements."""
        if not isinstance(other, NVector):
            return False
        return self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Returns True if self and other are not equal."""
        return not self == other

    def __add__(self, other: Union['NVector', Number]) -> 'NVector':
        """Returns self + other, element-wise for a vector or per element
        for a number.

        Raises ValueError if other is a vector of a different length.
        Returns NotImplemented for unsupported operand types.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError('NVector lengths differ')
            return NVector([a + b for a, b in zip(self.elements,
                                                  other.elements)])
        if isinstance(other, Number):
            return NVector([a + other for a in self.elements])
        return NotImplemented

    def __radd__(self, other: Number) -> 'NVector':
        """Returns other + self for a number other."""
        return self + other

    def __mul__(self, other: Union['NVector', Number]) -> Number:
        """Returns the scalar product of self and other.

        For a vector other, returns the sum of self[i] * other[i].
        For a number other, returns the sum of self[i] * other.
        Raises ValueError if other is a vector of a different length.
        Returns NotImplemented for unsupported operand types.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError('NVector lengths differ')
            return sum(a * b for a, b in zip(self.elements, other.elements))
        if isinstance(other, Number):
            return sum(a * other for a in self.elements)
        return NotImplemented

    def __rmul__(self, other: Number) -> Number:
        """Returns other * self for a number other."""
        return self * other

    @classmethod
    def zeros(cls, n: int) -> 'NVector':
        """Returns a new n-dimensional vector with all elements 0.

        Precondition: n is an int >= 1.
        Raises ValueError if n < 1.
        """
        if n < 1:
            raise ValueError('NVector dimension must be at least 1')
        return cls([0] * n)


def main() -> None:
    """Tests the NVector class with testif."""
    source = [3, 0, 1, -1]
    v_list = NVector(source)
    v_tuple = NVector((3, 0, 1, -1))
    v_args = NVector(3, 0, 1, -1)
    testif(v_list.elements == source, 'a) constructor from list')
    testif(v_list.elements is not source, 'a) constructor copies the list')
    testif(v_tuple.elements == source, 'a) constructor from tuple')
    testif(v_args.elements == source, 'b) constructor from arguments')
    try:
        NVector(5)
        testif(False, 'a) scalar argument raises TypeError')
    except TypeError:
        testif(True, 'a) scalar argument raises TypeError')
    try:
        NVector('abc')
        testif(False, 'a) non-number elements raise TypeError')
    except TypeError:
        testif(True, 'a) non-number elements raise TypeError')

    testif(len(v_args) == 4, 'c) __len__')

    testif(v_args[1] == 0, 'd) __getitem__')
    testif(v_args[-2] == 1, 'd) __getitem__ negative index')
    try:
        v_args[4]
        testif(False, 'd) __getitem__ raises IndexError')
    except IndexError:
        testif(True, 'd) __getitem__ raises IndexError')

    v = NVector(3, 0, 1, -1)
    v[2] = 5
    testif(v == NVector([3, 0, 5, -1]), 'e) __setitem__')
    v[-1] = 7
    testif(v[3] == 7, 'e) __setitem__ negative index')
    try:
        v[10] = 1
        testif(False, 'e) __setitem__ raises IndexError')
    except IndexError:
        testif(True, 'e) __setitem__ raises IndexError')

    testif(str(v_args) == '[3, 0, 1, -1]', 'f) __str__', str(v_args))

    testif(v_list == v_tuple, 'g) __eq__')
    testif(not v_list == NVector(1, 2, 3, 4), 'g) __eq__ different')
    testif(not v_list == [3, 0, 1, -1], 'g) __eq__ with non-NVector')
    testif(v_list != NVector(1, 2, 3, 4), 'g) __ne__')
    testif(not v_list != v_tuple, 'g) __ne__ equal vectors')

    other = NVector([1, 2, 3, 4])
    testif(v_list + other == NVector([4, 2, 4, 3]), 'h) __add__ vector')
    testif(v_list + 10 == NVector([13, 10, 11, 9]), 'h) __add__ number')
    testif(10 + v_list == NVector([13, 10, 11, 9]), 'h) __radd__')
    try:
        v_list + NVector(1, 2)
        testif(False, 'h) __add__ raises ValueError')
    except ValueError:
        testif(True, 'h) __add__ raises ValueError')

    testif(v_list * other == 2, 'i) __mul__ vector')
    testif(v_list * 2 == 6, 'i) __mul__ number')
    testif(2 * v_list == 6, 'i) __rmul__')

    testif(NVector.zeros(3) == NVector(0, 0, 0), 'j) zeros')


if __name__ == '__main__':
    main()
