#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import SqliteTable, Column, Nullable

__all__ = ["TablePricingStructuresTariffs"]


class TablePricingStructuresTariffs(SqliteTable):

    def __init__(self):
        super(TablePricingStructuresTariffs, self).__init__()
        self.pricing_structure_mrid: Column = self._create_column("pricing_structure_mrid", "TEXT", Nullable.NOT_NULL)
        self.tariff_mrid: Column = self._create_column("tariff_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "pricing_structures_tariffs"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePricingStructuresTariffs, self).unique_index_columns
        cols.append([self.pricing_structure_mrid, self.tariff_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePricingStructuresTariffs, self).non_unique_index_columns
        cols.append([self.pricing_structure_mrid])
        cols.append([self.tariff_mrid])
        return cols
