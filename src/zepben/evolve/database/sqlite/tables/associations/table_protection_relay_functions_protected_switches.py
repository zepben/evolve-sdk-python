#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import SqliteTable, Column, Nullable

__all__ = ["TableProtectionRelayFunctionsProtectedSwitches"]


class TableProtectionRelayFunctionsProtectedSwitches(SqliteTable):

    def __init__(self):
        super(TableProtectionRelayFunctionsProtectedSwitches, self).__init__()
        self.protection_relay_function_mrid: Column = self._create_column("protection_relay_function_mrid", "TEXT", Nullable.NOT_NULL)
        self.protected_switch_mrid: Column = self._create_column("protected_switch_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "protection_relay_functions_protected_switches"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionsProtectedSwitches, self).unique_index_columns
        cols.append([self.protection_relay_function_mrid, self.protected_switch_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableProtectionRelayFunctionsProtectedSwitches, self).non_unique_index_columns
        cols.append([self.protection_relay_function_mrid])
        cols.append([self.protected_switch_mrid])
        return cols
