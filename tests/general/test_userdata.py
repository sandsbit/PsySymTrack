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
import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from general.userdata import BasicUserData, Sex, load_user_data, save_user_data

class TestUserDataPersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.userdata_file = Path(self.temp_dir.name) / "user_data.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_user_data_creates_file(self):
        user_data = BasicUserData(
            date_of_birth=datetime(1990, 5, 15),
            sex=list(Sex)[0],
            height_cm=170,
        )

        with patch("general.userdata._USERDATA_FILE", self.userdata_file):
            save_user_data(user_data)

        self.assertTrue(self.userdata_file.exists())
        self.assertTrue(self.userdata_file.is_file())

    def test_save_user_data_writes_serializable_values(self):
        user_data = BasicUserData(
            date_of_birth=datetime(1990, 5, 15),
            sex=list(Sex)[0],
            height_cm=170,
        )

        with patch("general.userdata._USERDATA_FILE", self.userdata_file):
            save_user_data(user_data)

        data = json.loads(self.userdata_file.read_text(encoding="utf-8"))

        self.assertEqual(
            data["date_of_birth"],
            user_data.date_of_birth.isoformat(),
        )
        self.assertEqual(
            data["sex"],
            user_data.sex.value,
        )
        self.assertEqual(
            data["height_cm"],
            user_data.height_cm,
        )

    def test_load_user_data(self):
        original = BasicUserData(
            date_of_birth=datetime(1990, 5, 15),
            sex=list(Sex)[0],
            height_cm=170,
        )

        file_data = {
            "date_of_birth": original.date_of_birth.isoformat(),
            "sex": original.sex.value,
            "height_cm": original.height_cm,
        }

        self.userdata_file.write_text(
            json.dumps(file_data),
            encoding="utf-8",
        )

        with patch("general.userdata._USERDATA_FILE", self.userdata_file):
            loaded = load_user_data()

        self.assertEqual(loaded, original)

    def test_save_and_load_round_trip(self):
        original = BasicUserData(
            date_of_birth=datetime(1985, 12, 1),
            sex=list(Sex)[-1],
            height_cm=182,
        )

        with patch("general.userdata._USERDATA_FILE", self.userdata_file):
            save_user_data(original)
            loaded = load_user_data()

        self.assertEqual(loaded, original)


if __name__ == "__main__":
    unittest.main()