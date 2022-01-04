#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.test_common_two_way_connections import set_up_power_electronics_unit_two_way_link_test, check_power_electronics_unit_two_way_link_test
from test.cim.iec61970.base.wires.generation.production.test_power_electronics_unit import power_electronics_unit_kwargs, \
    verify_power_electronics_unit_constructor_default, verify_power_electronics_unit_constructor_kwargs, verify_power_electronics_unit_constructor_args, \
    power_electronics_unit_args
from zepben.evolve import PhotoVoltaicUnit
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_photo_voltaic_unit

photo_voltaic_unit_kwargs = power_electronics_unit_kwargs
photo_voltaic_unit_args = power_electronics_unit_args


def test_photo_voltaic_unit_constructor_default():
    verify_power_electronics_unit_constructor_default(PhotoVoltaicUnit())
    verify_power_electronics_unit_constructor_default(create_photo_voltaic_unit())


# noinspection PyShadowingNames
@given(data())
def test_photo_voltaic_unit_constructor_kwargs(data):
    verify(
        [PhotoVoltaicUnit, create_photo_voltaic_unit],
        data, photo_voltaic_unit_kwargs, verify_power_electronics_unit_constructor_kwargs
    )


def test_photo_voltaic_unit_constructor_args():
    verify_power_electronics_unit_constructor_args(PhotoVoltaicUnit(*photo_voltaic_unit_args))


def test_auto_two_way_connections_for_photo_voltaic_unit_constructor():
    up, ec, opr, f, pec = set_up_power_electronics_unit_two_way_link_test()
    pvu = create_photo_voltaic_unit(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f],
                                    power_electronics_connection=pec)
    check_power_electronics_unit_two_way_link_test(pvu, up, ec, opr, f, pec)
