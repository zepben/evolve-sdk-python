#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, text, data

from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.meas.test_measurement_value import measurement_value_kwargs, verify_measurement_value_constructor_default, \
    verify_measurement_value_constructor_kwargs, verify_measurement_value_constructor_args, measurement_value_args
from test.cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import DiscreteValue
from zepben.evolve.model.cim.iec61970.base.meas.create_meas_components import create_discrete_value

discrete_value_kwargs = {
    **measurement_value_kwargs,
    "value": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "discrete_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

discrete_value_args = [*measurement_value_args, 1, "a"]


def test_discrete_value_constructor_default():
    dv = DiscreteValue()
    dv2 = create_discrete_value()
    verify_default_discrete_value_constructor(dv)
    verify_default_discrete_value_constructor(dv2)


def verify_default_discrete_value_constructor(dv):
    verify_measurement_value_constructor_default(dv)
    assert dv.value == 0
    assert not dv.discrete_mrid


# noinspection PyShadowingNames
@given(data())
def test_discrete_value_constructor_kwargs(data):
    verify(
        [DiscreteValue, create_discrete_value],
        data, discrete_value_kwargs, verify_discrete_value_values
    )


def verify_discrete_value_values(dv, value, discrete_mrid, **kwargs):
    verify_measurement_value_constructor_kwargs(dv, **kwargs)
    assert dv.value == value
    assert dv.discrete_mrid == discrete_mrid


def test_discrete_value_constructor_args():
    # noinspection PyArgumentList
    dv = DiscreteValue(*discrete_value_args)

    verify_measurement_value_constructor_args(dv)
    assert dv.value == discrete_value_args[-2]
    assert dv.discrete_mrid == discrete_value_args[-1]
