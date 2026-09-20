"""Homework 2, Problem 5: Weather Station Analyzer.

Daniel Farafonov
"""

import datetime
import sys

DATE_FORMAT = '%I:%M:%S %p %m/%d/%Y'
MIN_TEMPERATURE = -100.0
MAX_TEMPERATURE = 150.0


def read_observations(filename: str) -> tuple:
    """Reads daily temperature observations for one or more stations.

    Each line of the input file must have the format
    "station,date,temperature", where date is parsed with
    datetime.datetime.strptime using format "%I:%M:%S %p %m/%d/%Y"
    (e.g. "09:28:09 AM 04/20/2026"), and temperature is a float in
    the inclusive range [-100.0, 150.0]. Malformed lines, invalid
    temperatures, and duplicate station/date combinations are
    rejected and reported in errors instead of raising.

    Args:
        filename: Path to the observations file.

    Returns:
        A tuple (observations, errors). observations is a dict
        mapping each station name to a list of (date, temperature)
        tuples sorted by date. errors is a list of
        (line_number, error_message) tuples, empty if there were no
        errors.

    Raises:
        OSError: If filename cannot be opened.
    """
    observations = {}
    errors = []
    seen = set()

    try:
        with open(filename, 'r', encoding='utf-8') as obs_file:
            for line_number, raw_line in enumerate(obs_file, start=1):
                line = raw_line.strip()
                if not line:
                    continue

                fields = line.split(',')
                if len(fields) != 3:
                    errors.append(
                        (line_number,
                         f'expected 3 fields, got {len(fields)}'))
                    continue
                station, date_text, temperature_text = (
                    field.strip() for field in fields)

                try:
                    date = datetime.datetime.strptime(date_text, DATE_FORMAT)
                except ValueError:
                    errors.append(
                        (line_number, f'invalid date "{date_text}"'))
                    continue

                try:
                    temperature = float(temperature_text)
                except ValueError:
                    errors.append(
                        (line_number,
                         f'invalid temperature "{temperature_text}"'))
                    continue

                if not MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE:
                    errors.append(
                        (line_number,
                         f'temperature {temperature} out of range '
                         f'[{MIN_TEMPERATURE}, {MAX_TEMPERATURE}]'))
                    continue

                if (station, date) in seen:
                    errors.append(
                        (line_number,
                         f'duplicate observation for station "{station}" '
                         f'at {date}'))
                    continue
                seen.add((station, date))

                observations.setdefault(station, []).append(
                    (date, temperature))
    except OSError as error:
        print(f'Error: could not read file "{filename}": {error}')
        raise

    for readings in observations.values():
        readings.sort(key=lambda item: item[0])

    return observations, errors


def station_statistics(observations: dict) -> dict:
    """Computes the minimum, maximum and mean temperature per station.

    Args:
        observations: Dict mapping station name to a list of
            (date, temperature) tuples, as returned by
            read_observations.

    Returns:
        A dict mapping each station to a dict with keys 'min', 'max'
        and 'mean' holding the corresponding temperature statistics.

    Raises:
        ValueError: If a station has no observations.
    """
    try:
        statistics = {}
        for station, readings in observations.items():
            temperatures = [temperature for _, temperature in readings]
            if not temperatures:
                raise ValueError(f'station "{station}" has no observations')
            statistics[station] = {
                'min': min(temperatures),
                'max': max(temperatures),
                'mean': sum(temperatures) / len(temperatures),
            }
        return statistics
    except ValueError as error:
        print(f'Error: could not compute statistics: {error}')
        raise


def station_outliers(observations: dict) -> dict:
    """Finds stations whose latest reported temperature exceeds their mean.

    Args:
        observations: Dict mapping station name to a list of
            (date, temperature) tuples, sorted by date, as returned by
            read_observations.

    Returns:
        A dict mapping each outlying station name to a
        (date, temperature, mean) tuple describing its latest
        observation and its mean temperature.
    """
    statistics = station_statistics(observations)
    return {
        station: (readings[-1][0], readings[-1][1],
                   statistics[station]['mean'])
        for station, readings in observations.items()
        if readings and readings[-1][1] > statistics[station]['mean']
    }


def write_statistics(filename: str, statistics: dict) -> None:
    """Writes station statistics to a text file in lexicographic order.

    Stations and, within each station, its numeric values are written
    with exactly one digit after the decimal point.

    Args:
        filename: Path of the file to write.
        statistics: Dict mapping station name to a dict with keys
            'min', 'max' and 'mean', as returned by
            station_statistics.

    Raises:
        OSError: If filename cannot be written.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as stats_file:
            for station in sorted(statistics):
                stats = statistics[station]
                stats_file.write(
                    f'{station}: min={stats["min"]:.1f} '
                    f'max={stats["max"]:.1f} mean={stats["mean"]:.1f}\n')
    except OSError as error:
        print(f'Error: could not write file "{filename}": {error}')
        raise


def main() -> None:
    """Reads an observations file and prints/writes its statistics.

    Usage:
        python p5_Farafonov_Daniel.py <input_file> <output_file>
    """
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <input_file> <output_file>')
        sys.exit(1)

    input_filename, output_filename = sys.argv[1], sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
    except OSError:
        sys.exit(1)

    if errors:
        print('Errors found while reading observations:')
        for line_number, message in errors:
            print(f'  line {line_number}: {message}')

    statistics = station_statistics(observations)
    outliers = station_outliers(observations)

    print('\nStation statistics:')
    for station in sorted(statistics):
        stats = statistics[station]
        print(f'  {station}: min={stats["min"]:.1f} '
              f'max={stats["max"]:.1f} mean={stats["mean"]:.1f}')

    print('\nStation outliers:')
    for station in sorted(outliers):
        date, temperature, mean = outliers[station]
        print(f'  {station}: {date} temperature={temperature:.1f} '
              f'mean={mean:.1f}')

    try:
        write_statistics(output_filename, statistics)
    except OSError:
        sys.exit(1)


if __name__ == '__main__':
    main()
