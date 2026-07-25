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

import inspect
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import ClassVar

from general.userdata import BasicUserData
from data import metrics
from tracking.valuestorsage import ValuesStorage

_HISTORY_TIMEDELTA = timedelta(days=31)

class Metric(ABC):
    """Base class for all Metrics - properties that are calculated based on values"""

    user_data: BasicUserData

    def __init__(self, user_data: BasicUserData):
        self.user_data = user_data

    # ==== About metric ====
    NAME: ClassVar[str]
    DESCRIPTION: ClassVar[str]

    USED_PARAMS_IDS: ClassVar[list[str]]
    NEEDS_HISTORY: ClassVar[bool]
    NEEDS_HISTORY_FOR: ClassVar[list[str] | None]
    RESULT_MIN: ClassVar[float]
    RESULT_MAX: ClassVar[float]
    RESULT_NORMAL_MIN: ClassVar[float | None]
    RESULT_NORMAL_MAX: ClassVar[float | None]
    RESULT_NOT_SEVERELY_ABNORMAL_MIN: ClassVar[float | None]
    RESULT_NOT_SEVERELY_ABNORMAL_MAX: ClassVar[float | None]
    INTERP: ClassVar[list[tuple[int, int, str]] | None]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        required_fields = {
            "NAME": str,
            "DESCRIPTION": str,
            "USED_PARAMS_IDS": list,
            "NEEDS_HISTORY": bool,
            "NEEDS_HISTORY_FOR": (list, type(None)),
            "RESULT_MIN": (float, int),
            "RESULT_MAX": (float, int),
            "RESULT_NORMAL_MIN": (float, int, type(None)),
            "RESULT_NORMAL_MAX": (float, int, type(None)),
            "RESULT_NOT_SEVERELY_ABNORMAL_MIN": (float, int, type(None)),
            "RESULT_NOT_SEVERELY_ABNORMAL_MAX": (float, int, type(None)),
        }

        for name, expected_type in required_fields.items():
            if name not in cls.__dict__:
                raise ValueError(f"{cls.__name__} must define class variable {name}")
            if not isinstance(getattr(cls, name), expected_type):
                raise ValueError(
                    f"{cls.__name__}.{name} has invalid type: expected {expected_type}, got {type(getattr(cls, name))}")

        if cls.NEEDS_HISTORY_FOR is None and cls.NEEDS_HISTORY:
            raise ValueError(f"{cls.__name__}.NEEDS_HISTORY_FOR cannot be None when NEEDS_HISTORY is True")

        ranges = [
            ("RESULT", cls.RESULT_MIN, cls.RESULT_MAX),
            ("RESULT_NORMAL", cls.RESULT_NORMAL_MIN, cls.RESULT_NORMAL_MAX),
            ("RESULT_NOT_SEVERELY_ABNORMAL", cls.RESULT_NOT_SEVERELY_ABNORMAL_MIN,
             cls.RESULT_NOT_SEVERELY_ABNORMAL_MAX),
        ]

        for name, minimum, maximum in ranges:
            if minimum is not None and maximum is not None and minimum > maximum:
                raise ValueError(f"{cls.__name__}: {name}_MIN must be <= {name}_MAX")

        if cls.RESULT_NORMAL_MIN is not None and cls.RESULT_MIN is not None and cls.RESULT_NORMAL_MIN < cls.RESULT_MIN:
            raise ValueError(f"{cls.__name__}: RESULT_NORMAL_MIN must be >= RESULT_MIN")

        if cls.RESULT_NORMAL_MIN is not None and cls.RESULT_MAX is not None and cls.RESULT_NORMAL_MIN > cls.RESULT_MAX:
            raise ValueError(f"{cls.__name__}: RESULT_NORMAL_MIN must be <= RESULT_MAX")

        if cls.RESULT_NORMAL_MAX is not None and cls.RESULT_MIN is not None and cls.RESULT_NORMAL_MAX < cls.RESULT_MIN:
            raise ValueError(f"{cls.__name__}: RESULT_NORMAL_MAX must be >= RESULT_MIN")

        if cls.RESULT_NORMAL_MAX is not None and cls.RESULT_MAX is not None and cls.RESULT_NORMAL_MAX > cls.RESULT_MAX:
            raise ValueError(f"{cls.__name__}: RESULT_NORMAL_MAX must be <= RESULT_MAX")

        if cls.RESULT_NOT_SEVERELY_ABNORMAL_MIN is not None and cls.RESULT_NORMAL_MIN is None:
            raise ValueError(f"{cls.__name__}: RESULT_NORMAL_MIN must be set when RESULT_NOT_SEVERELY_ABNORMAL_MIN is set")

        if cls.RESULT_NOT_SEVERELY_ABNORMAL_MIN is not None and cls.RESULT_NOT_SEVERELY_ABNORMAL_MIN > cls.RESULT_NORMAL_MIN:
            raise ValueError(f"{cls.__name__}: RESULT_NOT_SEVERELY_ABNORMAL_MIN must be <= RESULT_NORMAL_MIN")

        if cls.RESULT_NOT_SEVERELY_ABNORMAL_MAX is not None and cls.RESULT_NORMAL_MAX is None:
            raise ValueError(
                f"{cls.__name__}: RESULT_NORMAL_MAX must be set when RESULT_NOT_SEVERELY_ABNORMAL_MAX is set")

        if cls.RESULT_NOT_SEVERELY_ABNORMAL_MAX is not None and cls.RESULT_NOT_SEVERELY_ABNORMAL_MAX < cls.RESULT_NORMAL_MAX:
            raise ValueError(f"{cls.__name__}: RESULT_NOT_SEVERELY_ABNORMAL_MAX must be >= RESULT_NORMAL_MAX")

    @abstractmethod
    def calculate(self, params: dict[str, int | float], history: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        pass

type MetricT = type[Metric]

def get_all_metrics() -> list[MetricT]:
    """Get all children classes of Metric in data.metrics package"""
    metric_classes = []
    for _, module in inspect.getmembers(metrics, inspect.ismodule):
        metric_classes += [mcls for _, mcls in inspect.getmembers(module, inspect.isclass) if isinstance(mcls, Metric)]
    return metric_classes

def evaluate_metric(metric_cls: MetricT, user_data: BasicUserData, storage: ValuesStorage, date: datetime) -> float | None:
    metric = metric_cls(user_data)

    params = {}
    for param_id in metric_cls.USED_PARAMS_IDS:
        value = storage.get_value(param_id, date)
        if value is None:
            return None
        params[param_id] = value

    if metric_cls.NEEDS_HISTORY:
        history = {}
        for param_id in metric_cls.NEEDS_HISTORY_FOR:
            history[param_id] = storage.get_range(param_id, (date - _HISTORY_TIMEDELTA), date)

        return metric.calculate(params, history)

    return metric.calculate(params)
