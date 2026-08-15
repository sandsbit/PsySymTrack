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
import sys
import platform
from enum import Enum
from pathlib import Path

from app_info import APP_NAME

class OS(Enum):
    WINDOWS = 0
    MACOS = 1
    LINUX = 2
    OTHER = 3


def get_os() -> OS:
    """Return the user's operating system."""
    system = platform.system()

    match system:
        case "Windows":
            return OS.WINDOWS
        case "Darwin":
            return OS.MACOS
        case "Linux":
            return OS.LINUX
        case _:
            return OS.OTHER


def get_app_data_dir() -> Path:
    """
    Return the application's data directory, creating it if it does not exist.

    The directory location follows the platform-specific conventions:

    - Windows:
        Uses the `%APPDATA%` environment variable and creates the
        application directory inside it:
        `%APPDATA%/<app_name>`

    - macOS:
        Uses the standard Application Support directory:
        `~/Library/Application Support/<app_name>`

    - Linux and other Unix-like systems:
        Uses the `XDG_DATA_HOME` environment variable if defined:
        `$XDG_DATA_HOME/.<app_name>`

        If `XDG_DATA_HOME` is not defined, falls back to the user's home
        directory:
        `~/.<app_name>`

    The directory and any missing parent directories are created before
    returning the path.

    App name is defined in app_info.py.

    Returns:
        A Path object pointing to the application's data directory.
    """

    match get_os():
        case OS.WINDOWS:
            base_dir = Path(os.environ["APPDATA"])
            data_dir = base_dir / APP_NAME

        case OS.MACOS:
            data_dir = Path.home() / "Library" / "Application Support" / APP_NAME

        case _:
            xdg_data_home = os.environ.get("XDG_DATA_HOME")
            if xdg_data_home:
                base_dir = Path(xdg_data_home)
                data_dir = base_dir / f"{APP_NAME}"
            else:
                base_dir = Path.home()
                data_dir = base_dir / f".{APP_NAME}"


    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_working_dir_path() -> Path:
    """Returns directory where bundled app's files are located."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'): # running in a PyInstaller bundle
        if get_os() == OS.MACOS:
            return Path(__file__).resolve().parent.parent.parent / "Resources"
        else:
            return Path(__file__).resolve().parent.parent
    else:
        return Path(__file__).resolve().parent.parent.parent
