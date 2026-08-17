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

import unittest
from datetime import datetime
from typing import ClassVar

from analysis.alerts import Alert
from data.alerts.mood import MoodEpisodeAlerts
from data.metrics.ASRM import ASRM
from data.metrics.QIDS_SR import QIDS_SR_16
from general.userdata import BasicUserData, Sex


class TestMoodAlerts(unittest.TestCase):

    VALUES_NORMAL: ClassVar = {
        QIDS_SR_16: [
            (datetime(2026, 8, 3, 0, 0), 3),
            (datetime(2026, 8, 10, 0, 0), 4),
            (datetime(2026, 8, 17, 0, 0), 7),
            (datetime(2026, 8, 24, 0, 0), 4),
            (datetime(2026, 8, 31, 0, 0), 3)
        ],
        ASRM: [
            (datetime(2026, 8, 3, 0, 0), 0),
            (datetime(2026, 8, 10, 0, 0), 2),
            (datetime(2026, 8, 17, 0, 0), 0),
            (datetime(2026, 8, 24, 0, 0), 3),
            (datetime(2026, 8, 31, 0, 0), 0)
        ]
    }

    VALUES_MODERATELY_DEPRESSED: ClassVar = {
        QIDS_SR_16: [
            (datetime(2026, 8, 3, 0, 0), 13),
            (datetime(2026, 8, 10, 0, 0), 11),
            (datetime(2026, 8, 17, 0, 0), 15),
            (datetime(2026, 8, 24, 0, 0), 14),
            (datetime(2026, 8, 31, 0, 0), 14)
        ],
        ASRM: [
            (datetime(2026, 8, 3, 0, 0), 0),
            (datetime(2026, 8, 10, 0, 0), 0),
            (datetime(2026, 8, 17, 0, 0), 1),
            (datetime(2026, 8, 24, 0, 0), 0),
            (datetime(2026, 8, 31, 0, 0), 0)
        ]
    }

    VALUES_MANIC: ClassVar = {
        QIDS_SR_16: [
            (datetime(2026, 8, 3, 0, 0), 2),
            (datetime(2026, 8, 10, 0, 0), 1),
            (datetime(2026, 8, 17, 0, 0), 1),
            (datetime(2026, 8, 24, 0, 0), 2),
            (datetime(2026, 8, 31, 0, 0), 1)
        ],
        ASRM: [
            (datetime(2026, 8, 3, 0, 0), 17),
            (datetime(2026, 8, 10, 0, 0), 16),
            (datetime(2026, 8, 17, 0, 0), 16),
            (datetime(2026, 8, 24, 0, 0), 19),
            (datetime(2026, 8, 31, 0, 0), 17)
        ]
    }

    VALUES_MIXED: ClassVar = {
        QIDS_SR_16: VALUES_MODERATELY_DEPRESSED[QIDS_SR_16],
        ASRM: VALUES_MANIC[ASRM]
    }

    # noinspection unresolved-references
    def test_mood_alerts(self):
        alert_gen = MoodEpisodeAlerts(
            BasicUserData(datetime(2004, 8, 28, 0, 0), Sex.MALE, 178)
        )

        normal = alert_gen.generate_alert({}, self.VALUES_NORMAL)
        moderate_depression = alert_gen.generate_alert({}, self.VALUES_MODERATELY_DEPRESSED)
        mania = alert_gen.generate_alert({}, self.VALUES_MANIC)
        mixed = alert_gen.generate_alert({}, self.VALUES_MIXED)

        self.assertIsNone(normal)

        self.assertIsNotNone(moderate_depression)
        self.assertTrue("depress" in moderate_depression.name.lower())
        self.assertEqual(moderate_depression.severity, Alert.AlertSeverity.IMPORTANT)

        self.assertIsNotNone(mania)
        self.assertTrue("mania" in mania.name.lower())
        self.assertEqual(mania.severity, Alert.AlertSeverity.CRITICAL)

        self.assertIsNotNone(mixed)
        self.assertTrue("mixed" in mixed.name.lower())

if __name__ == '__main__':
    unittest.main()
