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
from tracking.metrics import Metric


class LithiumAlerts(AlertGen):
    USED_PARAMS_IDS = ["lithium"]
    USED_METRICS = [ASRM]
    GIVE_HISTORY_FOR = timedelta(days=31*3)

    def generate_alert(
            self,
            values: dict[str, list[tuple[datetime, float]]],
            metrics: dict[type[Metric], list[tuple[datetime, float]]]
    ) -> Alert | None:
        if len(values["lithium"]) == 0:
            return None

        lithium_serum = values["lithium"][-1][1]

        if 0 <= lithium_serum <= 0.5:
            return Alert(
                name="Subtheraputic lithium level",
                description="Lithium level is below theraputic range",
                severity=Alert.AlertSeverity.WARNING
            )
        elif 1.2 <= lithium_serum <= 1.5:
            if len(metrics[ASRM]) == 0 or metrics[ASRM][-1][1] < 6:
                return Alert(
                    name="High lithium level",
                    description="Lithium level is in mania-range but no acute mania",
                    severity=Alert.AlertSeverity.WARNING
                )
            return None
        elif 1.5 <= lithium_serum <= 2.0:
            return Alert(
                name="High lithium level",
                description="Lithium level is above theraputic range. Toxcicity is possible",
                severity=Alert.AlertSeverity.IMPORTANT
            )
        elif lithium_serum >= 2.0:
            return Alert(
                name="Toxic lithium level",
                description="Lithium level is in toxic range. Seek immidiate medical attention",
                severity=Alert.AlertSeverity.CRITICAL
            )
        else:
            return None
