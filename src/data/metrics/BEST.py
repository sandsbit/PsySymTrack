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

class BEST(Metric):
    """
    Borderline Evaluation of Severity over Time.

    12...72
    """

    NAME = "BEST"
    DESCRIPTION = "Borderline Evaluation of Severity over Time"

    USED_PARAMS_IDS = [
        "bpd_a_abandonment",
        "bpd_a_splitting",
        "bpd_a_self_image",
        "bpd_a_mood_swings",
        "bpd_a_dissociation",
        "bpd_a_angry",
        "bpd_a_empty",
        "bpd_a_suicide",
        "bpd_b_abandonment",
        "bpd_b_suicide",
        "bpd_b_impulsivity",
        "bpd_b_anger",
        "bpd_c_positive_behavior",
        "bpd_c_noticing",
        "bpd_c_therapy"
    ]
    NEEDS_HISTORY = False
    NEEDS_HISTORY_FOR = None

    RESULT_MIN = 12
    RESULT_MAX = 72
    RESULT_NORMAL_MIN = None
    RESULT_NORMAL_MAX = None
    RESULT_NOT_SEVERELY_ABNORMAL_MIN = None
    RESULT_NOT_SEVERELY_ABNORMAL_MAX = None
    INTERP = None

    def calculate(self, params: dict[str, int | float],
                  history: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        total_score = 15

        total_score += params["bpd_a_abandonment"]
        total_score += params["bpd_a_splitting"]
        total_score += params["bpd_a_self_image"]
        total_score += params["bpd_a_mood_swings"]
        total_score += params["bpd_a_dissociation"]
        total_score += params["bpd_a_angry"]
        total_score += params["bpd_a_empty"]
        total_score += params["bpd_a_suicide"]

        total_score += params["bpd_b_abandonment"]
        total_score += params["bpd_b_suicide"]
        total_score += params["bpd_b_impulsivity"]
        total_score += params["bpd_b_anger"]

        total_score -= params["bpd_c_positive_behavior"]
        total_score -= params["bpd_c_noticing"]
        total_score -= params["bpd_c_therapy"]

        return total_score
