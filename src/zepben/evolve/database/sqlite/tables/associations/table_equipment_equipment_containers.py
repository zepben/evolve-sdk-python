#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableEquipmentEquipmentContainers"]


class TableEquipmentEquipmentContainers(SqliteTable):

    def __init__(self):
        super(TableEquipmentEquipmentContainers, self).__init__()
        self.equipment_mrid: Column = self._create_column("equipment_mrid", "TEXT", Nullable.NOT_NULL)
        self.equipment_container_mrid: Column = self._create_column("equipment_container_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "equipment_equipment_containers"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentEquipmentContainers, self).unique_index_columns
        cols.append([self.equipment_mrid, self.equipment_container_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableEquipmentEquipmentContainers, self).non_unique_index_columns
        cols.append([self.equipment_mrid])
        cols.append([self.equipment_container_mrid])
        return cols
