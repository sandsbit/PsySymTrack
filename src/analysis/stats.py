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
from typing import Callable

import numpy as np
import numpy.typing as npt

from enum import Enum
from datetime import timedelta, datetime
from dataclasses import dataclass
from scipy.stats import pearsonr

from tracking.valuestorsage import ValuesStorage

class DateRange(Enum):
    DAYS_60 = "60 days"
    DAYS_90 = "90 days"
    DAYS_180 = "180 days"
    YEARS_1 = "1 year"
    YEARS_5 = "5 years"

    def get_timedelta(self) -> timedelta:
        return {
            DateRange.DAYS_60: timedelta(days=60),
            DateRange.DAYS_90: timedelta(days=90),
            DateRange.DAYS_180: timedelta(days=180),
            DateRange.YEARS_1: timedelta(days=365),
            DateRange.YEARS_5: timedelta(days=365*5)
        }[self]

@dataclass
class TrackingStatistics:
    min: float
    max: float
    mean: float
    median: float
    cv: float
    std: float
    rho: float
    p: float

def _monday_before(dt: datetime) -> datetime:
    monday = dt - timedelta(days=dt.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)

def _get_series(vid: str, date_range: DateRange) -> tuple[list[datetime], list[float]]:
    storage = ValuesStorage()
    try:
        end = _monday_before(datetime.now())
        start = _monday_before(end - date_range.get_timedelta())
        values = storage.get_range(vid, start, end)
        return values
    finally:
        storage.close()


# noinspection PyTypeChecker
def get_points(vid: str, date_range: DateRange) -> tuple[npt.NDArray[datetime], npt.NDArray[np.float64]]:
    return tuple(map(np.array, zip(*_get_series(vid, date_range), strict=True)))

def get_stats(vid: str, date_range: DateRange) -> TrackingStatistics:
    dates, values = get_points(vid, date_range)[1]
    dates = np.array([(date - dates[0]).days for date in dates])
    rho, p = pearsonr(dates, values)
    return TrackingStatistics(
        min=np.min(values),
        max=np.max(values),
        mean=np.mean(values),
        median=np.median(values),
        cv=np.std(values) / np.mean(values) * 100,
        std=np.std(values),
        rho=rho,
        p=p
    )
