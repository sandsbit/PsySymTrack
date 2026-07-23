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


class ScrollableFrame(ttk.Frame):
    """
    A vertically scrollable frame.

    Widgets should be added to self.scrollable_frame.
    """

    def __init__(self, parent, height=150, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            height=height
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = ttk.Frame(
            self.canvas
        )

        self.scrollable_frame.bind(
            "<Configure>",
            self._update_scroll_region
        )

        self._window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.columnconfigure(
            0,
            weight=1
        )

        self.rowconfigure(
            0,
            weight=1
        )

        self.canvas.bind(
            "<Configure>",
            self._resize_frame
        )

        # Important: do not let children decide the frame size
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.configure(
            height=height
        )

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _resize_frame(self, event):
        self.canvas.itemconfigure(
            self._window,
            width=event.width
        )
