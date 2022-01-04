#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, lists, data

from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_unordered
from test.cim.iec61970.base.wires.test_line import verify_line_constructor_default, verify_line_constructor_kwargs, verify_line_constructor_args, line_kwargs, \
    line_args
from zepben.evolve import Circuit, Loop, Terminal, Substation, Equipment
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.create_feeder_components import create_circuit

circuit_kwargs = {
    **line_kwargs,
    "loop": builds(Loop),
    "end_terminals": lists(builds(Terminal)),
    "end_substations": lists(builds(Substation))
}

circuit_args = [*line_args, Loop(), [Terminal], [Substation]]


def test_circuit_constructor_default():
    c = Circuit()
    c2 = create_circuit()
    verify_default_circuit_constructor(c)
    verify_default_circuit_constructor(c2)


def verify_default_circuit_constructor(c):
    verify_line_constructor_default(c)
    assert not c.loop
    assert not list(c.end_terminals)
    assert not list(c.end_substations)


# noinspection PyShadowingNames
@given(data())
def test_circuit_constructor_kwargs(data):
    verify(
        [Circuit, create_circuit],
        data, circuit_kwargs, verify_circuit_constructor_values
    )


def verify_circuit_constructor_values(c, loop, end_terminals, end_substations, **kwargs):
    verify_line_constructor_kwargs(c, **kwargs)
    assert c.loop == loop
    assert list(c.end_terminals) == end_terminals
    assert list(c.end_substations) == end_substations


def test_circuit_constructor_args():
    c = Circuit(*circuit_args)

    verify_line_constructor_args(c)
    assert c.loop == circuit_args[-3]
    assert list(c.end_terminals) == circuit_args[-2]
    assert list(c.end_substations) == circuit_args[-1]


def test_end_terminals_collection():
    verify_collection_unordered(Circuit,
                                lambda mrid, _: Terminal(mrid),
                                Circuit.num_end_terminals,
                                Circuit.get_end_terminal,
                                Circuit.end_terminals,
                                Circuit.add_end_terminal,
                                Circuit.remove_end_terminal,
                                Circuit.clear_end_terminals)


def test_end_substations_collection():
    verify_collection_unordered(Circuit,
                                lambda mrid, _: Substation(mrid),
                                Circuit.num_end_substations,
                                Circuit.get_end_substation,
                                Circuit.end_substations,
                                Circuit.add_end_substation,
                                Circuit.remove_end_substation,
                                Circuit.clear_end_substations)


def test_auto_two_way_connections_for_circuit_constructor():
    e = Equipment()
    loop = Loop()
    s = Substation()
    c = create_circuit(equipment=[e], loop=loop, end_substations=[s])

    assert e.get_container(c.mrid) == c
    assert loop.get_circuit(c.mrid) == c
    assert s.get_circuit(c.mrid) == c
