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

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from utils.osutil import OS, get_app_data_dir, get_os, get_working_dir_path


class TestGetOS(unittest.TestCase):
    def test_returns_os_enum_value(self):
        result = get_os()

        self.assertIsInstance(result, OS)


class TestGetAppDataDir(unittest.TestCase):
    def test_creates_directory(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            patch("utils.osutil.get_os", return_value=OS.LINUX),
            patch.dict(os.environ, {"XDG_DATA_HOME": temp_dir}),
        ):
            data_dir = get_app_data_dir()

            self.assertTrue(data_dir.exists())
            self.assertTrue(data_dir.is_dir())

    def test_uses_xdg_data_home(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            patch("utils.osutil.get_os", return_value=OS.LINUX),
            patch.dict(os.environ, {"XDG_DATA_HOME": temp_dir}),
        ):
            data_dir = get_app_data_dir()

            self.assertEqual(data_dir.parent, Path(temp_dir))

    def test_creates_missing_parent_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            xdg_path = Path(temp_dir) / "missing" / "xdg"

            with (
                patch("utils.osutil.get_os", return_value=OS.LINUX),
                patch.dict(os.environ, {"XDG_DATA_HOME": str(xdg_path)}),
            ):
                data_dir = get_app_data_dir()

                self.assertTrue(data_dir.exists())
                self.assertTrue(xdg_path.exists())

    def test_returns_same_existing_directory(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            patch("utils.osutil.get_os", return_value=OS.LINUX),
            patch.dict(os.environ, {"XDG_DATA_HOME": temp_dir}),
        ):
            first = get_app_data_dir()
            second = get_app_data_dir()

            self.assertEqual(first, second)

    def test_windows_path(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            patch("utils.osutil.get_os", return_value=OS.WINDOWS),
            patch.dict(os.environ, {"APPDATA": temp_dir}),
        ):
            data_dir = get_app_data_dir()

            self.assertEqual(data_dir.parent, Path(temp_dir))
            self.assertTrue(data_dir.exists())

    def test_macos_path(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            patch("utils.osutil.get_os", return_value=OS.MACOS),
            patch("pathlib.Path.home", return_value=Path(temp_dir)),
        ):
            data_dir = get_app_data_dir()

            self.assertEqual(
                data_dir.parent,
                Path(temp_dir) / "Library" / "Application Support",
            )
            self.assertTrue(data_dir.exists())

    def test_linux_fallback_to_home(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            patch("utils.osutil.get_os", return_value=OS.LINUX),
            patch.dict(os.environ, {}, clear=True),
            patch("pathlib.Path.home", return_value=Path(temp_dir)),
        ):
            data_dir = get_app_data_dir()

            self.assertEqual(data_dir.parent, Path(temp_dir))
            self.assertTrue(data_dir.name.startswith("."))
            self.assertTrue(data_dir.exists())


class TestGetWorkingDirectory(unittest.TestCase):
    def test_returns_correct_directory(self):
        wd = get_working_dir_path()

        self.assertTrue(wd.exists())
        self.assertTrue(wd.is_dir())
        self.assertTrue((wd / "pyproject.toml").exists())


if __name__ == "__main__":
    unittest.main()
