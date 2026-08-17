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

from typing import ClassVar

from data.metrics.templates import SimpleSummator
from tracking.metrics import Metric


# noinspection pep8-naming
class GAD_7(SimpleSummator, Metric):
    """
    The Generalized Anxiety Disorder 7-item (GAD-7) is a easy to perform initial screening tool for generalized anxiety disorder.

    Score 0-4: Minimal Anxiety
    Score 5-9: Mild Anxiety
    Score 10-14: Moderate Anxiety
    Score greater than 15: Severe Anxiety
    """

    NAME: ClassVar = "GAD-7"
    DESCRIPTION: ClassVar = "Screening tool for generalized anxiety disorder"

    USED_PARAMS_IDS: ClassVar = [
        "anxiety1",
        "anxiety2",
        "anxiety3",
        "anxiety4",
        "anxiety5",
        "anxiety6",
        "anxiety7",
    ]
    NEEDS_HISTORY: ClassVar = False
    NEEDS_HISTORY_FOR: ClassVar = None

    min_value = 0
    max_value = 21
    normal_min = 0
    normal_max = 4
    not_severely_abnormal_min = 0
    not_severely_abnormal_max = 14
    INTERP: ClassVar = [
        (0, 4, "Minimal Anxiety"),
        (5, 9, "Mild Anxiety"),
        (10, 14, "Moderate Anxiety"),
        (15, 21, "Severe Anxiety")
    ]
