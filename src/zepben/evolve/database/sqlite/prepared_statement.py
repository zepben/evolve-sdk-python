#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from sqlite3 import Cursor
from typing import Dict, Any, Optional

from dataclassy import dataclass
from zepben.evolve import Ratio


class SqlException(Exception):
    pass


@dataclass(slots=True)
class PreparedStatement(object):
    statement: str
    _values: Dict[int, Any] = dict()
    _num_cols: int = None

    def __init__(self):
        self._num_cols = self.statement.count('?')

    @property
    def num_columns(self):
        return self._num_cols

    @property
    def parameters(self):
        """
        Get the string representation of the current parameters set on this PreparedStatement.
        '(unset)' means this index has not yet been set.
        This function should be used for error handling and debugging only.

        Returns the string representation of all parameters that have been set on this PreparedStatement, separated by commas.
        """
        pm = []
        for i in range(1, self.num_columns + 1):
            try:
                pm.append(str(self._values[i]))
            except KeyError:
                pm.append("(unset)")
        return ", ".join(pm)

    def execute(self, cursor: Cursor):
        """
        Execute this PreparedStatement using the given `cursor`.

        Throws any exception possible from cursor.execute, typically `sqlite3.DatabaseError`
        """
        parameters = []
        missing = []
        for i in range(1, self.num_columns + 1):
            try:
                parameters.append(self._values[i])
            except KeyError:
                missing.append(str(i))

        if missing:
            raise SqlException(f"Missing values for indices {', '.join(missing)}. Ensure all ?'s have a corresponding value in the prepared statement.")

        cursor.execute(self.statement, parameters)

    def add_value(self, index: int, value: Any):
        if 0 < index <= self._num_cols:
            self._values[index] = value
        else:
            raise SqlException(f"index must be between 1 and {self.num_columns} for this statement, got {index}")

    def add_ratio(self, numerator_index: int, denominator_index: int, value: Optional[Ratio]):
        if value is None:
            self.add_value(numerator_index, None)
            self.add_value(denominator_index, None)
        else:
            self.add_value(numerator_index, value.numerator)
            self.add_value(denominator_index, value.denominator)
