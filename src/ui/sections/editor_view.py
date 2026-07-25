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
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from general.userdata import load_user_data
from tracking.values import Value, ScaleValue, PhysicalValue
from tracking.valuestorsage import ValuesStorage
from tracking.metrics import Metric, evaluate_metric

class EditorView(ttk.Frame):
    """
    Editor for Value objects.

    Allows:
    - selecting a week
    - editing the value for that week
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.value: Value | type[Metric] | None = None

        self.current_week = self._week_start(
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

        self.current_week = self._week_start(
            datetime.now()
        )

        self._update_week_display()
        self._build_editor()
        self._refresh_current_value()

    # ------------------------------------------------------------------
    # Week handling
    # ------------------------------------------------------------------

    def _week_start(self, date: datetime) -> datetime:
        """
        Return Monday 00:00 of the given week.
        """
        return datetime(
            date.year,
            date.month,
            date.day
        ) - timedelta(
            days=date.weekday()
        )

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

        self.current_week = self._week_start(
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

        if isinstance(self.value, ScaleValue):
            self._build_scale_editor()

        elif isinstance(self.value, PhysicalValue):
            self._build_physical_editor()

        elif issubclass(self.value, Metric):
            self._build_metric_editor()

    def _refresh_current_value(self):
        """
        Refresh selection/input when week changes.

        Reading existing value:
        """
        if self.value is None:
            return

        storage = ValuesStorage()
        try:
            if isinstance(self.value, ScaleValue):
                current_value = storage.get_value(self.value.id, self.current_week)
                if current_value is None:
                    self.scale_selection.set("")
                else:
                    self.scale_selection.set(
                        str(current_value)
                    )
            elif isinstance(self.value, PhysicalValue):
                # Clear previous value first
                self.physical_entry.delete(
                    0,
                    tk.END
                )

                current_value = storage.get_value(self.value.id, self.current_week)
                if current_value is not None:
                    self.physical_entry.delete(0, tk.END)
                    self.physical_entry.insert(0, str(current_value))
            elif issubclass(self.value, Metric):
                metric_value = evaluate_metric(self.value, load_user_data(), storage, self.current_week)
                if metric_value is None:
                    self.metric_value_label.configure(
                        text="—"
                    )

                    self.metric_progress["value"] = 0

                    self.metric_interp_label.configure(text="<UNK>")
                    self.metric_interpretation_label.configure(
                        text="Interpretation: N/A"
                    )
                else:
                    self.metric_value_label.configure(text=str(metric_value))
                    progress = (
                        metric_value - self.value.RESULT_MIN
                    ) / (
                        self.value.RESULT_MAX - self.value.RESULT_MIN
                    )
                    self.metric_progress["value"] = progress * 100

                    self.metric_interpretation_label.configure(
                        text="Interpretation: N/A"
                    )
                    int_text = ''
                    for minv, maxv, desc in self.value.INTERP:
                        int_text += f"{minv}-{maxv}: {desc}\n"
                        if minv <= metric_value <= maxv:
                            self.metric_interpretation_label.configure(
                                text="Interpretation: " + desc
                            )
                    self.metric_interp_label.configure(text=int_text)
        finally:
            storage.close()

    # ------------------------------------------------------------------
    # ScaleValue editor
    # ------------------------------------------------------------------

    def _build_scale_editor(self):
        assert isinstance(self.value, ScaleValue)

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

    def _save_scale_value(self):
        date = self.current_week
        selected_value = self.scale_selection.get()

        storage = ValuesStorage()
        try:
            storage.edit_value(self.value.id, date, int(selected_value))
        finally:
            storage.close()

    # ------------------------------------------------------------------
    # PhysicalValue editor
    # ------------------------------------------------------------------

    def _build_physical_editor(self):
        assert isinstance(self.value, PhysicalValue)

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

        storage = ValuesStorage()
        try:
            storage.edit_value(self.value.id, date, value)
        finally:
            storage.close()

    # ========= Metrics ========

    def _build_metric_editor(self):
        assert issubclass(self.value, Metric)

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
