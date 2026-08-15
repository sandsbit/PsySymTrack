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

class ReQoL_10(Metric):
    """
    Mental health quality of life.

    0...40
    """

    NAME = "ReQoL-10"
    DESCRIPTION = "Mental health quality of life"

    USED_PARAMS_IDS = [
        "qol_tasks",
        "qol_trust",
        "qol_coping",
        "qol_do_things",
        "qol_mood",
        "qol_life_worth",
        "qol_joy",
        "qol_hopeful",
        "qol_lonely",
        "qol_confident"
    ]
    NEEDS_HISTORY = False
    NEEDS_HISTORY_FOR = None

    RESULT_MIN = 0
    RESULT_MAX = 40
    RESULT_NORMAL_MIN = None
    RESULT_NORMAL_MAX = None
    RESULT_NOT_SEVERELY_ABNORMAL_MIN = None
    RESULT_NOT_SEVERELY_ABNORMAL_MAX = None
    INTERP = None

    def calculate(self, params: dict[str, int | float],
                  history: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        total_score = 0

        total_score += (4 - params["qol_tasks"])
        total_score += params["qol_trust"]
        total_score += (4 - params["qol_coping"])
        total_score += params["qol_do_things"]
        total_score += params["qol_mood"]
        total_score += params["qol_life_worth"]
        total_score += params["qol_joy"]
        total_score += params["qol_hopeful"]
        total_score += (4 - params["qol_lonely"])
        total_score += params["qol_confident"]


        return total_score
