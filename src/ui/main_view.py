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

from ui.add_value_window import AddValueWindow


class MainView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        ttk.Button(
            self,
            text="Add value",
            command=self.open_add_value
        ).pack()

    def open_add_value(self):
        AddValueWindow(self.parent)