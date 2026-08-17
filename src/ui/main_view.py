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

from tkinter import ttk

from ui.sections.data_view import DataView
from ui.sections.editor_view import EditorView
from ui.sections.left_panel import LeftPanel


class MainView(ttk.Frame):
    """
    Main application view.

    Layout:
        Left panel | Data view
                   | Editor view
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._create_layout()

    def _create_layout(self):
        # Main horizontal split
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

        self.left_panel = LeftPanel(
            self,
            on_selected=self._on_object_selected
        )

        self.left_panel.configure(
            width=250
        )

        self.left_panel.grid_propagate(False)

        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Right side split vertically
        self.right_panel = ttk.Frame(self)

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.right_panel.columnconfigure(
            0,
            weight=1
        )

        self.right_panel.rowconfigure(
            0,
            weight=1
        )

        self.right_panel.rowconfigure(
            1,
            weight=1
        )

        self.data_view = DataView(
            self.right_panel
        )

        self.data_view.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.editor_view = EditorView(
            self.right_panel
        )

        self.editor_view.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    def _on_object_selected(self, obj):
        self.data_view.show(obj)
        self.editor_view.show(obj)
