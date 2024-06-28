#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment_containers import TableEquipmentContainers

__all__ = ["TableSubstations"]


class TableSubstations(TableEquipmentContainers):

    def __init__(self):
        super(TableSubstations, self).__init__()
        self.sub_geographical_region_mrid: Column = self._create_column("sub_geographical_region_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "substations"

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableSubstations, self).non_unique_index_columns
        cols.append([self.sub_geographical_region_mrid])
        return cols