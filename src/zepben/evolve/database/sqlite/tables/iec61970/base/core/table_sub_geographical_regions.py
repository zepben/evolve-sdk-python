#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects

__all__ = ["TableSubGeographicalRegions"]


class TableSubGeographicalRegions(TableIdentifiedObjects):

    def __init__(self):
        super(TableSubGeographicalRegions, self).__init__()
        self.geographical_region_mrid: Column = self._create_column("geographical_region_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "sub_geographical_regions"

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableSubGeographicalRegions, self).non_unique_index_columns
        cols.append([self.geographical_region_mrid])
        return cols
