#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.model.cim.iec61970.base.wires.transformer_star_impedance import TransformerStarImpedance, ResistanceReactance
from zepben.evolve.model.cim.iec61970.base.wires.winding_connection import WindingConnection

__all__ = ["TransformerEndInfo"]


class TransformerEndInfo(AssetInfo):
    """Transformer end data."""

    connection_kind: WindingConnection = WindingConnection.UNKNOWN_WINDING
    """Kind of connection."""

    emergency_s: int = 0
    """Apparent power that the winding can carry under emergency conditions (also called long-term emergency power). Unit: VA"""

    end_number: int = 0
    """Number for this transformer end, corresponding to the end's order in the PowerTransformer.vectorGroup attribute. Highest voltage winding
         should be 1."""

    insulation_u: int = 0
    """Basic insulation level voltage rating. Unit: Volts"""

    phase_angle_clock: int = 0
    """Winding phase angle where 360 degrees are represented with clock hours, so the valid values are {0, ..., 11}. For example,
         to express the second winding in code 'Dyn11', set attributes as follows: 'endNumber'=2, 'connectionKind' = Yn and 'phaseAngleClock' = 11."""

    r: float = 0.0
    """DC resistance. Unit: Ohms"""

    rated_s: int = 0
    """Normal apparent power rating. Unit: VA"""

    rated_u: int = 0
    """Rated voltage: phase-phase for three-phase windings, and either phase-phase or phase-neutral for single-phase windings. Unit: Volts"""

    short_term_s: int = 0
    """Apparent power that this winding can carry for a short period of time (in emergency). Unit: VA"""

    transformer_tank_info: Optional[TransformerTankInfo] = None
    """Transformer tank data that this end description is part of."""

    transformer_star_impedance: Optional[TransformerStarImpedance] = None
    """Transformer star impedance calculated from this transformer end datasheet."""

    def resistance_reactance(self) -> Optional[ResistanceReactance]:
        """
        Get the `ResistanceReactance` for this `TransformerEndInfo` from either the pre-calculated `transformer_star_impedance` or
        calculated from the associated test data.

        Returns the `ResistanceReactance` for this `TransformerEndInfo` or None if it could not be calculated
        """
        if self.transformer_star_impedance is not None:
            return self.transformer_star_impedance.resistance_reactance().merge_if_incomplete(lambda: self.calculate_resistance_reactance_from_tests())
        else:
            return self.calculate_resistance_reactance_from_tests()

    def calculate_resistance_reactance_from_tests(self) -> Optional[ResistanceReactance]:
        return None
