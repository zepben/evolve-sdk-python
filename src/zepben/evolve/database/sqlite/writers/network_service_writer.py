#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService
from zepben.evolve.database.sqlite.writers.base_cim_writer import BaseCIMWriter
from zepben.evolve.database.sqlite.writers.network_cim_writer import NetworkCIMWriter


class NetworkServiceWriter(BaseCIMWriter):

    def save(self, service: NetworkService, writer: NetworkCIMWriter) -> bool:
        status = self.save(service, writer)
        # todo: Finish this method
        return False