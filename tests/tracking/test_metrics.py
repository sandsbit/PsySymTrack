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

import unittest
from datetime import datetime
from unittest.mock import patch

from general.userdata import BasicUserData, Sex
from tracking.metrics import Metric, evaluate_metric, get_all_metrics
from tracking.valuestorsage import ValuesStorage, open_storage


class TestMetricsPostInit(unittest.TestCase):
    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            class TestMetric(Metric):
                NAME = 10
                DESCRIPTION = "Desc"

                USED_PARAMS_IDS = []  # noqa: RUF012
                NEEDS_HISTORY = False
                NEEDS_HISTORY_FOR = None
                RESULT_MIN = 1
                RESULT_MAX = 5
                RESULT_NORMAL_MIN = 3
                RESULT_NORMAL_MAX = 3
                RESULT_NOT_SEVERELY_ABNORMAL_MIN = 2
                RESULT_NOT_SEVERELY_ABNORMAL_MAX = 4
                INTERP = None

                def calculate(
                    self,
                    params: dict[str, int | float],
                    history: dict[str, list[tuple[datetime, int]]] | None = None,
                ) -> float | None:
                    return None

        with self.assertRaises(TypeError):
            # noinspection redeclaration
            class TestMetric(Metric):
                NAME = "Name"
                DESCRIPTION = "Desc"

                USED_PARAMS_IDS = []  # noqa: RUF012
                NEEDS_HISTORY = True
                NEEDS_HISTORY_FOR = "None"
                RESULT_MIN = 1
                RESULT_MAX = 5
                RESULT_NORMAL_MIN = 3
                RESULT_NORMAL_MAX = 3
                RESULT_NOT_SEVERELY_ABNORMAL_MIN = 2
                RESULT_NOT_SEVERELY_ABNORMAL_MAX = 4
                INTERP = None

                def calculate(
                    self,
                    params: dict[str, int | float],
                    history: dict[str, list[tuple[datetime, int]]] | None = None,
                ) -> float | None:
                    return None

    def test_invalid_ranges(self):
        with self.assertRaises(ValueError):
            class TestMetric(Metric):
                NAME = "Name"
                DESCRIPTION = "Desc"

                USED_PARAMS_IDS = []  # noqa: RUF012
                NEEDS_HISTORY = False
                NEEDS_HISTORY_FOR = None
                RESULT_MIN = 6
                RESULT_MAX = 5
                RESULT_NORMAL_MIN = 3
                RESULT_NORMAL_MAX = 3
                RESULT_NOT_SEVERELY_ABNORMAL_MIN = 2
                RESULT_NOT_SEVERELY_ABNORMAL_MAX = 4
                INTERP = None

                def calculate(
                    self,
                    params: dict[str, int | float],
                    history: dict[str, list[tuple[datetime, int]]] | None = None,
                ) -> float | None:
                    return None

        with self.assertRaises(ValueError):
            # noinspection redeclaration
            class TestMetric(Metric):
                NAME = "Name"
                DESCRIPTION = "Desc"

                USED_PARAMS_IDS = []  # noqa: RUF012
                NEEDS_HISTORY = False
                NEEDS_HISTORY_FOR = None
                RESULT_MIN = 1
                RESULT_MAX = 5
                RESULT_NORMAL_MIN = 4
                RESULT_NORMAL_MAX = 3
                RESULT_NOT_SEVERELY_ABNORMAL_MIN = 2
                RESULT_NOT_SEVERELY_ABNORMAL_MAX = 4
                INTERP = None

                def calculate(
                    self,
                    params: dict[str, int | float],
                    history: dict[str, list[tuple[datetime, int]]] | None = None,
                ) -> float | None:
                    return None

        with self.assertRaises(ValueError):
            # noinspection redeclaration
            class TestMetric(Metric):
                NAME = "Name"
                DESCRIPTION = "Desc"

                USED_PARAMS_IDS = []  # noqa: RUF012
                NEEDS_HISTORY = False
                NEEDS_HISTORY_FOR = None
                RESULT_MIN = 1
                RESULT_MAX = 5
                RESULT_NORMAL_MIN = 3
                RESULT_NORMAL_MAX = 3
                RESULT_NOT_SEVERELY_ABNORMAL_MIN = 5
                RESULT_NOT_SEVERELY_ABNORMAL_MAX = 4
                INTERP = None

                def calculate(
                    self,
                    params: dict[str, int | float],
                    history: dict[str, list[tuple[datetime, int]]] | None = None,
                ) -> float | None:
                    return None

        with self.assertRaises(ValueError):
            # noinspection redeclaration
            class TestMetric(Metric):
                NAME = "Name"
                DESCRIPTION = "Desc"

                USED_PARAMS_IDS = []  # noqa: RUF012
                NEEDS_HISTORY = False
                NEEDS_HISTORY_FOR = None
                RESULT_MIN = 1
                RESULT_MAX = 5
                RESULT_NORMAL_MIN = -5
                RESULT_NORMAL_MAX = 5
                RESULT_NOT_SEVERELY_ABNORMAL_MIN = 2
                RESULT_NOT_SEVERELY_ABNORMAL_MAX = 4
                INTERP = None

                def calculate(
                    self,
                    params: dict[str, int | float],
                    history: dict[str, list[tuple[datetime, int]]] | None = None,
                ) -> float | None:
                    return None

        with self.assertRaises(ValueError):
            # noinspection redeclaration
            class TestMetric(Metric):
                NAME = "Name"
                DESCRIPTION = "Desc"

                USED_PARAMS_IDS = []  # noqa: RUF012
                NEEDS_HISTORY = False
                NEEDS_HISTORY_FOR = None
                RESULT_MIN = 1
                RESULT_MAX = 5
                RESULT_NORMAL_MIN = 2
                RESULT_NORMAL_MAX = 4
                RESULT_NOT_SEVERELY_ABNORMAL_MIN = 3
                RESULT_NOT_SEVERELY_ABNORMAL_MAX = 3
                INTERP = None

                def calculate(
                    self,
                    params: dict[str, int | float],
                    history: dict[str, list[tuple[datetime, int]]] | None = None,
                ) -> float | None:
                    return None


class TestMetricMethods(unittest.TestCase):

    class TestMetric(Metric):
        NAME = "Name"
        DESCRIPTION = "Desc"

        USED_PARAMS_IDS = ["test_id1", "test_id2"]  # noqa: RUF012
        NEEDS_HISTORY = False
        NEEDS_HISTORY_FOR = None
        RESULT_MIN = 1
        RESULT_MAX = 5
        RESULT_NORMAL_MIN = 3
        RESULT_NORMAL_MAX = 3
        RESULT_NOT_SEVERELY_ABNORMAL_MIN = 2
        RESULT_NOT_SEVERELY_ABNORMAL_MAX = 4
        INTERP = None

        def calculate(
                self,
                params: dict[str, int | float],
                history: dict[str, list[tuple[datetime, int]]] | None = None,
        ) -> float | None:
            assert history is None
            return (params["test_id1"] + params["test_id2"]) * 2

    def test_get_all_metrics(self):
        metrics = get_all_metrics()
        self.assertIn(TestMetricMethods.TestMetric, metrics)

    def test_evaluate_metric(self):
        # noinspection unused-parameter,shadowing-names
        def mock_get_value(self, series_id: str, _: datetime) -> float | None:
            match series_id:
                case "test_id1":
                    return 2
                case "test_id2":
                    return 3
                case _:
                    return None

        with patch.object(ValuesStorage, "get_value", mock_get_value), open_storage() as storage:
            result = evaluate_metric(
                TestMetricMethods.TestMetric,
                BasicUserData(datetime.now(), Sex.MALE, 178),
                storage,
                datetime.now()
            )

            self.assertEqual(result, 10)
