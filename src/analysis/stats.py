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

from general.userdata import load_user_data
from tracking.metrics import Metric, evaluate_metric, get_all_metrics
from tracking.values import Value, ValuesManager, ScaleValue, PhysicalValue
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

def _get_values_series(vid: str, date_range: DateRange) -> tuple[list[datetime], list[float]]:
    storage = ValuesStorage()
    try:
        end = _monday_before(datetime.now())
        start = _monday_before(end - date_range.get_timedelta())
        values = storage.get_range(vid, start, end)
        return values
    finally:
        storage.close()

def _points_for_metric(metric: type[Metric], date_range: DateRange) -> tuple[npt.NDArray[datetime], npt.NDArray[np.float64]]:
    date = _monday_before(datetime.now())
    end = _monday_before(date - date_range.get_timedelta())
    storage = ValuesStorage()
    try:
        dates = []
        values = []
        while date >= end:

            result = evaluate_metric(metric, load_user_data(), storage, date)
            if result is not None:
                dates.append(date)
                values.append(result)

            date -= timedelta(days=7)
        return (np.array(dates), np.array(values))
    finally:
        storage.close()

# noinspection PyTypeChecker
def get_points(vid: str | type[Metric], date_range: DateRange) -> tuple[npt.NDArray[datetime], npt.NDArray[np.float64]]:
    if type(vid) is str:
        return tuple(map(np.array, zip(*_get_values_series(vid, date_range), strict=True)))
    else:
        return _points_for_metric(vid, date_range)

def get_stats(vid: str| type[Metric], date_range: DateRange) -> TrackingStatistics | None:
    dates, values = get_points(vid, date_range)
    if len(values) < 2:
        return None
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

@dataclass
class WarningsResult:
    @dataclass
    class WarningDescription:
        mean_episode_value: float
        abnormal_weeks: int
        mean_severe_episode_value: float | None
        severely_abnormal_weeks: int | None

    values_new: list[tuple[Value, WarningDescription]]
    values_old: list[tuple[Value, WarningDescription]]
    metrics_new: list[tuple[type[Metric], WarningDescription]]
    metrics_old: list[tuple[type[Metric], WarningDescription]]

def _get_warning_for_value(value: Value) -> WarningsResult.WarningDescription | None:
    storage = ValuesStorage()
    values = []
    try:
        values = storage.get_range(
            value.id,
            datetime(1970, 1, 1, 0, 0, 0, 0),
            datetime.now()
        )
    finally:
        storage.close()

    is_abnormal: Callable[[Value], bool]
    is_severely_abnormal: Callable[[Value], bool]
    # TODO: the hell below should be eradicated ASAP
    if isinstance(value, ScaleValue):
        is_abnormal = lambda val: (
                ((val < value.normal_min) and (value.not_severly_abormal_min is None or val >= value.not_severly_abormal_min)) or
                                   ((val > value.normal_max) and (value.not_severly_abormal_max is None or val <= value.not_severly_abormal_max))
        )
        is_severely_abnormal = lambda val: (
                (value.not_severly_abormal_min is not None and val < value.not_severly_abormal_min) or
                (value.not_severly_abormal_max is not None and val > value.not_severly_abormal_max)
        )
    elif isinstance(value, PhysicalValue):
        is_abnormal = lambda val: (((value.normal_min is not None) and
                                   (val < value.normal_min) and (value.not_severly_abormal_min is None or val >= value.not_severly_abormal_min)) or
                                   (value.normal_max is not None) and (val > value.normal_max) and
                                   (value.not_severly_abormal_max is None or val <= value.not_severly_abormal_max))
        is_severely_abnormal = lambda val: (
                (value.not_severly_abormal_min is not None and val < value.not_severly_abormal_min) or
                (value.not_severly_abormal_max is not None and val > value.not_severly_abormal_max)
        )
    else:
        raise ValueError("Unrecognized child class of Value: only ScaleValue and PhysicalValue are supported.")

    values = values[::-1]
    severely_abnormal_streak = is_severely_abnormal(values[0][1])
    abnormal_streak = is_abnormal(values[0][1]) or severely_abnormal_streak
    abnormal_streak_since: datetime | None = None
    abnormal_streak_length = 0
    severely_abnormal_streak_length = 0
    severely_abnormal_streak_since: datetime | None = None
    for i in range(1, len(values)):
        val = values[i][1]
        if (not abnormal_streak) and (not severely_abnormal_streak):
            break

        if severely_abnormal_streak:
            severely_abnormal_streak_length += 1
            severely_abnormal_streak_since = values[i-1][0]
            severely_abnormal_streak = is_severely_abnormal(val)

        if abnormal_streak:
            abnormal_streak_length += 1
            abnormal_streak_since = values[i-1][0]
            abnormal_streak = is_abnormal(val) | is_severely_abnormal(val)

            if not abnormal_streak:
                next_abnormal = (i + 1 < len(values)) and (is_abnormal(values[i + 1][1]) or is_severely_abnormal(values[i + 1][1]))
                next_next_abnormal = (i + 2 < len(values)) and (is_abnormal(values[i + 2][1]) or is_severely_abnormal(values[i + 2][1]))
                if next_abnormal and next_next_abnormal:
                    abnormal_streak = True

    if abnormal_streak_since is None:
        assert(abnormal_streak_length == 0)
        return None

    assert(abnormal_streak_length != 0)

    return WarningsResult.WarningDescription(
        abnormal_weeks=round((datetime.now() - abnormal_streak_since).days / 7.0),
        mean_episode_value=np.mean(list(zip(*values))[1][:abnormal_streak_length]),
        severely_abnormal_weeks= None if severely_abnormal_streak_since is None
        else round((datetime.now() - severely_abnormal_streak_since).days / 7.0),
        mean_severe_episode_value= None if severely_abnormal_streak_since is None
        else np.mean(list(zip(*values))[1][:severely_abnormal_streak_length])
    )


def _get_warning_for_metric(metric: type[Metric]) -> WarningsResult.WarningDescription | None:
    metric_values = get_points(metric, DateRange.YEARS_5)

    is_abnormal: Callable[[Value], bool]
    is_severely_abnormal: Callable[[Value], bool]
    # TODO: the small second hell should also be no longer
    is_abnormal = lambda val: (((metric.RESULT_NORMAL_MIN is not None) and
                               (val < metric.RESULT_NORMAL_MIN) and (metric.RESULT_NOT_SEVERELY_ABNORMAL_MIN is None or val >= metric.RESULT_NOT_SEVERELY_ABNORMAL_MIN)) or
                               (metric.RESULT_NORMAL_MAX is not None) and (val > metric.RESULT_NORMAL_MAX) and
                               (metric.RESULT_NOT_SEVERELY_ABNORMAL_MAX is None or val <= metric.RESULT_NOT_SEVERELY_ABNORMAL_MAX))
    is_severely_abnormal = lambda val: (
            (metric.RESULT_NOT_SEVERELY_ABNORMAL_MIN is not None and val < metric.RESULT_NOT_SEVERELY_ABNORMAL_MIN) or
            (metric.RESULT_NOT_SEVERELY_ABNORMAL_MAX is not None and val > metric.RESULT_NOT_SEVERELY_ABNORMAL_MAX)
    )

    metric_values = (metric_values[0][::-1], metric_values[1][::-1])
    severely_abnormal_streak = is_severely_abnormal(metric_values[1][0])
    abnormal_streak = is_abnormal(metric_values[1][0]) or severely_abnormal_streak
    abnormal_streak_since: datetime | None = None
    abnormal_streak_length = 0
    severely_abnormal_streak_length = 0
    severely_abnormal_streak_since: datetime | None = None
    for i in range(1, len(metric_values)):
        val = metric_values[1][i]
        if (not abnormal_streak) and (not severely_abnormal_streak):
            break

        if severely_abnormal_streak:
            severely_abnormal_streak_length += 1
            severely_abnormal_streak_since = metric_values[0][i-1]
            severely_abnormal_streak = is_severely_abnormal(val)

        if abnormal_streak:
            abnormal_streak_length += 1
            abnormal_streak_since = metric_values[0][i-1]
            abnormal_streak = is_abnormal(val) | is_severely_abnormal(val)

            if not abnormal_streak:
                next_abnormal = (i + 1 < len(metric_values)) and (is_abnormal(metric_values[1][i + 1]) or is_severely_abnormal(metric_values[1][i + 1]))
                next_next_abnormal = (i + 2 < len(metric_values)) and (is_abnormal(metric_values[1][i + 2]) or is_severely_abnormal(metric_values[1][i + 2]))
                if next_abnormal and next_next_abnormal:
                    abnormal_streak = True

    if abnormal_streak_since is None:
        assert(abnormal_streak_length == 0)
        return None

    assert(abnormal_streak_length != 0)

    return WarningsResult.WarningDescription(
        abnormal_weeks=round((datetime.now() - abnormal_streak_since).days / 7.0),
        mean_episode_value=np.mean(metric_values[1][:abnormal_streak_length]),
        severely_abnormal_weeks= None if severely_abnormal_streak_since is None
        else round((datetime.now() - severely_abnormal_streak_since).days / 7.0),
        mean_severe_episode_value= None if severely_abnormal_streak_since is None
        else np.mean(metric_values[1][:severely_abnormal_streak_length])
    )

STATS_WARN_WEEKS_CUTOFF = 4

def get_warnings() -> WarningsResult:
    results = WarningsResult([], [], [], [])

    manager = ValuesManager()
    values = [value for category in manager.scale_values().values() for value in category]
    values += manager.physical_values()
    for value in values:
        warning = _get_warning_for_value(value)
        if warning is not None:
            if warning.abnormal_weeks > STATS_WARN_WEEKS_CUTOFF:
                results.values_old.append((value, warning))
            else:
                results.values_new.append((value, warning))

    for metric in get_all_metrics():
        warning = _get_warning_for_metric(metric)
        if warning is not None:
            if warning.abnormal_weeks > STATS_WARN_WEEKS_CUTOFF:
                results.metrics_old.append((metric, warning))
            else:
                results.metrics_new.append((metric, warning))

    sort_key = lambda x: (
        x[1].severely_abnormal_weeks is None,
        -x[1].abnormal_weeks,
    )

    results.values_old.sort(key=sort_key)
    results.values_new.sort(key=sort_key)
    results.metrics_old.sort(key=sort_key)
    results.metrics_new.sort(key=sort_key)

    return results
