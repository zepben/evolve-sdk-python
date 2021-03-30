#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable

__all__ = ["TableAssetOrganisationRolesAssets"]


class TableAssetOrganisationRolesAssets(SqliteTable):
    asset_organisation_role_mrid: Column = None
    asset_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.asset_organisation_role_mrid = Column(self.column_index, "asset_organisation_role_mrid", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.asset_mrid = Column(self.column_index, "asset_mrid", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "asset_organisation_roles_assets"

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super().unique_index_columns()
        cols.append([self.asset_organisation_role_mrid, self.asset_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super().non_unique_index_columns()
        cols.append([self.asset_organisation_role_mrid])
        cols.append([self.asset_mrid])
        return cols
