#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, List

from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo

__all__ = ["CurrentRelayInfo"]


class CurrentRelayInfo(AssetInfo):
    """Current Relay Datasheet Information."""

    curve_setting: Optional[str] = None
    """The type of curve used for the Current Relay."""

    reclose_delays: Optional[List[float]] = None
    """
     * The reclose delays for this curve and relay type. The index of the list is the reclose step, and the value is the overall delay time.
    """
