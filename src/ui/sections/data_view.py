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
import math
import tkinter as tk
from datetime import datetime
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from analysis.stats import DateRange, TrackingStatistics, get_points, get_stats
from tracking.basics import RangedEntity
from tracking.metrics import Metric
from tracking.values import Value
from utils import dateutil


class DataView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.current_object: Value | type[Metric] | None = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # Left side
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")

        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # Period selector
        period_frame = ttk.Frame(left_frame)
        period_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        ttk.Label(period_frame, text="Period:").pack(side="left")

        self.date_range_var = tk.StringVar()

        self.date_range_combo = ttk.Combobox(
            period_frame,
            textvariable=self.date_range_var,
            values=[date_range.value for date_range in DateRange],
            state="readonly",
        )
        self.date_range_combo.pack(side="left", padx=(5, 0))

        self.date_range_combo.bind(
            "<<ComboboxSelected>>",
            self._date_range_changed,
        )

        # Plot
        plot_frame = ttk.Frame(left_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew")

        self.figure = Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("No data")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=plot_frame,
        )
        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
        )

        # Right side statistics
        stats_frame = ttk.Frame(self, padding=10)
        stats_frame.grid(row=0, column=1, sticky="ns")

        self.stat_labels: dict[str, ttk.Label] = {}

        fields = [
            ("min", "Minimum"),
            ("max", "Maximum"),
            ("mean", "Mean"),
            ("median", "Median"),
            ("cv", "Coefficient of variation"),
            ("std", "Standard deviation"),
            ("rho", "Pearson correlation (ρ)"),
            ("p", "Pearson p-value"),
        ]

        for row, (field, label) in enumerate(fields):
            ttk.Label(
                stats_frame,
                text=f"{label}:",
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 10),
            )

            value_label = ttk.Label(
                stats_frame,
                text="-",
            )
            value_label.grid(
                row=row,
                column=1,
                sticky="w",
            )

            self.stat_labels[field] = value_label

    def show(self, obj: Value | type[Metric]) -> None:
        self.current_object = obj

        if len(DateRange) > 0:
            self.date_range_combo.current(0)

        self._refresh()

    def _date_range_changed(self, _event: tk.Event) -> None:
        self._refresh()

    def _refresh(self) -> None:
        if self.current_object is None:
            return

        selected_range = DateRange(self.date_range_var.get())

        if isinstance(self.current_object, Value):
            statistics = get_stats(self.current_object.id, selected_range)
        else:
            statistics = get_stats(self.current_object, selected_range)

        if statistics is not None:
            self._update_statistics(statistics)

        self.ax.clear()

        if isinstance(self.current_object, Value):
            dates, values = get_points(self.current_object.id, selected_range)
        else:
            # noinspection bad-argument-type
            dates, values = get_points(self.current_object, selected_range)
        self.ax.plot(dates, values)

        now = datetime.now()
        # noinspection bad-argument-type
        self.ax.set_xlim(dateutil.monday_before(now - selected_range.get_timedelta()), now)

        abs_min = self.current_object.min_value
        if math.isinf(abs_min):
            if len(values) > 0:
                abs_min = min(np.min(values), 0)
            else:
                abs_min = 0
        abs_max = self.current_object.max_value
        if math.isinf(abs_max):
            if len(values) > 0:
                abs_max = np.max(values) * 1.2
            else:
                abs_max = 100
        ranges = self.current_object.get_ranges(abs_min, abs_max)

        to_process = [
            RangedEntity.RangeType.NORMAL,
            RangedEntity.RangeType.MILDLY_ABNORMAL,
            RangedEntity.RangeType.SEVERELY_ABNORMAL
        ]
        colors = [
            "green",
            "yellow",
            "red"
        ]

        self.ax.set_ylim(*ranges[RangedEntity.RangeType.TOTAL_ALLOWED])

        for range_type, color in zip(to_process, colors):
            for start, end in ranges[range_type]:
                self.ax.axhspan(start, end, color=color, alpha=0.2)

        if isinstance(self.current_object, Value):
            self.ax.set_title(self.current_object.name)
        else:
            self.ax.set_title(self.current_object.NAME)
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Value")

        self.figure.autofmt_xdate()

        self.canvas.draw()

    def _update_statistics(
        self,
        statistics: TrackingStatistics,
    ) -> None:
        values = {
            "min": statistics.min,
            "max": statistics.max,
            "mean": statistics.mean,
            "median": statistics.median,
            "cv": statistics.cv,
            "std": statistics.std,
            "rho": statistics.rho,
            "p": statistics.p,
        }

        for key, value in values.items():
            self.stat_labels[key].configure(
                text=f"{value:.3f}",
            )

        color = "green" if statistics.p < 0.05 else "red"

        self.stat_labels["rho"].configure(
            foreground=color,
        )
        self.stat_labels["p"].configure(
            foreground=color,
        )
