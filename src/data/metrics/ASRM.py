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
from datetime import datetime

from tracking.metrics import Metric

class ASRM(Metric):
    """
    The Altman Self-Rating Mania Scale (ASRM) is a diagnostic tool designed to assess the presence and severity of manic symptoms in individuals.

    Cutoff 6.
    """

    NAME = "ASRM (simplified and adapted)"
    DESCRIPTION = "Diagnostic tool designed to assess the presence and severity of manic symptoms in individuals."

    USED_PARAMS_IDS = [
        "mood",
        "self_image",
        "sleep_duration",
        "energy",
        "agitation"
    ]
    NEEDS_HISTORY = False
    NEEDS_HISTORY_FOR = None

    RESULT_MIN = 0
    RESULT_MAX = 20
    RESULT_NORMAL_MIN = 0
    RESULT_NORMAL_MAX = 5
    RESULT_NOT_SEVERELY_ABNORMAL_MIN = 0
    RESULT_NOT_SEVERELY_ABNORMAL_MAX = 9
    INTERP = [
        (0, 5, "Normal / No MMania"),
        (6, 9, "Possible Hypomania"),
        (10, 14, "Possible Mania"),
        (15, 20, "Possible Severe Mania")
    ]

    @staticmethod
    def _transform_negative(value: int) -> int:
        if value > 0:
            return 0
        if value == -3:
            return 4
        return -value

    def calculate(self, params: dict[str, int | float],
                  history: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        total_score = 0

        total_score += self._transform_negative(params["mood"])
        total_score += self._transform_negative(params["self_image"])
        total_score += self._transform_negative(params["sleep_duration"])
        total_score += self._transform_negative(params["energy"])
        total_score += self._transform_negative(params["agitation"])

        return total_score
