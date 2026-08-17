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

from analysis.alerts import Alert, AlertGen
from data.alerts.methods import significant_change_last_month
from data.metrics.ReQoL import ReQoL_10
from tracking.metrics import Metric


class QualityOfLifeAlert(AlertGen):
    USED_PARAMS_IDS: ClassVar = []
    USED_METRICS: ClassVar = [ReQoL_10]
    GIVE_HISTORY_FOR: ClassVar = timedelta(days=31*3)

    def generate_alert(
            self,
            values: dict[str, list[tuple[datetime, float]]],
            metrics: dict[type[Metric], list[tuple[datetime, float]]]
    ) -> Alert | None:
        result = significant_change_last_month(metrics[ReQoL_10], "less")
        if result is not None:
            return Alert(
                name="Quality of Life has dropped",
                description=f"For the last month quality of life index is significantly lower (p = {result})",
                severity=Alert.AlertSeverity.IMPORTANT
            )
        return None
