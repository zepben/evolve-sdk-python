#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.iec61968.common.table_documents import TableDocuments

__all__ = ["TablePricingStructures"]


class TablePricingStructures(TableDocuments):

    @property
    def name(self) -> str:
        return "pricing_structures"