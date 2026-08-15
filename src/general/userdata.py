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

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from utils import osutil

class Sex(Enum):
    MALE = "male"
    FEMALE = "female"

@dataclass(frozen=True)
class BasicUserData:
    """Basic clinical information about the user."""
    date_of_birth: datetime
    sex: Sex
    height_cm: int

_USERDATA_FILE = osutil.get_app_data_dir() / "userdata.json"

def load_user_data() -> BasicUserData | None:
    """Loads the user information from the app's data directory, None if no is saved."""

    if not _USERDATA_FILE.exists():
        return None

    data = json.loads(_USERDATA_FILE.read_text(encoding="utf-8"))

    return BasicUserData(
        date_of_birth=datetime.fromisoformat(data["date_of_birth"]),
        sex=Sex(data["sex"]),
        height_cm=data["height_cm"]
    )

def save_user_data(user_data: BasicUserData) -> None:
    """Saves the user information in the app's data directory."""

    data = asdict(user_data)

    data["date_of_birth"] = user_data.date_of_birth.isoformat()
    data["sex"] = user_data.sex.value

    _USERDATA_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")