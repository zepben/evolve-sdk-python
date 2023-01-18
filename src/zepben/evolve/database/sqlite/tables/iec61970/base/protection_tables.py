#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableEquipment, TableIdentifiedObjects

__all__ = ["TableProtectionEquipment", "TableCurrentRelays", "TableRecloseSequences"]


# noinspection PyAbstractClass
class TableProtectionEquipment(TableEquipment):
    relay_delay_time: Column = None
    protection_kind: Column = None

    def __init__(self):
        super(TableProtectionEquipment, self).__init__()
        self.relay_delay_time = self._create_column("relay_delay_time", "NUMBER", Nullable.NULL)
        self.protection_kind = self._create_column("protection_kind", "TEXT", Nullable.NOT_NULL)


class TableCurrentRelays(TableProtectionEquipment):
    current_limit_1: Column = None
    inverse_time_flag: Column = None
    time_delay_1: Column = None
    current_relay_info_mrid: Column = None

    def __init__(self):
        super(TableCurrentRelays, self).__init__()
        self.current_limit_1 = self._create_column("current_limit_1", "NUMBER", Nullable.NULL)
        self.inverse_time_flag = self._create_column("inverse_time_flag", "BOOLEAN", Nullable.NULL)
        self.time_delay_1 = self._create_column("time_delay_1", "NUMBER", Nullable.NULL)
        self.current_relay_info_mrid = self._create_column("current_relay_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "current_relays"


class TableRecloseSequences(TableIdentifiedObjects):
    protected_switch_mrid: Column = None
    reclose_delay: Column = None
    reclose_step: Column = None

    def __init__(self):
        super(TableRecloseSequences, self).__init__()
        self.protected_switch_mrid = self._create_column("protected_switch_mrid", "TEXT", Nullable.NOT_NULL)
        self.reclose_delay = self._create_column("reclose_delay", "NUMBER", Nullable.NULL)
        self.reclose_step = self._create_column("reclose_step", "INTEGER", Nullable.NULL)

    def name(self) -> str:
        return "reclose_sequences"
