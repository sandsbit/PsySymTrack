# PsySymTrack
# Psychiatric symptom tracker with basic analysis
# Copyright (C) 2026 Nikita Serba. All rights reserved
# https://github.com/sandsbit/PsySymTrack
#
# PsySymTrack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# PsySymTrack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PsySymTrack. If not, see <https://www.gnu.org/licenses/>.

import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

from analysis.stats import (
    DateRange,
    _get_values_series,
    _points_for_metric,
    get_points,
    get_stats,
    get_warnings,
)
from tracking.metrics import Metric
from tracking.values import ScaleValue, ValuesManager
from tracking.valuestorsage import ValuesStorage, open_storage


class TestStatistics(unittest.TestCase):

    class TestMetric(Metric):
        NAME = "Name"
        DESCRIPTION = "Desc"

        USED_PARAMS_IDS = ["test_id1", "test_id2"]  # noqa: RUF012
        NEEDS_HISTORY = False
        NEEDS_HISTORY_FOR = None
        min_value = 1
        max_value = 5
        normal_min = 3
        normal_max = 3
        not_severely_abnormal_min = 2
        not_severely_abnormal_max = 4
        INTERP = None

        def calculate(
            self,
            params: dict[str, int | float],
            history: dict[str, list[tuple[datetime, int]]] | None = None,
        ) -> float | None:
            assert history is None
            return (params["test_id1"] + params["test_id2"]) * 2

    TEST_ID1_VALUES: ClassVar = [
        (datetime(2026, 6, 15, 0, 0), 1),
        (datetime(2026, 8, 3, 0, 0), 2),
        (datetime(2026, 8, 10, 0, 0), 3),
        (datetime(2026, 8, 17, 0, 0), 4),
        (datetime(2026, 8, 24, 0, 0), 2)
    ]
    TEST_ID2_VALUES: ClassVar = [
        (datetime(2026, 6, 15, 0, 0), 2),
        (datetime(2026, 8, 3, 0, 0), 4),
        (datetime(2026, 8, 10, 0, 0), 6),
        (datetime(2026, 8, 17, 0, 0), 6),
        (datetime(2026, 8, 24, 0, 0), 4)
    ]

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_patch = patch.object(
            ValuesStorage,
            "_DB_PATH",
            Path(self.temp_dir.name) / "test.sqlite",
        )
        self.db_patch.start()
        self.now_patch = patch("analysis.stats.datetime")
        dt_mock = self.now_patch.start()
        dt_mock.now.return_value=datetime(2026, 8, 31, 0, 0)
        with open_storage() as storage:
            for date, value in self.TEST_ID1_VALUES:
                storage.edit_value("test_id1", date, value)
            for date, value in self.TEST_ID2_VALUES:
                storage.edit_value("test_id2", date, value)

    def tearDown(self) -> None:
        self.db_patch.stop()
        self.now_patch.stop()
        self.temp_dir.cleanup()

    def test_get_values_series(self):
        values_series = _get_values_series("test_id1", DateRange.DAYS_60)
        self.assertCountEqual(
            values_series,
            [
                (datetime(2026, 8, 3, 0, 0), 2),
                (datetime(2026, 8, 10, 0, 0), 3),
                (datetime(2026, 8, 17, 0, 0), 4),
                (datetime(2026, 8, 24, 0, 0), 2)
            ]
        )

    def test_points_for_metric(self):
        metric_points = _points_for_metric(TestStatistics.TestMetric, DateRange.DAYS_60)
        # noinspection bad-argument-type
        metric_points = list(zip(*metric_points))

        self.assertCountEqual(
            metric_points,
            [
                (datetime(2026, 8, 3, 0, 0), 12),
                (datetime(2026, 8, 10, 0, 0), 18),
                (datetime(2026, 8, 17, 0, 0), 20),
                (datetime(2026, 8, 24, 0, 0), 12)
            ]
        )

    def test_get_points_value(self):
        value_points = get_points("test_id1", DateRange.DAYS_60)
        # noinspection bad-argument-type
        value_points = tuple(map(list, value_points))

        self.assertTupleEqual(
            value_points,
            (
                [
                    datetime(2026, 8, 3, 0, 0),
                    datetime(2026, 8, 10, 0, 0),
                    datetime(2026, 8, 17, 0, 0),
                    datetime(2026, 8, 24, 0, 0),
                ],
                [2, 3, 4, 2]
            )
        )

    # noinspection unresolved-references
    def test_get_stats(self):
        stats = get_stats(TestStatistics.TestMetric, DateRange.DAYS_60)

        self.assertIsNotNone(stats)
        self.assertEqual(stats.min, 12)
        self.assertEqual(stats.max, 20)
        self.assertAlmostEqual(stats.mean, (12 + 18 + 20 + 12)/4.0)
        self.assertEqual(stats.median, 15)
        self.assertAlmostEqual(stats.std, 3.5707, delta=0.001)
        self.assertAlmostEqual(stats.cv, 23.037, delta=0.1)

class TestWarnings(unittest.TestCase):

    class TestMetric(Metric):
        NAME = "Name"
        DESCRIPTION = "Desc"

        USED_PARAMS_IDS = ["test_id4"]  # noqa: RUF012
        NEEDS_HISTORY = False
        NEEDS_HISTORY_FOR = None
        min_value = 1
        max_value = 5
        normal_min = 3
        normal_max = 3
        not_severely_abnormal_min = 2
        not_severely_abnormal_max = 4
        INTERP = None

        def calculate(
            self,
            params: dict[str, int | float],
            history: dict[str, list[tuple[datetime, int]]] | None = None,
        ) -> float | None:
            assert history is None
            return params["test_id4"]

    TEST_ID1_VALUES: ClassVar = [
        (datetime(2026, 7, 20, 0, 0), 3),
        (datetime(2026, 8, 3, 0, 0), 3),
        (datetime(2026, 8, 10, 0, 0), 3),
        (datetime(2026, 8, 17, 0, 0), 3),
        (datetime(2026, 8, 24, 0, 0), 3)
    ]
    TEST_ID2_VALUES: ClassVar = [
        (datetime(2026, 6, 15, 0, 0), 3),
        (datetime(2026, 8, 3, 0, 0), 3),
        (datetime(2026, 8, 10, 0, 0), 3),
        (datetime(2026, 8, 17, 0, 0), 3),
        (datetime(2026, 8, 24, 0, 0), 4)
    ]
    TEST_ID3_VALUES: ClassVar = [
        (datetime(2026, 6, 15, 0, 0), 4),
        (datetime(2026, 8, 3, 0, 0), 5),
        (datetime(2026, 8, 10, 0, 0), 4),
        (datetime(2026, 8, 17, 0, 0), 3),
        (datetime(2026, 8, 24, 0, 0), 3)
    ]
    TEST_ID4_VALUES: ClassVar = [
        (datetime(2026, 6, 15, 0, 0), 4),
        (datetime(2026, 8, 3, 0, 0), 5),
        (datetime(2026, 8, 10, 0, 0), 4),
        (datetime(2026, 8, 17, 0, 0), 3),
        (datetime(2026, 8, 24, 0, 0), 4)
    ]
    TEST_ID5_VALUES: ClassVar = [
        (datetime(2026, 6, 15, 0, 0), 4),
        (datetime(2026, 8, 3, 0, 0), 4),
        (datetime(2026, 8, 10, 0, 0), 5),
        (datetime(2026, 8, 17, 0, 0), 5),
        (datetime(2026, 8, 24, 0, 0), 5)
    ]

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_patch = patch.object(
            ValuesStorage,
            "_DB_PATH",
            Path(self.temp_dir.name) / "test.sqlite",
        )
        self.db_patch.start()

        self.now_patch = patch("analysis.stats.datetime")
        dt_mock = self.now_patch.start()
        dt_mock.now.return_value=datetime(2026, 8, 31, 0, 0)

        values = {"cat1": []}
        for i in range(1, 6):
            values["cat1"].append(
                ScaleValue(
                    id="test_id"+str(i),
                    name="Name",
                    description="Desc",
                    category="cat1",
                    min_value=1,
                    max_value=5,
                    value_descriptions=["1 desc", "2 desc", "3 desc", "4 desc", "5 desc"],
                    has_inactive_values=False,
                    active_values=None,
                    normal_min=3,
                    normal_max=3,
                    not_severely_abnormal_min=2,
                    not_severely_abnormal_max=4
                )
            )
        self.manager_patch = patch.object(ValuesManager, "scale_values", return_value=values)
        self.manager_patch.start()

        with open_storage() as storage:
            for date, value in self.TEST_ID1_VALUES:
                storage.edit_value("test_id1", date, value)
            for date, value in self.TEST_ID2_VALUES:
                storage.edit_value("test_id2", date, value)
            for date, value in self.TEST_ID3_VALUES:
                storage.edit_value("test_id3", date, value)
            for date, value in self.TEST_ID4_VALUES:
                storage.edit_value("test_id4", date, value)
            for date, value in self.TEST_ID5_VALUES:
                storage.edit_value("test_id5", date, value)

    def tearDown(self) -> None:
        self.db_patch.stop()
        self.now_patch.stop()
        self.manager_patch.stop()
        self.temp_dir.cleanup()

    def test_no_warning_on_normal(self):
        warnings = get_warnings()
        for value, warning in warnings.values_new:
            self.assertNotEqual(value.id, "test_id1")
            self.assertNotEqual(value.id, "test_id2")
        for value, warning in warnings.values_old:
            self.assertNotEqual(value.id, "test_id1")
            self.assertNotEqual(value.id, "test_id2")

    def test_no_warning_interrupted(self):
        warnings = get_warnings()
        for value, warning in warnings.values_new:
            self.assertNotEqual(value.id, "test_id3")
        for value, warning in warnings.values_old:
            self.assertNotEqual(value.id, "test_id3")

    def test_warning_interrupted(self):
        warnings = get_warnings()
        for value, warning in warnings.values_old:
            if value.id == "test_id4":
                self.assertEqual(warning.abnormal_weeks, 5)
                self.assertIsNone(warning.severely_abnormal_weeks)
                return
        self.fail("No warning for test_id4 found.")

    def test_warning_severe(self):
        warnings = get_warnings()
        for value, warning in warnings.values_old:
            if value.id == "test_id5":
                self.assertEqual(warning.abnormal_weeks, 5)
                self.assertEqual(warning.severely_abnormal_weeks, 3)
                return
        self.fail("No warning for test_id5 found.")

    def test_warning_metric(self):
        warnings = get_warnings()
        for metric, warning in warnings.metrics_old:
            if metric is TestWarnings.TestMetric:
                self.assertEqual(warning.abnormal_weeks, 5)
                self.assertIsNone(warning.severely_abnormal_weeks)
                return
        self.fail("No warning for TestMetric found.")

if __name__ == "__main__":
    unittest.main()
