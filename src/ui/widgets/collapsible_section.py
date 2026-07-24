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
from typing import Callable, Any

from .object_entry import ObjectEntry


class CollapsibleSection(ttk.Frame):
    """
    Expandable/collapsible section containing ObjectEntry widgets.
    """

    def __init__(
        self,
        parent,
        title: str,
        on_selected: Callable[[Any], None],
        expanded: bool = True,
        *args,
        **kwargs
    ):
        super().__init__(parent, *args, **kwargs)

        self.title = title
        self.on_selected = on_selected
        self.expanded = expanded

        self.header = ttk.Button(
            self,
            text=self._header_text(),
            command=self.toggle
        )

        self.header.pack(
            fill="x"
        )

        self.content = ttk.Frame(self)

        if self.expanded:
            self.content.pack(
                fill="x"
            )

        self.entries: list[ObjectEntry] = []

    def _header_text(self) -> str:
        return (
            "▼ " if self.expanded else "▶ "
        ) + self.title

    def toggle(self):
        if self.expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        if not self.expanded:
            self.expanded = True
            self.content.pack(
                fill="x"
            )
            self.header.configure(
                text=self._header_text()
            )

    def collapse(self):
        if self.expanded:
            self.expanded = False
            self.content.pack_forget()
            self.header.configure(
                text=self._header_text()
            )

    def add_entry(
        self,
        obj: Any,
        text: str | None = None
    ):
        entry = ObjectEntry(
            self.content,
            obj,
            self.on_selected,
            text=text
        )

        entry.pack(
            fill="x"
        )

        self.entries.append(entry)

    def clear(self):
        for entry in self.entries:
            entry.destroy()

        self.entries.clear()
