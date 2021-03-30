#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.common_tables import TableOrganisationRoles
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects

__all__ = ["TableAssets", "TableAssetContainers", "TableAssetInfo", "TableAssetOrganisationRoles", "TableAssetOwners", "TableStructures", "TableStreetlights",
           "TablePoles"]


class TableAssets(TableIdentifiedObjects):
    location_mrid: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.location_mrid = Column(self.column_index, "location_mrid", "TEXT", Nullable.NULL)


class TableAssetContainers(TableAssets):
    pass


class TableAssetInfo(TableIdentifiedObjects):
    pass


class TableAssetOrganisationRoles(TableOrganisationRoles):
    pass


class TableAssetOwners(TableAssetOrganisationRoles):

    def name(self) -> str:
        return "asset_owners"


class TableStructures(TableAssetContainers):
    pass


class TablePoles(TableStructures):
    classification: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.classification = Column(self.column_index, "classification", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "poles"


class TableStreetlights(TableAssets):
    pole_mrid: Column = None
    lamp_kind: Column = None
    light_rating: Column = None

    def __init__(self):
        super().__init__()
        self.column_index += 1
        self.pole_mrid = Column(self.column_index, "pole_mrid", "TEXT", Nullable.NULL)
        self.column_index += 1
        self.lamp_kind = Column(self.column_index, "lamp_kind", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.light_rating = Column(self.column_index, "light_rating", "TEXT", Nullable.NOT_NULL)

    def name(self) -> str:
        return "streetlights"
