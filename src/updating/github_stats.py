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

import warnings

import requests

REST_RELEASES_URL = "https://api.github.com/repos/sandsbit/PsySymTrack/releases"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10"
}

def get_latest_version() -> str | None:
    response = requests.get(REST_RELEASES_URL, headers=HEADERS)
    if response.status_code != 200:
        warnings.warn("Could not get latest version from GitHub. Response code: " + str(response.status_code), RuntimeWarning)
        return None

    versions = response.json()
    for version in versions:
        number = version["tag_name"][1:]
        if "-" not in number:
            return number
    return None

