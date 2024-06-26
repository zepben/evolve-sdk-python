#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableCustomerAgreementsPricingStructures"]


class TableCustomerAgreementsPricingStructures(SqliteTable):

    def __init__(self):
        super(TableCustomerAgreementsPricingStructures, self).__init__()
        self.customer_agreement_mrid: Column = self._create_column("customer_agreement_mrid", "TEXT", Nullable.NOT_NULL)
        self.pricing_structure_mrid: Column = self._create_column("pricing_structure_mrid", "TEXT", Nullable.NOT_NULL)

    @property
    def name(self) -> str:
        return "customer_agreements_pricing_structures"

    @property
    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCustomerAgreementsPricingStructures, self).unique_index_columns
        cols.append([self.customer_agreement_mrid, self.pricing_structure_mrid])
        return cols

    @property
    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCustomerAgreementsPricingStructures, self).non_unique_index_columns
        cols.append([self.customer_agreement_mrid])
        cols.append([self.pricing_structure_mrid])
        return cols
