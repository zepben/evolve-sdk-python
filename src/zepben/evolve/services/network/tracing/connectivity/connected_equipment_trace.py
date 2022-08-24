#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Functions to create commonly used connectivity based traces. These ignore phases, they are purely to trace equipment that
are connected in any way. You can add custom step actions and stop conditions to the returned traversal.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from zepben.evolve import BasicTraversal, depth_first, ConductingEquipmentStepTracker, breadth_first, ignore_open, normally_open, currently_open, \
    ConductingEquipmentStep
from zepben.evolve.services.network.network_service import connected_equipment
from zepben.evolve.services.network.tracing.connectivity.connected_equipment_traversal import ConnectedEquipmentTraversal
from zepben.evolve.services.network.tracing.connectivity.limited_connected_equipment_trace import LimitedConnectedEquipmentTrace
if TYPE_CHECKING:
    from zepben.evolve.types import OpenTest, QueueNext
    T = TypeVar("T")

__all__ = ["new_connected_equipment_trace", "new_connected_equipment_breadth_trace", "new_normal_connected_equipment_trace",
           "new_current_connected_equipment_trace", "new_normal_limited_connected_equipment_trace", "new_current_limited_connected_equipment_trace"]


def _queue_next(open_test: OpenTest) -> QueueNext[ConductingEquipmentStep]:
    def queue_next(step: ConductingEquipmentStep, traversal: BasicTraversal[ConductingEquipmentStep]):
        if (step.step != 0) and open_test(step.conducting_equipment, None):
            return
        for cr in connected_equipment(step.conducting_equipment):
            if cr.to_equip:
                # noinspection PyArgumentList
                traversal.process_queue.put(ConductingEquipmentStep(cr.to_equip, step.step + 1))

    return queue_next


def new_connected_equipment_trace() -> ConnectedEquipmentTraversal:
    """
    :return: a traversal that traces equipment that are connected, ignoring open status.
    """
    # noinspection PyArgumentList
    return ConnectedEquipmentTraversal(queue_next=_queue_next(ignore_open), process_queue=depth_first(), tracker=ConductingEquipmentStepTracker())


def new_connected_equipment_breadth_trace() -> ConnectedEquipmentTraversal:
    """
    :return: a traversal that traces equipment that are connected, ignoring open status.
    """
    # noinspection PyArgumentList
    return ConnectedEquipmentTraversal(queue_next=_queue_next(ignore_open), process_queue=breadth_first(), tracker=ConductingEquipmentStepTracker())


def new_normal_connected_equipment_trace() -> ConnectedEquipmentTraversal:
    """
    :return: a traversal that traces equipment that are connected stopping at normally open points.
    """
    # noinspection PyArgumentList
    return ConnectedEquipmentTraversal(queue_next=_queue_next(normally_open), process_queue=depth_first(), tracker=ConductingEquipmentStepTracker())


def new_current_connected_equipment_trace() -> ConnectedEquipmentTraversal:
    """
    :return: a traversal that traces equipment that are connected stopping at currently open points.
    """
    # noinspection PyArgumentList
    return ConnectedEquipmentTraversal(queue_next=_queue_next(currently_open), process_queue=depth_first(), tracker=ConductingEquipmentStepTracker())


def new_normal_limited_connected_equipment_trace() -> LimitedConnectedEquipmentTrace:
    """
    :return: a limited connected equipment trace that traces equipment on the normal state of the network.
    """
    # noinspection PyArgumentList
    return LimitedConnectedEquipmentTrace(new_normal_connected_equipment_trace, lambda it: it.normal_feeder_direction)


def new_current_limited_connected_equipment_trace() -> LimitedConnectedEquipmentTrace:
    """
    :return: a limited connected equipment trace that traces equipment on the current state of the network.
    """
    # noinspection PyArgumentList
    return LimitedConnectedEquipmentTrace(new_current_connected_equipment_trace, lambda it: it.current_feeder_direction)
