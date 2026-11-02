"""Homework 3, Problem 5: recursion.

Daniel Farafonov
"""

import sys
import time
import turtle
from typing import Dict, List, Optional, Sequence, Tuple

from testif import testif

DIGITS = '0123456789ABCDEFGHIJKLMNOPQ'

# leaf shape: branch angle and how much each part shrinks per level
VEIN_ANGLE = 45
VEIN_SCALE = 0.45
MIDRIB_SCALE = 0.8
BLADE_SCALE = 0.6
CURVE_ANGLE = 6

# memo for Cnk_m: maps (n, k) to n-choose-k
cnk_memo: Dict[Tuple[int, int], int] = {}


def _leaf_branch(t: turtle.Turtle, level: int, length: float,
                 curve: float) -> None:
    """Draws one recursive leaf branch and returns the turtle to its
    starting position and heading.

    Each branch is a straight segment followed by a vein on each side and
    a shorter continuation of the midrib, each a smaller branch. At level 1
    the veins and the tip are single short lines. A non-zero curve bends
    the midrib to the right by curve degrees at every level.
    """
    t.forward(length)
    t.right(curve)
    if level <= 1:
        for angle in (VEIN_ANGLE, -VEIN_ANGLE, 0):
            t.left(angle)
            t.forward(length * VEIN_SCALE)
            t.backward(length * VEIN_SCALE)
            t.right(angle)
    else:
        t.left(VEIN_ANGLE)
        _leaf_branch(t, level - 1, length * VEIN_SCALE, curve)
        t.right(2 * VEIN_ANGLE)
        _leaf_branch(t, level - 1, length * VEIN_SCALE, curve)
        t.left(VEIN_ANGLE)
        _leaf_branch(t, level - 1, length * MIDRIB_SCALE, curve)
    t.left(curve)
    t.backward(length)


def _draw_leaf(level: int, length: float, curve: float) -> None:
    """Sets up a turtle, draws the petiole of the given length pointing up,
    then draws the recursive leaf blade on top of it.

    Precondition: level >= 1, length > 0.
    """
    if level < 1 or length <= 0:
        raise ValueError('level must be >= 1 and length > 0')
    screen = turtle.Screen()
    screen.setup(800, 800)
    turtle.delay(0)
    screen.tracer(0)
    t = turtle.Turtle()
    t.hideturtle()
    t.color('darkgreen')
    t.up()
    t.goto(0, -250)
    t.down()
    t.left(90)  # the turtle starts facing east; turn it to stand up
    t.pensize(3)
    t.forward(length)
    t.pensize(1)
    _leaf_branch(t, level, length * BLADE_SCALE, curve)
    screen.update()


def draw_leaf_straight(level: int, length: float) -> None:
    """Draws a straight recursive leaf with the given recursion level and
    petiole (lower stem) length.

    Precondition: level >= 1, length > 0.
    """
    _draw_leaf(level, length, 0)


def draw_leaf_curved(level: int, length: float) -> None:
    """Draws a recursive leaf whose midrib curves to the right, with the
    given recursion level and petiole (lower stem) length.

    Precondition: level >= 1, length > 0.
    """
    _draw_leaf(level, length, CURVE_ANGLE)


def strB(n: int, base: int = 10) -> str:
    """Returns the representation of n in the given base, recursively.

    Digits greater than 9 are the letters 'A' to 'Z'.
    Precondition: n is an int >= 0, base is an int with 2 <= base <= 26.
    Raises ValueError if a precondition is not met.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError('n must be a non-negative int')
    if not 2 <= base <= 26:
        raise ValueError('base must be between 2 and 26')
    if n < base:
        return DIGITS[n]
    return strB(n // base, base) + DIGITS[n % base]


def Cnk(n: int, k: int) -> int:
    """Returns n-choose-k with plain recursion, without memoization.

    Precondition: 0 <= k <= n.
    """
    if k == 0 or k == n:
        return 1
    return Cnk(n - 1, k - 1) + Cnk(n - 1, k)


def Cnk_m(n: int, k: int) -> int:
    """Returns n-choose-k recursively, memoizing results in cnk_memo.

    Precondition: n and k are ints with 0 <= k <= n.
    Raises ValueError if a precondition is not met.
    """
    if not 0 <= k <= n:
        raise ValueError('need 0 <= k <= n')
    if k == 0 or k == n:
        return 1
    if (n, k) not in cnk_memo:
        cnk_memo[(n, k)] = Cnk_m(n - 1, k - 1) + Cnk_m(n - 1, k)
    return cnk_memo[(n, k)]


def run_Cnk(pairs: Optional[Sequence[Tuple[int, int]]] = None) -> None:
    """Prints n-choose-k for each (n, k) in pairs with the time it took,
    comparing Cnk (no memoization, only for small n) and Cnk_m.
    """
    if pairs is None:
        pairs = [(5, 2), (10, 5), (20, 10), (24, 12), (50, 25), (100, 50)]
    for n, k in pairs:
        cnk_memo.clear()  # time Cnk_m without earlier results
        start = time.perf_counter()
        value = Cnk_m(n, k)
        memo_time = time.perf_counter() - start
        line = f'C({n}, {k}) = {value}, Cnk_m: {memo_time:.6f} s'
        if n <= 24:
            start = time.perf_counter()
            Cnk(n, k)
            line += f', Cnk: {time.perf_counter() - start:.6f} s'
        print(line)


def make_pairs(seq1: Sequence, seq2: Sequence,
               acc: Optional[List[tuple]] = None) -> List[tuple]:
    """Returns the list of tuples (seq1[i], seq2[i]) for every index i
    of the shorter sequence, built recursively in the accumulator acc.

    Precondition: seq1 and seq2 are sequences; acc is None or a list.
    """
    if acc is None:
        acc = []
    if not seq1 or not seq2:
        return acc
    acc.append((seq1[0], seq2[0]))
    return make_pairs(seq1[1:], seq2[1:], acc)


def test_strB() -> None:
    """Unit tests for strB."""
    testif(strB(0) == '0', 'strB zero')
    testif(strB(255, base=16) == 'FF', 'strB base 16')
    testif(strB(5, base=2) == '101', 'strB base 2')
    testif(strB(675, base=26) == 'PP', 'strB base 26', strB(675, base=26))


def test_Cnk_m() -> None:
    """Unit tests for Cnk_m."""
    testif(Cnk_m(5, 0) == 1 and Cnk_m(5, 5) == 1, 'Cnk_m base cases')
    testif(Cnk_m(5, 2) == 10, 'Cnk_m(5, 2)')
    testif(Cnk_m(30, 15) == 155117520, 'Cnk_m(30, 15)')
    testif(Cnk_m(100, 50) == 100891344545564193334812497256,
           'Cnk_m(100, 50)')


def test_make_pairs() -> None:
    """Unit tests for make_pairs."""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)],
           'make_pairs equal lengths')
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)],
           'make_pairs second shorter')
    testif(make_pairs([1, 2, 3], [4, 5, 6, 7, 8, 9])
           == [(1, 4), (2, 5), (3, 6)], 'make_pairs first shorter')
    testif(make_pairs([], [4, 5, 6]) == [], 'make_pairs first empty')
    testif(make_pairs([1, 2, 3], []) == [], 'make_pairs second empty')


def main() -> None:
    """Runs the unit tests and run_Cnk, then draws a leaf.

    Draws the curved leaf if the program is started with the argument
    "curved", otherwise the straight leaf.
    """
    test_strB()
    test_Cnk_m()
    test_make_pairs()
    print()
    run_Cnk()

    if sys.argv[1:] == ['curved']:
        draw_leaf_curved(6, 120)
    else:
        draw_leaf_straight(6, 120)
    print('Click the turtle window to close it.')
    turtle.exitonclick()


if __name__ == '__main__':
    main()
