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

from typing import ClassVar, override

from data.metrics.templates import SimpleSummator
from tracking.metrics import Metric


class ASRM(SimpleSummator, Metric):
    """
    The Altman Self-Rating Mania Scale (ASRM) is a diagnostic tool designed to assess the presence and severity of manic symptoms in individuals.

    Cutoff 6.
    """

    NAME: ClassVar = "ASRM (simplified and adapted)"
    DESCRIPTION: ClassVar = "Diagnostic tool designed to assess the presence and severity of manic symptoms in individuals."

    USED_PARAMS_IDS: ClassVar = [
        "mood",
        "self_image",
        "sleep_duration",
        "energy",
        "agitation"
    ]
    NEEDS_HISTORY: ClassVar = False
    NEEDS_HISTORY_FOR: ClassVar = None

    min_value = 0
    max_value = 20
    normal_min = 0
    normal_max = 5
    not_severely_abnormal_min = 0
    not_severely_abnormal_max = 9
    INTERP: ClassVar = [
        (0, 5, "Normal / No Mania"),
        (6, 9, "Possible Hypomania"),
        (10, 14, "Possible Mania"),
        (15, 20, "Possible Severe Mania")
    ]

    @override
    def processor(self, value: float) -> float:
        if value > 0:
            return 0
        if value == -3:
            return 4
        return -value
