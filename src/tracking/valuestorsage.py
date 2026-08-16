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
import contextlib
import sqlite3
from datetime import datetime
from typing import Generator

from tracking.values import ValuesManager
from utils import osutil


# TODO: should be Singleton
class ValuesStorage:
    """SQLite-backed storage for integer time series."""

    _DB_PATH = osutil.get_app_data_dir() / "values.db"

    def __init__(self) -> None:
        self._connection = sqlite3.connect(self._DB_PATH)
        self._create_tables()

    def close(self) -> None:
        """Close the database connection."""
        self._connection.close()

    def _create_tables(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements (
                series_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                value REAL NOT NULL,
                PRIMARY KEY (series_id, timestamp)
            )
            """
        )
        self._connection.commit()

    def edit_value(self, series_id: str, date: datetime, value: float) -> None:
        """Update an existing value or insert it if missing."""
        self._connection.execute(
            """
            INSERT INTO measurements (series_id, timestamp, value)
            VALUES (?, ?, ?)
            ON CONFLICT(series_id, timestamp)
            DO UPDATE SET value = excluded.value
            """,
            (series_id, date.isoformat(), value),
        )

        self._connection.commit()

    def delete_value(self, series_id: str, date: datetime) -> None:
        """Delete a value.

        Raises:
            KeyError: If no value exists for the given date.
        """
        cursor = self._connection.execute(
            """
            DELETE FROM measurements
            WHERE series_id = ? AND timestamp = ?
            """,
            (series_id, date.isoformat()),
        )

        if cursor.rowcount == 0:
            raise KeyError(
                f"No value found for series '{series_id}' at {date}"
            )

        self._connection.commit()

    def get_value(self, series_id: str, date: datetime) -> float | None:
        """Get a single value by date or None if no exists."""
        cursor = self._connection.execute(
            """
            SELECT value
            FROM measurements
            WHERE series_id = ? AND timestamp = ?
            """,
            (series_id, date.isoformat()),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row[0]

    def get_range(self, series_id: str, start: datetime, end: datetime) -> list[tuple[datetime, int]]:
        """Get values in an inclusive date range in sorted order."""
        cursor = self._connection.execute(
            """
            SELECT timestamp, value
            FROM measurements
            WHERE series_id = ?
              AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp
            """,
            (
                series_id,
                start.isoformat(),
                end.isoformat(),
            ),
        )

        return [
            (datetime.fromisoformat(timestamp), int(value))
            for timestamp, value in cursor.fetchall()
        ]


@contextlib.contextmanager
def open_storage() -> Generator[ValuesStorage, None, None]:
    storage = ValuesStorage()
    try:
        yield storage
    finally:
        storage.close()
