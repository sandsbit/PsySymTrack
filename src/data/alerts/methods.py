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
from typing import Literal

from scipy.stats import wilcoxon


def significant_change_last_month(
        points: list[tuple[datetime, float]],
        alternative: Literal["two-sided", "less", "greater"] = "greater"
    ) -> float | None:
    """
    Calculates whether there has been a significant change in data trend during last month.

    There should be at least two points during last month and two points before.

    For checks Wilcoxon signed-rank test is used.

    :param points: pairs (date, value) for last several months (recommended at least 2).
    :param alternative: "greater" tells to check for significant raise, "less" - for drop.
    :return: p-value, or None if too little data or result insignificant (p < 0.05).
    """
    month_before = datetime.now() - timedelta(days=31)
    values_old, values_new = [], []

    for date, value in points:
        if date < month_before:
            values_old.append(value)
        else:
            values_new.append(value)

    if len(values_old) < 2 or len(values_new) < 2:
        return None

    _, p = wilcoxon(values_new, values_old, alternative=alternative)
    if p <= 0.05:
        return p

    return None
