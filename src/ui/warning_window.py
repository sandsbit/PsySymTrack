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

from analysis.stats import WarningsResult, get_warnings
from tracking.metrics import Metric
from tracking.values import Value
from ui.misc.scrollable_frame import ScrollableFrame


class WarningsWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc):
        super().__init__(parent)

        self.title("Warnings")
        self.geometry("700x500")

        self.attributes("-topmost", True)

        self.category = tk.StringVar(value="Values")
        self.period = tk.StringVar(value="Acute")

        self._create_tab_selectors()

        self.blocks_frame = ScrollableFrame(self)
        self.blocks_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(5, 10)
        )

        self.reload()

    def _create_tab_selectors(self) -> None:
        selectors = ttk.Frame(self)
        selectors.pack(
            fill="x",
            padx=10,
            pady=10
        )

        category_frame = ttk.Frame(selectors)
        category_frame.pack(fill="x")

        ttk.Radiobutton(
            category_frame,
            text="Values",
            variable=self.category,
            value="Values",
            command=self.reload,
        ).pack(side="left")

        ttk.Radiobutton(
            category_frame,
            text="Metrics",
            variable=self.category,
            value="Metrics",
            command=self.reload,
        ).pack(side="left")

        period_frame = ttk.Frame(selectors)
        period_frame.pack(fill="x", pady=(5, 0))

        ttk.Radiobutton(
            period_frame,
            text="Acute",
            variable=self.period,
            value="Acute",
            command=self.reload,
        ).pack(side="left")

        ttk.Radiobutton(
            period_frame,
            text="Old",
            variable=self.period,
            value="Old",
            command=self.reload,
        ).pack(side="left")

    def reload(self) -> None:
        self.blocks_frame.clear()
        warnings = get_warnings()
        if self.category.get() == "Values":
            if self.period.get() == "Acute":
                self._add_warnings_values(warnings.values_new)
            else:
                self._add_warnings_values(warnings.values_old)
        else:
            if self.period.get() == "Acute":
                self._add_warnings_metrics(warnings.metrics_new)
            else:
                self._add_warnings_metrics(warnings.metrics_old)

    # noinspection string-conversion-without-dunder-method
    def _add_warnings_values(self, warns: list[tuple[Value, WarningsResult.WarningDescription]]):
        for value, description in warns:
            danger = description.severely_abnormal_weeks is not None
            descr = ""
            if danger:
                descr += f"Severely abnormal for {description.severely_abnormal_weeks} weeks"
            descr += f"Mean value for period: {description.mean_episode_value} (RANGE {value.normal_min}-{value.normal_max})"
            self.add_block(
                danger=danger,
                title=value.name + " is " + (" severely " if danger else "") + f"abnormal for {description.abnormal_weeks} weeks",
                description=descr
            )

    # noinspection string-conversion-without-dunder-method
    def _add_warnings_metrics(self, warns: list[tuple[type[Metric], WarningsResult.WarningDescription]]):
        for metric, description in warns:
            danger = description.severely_abnormal_weeks is not None
            descr = ""
            if danger:
                descr += f"Severely abnormal for {description.severely_abnormal_weeks} weeks\n"
            descr += f"Mean value for period: {description.mean_episode_value} (RANGE {metric.RESULT_NORMAL_MIN}-{metric.RESULT_NORMAL_MAX})"
            self.add_block(
                danger=danger,
                title=metric.NAME + " is " + (" severely " if danger else "") + f"abnormal for {description.abnormal_weeks} weeks",
                description=descr
            )

    def add_block(
        self,
        *,
        danger: bool,
        title: str,
        description: str,
    ) -> None:
        frame = ttk.Frame(
            self.blocks_frame.scrollable_frame,
            padding=10
        )

        frame.pack(
            fill="x",
            pady=5
        )

        icon = "🔴" if danger else "⚠️"

        ttk.Label(
            frame,
            text=icon,
            font=("", 18)
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="n",
            padx=(0, 10)
        )

        ttk.Label(
            frame,
            text=title,
            font=("", 10, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        ttk.Label(
            frame,
            text=description,
            wraplength=550,
            justify="left"
        ).grid(
            row=1,
            column=1,
            sticky="w"
        )

        frame.columnconfigure(
            1,
            weight=1
        )