"""Homework 2, Problem 4: IMDB top movies analysis.

Daniel Farafonov
"""

import csv


def load_top_rated(filename: str) -> dict:
    """Returns {(title, year): rating} from imdb-top-rated.csv."""
    try:
        top_rated = {}
        with open(filename, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            rating_column = reader.fieldnames[-1]
            for row in reader:
                top_rated[(row['Title'], row['Year'])] = float(
                    row[rating_column])
        return top_rated
    except OSError as error:
        print(f'Error: could not read file "{filename}": {error}')
        raise


def load_top_grossing(filename: str) -> dict:
    """Returns {(title, year): box office} from imdb-top-grossing.csv."""
    try:
        top_grossing = {}
        with open(filename, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                top_grossing[(row['Title'], row['Year'])] = int(
                    row['USA Box Office'])
        return top_grossing
    except OSError as error:
        print(f'Error: could not read file "{filename}": {error}')
        raise


def load_casts(filename: str) -> dict:
    """Returns {(title, year): (director, [actors])} from imdb-top-casts.csv."""
    try:
        casts = {}
        with open(filename, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) < 3:
                    continue
                title, year, director, *actors = row
                actors = [actor for actor in actors if actor]
                casts[(title, year)] = (director, actors)
        return casts
    except OSError as error:
        print(f'Error: could not read file "{filename}": {error}')
        raise


def _print_ranking(ranking: list, limit: int = None) -> None:
    """Prints up to limit numbered entries from ranking (all if limit is None)."""
    entries = ranking if limit is None else ranking[:limit]
    for position, entry in enumerate(entries, start=1):
        print(position, entry)


def display_top_collaborations(casts_filename: str, rated_filename: str,
                                limit: int = None) -> None:
    """Prints director/actor pairs ranked by movies together that are also top rated."""
    casts = load_casts(casts_filename)
    top_rated = load_top_rated(rated_filename)

    collaborations = {}
    for movie, (director, actors) in casts.items():
        if movie not in top_rated:
            continue
        for actor in actors:
            key = (director, actor)
            collaborations[key] = collaborations.get(key, 0) + 1

    ranking = sorted(
        ((director, actor, count)
         for (director, actor), count in collaborations.items()),
        key=lambda entry: entry[2], reverse=True)

    print('Top director/actor collaborations (top-rated movies):')
    _print_ranking(ranking, limit)


def display_top_actors(casts_filename: str, grossing_filename: str,
                        limit: int = None) -> None:
    """Prints actors ranked by total box office of their top grossing movies."""
    casts = load_casts(casts_filename)
    top_grossing = load_top_grossing(grossing_filename)

    totals = {}
    for movie, box_office in top_grossing.items():
        if movie not in casts:
            continue
        _, actors = casts[movie]
        for actor in actors:
            totals[actor] = totals.get(actor, 0) + box_office

    ranking = sorted(totals.items(), key=lambda entry: entry[1],
                      reverse=True)

    print('Top actors by total box office (top grossing movies):')
    _print_ranking(ranking, limit)


def main() -> None:
    """Tests display_top_collaborations and display_top_actors."""
    casts_file = 'imdb-top-casts.csv'
    rated_file = 'imdb-top-rated.csv'
    grossing_file = 'imdb-top-grossing.csv'

    display_top_collaborations(casts_file, rated_file, limit=10)
    print()
    display_top_actors(casts_file, grossing_file, limit=10)


if __name__ == '__main__':
    main()
