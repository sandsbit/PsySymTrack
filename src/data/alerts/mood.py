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

from analysis.alerts import Alert
from data.metrics.QIDS_SR import QIDS_SR_16
from tracking.metrics import Metric
from utils import dateutil


class MoodEpisodeAlerts(Alert):
    USED_PARAMS_IDS: []
    USED_METRICS: [QIDS_SR_16]
    GIVE_HISTORY_FOR: timedelta(days=31)

    def generate_alert(
            self,
            values: dict[str, list[tuple[datetime, float]]],
            metrics: dict[type[Metric], list[tuple[datetime, float]]]
    ) -> Alert | None:
        depression_score = metrics[QIDS_SR_16]
        if len(depression_score) < 2:
            return None

        if depression_score[0][0] < dateutil.n_weeks_before(datetime.now(), 1):
            return None

        severity_score = np.mean(zip(*depression_score)[1])
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
        
        # TODO: manic and mixed
