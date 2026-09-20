"""Homework 2, Problem 2: comprehensions.

Daniel Farafonov
"""


def main() -> None:
    """Builds and displays the results for parts a-f."""

    # a) All (a, b, c, d), 1 <= a,b,c,d <= 10, distinct, a^2+b^2 = c^2+d^2.
    pythagorean_quads = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4 and a ** 2 + b ** 2 == c ** 2 + d ** 2
    ]
    print('a)', pythagorean_quads)

    # b) (lowercase, length) for strings shorter than 5 characters.
    words = ['One', 'SEVEN', 'three', 'two', 'Ten']
    short_words = [(word.lower(), len(word)) for word in words
                    if len(word) < 5]
    print('b)', short_words)

    # c) "Firstname M. Lastname" from "Firstname Middlename Lastname".
    names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
    abbreviated_names = [
        f'{parts[0]} {parts[1][0]}. {parts[2]}'
        for parts in (name.split() for name in names)
    ]
    print('c)', abbreviated_names)

    # d) Anagram pairs (case insensitive) between lst1 and lst2.
    lst1 = ['Spam', 'Trams', 'Elbows', 'Tops', 'Astral']
    lst2 = ['Bowels', 'Sample', 'Altars', 'Stop', 'Course', 'Smart']
    anagram_pairs = [
        (word1, word2)
        for word1 in lst1
        for word2 in lst2
        if sorted(word1.lower()) == sorted(word2.lower())
    ]
    print('d)', anagram_pairs)

    # e) Map each string in s to its length.
    s = ['one', 'two', 'three']
    lengths = {word: len(word) for word in s}
    print('e)', lengths)

    # f) Map index -> character for each vowel in text (case insensitive).
    text = 'Hello world'
    vowel_positions = {
        index: char for index, char in enumerate(text)
        if char.lower() in 'aeiou'
    }
    print('f)', vowel_positions)


if __name__ == '__main__':
    main()
