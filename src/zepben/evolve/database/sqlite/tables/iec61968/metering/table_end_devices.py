#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_containers import TableAssetContainers

__all__ = ["TableEndDevices"]


class TableEndDevices(TableAssetContainers, ABC):

    def __init__(self):
        super(TableEndDevices, self).__init__()
        self.customer_mrid: Column = self._create_column("customer_mrid", "TEXT", Nullable.NULL)
        self.service_location_mrid: Column = self._create_column("service_location_mrid", "TEXT", Nullable.NULL)
