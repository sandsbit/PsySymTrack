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
import webbrowser


def showinfo_with_link(parent, title: str, message: str, link_text: str, url: str):
    window = tk.Toplevel(parent)
    window.title(title)
    window.resizable(False, False)

    tk.Label(
        window,
        text=message,
        wraplength=400,
        justify="left"
    ).pack(padx=20, pady=(20, 10))

    link = tk.Label(
        window,
        text=link_text,
        fg="blue",
        cursor="hand2"
    )
    link.pack(padx=20, pady=5)
    link.bind("<Button-1>", lambda e: webbrowser.open(url))

    tk.Button(
        window,
        text="OK",
        command=window.destroy
    ).pack(pady=(10, 20))

    window.transient(parent)
    window.grab_set()
    parent.wait_window(window)
