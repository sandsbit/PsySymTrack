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

from utils.versions import process_release_version


class TestVersions(unittest.TestCase):
    def test_valid_version(self):
        self.assertTupleEqual(process_release_version("5.6.1"), (5, 6, 1))
        self.assertTupleEqual(process_release_version("5.16.1-beta.2"), (5, 16, 1))

    def test_invalid_version(self):
        with self.assertRaises(ValueError):
            process_release_version("1.0")
        with self.assertRaises(ValueError):
            process_release_version("a.b.c")


if __name__ == "__main__":
    unittest.main()
