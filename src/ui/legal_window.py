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

from app_info import LEGAL_TEXT


class LegalView(tk.Frame):
    def __init__(self, parent: tk.Misc, on_agree):
        super().__init__(parent)

        self.on_agree = on_agree

        self.agreed = tk.BooleanVar(value=False)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Legal Information",
            font=("TkDefaultFont", 16, "bold"),
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 10)
        )

        # Scrollable legal information
        text_frame = ttk.Frame(self)
        text_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15
        )

        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        text = tk.Text(
            text_frame,
            wrap="word",
            state="normal"
        )
        text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=text.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        text.configure(yscrollcommand=scrollbar.set)

        text.insert(
            "1.0",
            LEGAL_TEXT
        )

        text.configure(state="disabled")

        # Agreement
        ttk.Checkbutton(
            self,
            text="I have read and agree to the legal information.",
            variable=self.agreed
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.continue_button = ttk.Button(
            self,
            text="Agree and continue",
            command=on_agree,
            state="disabled"
        )
        self.continue_button.grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="e"
        )

        self.agreed.trace_add(
            "write",
            self._update_button
        )

    def _update_button(self, *_):
        self.continue_button.configure(
            state="normal" if self.agreed.get() else "disabled"
        )
