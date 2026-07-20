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
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from tracking.valuestorsage import ValuesStorage


class TestTimeSeriesStore(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.sqlite"

        self.path_patch = patch.object(
            ValuesStorage,
            "_DB_PATH",
            self.db_path,
        )
        self.path_patch.start()

        self.store = ValuesStorage()

    def tearDown(self) -> None:
        if self.store:
            self.store.close()
        self.path_patch.stop()
        self.temp_dir.cleanup()

    def test_add_and_get_value(self) -> None:
        date = datetime(2026, 7, 20, 10, 30)

        self.store.add_value("weight", date, 75000)

        self.assertEqual(
            self.store.get_value("weight", date),
            75000,
        )

    def test_add_duplicate_value_fails(self) -> None:
        date = datetime(2026, 7, 20)

        self.store.add_value("weight", date, 75000)

        with self.assertRaises(ValueError):
            self.store.add_value("weight", date, 76000)

    def test_get_missing_value_fails(self) -> None:
        self.assertIsNone(
            self.store.get_value(
                "weight",
                datetime(2026, 7, 20),
            )
        )

    def test_edit_existing_value(self) -> None:
        date = datetime(2026, 7, 20)

        self.store.add_value("weight", date, 75000)
        self.store.edit_value("weight", date, 75500)

        self.assertEqual(
            self.store.get_value("weight", date),
            75500,
        )

    def test_edit_missing_value_fails(self) -> None:
        with self.assertRaises(KeyError):
            self.store.edit_value(
                "weight",
                datetime(2026, 7, 20),
                75500,
            )

    def test_delete_existing_value(self) -> None:
        date = datetime(2026, 7, 20)

        self.store.add_value("weight", date, 75000)
        self.store.delete_value("weight", date)

    def test_delete_missing_value_fails(self) -> None:
        with self.assertRaises(KeyError):
            self.store.delete_value(
                "weight",
                datetime(2026, 7, 20),
            )

    def test_get_range_returns_sorted_values(self) -> None:
        self.store.add_value(
            "weight",
            datetime(2026, 7, 3),
            73000,
        )
        self.store.add_value(
            "weight",
            datetime(2026, 7, 1),
            72000,
        )
        self.store.add_value(
            "weight",
            datetime(2026, 7, 2),
            72500,
        )

        result = self.store.get_range(
            "weight",
            datetime(2026, 7, 1),
            datetime(2026, 7, 3),
        )

        self.assertEqual(
            result,
            [
                (datetime(2026, 7, 1), 72000),
                (datetime(2026, 7, 2), 72500),
                (datetime(2026, 7, 3), 73000),
            ],
        )

    def test_get_range_excludes_other_series(self) -> None:
        date = datetime(2026, 7, 20)

        self.store.add_value("weight", date, 75000)
        self.store.add_value("height", date, 180)

        result = self.store.get_range(
            "weight",
            datetime(2026, 1, 1),
            datetime(2026, 12, 31),
        )

        self.assertEqual(
            result,
            [(date, 75000)],
        )

    def test_multiple_series_can_have_same_date(self) -> None:
        date = datetime(2026, 7, 20)

        self.store.add_value("weight", date, 75000)
        self.store.add_value("blood_pressure", date, 120)

        self.assertEqual(
            self.store.get_value("weight", date),
            75000,
        )
        self.assertEqual(
            self.store.get_value("blood_pressure", date),
            120,
        )

    def test_data_survives_reopening(self) -> None:
        date = datetime(2026, 7, 20, 10, 30)

        self.store.add_value("weight", date, 75000)
        self.store.close()

        reopened_store = ValuesStorage()

        try:
            self.assertEqual(
                reopened_store.get_value("weight", date),
                75000,
            )
        finally:
            reopened_store.close()

if __name__ == "__main__":
    unittest.main()