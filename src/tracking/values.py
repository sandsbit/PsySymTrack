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
from pathlib import Path

from utils import osutil

@dataclass
class Value:
    """Parent class for two major types of values stored in the app. See children below."""
    id: str  # unique
    name: str  # human-readable
    description: str


@dataclass
class ScaleValue(Value):
    """
    Stores values where only discrete integer values in a range are possible.

    Example: sadness level from 1 to 5.

    If you need to exclude some integers from the possible values, set 'has_inactive_values'
    to True and specify which values are active using bool mask 'active_values' of size
    (max_value - min_value + 1).

    Resul will be interpreted as follows:
    - Severely abnormal: (-oo, not_severly_abormal_min) U (not_severly_abormal_max, +oo)
    - Abnormal: [not_severly_abormal_min, normal_min) U (normal_max, not_severly_abormal_max]
    - Normal: [normal_min, normal_max]
    Treat 'not_severly_abormal_min' and 'not_severly_abormal_max' as -oo and +oo respectively
    if None.
    """
    category: str

    min_value: int
    max_value: int
    value_descriptions: list[str]
    has_inactive_values: bool
    active_values: list[bool] | None

    normal_min: float
    normal_max: float
    # i.e. mildly abnormal range + normal range
    not_severly_abormal_min: float | None
    not_severly_abormal_max: float | None

    def __post_init__(self):
        """Checking whether all rules are complied with and smooth ranges."""
        if self.min_value > self.max_value:
            raise ValueError("min_value must be less than max_value")
        if self.normal_min > self.normal_max:
            raise ValueError("normal_min must be less than normal_max")
        if self.normal_min < self.min_value:
            raise ValueError("normal_min must be greater than min_value")
        if self.normal_max > self.max_value:
            raise ValueError("normal_max must be less than max_value")
        if (self.not_severly_abormal_min is not None) and (self.not_severly_abormal_min > self.normal_min):
            raise ValueError("not_severly_abormal_min must be less than normal_min")
        if (self.not_severly_abormal_max is not None) and (self.not_severly_abormal_max < self.normal_max):
            raise ValueError("not_severly_abormal_max must be greater than normal_max")

        self.normal_min -= 0.5
        self.normal_max += 0.5
        if self.not_severly_abormal_min is not None:
            self.not_severly_abormal_min -= 0.5
        if self.not_severly_abormal_max is not None:
            self.not_severly_abormal_max += 0.5

    def active_value_description_pairs(self) -> list[tuple[int, str]]:
        """Returns a list of active values and their descriptions in ascending order."""

        assert (self.max_value - self.min_value + 1) == len(self.value_descriptions)

        paired_values = [(self.min_value + i, v) for i, v in enumerate(self.value_descriptions)]

        if not self.has_inactive_values:
            return paired_values

        assert len(self.active_values) == len(paired_values)

        paired_values = [x for x, active in zip(paired_values, self.active_values) if active]
        return paired_values


def _TEST_example_ScaleValue() -> ScaleValue:
    """Randmon ScaleValue for unit tests."""
    return ScaleValue(
        id="unique_id_1",
        name="Test scale value",
        description="Test scale value description",
        category="Cat1",
        min_value=1,
        max_value=5,
        value_descriptions=["1 desc", "2 desc", "3 desc", "4 desc", "5 desc"],
        has_inactive_values=False,
        active_values=None,
        normal_min=3,
        normal_max=3,
        not_severly_abormal_min=2,
        not_severly_abormal_max=4
    )

@dataclass
class PhysicalValue(Value):
    """
        Stores values which can have any float value between two numbers (min_value, max_value).

        Example: weight, lithium blood level.

        For normal/abnormal interpretation check docs for 'ScaleValue'. The difference is that
        physical values can have no set normal range (in that case 'normal_min' and 'normal_max'
        are both None).
        """
    min_value: float | None
    max_value: float | None
    normal_min: float | None
    normal_max: float | None
    # i.e. mildly abnormal range + normal range
    not_severly_abormal_min: float | None
    not_severly_abormal_max: float | None

    def __post_init__(self):
        """Checking whether all rules are complied with."""
        if (self.min_value is not None and self.max_value is not None) and (self.min_value > self.max_value):
            raise ValueError("min_value must be less than max_value")
        if (self.normal_min is not None and self.normal_max is not None) and (self.normal_min > self.normal_max):
            raise ValueError("normal_min must be less than normal_max")
        if (self.normal_min is not None and self.min_value is not None) and (self.normal_min < self.min_value):
            raise ValueError("normal_min must be greater than min_value")
        if (self.normal_max is not None and self.max_value is not None) and (self.normal_max > self.max_value):
            raise ValueError("normal_max must be less than max_value")
        if self.not_severly_abormal_min is not None and self.normal_min is None:
            raise ValueError("normal_min must be defined if not_severly_abormal_min is defined")
        if self.not_severly_abormal_max is not None and self.normal_max is None:
            raise ValueError("normal_max must be defined if not_severly_abormal_max is defined")
        if (self.not_severly_abormal_min is not None) and (self.not_severly_abormal_min > self.normal_min):
            raise ValueError("not_severly_abormal_min must be less than normal_min")
        if (self.not_severly_abormal_max is not None) and (self.not_severly_abormal_max < self.normal_max):
            raise ValueError("not_severly_abormal_max must be greater than normal_max")

def _TEST_example_PhysicalValue() -> PhysicalValue:
    """Randmon PhysicalValue for unit tests."""

    return PhysicalValue(
        id="unique_id_2",
        name="Test physical value",
        description="Test physical value description",
        min_value=-10.5,
        max_value=10.5,
        normal_min=-3,
        normal_max=3,
        not_severly_abormal_min=-5,
        not_severly_abormal_max=5,
    )

class ValuesManager:
    """Stores description of all values in one place (singleton)"""
    _instance = None

    _scales_file_path = osutil.get_app_data_dir() / "scales.json"
    _physicals_file_path = osutil.get_app_data_dir() / "physicals.json"

    # Stored separately so that only custom values are saved on the disk.
    _scale_values_standard: dict[str, list[ScaleValue]] = {}  # sorted by category
    _physical_values_standard: list[PhysicalValue] = []
    _scale_values_custom: list[ScaleValue] = []
    _physical_values_custom: list[PhysicalValue] = []

    def __new__(cls, *args, **kwargs):
        """Singleton logic."""
        if not cls._instance:
            cls._instance = super(ValuesManager, cls).__new__(cls, *args, **kwargs)

            cls._instance._load_standard_scale_values()
            cls._instance._load_standard_physical_values()
            cls._instance._scale_values_custom +=  cls._instance._load_values_from_file(cls._instance._scales_file_path, ScaleValue)
            cls._instance._physical_values_custom += cls._instance._load_values_from_file(cls._instance._physicals_file_path, PhysicalValue)
        return cls._instance

    def __init__(self):
        """Loads predefined values that come with the app and custom values from disk."""
        self._load_standard_scale_values()
        self._load_standard_physical_values()
        self._scale_values_custom += self._load_values_from_file(self._scales_file_path, ScaleValue)
        self._physical_values_custom += self._load_values_from_file(self._physicals_file_path, PhysicalValue)

    def _load_standard_scale_values(self) -> None:
        """Loads predefined scale values that come with the app.

        Such scale values should be placed in <working dir>/values/scales/<category>.json
        files which represent a json list of objects with the same structure as 'ScaleValue'.
        """
        scale_values_dir = Path.cwd() / "values" / "scales"
        if not scale_values_dir.exists():
            return
        categories_files = scale_values_dir.glob("*.json")
        for category_file in categories_files:
            category = category_file.stem
            self._scale_values_standard[category] = []
            values_obj_list = json.loads(category_file.read_text(encoding="utf-8"))
            for value_obj in values_obj_list:
                value_obj["category"] = category
                self._scale_values_standard[category].append(ScaleValue(**value_obj))

    def _load_standard_physical_values(self) -> None:
        """Loads predefined physical values that come with the app.

        Such physical values should be placed in <working dir>/values/physicals.json
        file which represents a json list of objects with the same structure as 'PhysicalValue'.
        """
        physical_values_file = Path.cwd() / "values" / "physicals.json"
        if physical_values_file.exists():
            values_obj_list = json.loads(physical_values_file.read_text(encoding="utf-8"))
            for value_obj in values_obj_list:
                self._physical_values_standard.append(PhysicalValue(**value_obj))

    @staticmethod
    def _load_values_from_file(file: Path, Subtype: type[Value]) -> list[Value]:
        """Loads a list of values from a json file.

        If file exists, it is parsed as a json list and every element of the list
        is passed as kwargs to Subtype constructor. If file doesn't exist, empty
        list is returned."""
        if file.exists():
            dict_list = json.loads(file.read_text(encoding="utf-8"))
            return [Subtype(**obj) for obj in dict_list]
        else:
            return []

    def scale_values(self) -> dict[str, list[ScaleValue]]:
        """Returns all stored scale values as lists of 'ScaleValue' sorted by category
        field in a dict."""
        merged = self._scale_values_standard.copy()
        for value in self._scale_values_custom:
            merged.setdefault(value.category, []).append(value)
        return merged

    def physical_values(self) -> list[PhysicalValue]:
        """Returns all stored physical values as a list of 'PhysicalValue'."""
        return self._physical_values_standard + self._physical_values_custom

    def get_value_by_id(self, value_id: str) -> Value | None:
        """Returns 'ScaleValue' or 'PhysicalValue' object with the given id, or None."""
        for values in self.scale_values().values():
            for value in values:
                if value.id == value_id:
                    return value
        for value in self.physical_values():
            if value.id == value_id:
                return value
        return None

    def remove_by_id(self, value_id: str) -> None:
        """Deletes scale or physical value by its id if such exists. Only added (custom) values
        can be deleted."""
        self._scale_values_custom = [x for x in self._scale_values_custom if x.id != value_id]
        self._physical_values_custom = [x for x in self._physical_values_custom if x.id != value_id]

        self._save_all()

    def add_scale_value(self, value: ScaleValue) -> None:
        """Add a given custom scale value to the database. Result is immediately saved on the disk."""
        self._scale_values_custom.append(value)
        self._save_all()

    def add_physical_value(self, value: PhysicalValue) -> None:
        """Add a given custom physical value to the database. Result is immediately saved on the disk."""
        self._physical_values_custom.append(value)
        self._save_all()

    def _save_all(self) -> None:
        """Save all sored custom values as a json files in the working directory. Paths to files
        are defined above in the class."""
        obj_list = list(map(asdict, self._scale_values_custom))
        self._scales_file_path.write_text(json.dumps(obj_list, indent=4), encoding="utf-8")

        obj_list = list(map(asdict, self._physical_values_custom))
        self._physicals_file_path.write_text(json.dumps(obj_list, indent=4), encoding="utf-8")