#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists, data

from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_unordered
from test.cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from zepben.evolve import Feeder, Terminal, Substation, Equipment
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_feeder

feeder_kwargs = {
    **equipment_container_kwargs,
    "normal_head_terminal": builds(Terminal),
    "normal_energizing_substation": builds(Substation),
    "current_equipment": lists(builds(Equipment), max_size=2)
}

feeder_args = [*equipment_container_args, Terminal(), Substation(), {"ce": Equipment()}]


def test_feeder_constructor_default():
    f = Feeder()
    f2 = create_feeder()
    verify_default_feeder(f)
    verify_default_feeder(f2)


def verify_default_feeder(f):
    verify_equipment_container_constructor_default(f)
    assert not f.normal_head_terminal
    assert not f.normal_energizing_substation
    assert not list(f.current_equipment)


# noinspection PyShadowingNames
@given(data())
def test_feeder_constructor_kwargs(data):
    verify(
        [Feeder, create_feeder],
        data, feeder_kwargs, verify_feeder_values
    )


def verify_feeder_values(f, normal_head_terminal, normal_energizing_substation, current_equipment, **kwargs):
    verify_equipment_container_constructor_kwargs(f, **kwargs)
    assert f.normal_head_terminal == normal_head_terminal
    assert f.normal_energizing_substation == normal_energizing_substation
    assert list(f.current_equipment) == current_equipment


def test_feeder_constructor_args():
    f = Feeder(*feeder_args)

    verify_equipment_container_constructor_args(f)
    assert f.normal_head_terminal == feeder_args[-3]
    assert f.normal_energizing_substation == feeder_args[-2]
    assert list(f.current_equipment) == list(feeder_args[-1].values())


def test_current_equipment_collection():
    verify_collection_unordered(Feeder,
                                lambda mrid, _: Equipment(mrid),
                                Feeder.num_current_equipment,
                                Feeder.get_current_equipment,
                                Feeder.current_equipment,
                                Feeder.add_current_equipment,
                                Feeder.remove_current_equipment,
                                Feeder.clear_current_equipment,
                                KeyError)


def test_auto_two_way_connections_for_feeder_constructor():
    s = Substation()
    e = Equipment()
    f = create_feeder(normal_energizing_substation=s, current_equipment=[e])

    assert s.get_feeder(f.mrid) == f
    assert e.get_current_feeder(f.mrid) == f
