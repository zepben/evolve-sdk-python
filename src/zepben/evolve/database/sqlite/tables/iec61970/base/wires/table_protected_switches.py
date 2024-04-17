#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_switches import TableSwitches

__all__ = ["TableProtectedSwitches"]


class TableProtectedSwitches(TableSwitches, ABC):

    def __init__(self):
        super(TableProtectedSwitches, self).__init__()
        self.breaking_capacity: Column = self._create_column("breaking_capacity", "INTEGER", Nullable.NULL)
