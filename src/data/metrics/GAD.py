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

class GAD_7(Metric):
    """
    The Generalized Anxiety Disorder 7-item (GAD-7) is a easy to perform initial screening tool for generalized anxiety disorder.

    Score 0-4: Minimal Anxiety
    Score 5-9: Mild Anxiety
    Score 10-14: Moderate Anxiety
    Score greater than 15: Severe Anxiety
    """

    NAME = "GAD-7"
    DESCRIPTION = "Screening tool for generalized anxiety disorder"

    USED_PARAMS_IDS = [
        "sleep_onset"
    ]
    NEEDS_HISTORY = False
    NEEDS_HISTORY_FOR = None

    RESULT_MIN = 0
    RESULT_MAX = 21
    RESULT_NORMAL_MIN = 0
    RESULT_NORMAL_MAX = 4
    RESULT_NOT_SEVERELY_ABNORMAL_MIN = 0
    RESULT_NOT_SEVERELY_ABNORMAL_MAX = 14
    INTERP = [
        (0, 4, "Minimal Anxiety"),
        (5, 9, "Mild Anxiety"),
        (10, 14, "Moderate Anxiety"),
        (15, 21, "Severe Anxiety")
    ]

    def calculate(self, params: dict[str, int | float],
                  history: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        total_score = 0

        for i in range(1, 7):
            total_score += params["anxiety" + str(i)]

        return total_score
