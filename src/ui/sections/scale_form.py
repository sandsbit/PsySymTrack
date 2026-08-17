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
from tkinter.ttk import Combobox

from app_info import get_working_dir_path
from tracking.values import ScaleValue, ValuesManager
from ui.misc.placeholder_entry import PlaceholderEntry
from ui.misc.scrollable_frame import ScrollableFrame


class ScaleForm(ttk.Frame):

    category_options: list[str]

    def __init__(self, parent):
        super().__init__(parent)

        scale_values_dir = get_working_dir_path() / "values" / "scales"
        self.category_options = []
        if scale_values_dir.exists():
            categories_files = scale_values_dir.glob("*.json")
            for category_file in categories_files:
                self.category_options.append(category_file.stem)

        self.entries: dict[str, PlaceholderEntry | Combobox] = {}

        self.description_entries: list[tk.StringVar] = []
        self.active_entries: list[tk.BooleanVar] = []

        self.has_inactive_var = tk.BooleanVar()

        self._create_widgets()

    def _create_widgets(self):
        row = 0

        fields = [
            ("id", "Unique ID (no spaces)", ""),
            ("name", "Name", ""),
            ("description", "Description", ""),
            ("category", "Category", ""),
            ("min_value", "Minimum value (usually 1 or -3)", ""),
            ("max_value", "Maximum value (usually 5 or 3)", ""),
            ("normal_min", "Minimum of normal range", ""),
            ("normal_max", "Maximum of normal range", ""),
            ("not_severly_abormal_min", "Maximum of severely low range", "-oo"),
            ("not_severly_abormal_max", "Minimum of severely high range", "+oo"),
        ]

        for row, (name, label, placeholder) in enumerate(fields):
            self._create_entry(
                row,
                name,
                label,
                placeholder
            )
            row += 1

        ttk.Checkbutton(
            self,
            text="Nor all values in the range are permitted",
            variable=self.has_inactive_var,
            command=self._toggle_active_values
        ).grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="w"
        )

        row += 1

        ttk.Label(
            self,
            text="Specific values descriptions"
        ).grid(
            row=row,
            column=0,
            sticky="w"
        )

        row += 1

        self.description_frame = ScrollableFrame(self, height=120)
        self.description_frame.grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        row += 1

        ttk.Label(
            self,
            text="Active (permitted) values"
        ).grid(
            row=row,
            column=0,
            sticky="w"
        )

        row += 1

        self.active_frame = ScrollableFrame(self, height=120)
        self.active_frame.grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        self.active_frame.grid_remove()

        self.entries["min_value"].trace_add(
            "write",
            lambda *_: self._rebuild_dynamic_fields()
        )

        self.entries["max_value"].trace_add(
            "write",
            lambda *_: self._rebuild_dynamic_fields()
        )

        self.columnconfigure(1, weight=1)

        self.rowconfigure(
            row,
            weight=0
        )

    def _create_entry(
            self,
            row: int,
            name: str,
            label: str,
            placeholder: str
    ):
        ttk.Label(
            self,
            text=label
        ).grid(
            row=row,
            column=0,
            sticky="w"
        )

        if name == "category":
            entry = ttk.Combobox(
                self,
                values=self.category_options,
                state="readonly"
            )

            entry.current(0)

        else:
            entry = PlaceholderEntry(
                self,
                placeholder=placeholder
            )

        entry.grid(
            row=row,
            column=1,
            sticky="ew"
        )

        self.entries[name] = entry

    def _get_range(self):
        try:
            minimum = int(
                self.entries["min_value"].get()
            )
            maximum = int(
                self.entries["max_value"].get()
            )
        except ValueError:
            return None

        if maximum < minimum:
            return None

        return range(
            minimum,
            maximum + 1
        )

    def _rebuild_dynamic_fields(self):
        self._rebuild_value_descriptions()
        self._rebuild_active_values()

    def _rebuild_value_descriptions(self):
        frame = self.description_frame.scrollable_frame

        for child in frame.winfo_children():
            child.destroy()

        self.description_entries.clear()

        value_range = self._get_range()

        if value_range is None:
            return

        for row, value in enumerate(value_range):
            ttk.Label(
                frame,
                text=str(value)
            ).grid(
                row=row,
                column=0
            )

            var = tk.StringVar()

            ttk.Entry(
                frame,
                textvariable=var
            ).grid(
                row=row,
                column=1,
                sticky="ew"
            )

            self.description_entries.append(var)

    def _rebuild_active_values(self):
        frame = self.active_frame.scrollable_frame

        for child in frame.winfo_children():
            child.destroy()

        self.active_entries.clear()

        if not self.has_inactive_var.get():
            return

        value_range = self._get_range()

        if value_range is None:
            return

        for row, value in enumerate(value_range):
            var = tk.BooleanVar(
                value=True
            )

            ttk.Checkbutton(
                frame,
                text=str(value),
                variable=var
            ).grid(
                row=row,
                column=0,
                sticky="w"
            )

            self.active_entries.append(var)

    def _toggle_active_values(self):
        if self.has_inactive_var.get():
            self.active_frame.grid()
            self._rebuild_active_values()
        else:
            self.active_frame.grid_remove()
            self.active_entries.clear()

    def validate(self) -> list[str]:
        errors = []

        # Required string fields
        for name in [
            "id",
            "name",
            "description",
            "category",
        ]:
            if not self.entries[name].get().strip():
                errors.append(
                    f"{name} is required"
                )

        # Integer fields
        integer_fields = [
            "min_value",
            "max_value",
            "normal_min",
            "normal_max",
        ]

        values = {}

        for name in integer_fields:
            try:
                values[name] = int(
                    self.entries[name].get()
                )
            except ValueError:
                errors.append(
                    f"{name} must be an integer"
                )

        if ("min_value" in values and "max_value" in values) and values["max_value"] < values["min_value"]:
            errors.append(
                "max_value must be greater than min_value"
            )

        if ("normal_min" in values and "normal_max" in values) and values["normal_max"] < values["normal_min"]:
            errors.append(
                "normal_max must be greater than normal_min"
            )

        # Optional abnormal ranges
        abnormal_min = self._optional_int(
            "not_severly_abormal_min"
        )
        abnormal_max = self._optional_int(
            "not_severly_abormal_max"
        )

        if abnormal_min is None and self.entries["not_severly_abormal_min"].get().strip():
            errors.append(
                "not_severly_abormal_min must be an integer"
            )

        if abnormal_max is None and self.entries["not_severly_abormal_max"].get().strip():
            errors.append(
                "not_severly_abormal_max must be an integer"
            )

        if (abnormal_min is not None and "normal_min" in values) and abnormal_min > values["normal_min"]:
            errors.append(
                "not_severly_abormal_min must be smaller than normal_min"
            )

        if (abnormal_max is not None and "normal_max" in values) and abnormal_max < values["normal_max"]:
            errors.append(
                "not_severly_abormal_max must be greater than normal_max"
            )

        new_id = self.entries["id"].get().strip()
        manager = ValuesManager()
        all_values = [value for values in manager.scale_values().values() for value in values]
        all_values += manager.physical_values()
        for value in all_values:
            if value.id == new_id:
                errors.append(
                    "ID is not unique, chose another one"
                )

        expected_count = None
        if "min_value" in values and "max_value" in values:
            expected_count = (
                values["max_value"]
                - values["min_value"]
                + 1
            )

        if expected_count is not None:
            if len(self.description_entries) != expected_count:
                errors.append(
                    "Incorrect number of value descriptions"
                )

            if self.has_inactive_var.get() and len(self.active_entries) != expected_count:
                errors.append(
                    "Incorrect number of active values"
                )

        return errors

    def _optional_int(self, name):
        text = self.entries[name].get().strip()

        if not text:
            return None

        try:
            return int(text)
        except ValueError:
            return None

    # noinspection bad-argument-type
    def build(self) -> ScaleValue:
        return ScaleValue(
            id=self.entries["id"].get(),
            name=self.entries["name"].get(),
            description=self.entries["description"].get(),
            category=self.entries["category"].get(),

            min_value=int(self.entries["min_value"].get()),
            max_value=int(self.entries["max_value"].get()),

            value_descriptions=[
                v.get()
                for v in self.description_entries
            ],

            has_inactive_values=self.has_inactive_var.get(),

            active_values=(
                [
                    v.get()
                    for v in self.active_entries
                ]
                if self.has_inactive_var.get()
                else None
            ),

            normal_min=int(
                self.entries["normal_min"].get()
            ),
            normal_max=int(
                self.entries["normal_max"].get()
            ),

            not_severely_abnormal_min=self._optional_int(
                "not_severly_abormal_min"
            ),
            not_severely_abnormal_max=self._optional_int(
                "not_severly_abormal_max"
            ),
        )
