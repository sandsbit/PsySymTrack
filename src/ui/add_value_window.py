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

from ui.forms.scale_form import ScaleForm
from ui.forms.physical_form import PhysicalForm

from tracking.values import ValuesManager, ScaleValue, PhysicalValue


class AddValueWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title(
            "Add value"
        )

        self.geometry("600x700")
        self.minsize(600, 400)

        self.form = None

        self.value_type = tk.StringVar(
            value="Scale"
        )

        self._create_widgets()

        self._switch_form()

    def _create_widgets(self):

        ttk.Label(
            self,
            text="Value type"
        ).pack(
            anchor="w",
            padx=10,
            pady=5
        )

        selector = ttk.Combobox(
            self,
            state="readonly",
            values=[
                "Scale",
                "Physical",
            ],
            textvariable=self.value_type
        )

        selector.pack(
            fill="x",
            padx=10
        )

        selector.bind(
            "<<ComboboxSelected>>",
            lambda _: self._switch_form()
        )

        self.form_container = ttk.Frame(
            self
        )

        self.form_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.add_button = ttk.Button(
            self,
            text="Add",
            command=self._add
        )

        self.add_button.pack(
            pady=10
        )

    def _switch_form(self):

        for child in self.form_container.winfo_children():
            child.destroy()

        if self.value_type.get() == "Scale":
            self.form = ScaleForm(
                self.form_container
            )
        else:
            self.form = PhysicalForm(
                self.form_container
            )

        self.form.pack(
            fill="both",
            expand=False
        )

    def _add(self):

        errors = self.form.validate()

        if errors:
            messagebox.showerror(
                "Invalid value",
                "\n".join(errors),
                parent=self
            )
            return

        value = self.form.build()

        manager = ValuesManager()

        if isinstance(value, ScaleValue):
            manager.add_scale_value(
                value
            )

        elif isinstance(value, PhysicalValue):
            manager.add_physical_value(
                value
            )

        self.destroy()
