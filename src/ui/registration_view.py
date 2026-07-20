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
from datetime import datetime
from typing import Callable

from general.userdata import BasicUserData, Sex, save_user_data


class RegistrationView(ttk.Frame):
    def __init__(
            self,
            parent,
            on_saved: Callable[[], None]
    ):
        super().__init__(parent, padding=20)

        self.on_saved = on_saved

        ttk.Label(
            self,
            text="Enter basic information",
            font=("Segoe UI", 14)
        ).pack(pady=(0, 20))

        # Date of birth
        ttk.Label(self, text="Date of birth (YYYY-MM-DD)").pack(anchor="w")

        self.date_var = tk.StringVar()

        ttk.Entry(
            self,
            textvariable=self.date_var
        ).pack(fill="x", pady=(0, 10))

        # Sex
        ttk.Label(self, text="Sex").pack(anchor="w")

        self.sex_var = tk.StringVar()

        self.sex_dropdown = ttk.Combobox(
            self,
            textvariable=self.sex_var,
            values=[sex.value for sex in Sex],
            state="readonly"
        )

        self.sex_dropdown.pack(fill="x", pady=(0, 10))

        if len(Sex) > 0:
            self.sex_dropdown.current(0)

        # Height
        ttk.Label(self, text="Height (cm)").pack(anchor="w")

        self.height_var = tk.StringVar()

        ttk.Entry(
            self,
            textvariable=self.height_var
        ).pack(fill="x", pady=(0, 20))

        ttk.Button(
            self,
            text="Save",
            command=self.save
        ).pack()

    def save(self):
        # Date validation
        try:
            date_of_birth = datetime.strptime(
                self.date_var.get(),
                "%Y-%m-%d"
            )
        except ValueError:
            messagebox.showerror(
                "Invalid value",
                "Date must have format YYYY-MM-DD."
            )
            return

        # Height validation
        try:
            height = int(self.height_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid value",
                "Height must be an integer."
            )
            return

        if height <= 0:
            messagebox.showerror(
                "Invalid value",
                "Height must be positive."
            )
            return

        # Enum validation
        try:
            sex = Sex(self.sex_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid value",
                "Please select a valid sex."
            )
            return

        user_data = BasicUserData(
            date_of_birth=date_of_birth,
            sex=sex,
            height_cm=height
        )

        save_user_data(user_data)

        self.on_saved()