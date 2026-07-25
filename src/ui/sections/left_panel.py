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
from typing import Callable

from tracking.metrics import get_all_metrics, Metric
from ui.misc.scrollable_frame import ScrollableFrame
from ui.widgets.collapsible_section import CollapsibleSection
from ui.add_value_window import AddValueWindow

from tracking.values import ValuesManager, Value


class LeftPanel(ttk.Frame):
    """
    Left navigation panel.

    Contains:
        - Add button
        - Scrollable list of grouped objects
    """

    def __init__(
        self,
        parent,
        on_selected: Callable[[Value], None],
        *args,
        **kwargs
    ):
        super().__init__(parent, *args, **kwargs)

        self.on_selected = on_selected

        self._create_layout()

    def _create_layout(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.add_button = ttk.Button(
            self,
            text="Add",
            command=self._open_add_window
        )

        self.add_button.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        self.scrollable = ScrollableFrame(
            self
        )

        self.scrollable.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.sections: list[CollapsibleSection] = []

        self.reload()

    def _open_add_window(self):
        AddValueWindow(
            self,
            on_saved=self.reload
        )

    def reload(self):
        """
        Reload objects and rebuild the list.

        Loading logic intentionally left empty.
        """

        self._clear_sections()

        manager = ValuesManager()

        scales = manager.scale_values()
        for category, values in scales.items():
            self._add_section(category, values)
        self._add_section("Physical values", manager.physical_values())

        metrics = get_all_metrics()
        self._add_section("Metrics", metrics)

    def _add_section(
        self,
        title: str,
        objects: list[Value | type[Metric]]
    ):
        section = CollapsibleSection(
            self.scrollable.scrollable_frame,
            title=title,
            on_selected=self.on_selected
        )

        section.pack(
            fill="x",
            pady=2
        )

        for obj in objects:
            section.add_entry(
                obj
            )

        self.sections.append(section)

    def _clear_sections(self):
        for section in self.sections:
            section.destroy()

        self.sections.clear()
