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

from datetime import datetime
from typing import ClassVar


class SimpleSummator:
    """Base class for metrics that just find a sum of all parameters. You can override processor
    method to process values before adding them to the sum."""

    USED_PARAMS_IDS: ClassVar[list[str]]

    # noinspection method-may-be-static
    def processor(self, value: float) -> float:
        return value

    def calculate(self, params: dict[str, int | float],
                  _: dict[str, list[tuple[datetime, int]]] | None = None) -> float | None:
        sum_ = 0
        for param in self.USED_PARAMS_IDS:
            sum_ += self.processor(params[param])
        return sum_
