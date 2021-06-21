#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, integers

from test.cim.iec61970.base.core.test_ac_dc_terminal import ac_dc_terminal_kwargs, verify_ac_dc_terminal_constructor_default, \
    verify_ac_dc_terminal_constructor_kwargs, verify_ac_dc_terminal_constructor_args, ac_dc_terminal_args
from test.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import Terminal, ConnectivityNode, TracedPhases, ConductingEquipment, PhaseCode

terminal_kwargs = {
    **ac_dc_terminal_kwargs,
    "conducting_equipment": builds(ConductingEquipment),
    "phases": sampled_from(PhaseCode),
    "sequence_number": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "traced_phases": builds(TracedPhases),
    "connectivity_node": builds(ConnectivityNode)
}

terminal_args = [*ac_dc_terminal_args, ConductingEquipment(), PhaseCode.XYN, 1, TracedPhases(1, 2), ConnectivityNode()]


def test_terminal_constructor_default():
    t = Terminal()

    verify_ac_dc_terminal_constructor_default(t)
    assert not t.conducting_equipment
    assert t.phases == PhaseCode.ABC
    assert t.sequence_number == 0
    assert t.traced_phases == TracedPhases()
    assert not t.connectivity_node


@given(**terminal_kwargs)
def test_terminal_constructor_kwargs(conducting_equipment, phases, sequence_number, traced_phases, connectivity_node, **kwargs):
    t = Terminal(conducting_equipment=conducting_equipment,
                 phases=phases,
                 sequence_number=sequence_number,
                 traced_phases=traced_phases,
                 connectivity_node=connectivity_node,
                 **kwargs)

    verify_ac_dc_terminal_constructor_kwargs(t, **kwargs)
    assert t.conducting_equipment == conducting_equipment
    assert t.phases == phases
    assert t.sequence_number == sequence_number
    assert t.traced_phases == traced_phases
    assert t.connectivity_node == connectivity_node


def test_terminal_constructor_args():
    t = Terminal(*terminal_args)

    verify_ac_dc_terminal_constructor_args(t)
    assert t.conducting_equipment == terminal_args[-5]
    assert t.phases == terminal_args[-4]
    assert t.sequence_number == terminal_args[-3]
    assert t.traced_phases == terminal_args[-2]
    assert t.connectivity_node == terminal_args[-1]