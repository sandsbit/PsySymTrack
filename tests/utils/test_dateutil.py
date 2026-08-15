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

from utils.dateutil import monday_before, n_weeks_before


class TestMondayBefore(unittest.TestCase):

    def test_monday(self):
        dt = datetime(2026, 8, 10, 15, 30, 45, 123456)

        result = monday_before(dt)

        self.assertEqual(result, datetime(2026, 8, 10))

    def test_other_weekday(self):
        dt = datetime(2026, 8, 13, 15, 30, 45, 123456)  # Thursday

        result = monday_before(dt)

        self.assertEqual(result, datetime(2026, 8, 10))

    def test_sunday(self):
        dt = datetime(2026, 8, 16, 23, 59, 59, 999999)

        result = monday_before(dt)

        self.assertEqual(result, datetime(2026, 8, 10))

    def test_resets_time(self):
        dt = datetime(2026, 8, 12, 23, 59, 59, 999999)

        result = monday_before(dt)

        self.assertEqual(result.hour, 0)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)
        self.assertEqual(result.microsecond, 0)

    def test_preserves_date_before_monday(self):
        dt = datetime(2026, 8, 9, 12, 0)  # Sunday

        result = monday_before(dt)

        self.assertEqual(result, datetime(2026, 8, 3))


class TestNWeeksBefore(unittest.TestCase):

    def test_zero_weeks(self):
        dt = datetime(2026, 8, 13, 15, 30)

        self.assertEqual(
            n_weeks_before(dt, 0),
            datetime(2026, 8, 10),
        )

    def test_one_week(self):
        dt = datetime(2026, 8, 13, 15, 30)

        self.assertEqual(
            n_weeks_before(dt, 1),
            datetime(2026, 8, 3),
        )

    def test_multiple_weeks(self):
        dt = datetime(2026, 8, 13, 15, 30)

        self.assertEqual(
            n_weeks_before(dt, 4),
            datetime(2026, 7, 13),
        )

    def test_input_is_not_monday(self):
        dt = datetime(2026, 8, 16, 23, 59)  # Sunday

        self.assertEqual(
            n_weeks_before(dt, 2),
            datetime(2026, 7, 27),
        )

    def test_input_is_monday(self):
        dt = datetime(2026, 8, 10, 12, 30)

        self.assertEqual(
            n_weeks_before(dt, 2),
            datetime(2026, 7, 27),
        )


if __name__ == "__main__":
    unittest.main()
