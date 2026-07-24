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

import tkinter as tk
from tkinter import ttk

from ui.misc.placeholder_entry import PlaceholderEntry

from tracking.values import PhysicalValue


class PhysicalForm(ttk.Frame):

    entries: dict[str, PlaceholderEntry] = {}

    def __init__(self, parent):
        super().__init__(parent)

        self._create_widgets()

    def _create_widgets(self):
        fields = [
            ("id", "Unique ID", ""),
            ("name", "Name", ""),
            ("description", "Description", ""),
            ("min_value", "Minimal possible value", "-oo"),
            ("max_value", "Maximal possible value", "+oo"),
            ("normal_min", "Minimum of the normal range", "-oo"),
            ("normal_max", "Maximum of the normal range", "+oo"),
            ("not_severly_abormal_min", "Maximum of severely low range", "-oo"),
            ("not_severly_abormal_max", "Minimum of severely high range", "+oo"),
        ]

        for row, (name, label, default) in enumerate(fields):
            self._create_entry(
                row,
                name,
                label,
                default
            )

        self.columnconfigure(1, weight=1)

    def _create_entry(
            self,
            row: int,
            name: str,
            label: str,
            default: str
    ):
        ttk.Label(
            self,
            text=label
        ).grid(
            row=row,
            column=0,
            sticky="w"
        )

        entry = PlaceholderEntry(
            self,
            placeholder=default
        )

        entry.grid(
            row=row,
            column=1,
            sticky="ew"
        )

        self.entries[name] = entry

    def _optional_float(self, name):
        text = self.entries[name].get().strip()

        if not text:
            return None

        try:
            return float(text)
        except ValueError:
            return None

    def validate(self) -> list[str]:
        errors = []

        for name in [
            "id",
            "name",
            "description",
        ]:
            if not self.entries[name].get().strip():
                errors.append(
                    f"{name} is required"
                )

        values = {}

        for name in [
            "min_value",
            "max_value",
            "normal_min",
            "normal_max",
        ]:
            value = self._optional_float(name)

            if (
                value is None
                and self.entries[name].get().strip()
                not in ("", "None")
            ):
                errors.append(
                    f"{name} must be a number"
                )
            else:
                values[name] = value

        if (
            values["min_value"] is not None
            and values["max_value"] is not None
            and values["max_value"] < values["min_value"]
        ):
            errors.append(
                "max_value must be greater than min_value"
            )

        if (
            values["normal_min"] is not None
            and values["normal_max"] is not None
            and values["normal_max"] < values["normal_min"]
        ):
            errors.append(
                "normal_max must be greater than normal_min"
            )

        abnormal_min = self._optional_float(
            "not_severly_abormal_min"
        )

        abnormal_max = self._optional_float(
            "not_severly_abormal_max"
        )

        if (
            abnormal_min is not None
            and values["normal_min"] is not None
            and abnormal_min > values["normal_min"]
        ):
            errors.append(
                "not_severly_abormal_min must be smaller than normal_min"
            )

        if (
            abnormal_max is not None
            and values["normal_max"] is not None
            and abnormal_max < values["normal_max"]
        ):
            errors.append(
                "not_severly_abormal_max must be greater than normal_max"
            )

        # TODO: Check whether id is unique.

        return errors

    def build(self) -> PhysicalValue:
        return PhysicalValue(
            id=self.entries["id"].get(),
            name=self.entries["name"].get(),
            description=self.entries["description"].get(),

            min_value=self._optional_float(
                "min_value"
            ),
            max_value=self._optional_float(
                "max_value"
            ),

            normal_min=self._optional_float(
                "normal_min"
            ),
            normal_max=self._optional_float(
                "normal_max"
            ),

            not_severly_abormal_min=self._optional_float(
                "not_severly_abormal_min"
            ),
            not_severly_abormal_max=self._optional_float(
                "not_severly_abormal_max"
            ),
        )
