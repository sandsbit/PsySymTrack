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

from scipy.stats import wilcoxon
from datetime import timedelta, datetime

from analysis.alerts import Alert, AlertGen
from data.metrics.BEST import BEST
from tracking.metrics import Metric


class BPDAlert(AlertGen):
    USED_PARAMS_IDS = []
    USED_METRICS = [BEST]
    GIVE_HISTORY_FOR = timedelta(days=31*3)

    def generate_alert(
            self,
            values: dict[str, list[tuple[datetime, float]]],
            metrics: dict[type[Metric], list[tuple[datetime, float]]]
    ) -> Alert | None:
        month_before = datetime.now() - timedelta(days=31)
        values_old, values_new = [], []

        for date, value in metrics[BEST]:
            if date < month_before:
                values_old.append(value)
            else:
                values_new.append(value)

        if len(values_old) < 2 or len(values_new) < 2:
            return None

        _, p = wilcoxon(values_new, values_old, alternative="greater")
        if p <= 0.05:
            return Alert(
                name="BPD Severity has risen",
                description=f"For the last month BPD symptoms are significantly severe (p = {p})",
                severity=Alert.AlertSeverity.IMPORTANT
            )

        return None
