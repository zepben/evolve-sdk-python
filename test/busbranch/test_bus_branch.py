#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Union, FrozenSet

import pytest

from busbranch.test_bus_branch_creator import TestBusBranchCreator, create_terminal_based_id
from zepben.evolve import ConnectivityNode, Junction, Disconnector, BusbarSection, Switch, BusBranchNetworkCreationLogger
from zepben.evolve.model.busbranch.bus_branch import _group_negligible_impedance_terminals, _group_common_ac_line_segment_terminals


# TODO: Need to add test for the mappings in the result of creating a bus-branch network

def test_create_bus_branch_model_callbacks(simple_node_breaker_network):
    nb_network = simple_node_breaker_network
    assert nb_network is not None

    plsi = nb_network.get("plsi")
    assert plsi is not None

    wire_info = nb_network.get("wire_info")
    assert wire_info is not None

    pt_info = nb_network.get("pt_info")
    assert pt_info is not None

    es = nb_network.get("grid_connection")
    assert es is not None

    pt = nb_network.get("transformer")
    assert pt is not None

    line = nb_network.get("line")
    assert line is not None

    ec = nb_network.get("load")
    assert ec is not None

    pec = nb_network.get("pec")
    assert pec is not None

    # noinspection PyTypeChecker
    logger_mock: BusBranchNetworkCreationLogger = "logger"  # This is an int because we are not interested in the logger functionality in this test
    creator = TestBusBranchCreator()
    result = creator.create(nb_network, logger=logger_mock)
    bb_network = result.network

    assert bb_network is not None

    # Validation
    # Bus
    expected_bus_0 = (
        create_terminal_based_id({next(es.terminals), list(pt.terminals)[0]}),
        (
            20000,
            frozenset(),
            frozenset({list(es.terminals)[0], list(pt.terminals)[0]}),
            frozenset(),
            nb_network,
            logger_mock
        )
    )
    expected_bus_1 = (
        create_terminal_based_id({list(pt.terminals)[1], list(line.terminals)[0]}),
        (
            400,
            frozenset(),
            frozenset({list(line.terminals)[0], list(pt.terminals)[1]}),
            frozenset(),
            nb_network,
            logger_mock
        )
    )
    expected_bus_2 = (
        create_terminal_based_id({list(line.terminals)[1], next(ec.terminals), next(pec.terminals)}),
        (
            400,
            frozenset(),
            frozenset({list(ec.terminals)[0], list(line.terminals)[1], list(pec.terminals)[0]}),
            frozenset(),
            nb_network,
            logger_mock
        )
    )
    _assert_are_equal(bb_network.bus, {expected_bus_0, expected_bus_1, expected_bus_2})

    # Branch Type
    expected_branch_type = (f"tbt_{wire_info.mrid}", (plsi, wire_info, 400, nb_network, logger_mock))
    _assert_are_equal(bb_network.branch_type, {expected_branch_type})

    # Branch
    expected_branch = (
        f"tb_{line.mrid}",
        (
            (expected_bus_1[1], expected_bus_2[1]),
            100,
            expected_branch_type[1],
            frozenset({line}),
            frozenset({*line.terminals}),
            frozenset(),
            nb_network,
            logger_mock
        )
    )
    _assert_are_equal(bb_network.branch, {expected_branch})

    # Transformer Type
    expected_transformer_type = (f"ptt_{pt_info.mrid}", (pt, nb_network, logger_mock))
    _assert_are_equal(bb_network.transformer_type, {expected_transformer_type})

    # Transformer
    expected_end_to_bus_pairs = ((list(pt.ends)[0], expected_bus_0[1]), (list(pt.ends)[1], expected_bus_1[1]))
    expected_transformer = (
        f"pt_{pt.mrid}",
        (
            pt,
            expected_end_to_bus_pairs,
            expected_transformer_type[1],
            nb_network,
            logger_mock
        )
    )
    _assert_are_equal(bb_network.transformer, {expected_transformer})

    # Source
    expected_energy_source = (
        f"es_{es.mrid}",
        (
            es,
            expected_bus_0[1],
            nb_network,
            logger_mock
        )
    )
    _assert_are_equal(bb_network.energy_source, {expected_energy_source})

    # Consumer
    expected_energy_consumer = (
        f"ec_{ec.mrid}",
        (
            ec,
            expected_bus_2[1],
            nb_network,
            logger_mock
        )
    )
    _assert_are_equal(bb_network.energy_consumer, {expected_energy_consumer})

    # PowerElectronicsConnection
    expected_power_electronics_connection = (
        f"pec_{pec.mrid}",
        (
            pec,
            expected_bus_2[1],
            nb_network,
            logger_mock
        )
    )
    _assert_are_equal(bb_network.power_electronics_connection, {expected_power_electronics_connection})


@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [False, True],
    indirect=True
)
def test_group_common_ac_line_segment_terminals_single_branch(single_branch_common_lines_network):
    assert single_branch_common_lines_network is not None

    acls1 = single_branch_common_lines_network.get("acls1")
    assert acls1 is not None
    acls2 = single_branch_common_lines_network.get("acls2")
    assert acls2 is not None
    acls3 = single_branch_common_lines_network.get("acls3")
    assert acls3 is not None
    acls4 = single_branch_common_lines_network.get("acls4")
    assert acls4 is not None
    acls5 = single_branch_common_lines_network.get("acls5")
    assert acls5 is not None

    # Validation
    # acls1, acls2, acls3
    for a in acls1, acls2, acls3:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {acls1, acls2, acls3})
        _assert_are_equal(inner_terms, {*acls1.terminals, *acls2.terminals, list(acls3.terminals)[0]})
        _assert_are_equal(border_terms, {list(acls3.terminals)[1]})

    # acls4
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(acls4)
    _assert_are_equal(common_lines, {acls4})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*acls4.terminals})

    # acls5
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(acls5)
    _assert_are_equal(common_lines, {acls5})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*acls5.terminals})


def test_group_common_ac_line_segment_terminals_multi_branch(multi_branch_common_lines_network):
    assert multi_branch_common_lines_network is not None

    a0 = multi_branch_common_lines_network.get("a0")
    assert a0 is not None
    a1 = multi_branch_common_lines_network.get("a1")
    assert a1 is not None
    a2 = multi_branch_common_lines_network.get("a2")
    assert a2 is not None
    a3 = multi_branch_common_lines_network.get("a3")
    assert a3 is not None
    a4 = multi_branch_common_lines_network.get("a4")
    assert a4 is not None
    a5 = multi_branch_common_lines_network.get("a5")
    assert a5 is not None
    a6 = multi_branch_common_lines_network.get("a6")
    assert a6 is not None
    a7 = multi_branch_common_lines_network.get("a7")
    assert a7 is not None
    a8 = multi_branch_common_lines_network.get("a8")
    assert a8 is not None

    # Validation
    # a0, a1, a2
    for a in a0, a1, a2:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a0, a1, a2})
        _assert_are_equal(inner_terms, {list(a0.terminals)[0], *a1.terminals, list(a2.terminals)[0]})
        _assert_are_equal(border_terms, {list(a2.terminals)[1]})

    # a3
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a3)
    _assert_are_equal(common_lines, {a3})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*a3.terminals})

    # a4, a5
    for a in a4, a5:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a4, a5})
        _assert_are_equal(inner_terms, {list(a4.terminals)[1], list(a5.terminals)[0]})
        _assert_are_equal(border_terms, {list(a4.terminals)[0], list(a5.terminals)[1]})

    # a6, a7
    for a in a6, a7:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a6, a7})
        _assert_are_equal(inner_terms, {list(a6.terminals)[1], *a7.terminals})
        _assert_are_equal(border_terms, {list(a6.terminals)[0]})

    # a8
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a8)
    _assert_are_equal(common_lines, {a8})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*a8.terminals})


def test_group_common_ac_line_segment_terminals_end_of_branch_multiple_ec_pec(end_of_branch_multiple_ec_pec):
    assert end_of_branch_multiple_ec_pec is not None

    a1 = end_of_branch_multiple_ec_pec.get("a1")
    assert a1 is not None
    a2 = end_of_branch_multiple_ec_pec.get("a2")
    assert a2 is not None
    ec = end_of_branch_multiple_ec_pec.get("ec")
    assert ec is not None
    pec1 = end_of_branch_multiple_ec_pec.get("pec1")
    assert pec1 is not None
    pec2 = end_of_branch_multiple_ec_pec.get("pec2")
    assert pec2 is not None

    # Validation
    # a1, a2
    for a in a1, a2:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a1, a2})
        _assert_are_equal(inner_terms, {list(a1.terminals)[1], list(a2.terminals)[0]})
        _assert_are_equal(border_terms, {list(a1.terminals)[0], list(a2.terminals)[1]})


@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [False],
    indirect=True
)
def test_group_negligible_impedance_terminals_single_branch_closed_switch(single_branch_common_lines_network):
    assert single_branch_common_lines_network is not None

    acls1 = single_branch_common_lines_network.get("acls1")
    assert acls1 is not None
    acls2 = single_branch_common_lines_network.get("acls2")
    assert acls2 is not None
    acls3 = single_branch_common_lines_network.get("acls3")
    assert acls3 is not None
    acls4 = single_branch_common_lines_network.get("acls4")
    assert acls4 is not None
    acls5 = single_branch_common_lines_network.get("acls5")
    assert acls5 is not None
    sw = single_branch_common_lines_network.get("sw")
    assert sw is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in single_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a1_a2
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls1_acls2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[0], *acls1.terminals})

    # a2_a3
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls2_acls3"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[1], list(acls3.terminals)[0]})

    # a3_sw
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls3_sw"], get_is_open)
    _assert_are_equal(closed_switches, {sw})
    _assert_are_equal(inner_terms, {*sw.terminals})
    _assert_are_equal(border_terms, {list(acls3.terminals)[1], list(acls4.terminals)[0]})

    # sw_a4
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_sw"], get_is_open)
    _assert_are_equal(closed_switches, {sw})
    _assert_are_equal(inner_terms, {*sw.terminals})
    _assert_are_equal(border_terms, {list(acls3.terminals)[1], list(acls4.terminals)[0]})

    # a4_a5
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_acls5"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls4.terminals)[1], *acls5.terminals})


@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [True],
    indirect=True
)
def test_group_negligible_impedance_terminals_single_branch_open_switch(single_branch_common_lines_network):
    assert single_branch_common_lines_network is not None

    acls1 = single_branch_common_lines_network.get("acls1")
    assert acls1 is not None
    acls2 = single_branch_common_lines_network.get("acls2")
    assert acls2 is not None
    acls3 = single_branch_common_lines_network.get("acls3")
    assert acls3 is not None
    acls4 = single_branch_common_lines_network.get("acls4")
    assert acls4 is not None
    acls5 = single_branch_common_lines_network.get("acls5")
    assert acls5 is not None
    sw = single_branch_common_lines_network.get("sw")
    assert sw is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in single_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a1_a2
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls1_acls2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[0], *acls1.terminals})

    # a2_a3
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls2_acls3"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[1], list(acls3.terminals)[0]})

    # a3_sw
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls3_sw"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls3.terminals)[1], list(sw.terminals)[0]})

    # sw_a4
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_sw"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(sw.terminals)[1], list(acls4.terminals)[0]})

    # a4_a5
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_acls5"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls4.terminals)[1], *acls5.terminals})


def test_group_negligible_impedance_terminals_multi_branch(multi_branch_common_lines_network):
    assert multi_branch_common_lines_network is not None

    a0 = multi_branch_common_lines_network.get("a0")
    assert a0 is not None
    a1 = multi_branch_common_lines_network.get("a1")
    assert a1 is not None
    a2 = multi_branch_common_lines_network.get("a2")
    assert a2 is not None
    a3 = multi_branch_common_lines_network.get("a3")
    assert a3 is not None
    a4 = multi_branch_common_lines_network.get("a4")
    assert a4 is not None
    a5 = multi_branch_common_lines_network.get("a5")
    assert a5 is not None
    a6 = multi_branch_common_lines_network.get("a6")
    assert a6 is not None
    a7 = multi_branch_common_lines_network.get("a7")
    assert a7 is not None
    a8 = multi_branch_common_lines_network.get("a8")
    assert a8 is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in multi_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a0_a1
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a0_a1"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a1.terminals)[0], *a0.terminals})

    # a1_a2
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a1_a2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a1.terminals)[1], list(a2.terminals)[0]})

    # a2_a3_a6
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a2_a3_a6"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a6.terminals)[0]})

    # a3_a4_a8
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a3_a4_a8"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a3.terminals)[1], list(a4.terminals)[0], *a8.terminals})

    # a4_a5
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a4_a5"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a4.terminals)[1], list(a5.terminals)[0]})

    # a6_a7
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a6_a7"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a6.terminals)[1], *a7.terminals})


@pytest.mark.parametrize(
    'negligible_impedance_equipment_basic_network',
    [
        lambda mrid: Junction(mrid=mrid),
        lambda mrid: Disconnector(mrid=mrid),
        lambda mrid: BusbarSection(mrid=mrid)
    ],
    indirect=True
)
def test_group_negligible_impedance_terminals_groups_negligible_impedance_equipment(negligible_impedance_equipment_basic_network):
    assert negligible_impedance_equipment_basic_network is not None

    nie1 = negligible_impedance_equipment_basic_network.get("nie1")
    assert nie1 is not None
    nie2 = negligible_impedance_equipment_basic_network.get("nie2")
    assert nie2 is not None
    a0 = negligible_impedance_equipment_basic_network.get("a0")
    assert a0 is not None
    a1 = negligible_impedance_equipment_basic_network.get("a1")
    assert a1 is not None
    a2 = negligible_impedance_equipment_basic_network.get("a2")
    assert a2 is not None
    a3 = negligible_impedance_equipment_basic_network.get("a3")
    assert a3 is not None
    a4 = negligible_impedance_equipment_basic_network.get("a4")
    assert a4 is not None
    a5 = negligible_impedance_equipment_basic_network.get("a5")

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in
          negligible_impedance_equipment_basic_network.objects(ConnectivityNode)}

    # Validation
    # a0_nie1
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a0_nie1"], get_is_open)
    _assert_are_equal(ni_equipment, {nie1})
    _assert_are_equal(inner_terms, {*nie1.terminals})
    _assert_are_equal(border_terms, {list(a1.terminals)[0], *a0.terminals})

    # j1_a1
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a1_nie1"], get_is_open)
    _assert_are_equal(ni_equipment, {nie1})
    _assert_are_equal(inner_terms, {*nie1.terminals})
    _assert_are_equal(border_terms, {list(a1.terminals)[0], *a0.terminals})

    # a1_a2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a1_a2"], get_is_open)
    _assert_are_equal(ni_equipment, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a1.terminals)[1], list(a2.terminals)[0]})

    # a2_nie2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a2_nie2"], get_is_open)
    _assert_are_equal(ni_equipment, {nie2})
    _assert_are_equal(inner_terms, {*nie2.terminals})
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a3_nie2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a3_nie2"], get_is_open)
    _assert_are_equal(ni_equipment, {nie2})
    _assert_are_equal(inner_terms, {*nie2.terminals})
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a4_nie2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a4_nie2"], get_is_open)
    _assert_are_equal(ni_equipment, {nie2})
    _assert_are_equal(inner_terms, {*nie2.terminals})
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a4_a5
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a4_a5"], get_is_open)
    _assert_are_equal(ni_equipment, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a4.terminals)[1], *a5.terminals})


def test_group_negligible_impedance_terminals_end_of_branch_multiple_ec_pec(end_of_branch_multiple_ec_pec):
    assert end_of_branch_multiple_ec_pec is not None

    a1 = end_of_branch_multiple_ec_pec.get("a1")
    assert a1 is not None
    a2 = end_of_branch_multiple_ec_pec.get("a2")
    assert a2 is not None
    ec = end_of_branch_multiple_ec_pec.get("ec")
    assert ec is not None
    pec1 = end_of_branch_multiple_ec_pec.get("pec1")
    assert pec1 is not None
    pec2 = end_of_branch_multiple_ec_pec.get("pec2")
    assert pec2 is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in end_of_branch_multiple_ec_pec.objects(ConnectivityNode)}

    # Validation
    # a2_ec
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a2_ec_pec1_pec2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(ec.terminals)[0], list(pec1.terminals)[0], list(pec2.terminals)[0]})


def _assert_are_equal(a: Union[Set, FrozenSet], b: Union[Set, FrozenSet]):
    diff = a ^ b
    assert not diff, f"Sets {a} and {b} are different"


def _assert_sets_of_sets_are_equal(a: Union[Set, FrozenSet], b: Union[Set, FrozenSet]):
    b_c = b.copy()
    for cl in a:
        matched_group = None
        for ex_g in b_c:
            diff = cl ^ ex_g
            if not diff:
                matched_group = ex_g
                break
        if matched_group is not None:
            b_c.remove(matched_group)
    assert len(b_c) == 0, f"Sets are not equal. Number of non-matching elements: {len(b_c)}"
