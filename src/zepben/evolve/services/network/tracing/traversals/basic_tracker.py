#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["BasicTracker"]

from typing import TypeVar, Set

from zepben.evolve import Tracker

T = TypeVar("T")


class BasicTracker(Tracker[T]):
    """
    An interface used by `Traversal`'s to 'track' items that have been visited.
    """
    visited: Set = set()

    def has_visited(self, item: T) -> bool:
        """
        Check if the tracker has already seen an item.
        `item` The item to check if it has been visited.
        Returns true if the item has been visited, otherwise false.
        """
        return item in self.visited

    def visit(self, item: T) -> bool:
        """
        Visit an item. Item will not be visited if it has previously been visited.
        `item` The item to visit.
        Returns True if visit succeeds. False otherwise.
        """
        if item in self.visited:
            return False
        else:
            self.visited.add(item)
            return True

    def clear(self):
        """
        Clear the tracker, removing all visited items.
        """
        self.visited.clear()

    def copy(self):
        """
        Create a new `BasicTracker` with the same visited items. Does not other class members. e.g. queue, step actions or stop conditions etc.
        """
        # noinspection PyArgumentList
        return BasicTracker(visited=self.visited.copy())
