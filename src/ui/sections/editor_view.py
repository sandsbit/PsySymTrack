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
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

from general.userdata import load_user_data
from tracking.metrics import Metric, evaluate_metric
from tracking.values import PhysicalValue, ScaleValue, Value
from tracking.valuestorsage import ValuesStorage, open_storage
from utils import dateutil


class EditorView(ttk.Frame):
    """
    Editor for Value objects.

    Allows:
    - selecting a week
    - editing the value for that week
    """

    def __init__(self, parent, main_view, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.main_view = main_view

        self.value: Value | type[Metric] | None = None

        self.current_week = dateutil.monday_before(
            datetime.now()
        )

        self._create_layout()

    def _create_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Week selector
        self.week_frame = ttk.Frame(self)

        self.week_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=5
        )

        ttk.Button(
            self.week_frame,
            text="◀",
            command=lambda: self._change_week(-1)
        ).pack(
            side="left"
        )

        self.date_entry = ttk.Entry(
            self.week_frame,
            width=12
        )

        self.date_entry.pack(
            side="left",
            padx=5
        )

        self.date_entry.bind(
            "<Return>",
            self._date_entered
        )

        ttk.Button(
            self.week_frame,
            text="▶",
            command=lambda: self._change_week(1)
        ).pack(
            side="left"
        )

        # Editor area
        self.editor_frame = ttk.Frame(self)

        self.editor_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self._update_week_display()

    def show(self, value: Value):
        """
        Display editor for a selected Value object.
        """
        self.value = value

        self.current_week = dateutil.monday_before(
            datetime.now()
        )

        self._update_week_display()
        self._build_editor()
        self._refresh_current_value()

    # ------------------------------------------------------------------
    # Week handling
    # ------------------------------------------------------------------

    def _change_week(self, offset: int):
        self.current_week += timedelta(
            weeks=offset
        )

        self._update_week_display()
        self._refresh_current_value()

    def _date_entered(self, _event=None):
        try:
            date = datetime.fromisoformat(
                self.date_entry.get()
            )
        except ValueError:
            return

        self.current_week = dateutil.monday_before(
            date
        )

        self._update_week_display()
        self._refresh_current_value()

    def _update_week_display(self):
        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            self.current_week.strftime("%Y-%m-%d")
        )

    # ------------------------------------------------------------------
    # Editor creation
    # ------------------------------------------------------------------

    def _build_editor(self):
        for widget in self.editor_frame.winfo_children():
            widget.destroy()

        # noinspection bad-argument-type
        if isinstance(self.value, ScaleValue):
            self._build_scale_editor()

        elif isinstance(self.value, PhysicalValue):
            self._build_physical_editor()

        elif issubclass(self.value, Metric):
            self._build_metric_editor()

    # noinspection unresolved-references
    def _refresh_current_value_scale(self, storage: ValuesStorage):
        current_value = storage.get_value(self.value.id, self.current_week)
        if current_value is None:
            self.scale_selection.set("")
        else:
            self.scale_selection.set(
                str(int(current_value))
            )

    # noinspection unresolved-references
    def _refresh_current_value_physical(self, storage: ValuesStorage):
        # Clear previous value first
        self.physical_entry.delete(0, tk.END)

        current_value = storage.get_value(self.value.id, self.current_week)
        if current_value is not None:
            self.physical_entry.delete(0, tk.END)
            self.physical_entry.insert(0, str(current_value))

    # noinspection bad-argument-type,unresolved-references
    def _refresh_current_value_metric(self, storage: ValuesStorage):
        user_data = load_user_data()
        assert user_data is not None
        metric_value = evaluate_metric(
            self.value, user_data, storage, self.current_week
        )
        if metric_value is None:
            self.metric_value_label.configure(text="—")

            self.metric_progress["value"] = 0

            self.metric_interp_label.configure(text="<UNK>")
            self.metric_interpretation_label.configure(text="Interpretation: N/A")
        else:
            self.metric_value_label.configure(text=str(metric_value))
            progress = (metric_value - self.value.RESULT_MIN) / (
                self.value.RESULT_MAX - self.value.RESULT_MIN
            )
            self.metric_progress["value"] = progress * 100

            self.metric_interpretation_label.configure(text="Interpretation: N/A")
            int_text = ""
            if self.value.INTERP is not None:
                for minv, maxv, desc in self.value.INTERP:
                    int_text += f"{minv}-{maxv}: {desc}\n"
                    if minv <= metric_value <= maxv:
                        self.metric_interpretation_label.configure(
                            text="Interpretation: " + desc
                        )
            self.metric_interp_label.configure(text=int_text)

    def _refresh_current_value(self):
        """
        Refresh selection/input when week changes.

        Reading existing value:
        """
        if self.value is None:
            return

        with open_storage() as storage:
            # noinspection bad-argument-type
            if isinstance(self.value, ScaleValue):
                self._refresh_current_value_scale(storage)
            elif isinstance(self.value, PhysicalValue):
                self._refresh_current_value_physical(storage)
            elif issubclass(self.value, Metric):
                self._refresh_current_value_metric(storage)

    # ------------------------------------------------------------------
    # ScaleValue editor
    # ------------------------------------------------------------------

    def _build_scale_editor(self):
        assert isinstance(self.value, ScaleValue)

        ttk.Label(
            self.editor_frame,
            text=self.value.name,
            font="Helvetica 22 bold"
        ).pack(
                anchor="w"
        )

        ttk.Label(
            self.editor_frame,
            text=self.value.description,
            font="Helvetica 16"
        ).pack(
                anchor="w"
        )

        self.scale_selection = tk.StringVar(value="")

        for value, description in (
            self.value.active_value_description_pairs()
        ):
            ttk.Radiobutton(
                self.editor_frame,
                text=f"{value}: {description}",
                variable=self.scale_selection,
                value=str(value),
                command=self._save_scale_value
            ).pack(
                anchor="w"
            )

    # noinspection unresolved-references
    def _save_scale_value(self):
        date = self.current_week
        selected_value = self.scale_selection.get()

        with open_storage() as storage:
            storage.edit_value(self.value.id, date, int(selected_value))
            self.main_view.data_view.refresh()

    # ------------------------------------------------------------------
    # PhysicalValue editor
    # ------------------------------------------------------------------

    def _build_physical_editor(self):
        assert isinstance(self.value, PhysicalValue)

        ttk.Label(
            self.editor_frame,
            text=self.value.name,
            font="Helvetica 22 bold"
        ).pack(
                anchor="w"
        )

        ttk.Label(
            self.editor_frame,
            text=self.value.description,
            font="Helvetica 16"
        ).pack(
                anchor="w"
        )

        label = (
            f"{self.value.name} "
            f"({self.value.min_value} - {self.value.max_value}):"
        )

        ttk.Label(
            self.editor_frame,
            text=label
        ).pack(
            anchor="w"
        )

        self.physical_entry = ttk.Entry(
            self.editor_frame
        )

        self.physical_entry.pack(
            fill="x"
        )

        ttk.Button(
            self.editor_frame,
            text="Save",
            command=self._save_physical_value
        ).pack(
            pady=5
        )

    def _save_physical_value(self):
        try:
            value = float(
                self.physical_entry.get()
            )

        except ValueError:
            messagebox.showerror(
                "Invalid value",
                "Value must be a number."
            )
            return

        assert isinstance(self.value, PhysicalValue)

        if not (
            self.value.min_value
            <= value
            <= self.value.max_value
        ):
            messagebox.showerror(
                "Invalid value",
                "Value is outside allowed range."
            )
            return

        date = self.current_week

        with open_storage() as storage:
            storage.edit_value(self.value.id, date, value)
            self.main_view.data_view.refresh()

    # ========= Metrics ========

    def _build_metric_editor(self):
        # noinspection bad-argument-type
        assert issubclass(self.value, Metric)

        ttk.Label(
            self.editor_frame,
            text=self.value.NAME,
            font="Helvetica 22 bold"
        ).pack(
                anchor="w"
        )

        ttk.Label(
            self.editor_frame,
            text=self.value.DESCRIPTION,
            font="Helvetica 16"
        ).pack(
                anchor="w"
        )

        #
        # Current value
        #

        self.metric_value_label = ttk.Label(
            self.editor_frame,
            font=("", 18, "bold")
        )

        self.metric_value_label.pack(
            pady=(5, 10)
        )

        #
        # Progress bar
        #

        self.metric_progress = ttk.Progressbar(
            self.editor_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100
        )

        self.metric_progress.pack(
            fill="x",
            padx=10
        )

        #
        # General interpretation
        #

        self.metric_interp_label = ttk.Label(
            self.editor_frame,
            wraplength=450,
            justify="left"
        )
        self.metric_interp_label.pack(
            anchor="w",
            padx=10,
            pady=(10, 0)
        )

        #
        # Current interpretation
        #

        self.metric_interpretation_label = ttk.Label(
            self.editor_frame,
            foreground="red",
            wraplength=450,
            justify="left"
        )

        self.metric_interpretation_label.pack(
            anchor="w",
            padx=10,
            pady=(5, 0)
        )
