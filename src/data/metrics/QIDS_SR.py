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
class QIDS_SR_16(Metric):
    """
    The QIDS-SR16 can be useful in identifying depressive symptom severity and changes in these symptoms over time.
    https://alnursing.org/wp-content/uploads/2020/03/Depression-Questionnaire-QIDS-SR-16.pdf

    Normal/No Depression 0-5
    Mild Depression 6-10
    Moderate Depression 11-15
    Severe Depression 16-20
    Very Severe Depression 21-27
    """

    NAME: ClassVar = "QIDS-SR16"
    DESCRIPTION: ClassVar = "Quick self-report depressive symptoms severity scale"

    USED_PARAMS_IDS: ClassVar = [
        "sleep_onset",
        "sleep_maintenance",
        "sleep_early_awakening",
        "sleep_duration",
        "mood",
        "appetite",
        "weight_tmp_scale",
        "cognitive_concentration",
        "self_image",
        "suicide",
        "general_interest",
        "energy",
        "agitation"
    ]
    NEEDS_HISTORY: ClassVar = False
    NEEDS_HISTORY_FOR: ClassVar = None

    min_value = 0
    max_value = 27
    normal_min = 0
    normal_max = 5
    not_severely_abnormal_min = 0
    not_severely_abnormal_max = 15
    INTERP: ClassVar = [
        (0, 5, "Normal / No Depression"),
        (6, 10, "Mild Depression"),
        (11, 15, "Moderate Depression"),
        (16, 20, "Severe Depression"),
        (21, 27, "Very Severe Depression")
    ]

    def calculate(self, params: dict[str, int | float],
                  history: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        total_score = 0

        total_score += (params["sleep_onset"] - 1) if params["sleep_onset"] >= 2 else 0
        total_score += params["sleep_maintenance"]
        total_score += params["sleep_early_awakening"]
        total_score += max(params["sleep_duration"], 0)
        total_score += max(params["mood"], 0)
        total_score += abs(params["appetite"])
        total_score += abs(params["weight_tmp_scale"])
        total_score += params["cognitive_concentration"]
        total_score += max(params["self_image"], 0)
        total_score += params["suicide"]
        total_score += max(params["general_interest"], 0)
        total_score += max(params["energy"], 0)
        total_score += abs(params["agitation"])

        return total_score
