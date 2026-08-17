# noqa: N999
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
from typing import ClassVar

from tracking.metrics import Metric


# noinspection pep8-naming
class ReQoL_10(Metric):
    """
    Mental health quality of life.

    0...40
    """

    NAME: ClassVar = "ReQoL-10"
    DESCRIPTION: ClassVar = "Mental health quality of life"

    USED_PARAMS_IDS: ClassVar = [
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
    NEEDS_HISTORY: ClassVar = False
    NEEDS_HISTORY_FOR: ClassVar = None

    min_value = 0
    max_value = 40
    normal_min = 0
    normal_max = 40
    not_severely_abnormal_min = 0
    not_severely_abnormal_max = 40
    INTERP: ClassVar = None

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
