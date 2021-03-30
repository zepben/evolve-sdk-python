#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableConductingEquipment

__all__ = ["TableSwitches", "TableProtectedSwitches", "TableFuses", "TableLoadBreakSwitches", "TableBreakers", "TableReclosers", "TableJumpers",
           "TableDisconnectors"]


class TableSwitches(TableConductingEquipment):
    normal_open: Column = None
    open: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.normal_open = Column(self.column_index, "normal_open", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.open = Column(self.column_index, "open", "INTEGER", Nullable.NOT_NULL)


class TableProtectedSwitches(TableSwitches):
    pass


class TableBreakers(TableProtectedSwitches):
    def name(self) -> str:
        return "breakers"


class TableDisconnectors(TableSwitches):
    def name(self) -> str:
        return "disconnectors"


class TableFuses(TableSwitches):
    def name(self) -> str:
        return "fuses"


class TableJumpers(TableSwitches):
    def name(self) -> str:
        return "jumpers"


class TableLoadBreakSwitches(TableProtectedSwitches):
    def name(self) -> str:
        return "load_break_switches"


class TableReclosers(TableProtectedSwitches):
    def name(self) -> str:
        return "reclosers"

