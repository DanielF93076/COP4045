"""Homework 2, Problem 3: a simplified social network.

Daniel Farafonov
"""

import csv

from testif import testif


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Adds a new user with no friends; returns False if username already exists."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except TypeError as error:
        print(f'Error: could not add user "{username}": {error}')
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Adds a mutual friend link; returns False if user1 or user2 is not in sn."""
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
    """Returns user1's friends up to distance links away, breadth-first, no repeats."""
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
    """Writes sn to filename as CSV rows: username,fullname,friend1,friend2,..."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname] + friends)
    except OSError as error:
        print(f'Error: could not save network to "{filename}": {error}')
        raise


def load_network(filename: str) -> dict:
    """Reads a social network dict from a CSV file written by save_network."""
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
    testif(not add_user(sn, 'alice', 'Alice Smith'), 'add_user duplicate')
    add_user(sn, 'maria', 'Maria Cortez')
    testif(add_friend(sn, 'alice', 'maria'), 'add_friend valid users')
    testif(not add_friend(sn, 'alice', 'bob'), 'add_friend missing user')
    testif(get_friends(sn, 'alice', 1) == ['maria'], 'get_friends distance 1')
    save_network('test_network.csv', sn)
    testif(load_network('test_network.csv') == sn, 'save/load round trip')


def main() -> None:
    """Builds the example social network and tests all functions."""
    sn = {
        'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria']),
    }
    print('Social network:', sn)
    print('add_user("frank", ...) ->', add_user(sn, 'frank', 'Frank Ocean'))
    print('add_friend("frank", "alice") ->',
          add_friend(sn, 'frank', 'alice'))
    print('get_friends("alice", 2) ->', get_friends(sn, 'alice', 2))

    save_network('social_network.csv', sn)
    print('Reloaded network matches original:',
          load_network('social_network.csv') == sn)

    print('\nExtra credit tests:')
    test()


if __name__ == '__main__':
    main()
