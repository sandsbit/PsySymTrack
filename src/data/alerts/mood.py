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

import numpy as np
from datetime import timedelta, datetime

from analysis.alerts import Alert, AlertGen
from data.metrics.ASRM import ASRM
from data.metrics.QIDS_SR import QIDS_SR_16
from tracking.metrics import Metric
from utils import dateutil


class MoodEpisodeAlerts(AlertGen):
    USED_PARAMS_IDS = []
    USED_METRICS = [QIDS_SR_16, ASRM]
    GIVE_HISTORY_FOR = timedelta(days=31)

    @staticmethod
    def _depression_alert(depression_score: list[tuple[datetime, float]]) -> Alert | None:
        if len(depression_score) < 2:
            return None

        if depression_score[-1][0] < dateutil.n_weeks_before(datetime.now(), 1):
            return None

        severity_score = np.mean(list(zip(*depression_score))[1])
        if 6 <= severity_score <= 10.5:
            return Alert(
                name="Mild Depression Alert",
                description=f"Mild depression with mean QIDS_SR_16 score of {severity_score}/27",
                severity=Alert.AlertSeverity.WARNING
            )
        elif 10.5 <= severity_score <= 15.5:
            return Alert(
                name="Moderate Depression Alert",
                description=f"Moderate depression with mean QIDS_SR_16 score of {severity_score}/27",
                severity=Alert.AlertSeverity.IMPORTANT
            )
        elif 15.5 <= severity_score <= 27:
            return Alert(
                name="Severe Depression Alert",
                description=f"Severe depression with mean QIDS_SR_16 score of {severity_score}/27",
                severity=Alert.AlertSeverity.CRITICAL
            )
        else:
            return None

    @staticmethod
    def _mania_alert(mania_score: list[tuple[datetime, float]]) -> Alert | None:
        if len(mania_score) < 1:
            return None

        if mania_score[-1][0] < dateutil.n_weeks_before(datetime.now(), 1):
            return None

        severity_score = max(np.mean(list(zip(*mania_score))[1]), mania_score[-1][1])
        if 6 <= severity_score <= 9.5:
            return Alert(
                name="Hypomania Alert",
                description=f"Possible hypomania (or mania) with mean ASRM (adapted) score of {severity_score}/20",
                severity=Alert.AlertSeverity.WARNING
            )
        elif 9.5 <= severity_score <= 14.5:
            return Alert(
                name="Mania Alert",
                description=f"Possible mania (or hypomania) with mean ASRM (adapted) score of {severity_score}/20",
                severity=Alert.AlertSeverity.IMPORTANT
            )
        elif 14.5 <= severity_score <= 20:
            return Alert(
                name="Severe Mania Alert",
                description=f"Possible mania (or hypomania) with mean ASRM (adapted) score of {severity_score}/20",
                severity=Alert.AlertSeverity.CRITICAL
            )
        else:
            return None

    def generate_alert(
            self,
            values: dict[str, list[tuple[datetime, float]]],
            metrics: dict[type[Metric], list[tuple[datetime, float]]]
    ) -> Alert | None:
        depression_alert = self._depression_alert(metrics[QIDS_SR_16])
        mania_alert = self._mania_alert(metrics[ASRM])

        if (depression_alert is not None and depression_alert.AlertSeverity != Alert.AlertSeverity.WARNING) and mania_alert is not None:
            return Alert(
                name="Mixed Episode Alert",
                description="Possible depression/(hypo)mania with mixed features!",
                severity=Alert.AlertSeverity.CRITICAL
            )
        if mania_alert is not None:
            return mania_alert
        return depression_alert
