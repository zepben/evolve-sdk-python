#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists

from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from zepben.evolve import Feeder, Terminal, Substation, Equipment, LvFeeder

lv_feeder_kwargs = {
    **equipment_container_kwargs,
    "normal_head_terminal": builds(Terminal),
    "normal_energizing_substation": builds(Substation),
    "current_equipment": lists(builds(Equipment), max_size=2)
}

feeder_args = [*equipment_container_args, Terminal(), Substation(), {"ce": Equipment()}]


def test_feeder_constructor_default():
    f = Feeder()

    verify_equipment_container_constructor_default(f)
    assert not f.normal_head_terminal
    assert not f.normal_energizing_substation
    assert not list(f.current_equipment)


@given(**lv_feeder_kwargs)
def test_feeder_constructor_kwargs(normal_head_terminal, normal_energizing_substation, current_equipment, **kwargs):
    f = Feeder(normal_head_terminal=normal_head_terminal,
               normal_energizing_substation=normal_energizing_substation,
               current_equipment=current_equipment,
               **kwargs)

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
    validate_collection_unordered(Feeder,
                                  lambda mrid, _: Equipment(mrid),
                                  Feeder.num_current_equipment,
                                  Feeder.get_current_equipment,
                                  Feeder.current_equipment,
                                  Feeder.add_current_equipment,
                                  Feeder.remove_current_equipment,
                                  Feeder.clear_current_equipment,
                                  KeyError)


def test_normal_energized_lv_feeder_collection():
    validate_collection_unordered(Feeder,
                                  lambda mrid, _: LvFeeder(mrid),
                                  Feeder.num_normal_energized_lv_feeders,
                                  Feeder.get_normal_energized_lv_feeder,
                                  Feeder.normal_energized_lv_feeders,
                                  Feeder.add_normal_energized_lv_feeder,
                                  Feeder.remove_normal_energized_lv_feeder,
                                  Feeder.clear_normal_energized_lv_feeders,
                                  KeyError)