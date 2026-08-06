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
import importlib
import pkgutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta, datetime
from enum import Enum
from typing import ClassVar

from general.userdata import BasicUserData
from tracking.metrics import Metric, evaluate_metric
from data import alerts
from tracking.valuestorsage import ValuesStorage


@dataclass
class Alert:
    class AlertSeverity(Enum):
        WARNING = 0
        IMPORTANT = 1
        CRITICAL = 2

    name: str
    description: str
    severity: AlertSeverity

class AlertGen(ABC):
    """Base class for all Alerts - important notifications based on values and metrics."""

    user_data: BasicUserData

    def __init__(self, user_data: BasicUserData):
        self.user_data = user_data

    USED_PARAMS_IDS: ClassVar[list[str]]
    USED_METRICS: ClassVar[list[type[Metric]]]
    GIVE_HISTORY_FOR: ClassVar[timedelta]

    @abstractmethod
    def generate_alert(
            self,
            values: dict[str, list[tuple[datetime, float]]],
            metrics: dict[type[Metric], list[tuple[datetime, float]]]
    ) -> Alert | None:
        pass

type AlertGenT = type[AlertGen]

def get_all_metrics() -> list[AlertGenT]:
    for _, module_name, _ in pkgutil.iter_modules(alerts.__path__):
        importlib.import_module(f"{alerts.__name__}.{module_name}")
    return AlertGen.__subclasses__()

def _monday_before(dt: datetime) -> datetime:
    monday = dt - timedelta(days=dt.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)

def evaluate_alert(alert_cls: AlertGenT, user_data: BasicUserData, storage: ValuesStorage) -> Alert | None:
    alert_gen = alert_cls(user_data)

    end = _monday_before(datetime.now())
    start = _monday_before(end - alert_cls.GIVE_HISTORY_FOR)

    params = {}
    for param_id in alert_gen.USED_PARAMS_IDS:
        values = storage.get_range(param_id, start, end)
        params[param_id] = values

    metrics = {}
    for metricT in alert_gen.USED_METRICS:
        metrics[metricT] = []
        date = start
        while date <= end:
            metric_value = evaluate_metric(metricT, user_data, storage, date)
            if metric_value is not None:
                metrics[metricT].append((date, metric_value))

            date += timedelta(days=7)

    return alert_gen.generate_alert(params, metrics)
