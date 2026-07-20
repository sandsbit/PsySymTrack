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

from .registration_view import RegistrationView
from .main_view import MainView

from general.userdata import load_user_data


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Clinical Assessment")
        self.geometry("450x350")
        self.resizable(False, False)

        self.show_initial_view()

    def show_initial_view(self):
        user_data = load_user_data()

        if user_data is None:
            self.show_user_data_view()
        else:
            self.show_main_view()

    def clear_view(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_user_data_view(self):
        self.clear_view()

        view = RegistrationView(
            self,
            on_saved=self.show_main_view
        )
        view.pack(fill="both", expand=True)

    def show_main_view(self):
        self.clear_view()

        view = MainView(self)
        view.pack(fill="both", expand=True)