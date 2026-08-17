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

from analysis.alerts import Alert, generate_alerts
from general.userdata import load_user_data
from tracking.valuestorsage import open_storage
from ui.misc.scrollable_frame import ScrollableFrame


class AlertsWindow(tk.Toplevel):
    def __init__(self, parent: tk.Misc):
        super().__init__(parent)

        self.title("Alerts")
        self.geometry("700x500")

        self.attributes("-topmost", True)

        self.blocks_frame = ScrollableFrame(self)
        self.blocks_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(5, 10)
        )

        self.reload()

    def reload(self) -> None:
        self.blocks_frame.clear()

        with open_storage() as storage:
            # noinspection bad-argument-type
            warnings = generate_alerts(load_user_data(), storage)
            for warning in warnings:
                self.add_block(
                    severity=warning.severity,
                    title=warning.name,
                    description=warning.description
                )

    def add_block(
        self,
        *,
        severity: Alert.AlertSeverity,
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

        icon = ""
        match severity:
            case Alert.AlertSeverity.WARNING:
                icon = "⚠️"
            case Alert.AlertSeverity.IMPORTANT:
                icon = "🔴"
            case Alert.AlertSeverity.CRITICAL:
                icon = "☠️"

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