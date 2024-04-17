#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo

__all__ = ["TableWireInfo"]


class TableWireInfo(TableAssetInfo, ABC):

    def __init__(self):
        super().__init__()
        self.rated_current: Column = self._create_column("rated_current", "NUMBER", Nullable.NULL)
        self.material: Column = self._create_column("material", "TEXT", Nullable.NOT_NULL)
