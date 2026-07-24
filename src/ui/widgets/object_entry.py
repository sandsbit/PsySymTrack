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
from typing import Callable

from tracking.values import Value


class ObjectEntry(ttk.Frame):
    """
    A clickable row representing one object.

    Displays an optional icon, title, and description.
    Calls on_selected(object) when clicked.
    """

    def __init__(
        self,
        parent,
        obj: Value,
        on_selected: Callable[[Value], None],
        title: str,
        description: str | None = None,
        icon: tk.PhotoImage | None = None,
        *args,
        **kwargs
    ):
        super().__init__(parent, *args, **kwargs)

        self.obj = obj
        self.on_selected = on_selected

        self.icon = icon

        # Keep reference to image.
        # Otherwise Tkinter may garbage collect it.
        self._icon_label = None

        if icon is not None:
            self._icon_label = ttk.Label(
                self,
                image=icon
            )
            self._icon_label.grid(
                row=0,
                column=0,
                rowspan=2,
                padx=(5, 5),
                pady=3
            )

        text_frame = ttk.Frame(self)

        text_frame.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="w",
            padx=5,
            pady=3
        )

        self.title_label = ttk.Label(
            text_frame,
            text=title,
            anchor="w"
        )

        self.title_label.pack(
            fill="x"
        )

        self.description_label = None

        if description:
            self.description_label = ttk.Label(
                text_frame,
                text=description,
                anchor="w"
            )

            self.description_label.pack(
                fill="x"
            )

        self.columnconfigure(
            1,
            weight=1
        )

        self._bind_click(self)

    def _bind_click(self, widget):
        widget.bind(
            "<Button-1>",
            self._clicked
        )

        for child in widget.winfo_children():
            self._bind_click(child)

    def _clicked(self, _event=None):
        self.on_selected(self.obj)
