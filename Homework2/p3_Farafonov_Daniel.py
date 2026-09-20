"""Homework 2, Problem 3: a simplified social network.

Daniel Farafonov
"""

import csv

from testif import testif


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Adds a new user with no friends to a social network.

    Args:
        sn: Social network dict mapping username to
            (full_name, [friend, ...]).
        username: Username of the user to add.
        fullname: Full name of the user to add.

    Returns:
        True if the user was added, False if username already existed.

    Raises:
        TypeError: If sn is not a dict.
    """
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except TypeError as error:
        print(f'Error: could not add user "{username}": {error}')
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Adds a mutual friend link between two users of a social network.

    Args:
        sn: Social network dict mapping username to
            (full_name, [friend, ...]).
        user1: Username of the first user.
        user2: Username of the second user.

    Returns:
        True if the link was added, False if user1 or user2 is not
        found in sn.

    Raises:
        TypeError: If sn is not a dict.
    """
    try:
        if user1 not in sn or user2 not in sn:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except TypeError as error:
        print(f'Error: could not link "{user1}" and "{user2}": {error}')
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    """Finds every friend of user1 within a given link distance.

    Friends at distance 1 are the users in user1's immediate friend
    list. Friends at distance 2 are those, plus the friends of those,
    and so on. Avoids revisiting a user through a cycle.

    Args:
        sn: Social network dict mapping username to
            (full_name, [friend, ...]).
        user1: Username to start from.
        distance: Maximum link distance to explore (positive int).

    Returns:
        A list of usernames reachable within distance links of user1,
        in breadth-first order. Empty if user1 is not found in sn or
        distance is not positive.

    Raises:
        TypeError: If sn is not a dict.
    """
    try:
        if user1 not in sn or distance < 1:
            return []

        visited = {user1}
        result = []
        frontier = [user1]
        for _ in range(distance):
            next_frontier = []
            for user in frontier:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.add(friend)
                        result.append(friend)
                        next_frontier.append(friend)
            frontier = next_frontier
            if not frontier:
                break
        return result
    except TypeError as error:
        print(f'Error: could not compute friends of "{user1}": {error}')
        raise


def save_network(filename: str, sn: dict) -> None:
    """Saves a social network dictionary to a CSV file.

    Each row of the file has format: username,fullname,friend1,friend2,...

    Args:
        filename: Path of the CSV file to create.
        sn: Social network dict mapping username to
            (full_name, [friend, ...]).

    Raises:
        OSError: If filename cannot be written (e.g. FileNotFoundError).
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname] + friends)
    except OSError as error:
        print(f'Error: could not save network to "{filename}": {error}')
        raise


def load_network(filename: str) -> dict:
    """Loads a social network dictionary from a CSV file.

    Args:
        filename: Path of a CSV file previously written by
            save_network.

    Returns:
        The social network dict mapping username to
        (full_name, [friend, ...]).

    Raises:
        OSError: If filename cannot be read (e.g. FileNotFoundError).
    """
    try:
        sn = {}
        with open(filename, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if not row:
                    continue
                username, fullname, *friends = row
                sn[username] = (fullname, friends)
        return sn
    except OSError as error:
        print(f'Error: could not load network from "{filename}": {error}')
        raise


def test() -> None:
    """Extra credit: tests parts a)-e) using the testif module."""
    sn = {}
    testif(add_user(sn, 'alice', 'Alice Smith'), 'add_user new user')
    testif(not add_user(sn, 'alice', 'Alice Smith'),
           'add_user duplicate user')
    add_user(sn, 'maria', 'Maria Cortez')
    add_user(sn, 'joe', 'Joseph Adams')

    testif(add_friend(sn, 'alice', 'maria'), 'add_friend valid users')
    testif(not add_friend(sn, 'alice', 'bob'), 'add_friend missing user')
    testif('maria' in sn['alice'][1] and 'alice' in sn['maria'][1],
           'add_friend creates a mutual link')

    add_friend(sn, 'maria', 'joe')
    testif(get_friends(sn, 'alice', 1) == ['maria'], 'get_friends distance 1')
    testif(get_friends(sn, 'alice', 2) == ['maria', 'joe'],
           'get_friends distance 2')
    testif(get_friends(sn, 'nobody', 1) == [], 'get_friends unknown user')

    save_network('test_network.csv', sn)
    loaded = load_network('test_network.csv')
    testif(loaded == sn, 'save_network/load_network round trip')


def main() -> None:
    """Builds the example social network and tests all functions."""
    sn = {
        'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria']),
    }
    print('Social network:', sn, '\n')

    print('add_user("eve", ...) ->', add_user(sn, 'eve', 'Evelyn Cooper'))
    print('add_user("frank", "Frank Ocean") ->',
          add_user(sn, 'frank', 'Frank Ocean'))
    print('add_friend("frank", "alice") ->',
          add_friend(sn, 'frank', 'alice'))
    print('add_friend("frank", "ghost") ->',
          add_friend(sn, 'frank', 'ghost'))

    print('get_friends("alice", 1) ->', get_friends(sn, 'alice', 1))
    print('get_friends("alice", 2) ->', get_friends(sn, 'alice', 2))

    save_network('social_network.csv', sn)
    loaded_sn = load_network('social_network.csv')
    print('Network reloaded from CSV matches original:', loaded_sn == sn)

    print('\nExtra credit tests:')
    test()


if __name__ == '__main__':
    main()
