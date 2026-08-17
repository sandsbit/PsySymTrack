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
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from analysis.alerts import (
    Alert,
    AlertGen,
    evaluate_alert,
    generate_alerts,
    get_all_alerts,
)
from general.userdata import BasicUserData, Sex
from tracking.metrics import Metric
from tracking.valuestorsage import ValuesStorage, open_storage


class TestAlerts(unittest.TestCase):

    class TestMetric(Metric):
        NAME = "Name"
        DESCRIPTION = "Desc"

        USED_PARAMS_IDS = ["test_id2"]  # noqa: RUF012
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
            return params["test_id2"]

    def test_get_alerts(self):
        class TestAlertGen(AlertGen):
            USED_PARAMS_IDS = []  # noqa: RUF012
            USED_METRICS = []  # noqa: RUF012
            GIVE_HISTORY_FOR = timedelta(days=7)

            def generate_alert(
                self,
                values: dict[str, list[tuple[datetime, float]]],
                metrics: dict[type[Metric], list[tuple[datetime, float]]],
            ) -> Alert | None:
                return None

        self.assertIn(TestAlertGen, get_all_alerts())

    def test_evaluate_alert(self):
        date_point = datetime(2026, 8, 3, 0, 0)
        old_date_point = datetime(2026, 4, 6, 0, 0)
        week = timedelta(days=7)

        old_dates = [old_date_point + (i * week) for i in range(4)]
        new_dates = [date_point + (i * week) for i in range(5)]

        old_values1 = [-1, -2, -3, -4]
        new_values1 = [1, 2, 3, 4, 5]
        old_values2 = [-5, -6, -7, -8]
        new_values2 = [6, 7, 8, 9, 10]

        alert = Alert("Name", "Desc", Alert.AlertSeverity.CRITICAL)

        myself = self
        class TestAlertGen(AlertGen):
            USED_PARAMS_IDS = ["test_id1"]  # noqa: RUF012
            USED_METRICS = [TestAlerts.TestMetric]  # noqa: RUF012
            GIVE_HISTORY_FOR = timedelta(days=31)

            def generate_alert(
                self,
                values: dict[str, list[tuple[datetime, float]]],
                metrics: dict[type[Metric], list[tuple[datetime, float]]],
            ) -> Alert | None:
                myself.assertListEqual(list(values.keys()), ["test_id1"])
                myself.assertListEqual(list(metrics.keys()), [TestAlerts.TestMetric])
                dates1, values1 = zip(*values["test_id1"])
                dates2, values2 = zip(*metrics[TestAlerts.TestMetric])
                myself.assertCountEqual(dates1, new_dates)
                myself.assertCountEqual(dates2, new_dates)
                myself.assertCountEqual(values1, [1, 2, 3, 4, 5])
                myself.assertCountEqual(values2, [6, 7, 8, 9, 10])
                return alert

        with tempfile.TemporaryDirectory() as tmpdir:
            db_file = Path(tmpdir) / "test.sqlite"
            with (patch.object(ValuesStorage, "_DB_PATH", db_file),
                  open_storage() as storage,
                  patch("analysis.alerts.datetime") as mock_datetime):
                mock_datetime.now.return_value = datetime(2026, 8, 31, 0, 0)
                for i in range(4):
                    storage.edit_value("test_id1", old_dates[i], old_values1[i])
                    storage.edit_value("test_id1", new_dates[i], new_values1[i])
                storage.edit_value("test_id1", new_dates[4], new_values1[4])
                for i in range(4):
                    storage.edit_value("test_id2", old_dates[i], old_values2[i])
                    storage.edit_value("test_id2", new_dates[i], new_values2[i])
                storage.edit_value("test_id2", new_dates[4], new_values2[4])

                alert_result = evaluate_alert(
                    TestAlertGen,
                    BasicUserData(datetime.now(), Sex.MALE, 178),
                    storage
                )

                self.assertEqual(alert_result.severity, alert.severity)

    def test_generate_alerts(self):
            class TestAlertGen1(AlertGen):
                USED_PARAMS_IDS = []  # noqa: RUF012
                USED_METRICS = []  # noqa: RUF012
                GIVE_HISTORY_FOR = timedelta(days=7)

                def generate_alert(
                    self,
                    values: dict[str, list[tuple[datetime, float]]],
                    metrics: dict[type[Metric], list[tuple[datetime, float]]],
                ) -> Alert | None:
                    return Alert("Name1", "Desc1", Alert.AlertSeverity.IMPORTANT)

            class TestAlertGen2(AlertGen):
                USED_PARAMS_IDS = []  # noqa: RUF012
                USED_METRICS = []  # noqa: RUF012
                GIVE_HISTORY_FOR = timedelta(days=7)

                def generate_alert(
                    self,
                    values: dict[str, list[tuple[datetime, float]]],
                    metrics: dict[type[Metric], list[tuple[datetime, float]]],
                ) -> Alert | None:
                    return Alert("Name2", "Desc2", Alert.AlertSeverity.CRITICAL)

            with (patch("analysis.alerts.get_all_alerts", return_value=[TestAlertGen1, TestAlertGen2]),
                  open_storage() as storage):
                alerts = generate_alerts(BasicUserData(datetime.now(), Sex.MALE, 178), storage)
                self.assertEqual(len(alerts), 2)
                self.assertEqual(alerts[0].severity, Alert.AlertSeverity.CRITICAL)

if __name__ == "__main__":
    unittest.main()
