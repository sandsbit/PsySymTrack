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

from datetime import datetime, timedelta
from typing import ClassVar

import numpy as np

from analysis.alerts import Alert, AlertGen
from data.metrics.GAD import GAD_7
from tracking.metrics import Metric
from utils import dateutil


class AnxietyAlerts(AlertGen):
    USED_PARAMS_IDS: ClassVar = []
    USED_METRICS: ClassVar = [GAD_7]
    GIVE_HISTORY_FOR: ClassVar = timedelta(days=31)

    def generate_alert(
            self,
            values: dict[str, list[tuple[datetime, float]]],
            metrics: dict[type[Metric], list[tuple[datetime, float]]]
    ) -> Alert | None:
        anxiety_score = metrics[GAD_7]

        if len(anxiety_score) < 2:
            return None

        if anxiety_score[-1][0] < dateutil.n_weeks_before(datetime.now(), 1):
            return None

        severity_score = float(np.mean(list(zip(*anxiety_score))[1]))
        if 4.5 <= severity_score <= 9.5:
            return Alert(
                name="Mild Anxiety Alert",
                description=f"Mild anxiety with mean GAD-7 score of {severity_score}/21",
                severity=Alert.AlertSeverity.WARNING
            )
        elif 10.5 <= severity_score <= 14.5:
            return Alert(
                name="Moderate Anxiety Alert",
                description=f"Moderate anxiety with mean GAD-7 score of {severity_score}/21",
                severity=Alert.AlertSeverity.IMPORTANT
            )
        elif 14.5 <= severity_score <= 21:
            return Alert(
                name="Severe Anxiety Alert",
                description=f"Severe anxiety with mean GAD-7 score of {severity_score}/21",
                severity=Alert.AlertSeverity.CRITICAL
            )
        else:
            return None
