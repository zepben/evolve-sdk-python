#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import SqliteTable, Column, Nullable

__all__ = ["TablePowerTransformerEndRatings"]


class TablePowerTransformerEndRatings(SqliteTable):

    def __init__(self):
        super(TablePowerTransformerEndRatings, self).__init__()
        self.power_transformer_end_mrid: Column = self._create_column("power_transformer_end_mrid", "TEXT", Nullable.NOT_NULL)
        self.cooling_type: Column = self._create_column("cooling_type", "TEXT", Nullable.NOT_NULL)
        self.rated_s: Column = self._create_column("rated_s", "INTEGER", Nullable.NOT_NULL)

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerTransformerEndRatings, self).non_unique_index_columns
        cols.append([self.power_transformer_end_mrid])
        return cols

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePowerTransformerEndRatings, self).unique_index_columns
        cols.append([self.power_transformer_end_mrid, self.cooling_type])
        return cols

    @property
    def name(self) -> str:
        return "power_transformer_end_ratings"
