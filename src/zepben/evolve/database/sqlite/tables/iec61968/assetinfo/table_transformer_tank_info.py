#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo

__all__ = ["TableTransformerTankInfo"]


class TableTransformerTankInfo(TableAssetInfo):

    def __init__(self):
        super().__init__()
        self.power_transformer_info_mrid: Column = self._create_column("power_transformer_info_mrid", "TEXT", Nullable.NULL)

    @property
    def name(self) -> str:
        return "transformer_tank_info"

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns
        cols.append([self.power_transformer_info_mrid])
        return cols
