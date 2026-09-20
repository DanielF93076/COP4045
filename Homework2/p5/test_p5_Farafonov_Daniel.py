"""Unit tests for the weather station analyzer (Homework 2, Problem 5).

Daniel Farafonov
"""

import os
import tempfile
import unittest

from p5_Farafonov_Daniel import (
    read_observations, station_statistics, station_outliers,
    write_statistics)


class WeatherStationAnalyzerTest(unittest.TestCase):
    """Tests for read_observations, station_statistics, station_outliers
    and write_statistics."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _make_file(self, name: str, content: str) -> str:
        path = os.path.join(self.temp_dir.name, name)
        with open(path, 'w', encoding='utf-8') as obs_file:
            obs_file.write(content)
        return path

    def test_multiple_stations(self) -> None:
        path = self._make_file(
            'multi.csv',
            'A,09:00:00 AM 04/20/2026,60.0\n'
            'B,10:00:00 AM 04/20/2026,70.0\n'
            'A,08:00:00 AM 04/19/2026,55.0\n')
        observations, errors = read_observations(path)
        self.assertEqual(errors, [])
        self.assertEqual(set(observations), {'A', 'B'})
        self.assertEqual([temp for _, temp in observations['A']],
                          [55.0, 60.0])

    def test_negative_temperature(self) -> None:
        path = self._make_file(
            'neg.csv', 'A,09:00:00 AM 04/20/2026,-40.5\n')
        observations, errors = read_observations(path)
        self.assertEqual(errors, [])
        self.assertEqual(observations['A'][0][1], -40.5)

    def test_duplicate_observation(self) -> None:
        path = self._make_file(
            'dup.csv',
            'A,09:00:00 AM 04/20/2026,60.0\n'
            'A,09:00:00 AM 04/20/2026,61.0\n')
        observations, errors = read_observations(path)
        self.assertEqual(len(observations['A']), 1)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], 2)

    def test_invalid_temperature_range(self) -> None:
        path = self._make_file(
            'range.csv',
            'A,09:00:00 AM 04/20/2026,200.0\n'
            'A,10:00:00 AM 04/20/2026,-150.0\n')
        observations, errors = read_observations(path)
        self.assertNotIn('A', observations)
        self.assertEqual(len(errors), 2)

    def test_calculated_statistics(self) -> None:
        path = self._make_file(
            'stats.csv',
            'A,09:00:00 AM 04/20/2026,10.0\n'
            'A,09:00:00 AM 04/21/2026,20.0\n'
            'A,09:00:00 AM 04/22/2026,30.0\n')
        observations, _ = read_observations(path)
        statistics = station_statistics(observations)
        self.assertAlmostEqual(statistics['A']['min'], 10.0)
        self.assertAlmostEqual(statistics['A']['max'], 30.0)
        self.assertAlmostEqual(statistics['A']['mean'], 20.0)

    def test_outliers(self) -> None:
        path = self._make_file(
            'outliers.csv',
            'A,09:00:00 AM 04/20/2026,10.0\n'
            'A,09:00:00 AM 04/21/2026,50.0\n')
        observations, _ = read_observations(path)
        outliers = station_outliers(observations)
        self.assertIn('A', outliers)
        _, temperature, _ = outliers['A']
        self.assertEqual(temperature, 50.0)

    def test_sorted_output(self) -> None:
        statistics = {
            'Zeta': {'min': 1.0, 'max': 2.0, 'mean': 1.5},
            'Alpha': {'min': 3.0, 'max': 4.5, 'mean': 3.75},
        }
        out_path = os.path.join(self.temp_dir.name, 'out.txt')
        write_statistics(out_path, statistics)
        with open(out_path, 'r', encoding='utf-8') as stats_file:
            lines = stats_file.readlines()
        self.assertTrue(lines[0].startswith('Alpha'))
        self.assertTrue(lines[1].startswith('Zeta'))
        self.assertIn('mean=3.8', lines[0])

    def test_missing_file(self) -> None:
        missing_path = os.path.join(self.temp_dir.name, 'does_not_exist.csv')
        with self.assertRaises(OSError):
            read_observations(missing_path)


if __name__ == '__main__':
    unittest.main()
