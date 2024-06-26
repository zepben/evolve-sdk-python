#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["MetadataCollectionWriter"]

from zepben.evolve.database.sqlite.common.base_collection_writer import BaseCollectionWriter
from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.common.metadata_entry_writer import MetadataEntryWriter
from zepben.evolve.services.common.meta.data_source import DataSource
from zepben.evolve.services.common.meta.metadata_collection import MetadataCollection


class MetadataCollectionWriter(BaseCollectionWriter):
    """
    Class for writing the `MetadataCollection` to the database.

    :param metadata: The `MetadataCollection` to save to the database.
    :param database_tables: The tables available in the database.
    """

    def __init__(
        self,
        metadata: MetadataCollection,
        database_tables: BaseDatabaseTables,
        writer: MetadataEntryWriter = None
    ):
        super().__init__()
        self._metadata: MetadataCollection = metadata
        self._writer: MetadataEntryWriter = writer if writer is not None else MetadataEntryWriter(database_tables)


    def save(self) -> bool:
        def log_error(it: DataSource, e: Exception):
            #todo check logging of {it}
            self._logger.error(f"Failed to save {it.__class__.__name__} {it.source}]: {e}", e)

        return self._save_each(self._metadata.data_sources, self._writer.save_data_source, log_error)
