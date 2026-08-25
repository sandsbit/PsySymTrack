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

"""Information about the app to use in code."""

import sys
import tomllib
from pathlib import Path

APP_NAME: str
APP_VERSION: str
APP_DESCRIPTION: str

LEGAL_TEXT = """Copyright © 2026 Nikita S., All Rights Reserved

PsySymTrack is a symptom tracking and analysis tool, not a medical
device or substitute for professional medical advice, diagnosis, or
treatment. Its scores, analyses, episode detections, and warnings are
for informational purposes only and may be inaccurate. Do not use
PsySymTrack to make medication or treatment decisions. Always consult
a qualified healthcare professional regarding your health.

PsySymTrack is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PsySymTrack is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PsySymTrack. If not, see <https://www.gnu.org/licenses/>.
"""

def _get_working_dir_path() -> Path:
    """Returns directory where bundled app's files are located."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):  # running in a PyInstaller bundle
        if sys.platform == "darwin":
            return Path(__file__).resolve().parent.parent / "Resources"
        else:
            return Path(__file__).resolve().parent
    else:
        return Path(__file__).resolve().parent.parent


toml_path = _get_working_dir_path() / "pyproject.toml"
with toml_path.open("rb") as f:
    toml = tomllib.load(f)

APP_NAME = toml["project"]["name"]
APP_VERSION = toml["project"]["version"]
APP_DESCRIPTION = toml["project"]["description"]
