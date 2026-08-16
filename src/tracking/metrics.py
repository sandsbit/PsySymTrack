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
import math
import pkgutil
import warnings
from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import ClassVar

from data import metrics
from general.userdata import BasicUserData
from tracking.basics import RangedEntity
from tracking.valuestorsage import ValuesStorage

_HISTORY_TIMEDELTA = timedelta(days=31)


# noinspection unresolved-references,attribute-outside-init
class MetricNameMigrationMeta(ABCMeta):
    @property
    def RESULT_MIN(cls) -> float:
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        return cls.min_value

    @RESULT_MIN.setter
    def RESULT_MIN(cls, value: float | None):
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        if value is None:
            cls.min_value = -math.inf
        else:
            cls.min_value = value

    @property
    def RESULT_MAX(cls) -> float:
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        return cls.max_value

    @RESULT_MAX.setter
    def RESULT_MAX(cls, value: float | None):
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        if value is None:
            cls.max_value = math.inf
        else:
            cls.max_value = value

    @property
    def RESULT_NORMAL_MIN(cls) -> float:
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        return cls.normal_min

    @RESULT_NORMAL_MIN.setter
    def RESULT_NORMAL_MIN(cls, value: float | None):
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        if value is None:
            cls.normal_min = -math.inf
        else:
            cls.normal_min = value

    @property
    def RESULT_NORMAL_MAX(cls) -> float:
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        return cls.normal_max

    @RESULT_NORMAL_MAX.setter
    def RESULT_NORMAL_MAX(cls, value: float | None):
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        if value is None:
            cls.normal_max = math.inf
        else:
            cls.normal_max = value

    @property
    def RESULT_NOT_SEVERELY_ABNORMAL_MIN(cls) -> float:
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        return cls.not_severely_abnormal_min

    @RESULT_NOT_SEVERELY_ABNORMAL_MIN.setter
    def RESULT_NOT_SEVERELY_ABNORMAL_MIN(cls, value: float | None):
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        if value is None:
            cls.not_severely_abnormal_min = -math.inf
        else:
            cls.not_severely_abnormal_min = value

    @property
    def RESULT_NOT_SEVERELY_ABNORMAL_MAX(cls) -> float:
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        return cls.not_severely_abnormal_max

    @RESULT_NOT_SEVERELY_ABNORMAL_MAX.setter
    def RESULT_NOT_SEVERELY_ABNORMAL_MAX(cls, value: float | None):
        warnings.warn(
            "Old (capitalized) range fields are deprecated; use the ones from RangedEntity instead",
            DeprecationWarning,
            stacklevel=2
        )
        if value is None:
            cls.not_severely_abnormal_max = math.inf
        else:
            cls.not_severely_abnormal_max = value


class Metric(RangedEntity, ABC, metaclass=MetricNameMigrationMeta):
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
        RangedEntity.__init_subclass__()

        required_fields = {
            "NAME": str,
            "DESCRIPTION": str,
            "USED_PARAMS_IDS": list,
            "NEEDS_HISTORY": bool,
            "NEEDS_HISTORY_FOR": (list, type(None))
        }

        for name, expected_type in required_fields.items():
            if name not in cls.__dict__:
                raise ValueError(f"{cls.__name__} must define class variable {name}")
            if not isinstance(getattr(cls, name), expected_type):
                # noinspection string-conversion-without-dunder-method
                raise TypeError(
                    f"{cls.__name__}.{name} has invalid type: expected {expected_type}, got {type(getattr(cls, name))}")

        if cls.NEEDS_HISTORY_FOR is None and cls.NEEDS_HISTORY:
            raise ValueError(f"{cls.__name__}.NEEDS_HISTORY_FOR cannot be None when NEEDS_HISTORY is True")

        # Sadly it is code duplication from RangedEntity class. I haven't found a way to avoid it.
        if cls.min_value > cls.max_value:
            raise ValueError("min_value must be less than max_value")
        if cls.normal_min > cls.normal_max:
            raise ValueError("normal_min must be less than normal_max")
        if cls.normal_min < cls.min_value:
            raise ValueError("normal_min must be greater than min_value")
        if cls.normal_max > cls.max_value:
            raise ValueError("normal_max must be less than max_value")
        if cls.not_severely_abnormal_min > cls.normal_min:
            raise ValueError("not_severly_abormal_min must be less than normal_min")
        if cls.not_severely_abnormal_max < cls.normal_max:
            raise ValueError("not_severly_abormal_max must be greater than normal_max")

    @abstractmethod
    def calculate(self, params: dict[str, int | float], history: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        pass

type MetricT = type[Metric]

def get_all_metrics() -> list[MetricT]:
    """Get all children classes of Metric in data.metrics package"""
    for _, module_name, _ in pkgutil.iter_modules(metrics.__path__):
        importlib.import_module(f"{metrics.__name__}.{module_name}")
    return Metric.__subclasses__()

def evaluate_metric(metric_cls: MetricT, user_data: BasicUserData, storage: ValuesStorage, date: datetime) -> float | None:
    """Calculate metric on given date using given BasicUserData and values storage."""
    metric = metric_cls(user_data)

    params = {}
    for param_id in metric_cls.USED_PARAMS_IDS:
        value = storage.get_value(param_id, date)
        if value is None:
            return None
        params[param_id] = value

    if metric_cls.NEEDS_HISTORY:
        history = {}
        # noinspection not-iterable
        for param_id in metric_cls.NEEDS_HISTORY_FOR:
            history[param_id] = storage.get_range(param_id, (date - _HISTORY_TIMEDELTA), date)

        return metric.calculate(params, history)

    return metric.calculate(params)
