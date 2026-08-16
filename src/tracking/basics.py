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

from abc import ABC
from dataclasses import dataclass
from enum import Enum


@dataclass
class RangedEntity(ABC):

    min_value: float
    max_value: float
    normal_min: float
    normal_max: float
    # i.e. mildly abnormal range + normal range
    not_severely_abnormal_min: float
    not_severely_abnormal_max: float


    def _check_fields(self):
        """Checking whether all rules are complied with and smooth ranges."""
        if self.min_value > self.max_value:
            raise ValueError("min_value must be less than max_value")
        if self.normal_min > self.normal_max:
            raise ValueError("normal_min must be less than normal_max")
        if self.normal_min < self.min_value:
            raise ValueError("normal_min must be greater than min_value")
        if self.normal_max > self.max_value:
            raise ValueError("normal_max must be less than max_value")
        if self.not_severely_abnormal_min > self.normal_min:
            raise ValueError("not_severly_abormal_min must be less than normal_min")
        if self.not_severely_abnormal_max < self.normal_max:
            raise ValueError("not_severly_abormal_max must be greater than normal_max")

    class RangeValue(Enum):
        NOT_ALLOWED = 0
        NORMAL = 1
        MILDLY_ABNORMAL = 2
        SEVERELY_ABNORMAL = 3

    def check_range_for_value(self, value: float) -> RangeValue:
        if self.normal_min <= value <= self.normal_max:
            return RangedEntity.RangeValue.NORMAL
        elif self.not_severely_abnormal_min <= value <= self.not_severely_abnormal_max:
            return RangedEntity.RangeValue.MILDLY_ABNORMAL
        elif value < self.min_value or value > self.max_value:
            return RangedEntity.RangeValue.NOT_ALLOWED
        else:
            return RangedEntity.RangeValue.SEVERELY_ABNORMAL

    def is_allowed(self, value: float) -> bool:
        return self.check_range_for_value(value) != RangedEntity.RangeValue.NOT_ALLOWED

    def is_normal(self, value: float) -> bool:
        return self.check_range_for_value(value) == RangedEntity.RangeValue.NORMAL

    def is_mildly_abnormal(self, value: float) -> bool:
        return self.check_range_for_value(value) == RangedEntity.RangeValue.MILDLY_ABNORMAL

    def is_severely_abnormal(self, value: float) -> bool:
        return self.check_range_for_value(value) == RangedEntity.RangeValue.SEVERELY_ABNORMAL

    def is_abnormal(self, value: float) -> bool:
        return self.check_range_for_value(value) in [RangedEntity.RangeValue.MILDLY_ABNORMAL, RangedEntity.RangeValue.SEVERELY_ABNORMAL]
