#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableUsagePointsEndDevices"]


class TableUsagePointsEndDevices(SqliteTable):

    def __init__(self):
        super(TableUsagePointsEndDevices, self).__init__()
        self.usage_point_mrid: Column = self._create_column("usage_point_mrid", "TEXT", Nullable.NOT_NULL)
        self.end_device_mrid: Column = self._create_column("end_device_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "usage_points_end_devices"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableUsagePointsEndDevices, self).unique_index_columns
        cols.append([self.usage_point_mrid, self.end_device_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableUsagePointsEndDevices, self).non_unique_index_columns
        cols.append([self.usage_point_mrid])
        cols.append([self.end_device_mrid])
        return cols
