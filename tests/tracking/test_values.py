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
import dataclasses
import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from tracking.values import ScaleValue, PhysicalValue, ValuesManager, _TEST_example_ScaleValue, _TEST_example_PhysicalValue


class TestScaleValue(unittest.TestCase):

    def test_active_value_description_pairs_returns_only_active_values(self):
        value = _TEST_example_ScaleValue()
        value.min_value = 1
        value.max_value = 5
        value.value_descriptions = ["1", "2", "3", "4", "5"]
        value.has_inactive_values = True
        value.active_values = [True, False, True, False, True]

        pairs = value.active_value_description_pairs()

        returned_values = [number for number, _ in pairs]

        self.assertEqual(
            returned_values,
            [1, 3, 5]
        )


    def test_active_value_description_pairs_returns_all_active_descriptions(self):
        value = _TEST_example_ScaleValue()
        value.min_value = 1
        value.max_value = 3
        value.value_descriptions = ["low", "unused", "high"]
        value.has_inactive_values = True
        value.active_values = [True, False, True]

        pairs = value.active_value_description_pairs()

        self.assertEqual(
            pairs,
            [
                (1, "low"),
                (3, "high"),
            ]
        )


    def test_active_value_description_pairs_is_sorted(self):
        value = _TEST_example_ScaleValue()

        pairs = value.active_value_description_pairs()

        values = [number for number, _ in pairs]

        self.assertEqual(values, sorted(values))


class TestLoadValuesFromFile(unittest.TestCase):

    def test_missing_file_returns_empty_list(self):
        result = ValuesManager._load_values_from_file(
            Path("does_not_exist.json"),
            ScaleValue,
        )

        self.assertEqual(result, [])

    def test_loads_objects_from_json(self):
        original = _TEST_example_ScaleValue()

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "values.json"

            path.write_text(
                json.dumps([dataclasses.asdict(original)]),
                encoding="utf-8",
            )

            result = ValuesManager._load_values_from_file(
                path,
                ScaleValue,
            )

        self.assertEqual(len(result), 1)

        loaded = result[0]

        self.assertIsInstance(loaded, ScaleValue)
        self.assertEqual(
            dataclasses.asdict(loaded),
            dataclasses.asdict(original),
        )


# TODO: unit tests missing getting new instance produces duplicates

class TestValuesManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.scales_file = Path(self.temp_dir.name) / "scales.json"
        self.physicals_file = Path(self.temp_dir.name) / "physicals.json"

        self.scales_patch = patch.object(
            ValuesManager,
            "_scales_file_path",
            self.scales_file,
        )
        self.physicals_patch = patch.object(
            ValuesManager,
            "_physicals_file_path",
            self.physicals_file,
        )

        self.scales_patch.start()
        self.physicals_patch.start()

        # Reset singleton after patching paths.
        ValuesManager._instance = None

        self.manager = ValuesManager()

    def tearDown(self):
        ValuesManager._instance = None

        self.scales_patch.stop()
        self.physicals_patch.stop()

        self.temp_dir.cleanup()

    def test_singleton(self):
        another = ValuesManager()

        self.assertIs(self.manager, another)


    def test_get_missing_value_returns_none(self):
        result = self.manager.get_value_by_id("missing")

        self.assertIsNone(result)


    def test_add_scale_value_can_be_found(self):
        value = _TEST_example_ScaleValue()

        self.manager.add_scale_value(value)

        result = self.manager.get_value_by_id(value.id)

        self.assertIs(result, value)


    def test_add_physical_value_can_be_found(self):
        value = _TEST_example_PhysicalValue()

        self.manager.add_physical_value(value)

        result = self.manager.get_value_by_id(value.id)

        self.assertIs(result, value)


    def test_scale_values_grouped_by_category(self):
        first, second, third = (_TEST_example_ScaleValue() for i in range(3))
        first.category = "a"
        second.category = "a"
        third.category = "b"

        self.manager.add_scale_value(first)
        self.manager.add_scale_value(second)
        self.manager.add_scale_value(third)

        result = self.manager.scale_values()

        self.assertCountEqual(
            result["a"],
            [first, second]
        )

        self.assertCountEqual(
            result["b"],
            [third]
        )


    def test_remove_scale_value(self):
        value = _TEST_example_ScaleValue()

        self.manager.add_scale_value(value)
        self.manager.remove_by_id(value.id)

        self.assertIsNone(
            self.manager.get_value_by_id(value.id)
        )


    def test_remove_physical_value(self):
        value = _TEST_example_PhysicalValue()

        self.manager.add_physical_value(value)
        self.manager.remove_by_id(value.id)

        self.assertIsNone(
            self.manager.get_value_by_id(value.id)
        )


    def test_remove_missing_value_does_nothing(self):
        before = self.manager.scale_values()

        self.manager.remove_by_id("missing")

        after = self.manager.scale_values()

        self.assertEqual(before, after)

    def test_standard_value_cannot_be_removed(self):
        standard = _TEST_example_ScaleValue()

        self.manager._scale_values_standard = {"a": [standard]}

        self.manager.remove_by_id(standard.id)

        self.assertIsNotNone(
            self.manager.get_value_by_id(standard.id)
        )


if __name__ == "__main__":
    unittest.main()
