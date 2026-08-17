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


class PlaceholderEntry(ttk.Entry):
    """Tkinter's entry with placeholder text"""

    _has_placeholder: bool
    placeholder: str
    var: tk.StringVar

    def __init__(
        self,
        parent,
        placeholder: str,
        **kwargs
    ):
        self.placeholder = placeholder

        self.var = tk.StringVar()

        super().__init__(
            parent,
            textvariable=self.var,
            **kwargs
        )

        self._has_placeholder = False

        self._put_placeholder()

        self.bind(
            "<FocusIn>",
            self._remove_placeholder
        )

        self.bind(
            "<FocusOut>",
            self._put_placeholder
        )

    def _put_placeholder(self, *_):
        if not self.var.get():
            self.var.set(
                self.placeholder
            )

            self.configure(
                foreground="grey"
            )

            self._has_placeholder = True

    def _remove_placeholder(self, *_):
        if self._has_placeholder:
            self.var.set("")
            self.configure(
                foreground="black"
            )

            self._has_placeholder = False

    def get_value(self):
        if self._has_placeholder:
            return ""

        return self.var.get()

    def trace_add(self, mode, callback):
        self.var.trace_add(mode, callback)
