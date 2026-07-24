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
from typing import Any


class DataView(ttk.Frame):
    """
    Upper-right panel for displaying data of the selected object.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.current_object: Any | None = None

    def show(self, obj: Any) -> None:
        """
        Display data for the selected object.

        Implementation will be added later.
        """
        self.current_object = obj
