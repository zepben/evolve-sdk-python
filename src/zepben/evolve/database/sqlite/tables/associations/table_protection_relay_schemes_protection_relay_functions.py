#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import SqliteTable, Column, Nullable

__all__ = ["TableProtectionRelaySchemesProtectionRelayFunctions"]


class TableProtectionRelaySchemesProtectionRelayFunctions(SqliteTable):

    def __init__(self):
        super(TableProtectionRelaySchemesProtectionRelayFunctions, self).__init__()
        self.protection_relay_scheme_mrid: Column = self._create_column("protection_relay_scheme_mrid", "TEXT", Nullable.NOT_NULL)
        self.protection_relay_function_mrid: Column = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "protection_relay_scheme_protection_relay_functions"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelaySchemesProtectionRelayFunctions, self).unique_index_columns
        cols.append([self.protection_relay_scheme_mrid, self.protection_relay_function_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelaySchemesProtectionRelayFunctions, self).non_unique_index_columns
        cols.append([self.protection_relay_scheme_mrid])
        cols.append([self.protection_relay_function_mrid])
        return cols
