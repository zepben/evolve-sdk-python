#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import importlib
import importlib.util
import importlib.util
import pkgutil
from abc import ABC

from pytest import raises

from zepben.evolve import CustomerDatabaseTables, DiagramDatabaseTables, NetworkDatabaseTables
from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.tables.exceptions import MissingTableConfigException
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


def isabstract(obj):
    return ABC in obj.__bases__


def all_subclasses(cls, package):
    """
    Get all concrete subclasses of a given class that are defined under `package`
    :param cls: The class to check
    :param package: The package to find classes under
    :return: A set of all concrete implementations of `cls` under `package`
    """
    y = set()
    for c in cls.__subclasses__():
        if not isabstract(c) and c.__module__.startswith(package):
            y.add(c)
        y.update(all_subclasses(c, package))
    return y


def import_submodules(package: str, recursive=True):
    """ Import all submodules of a module, optionally recursively, including subpackages

    `package` package (name or actual module)
    `recursive` Whether to recursively import modules
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = f"{package.__name__}.{module_name}"
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def test_has_all_tables():
    """
    This test detects if a Table class has been added under zepben.evolve.database.sqlite.tables however hasn't been added to
    DatabaseTables
    """
    _ = import_submodules('zepben.evolve.database.sqlite.tables')
    all_final_tables = all_subclasses(SqliteTable, 'zepben.evolve.database.sqlite.tables')

    table_collections = [CustomerDatabaseTables(), DiagramDatabaseTables(), NetworkDatabaseTables()]
    used_tables = {type(it) for collection in table_collections for it in collection.tables}

    misplaced = used_tables.difference(all_final_tables)
    assert not misplaced, (
        "Using tables that aren't defined under `zepben.evolve.database.sqlite.tables`: "
        f"{', '.join([it.__name__ for it in misplaced])}"
    )

    unused = all_final_tables.difference(used_tables)
    assert not unused, (
        "Not using tables defined under `zepben.evolve.database.sqlite.tables`: "
        f"{', '.join([it.__name__ for it in unused])}"
    )


def test_database_tables():
    class MissingTable(SqliteTable, ABC):
        pass

    d = BaseDatabaseTables()

    with raises(MissingTableConfigException):
        d.get_table(MissingTable)

    with raises(MissingTableConfigException):
        d.get_insert(MissingTable)
