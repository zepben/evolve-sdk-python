#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from _pytest.python_api import raises
from hypothesis import given
from hypothesis.strategies import floats, data
from test.cim.common_testing_functions import verify
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import DiagramObjectPoint
from zepben.evolve.model.cim.iec61970.base.diagramlayout.create_diagram_layout_components import create_diagram_object_point

diagram_object_point_kwargs = {
    "x_position": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "y_position": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

diagram_object_point_args = [1.1, 2.2]


# noinspection PyArgumentList
def test_diagram_object_point_constructor_default():
    #
    # NOTE: There is no blank constructor, so check we need to pass both values.
    #
    with raises(TypeError):
        DiagramObjectPoint()
        create_diagram_object_point()
    with raises(TypeError):
        DiagramObjectPoint(1.0)
        create_diagram_object_point(1.0)
    with raises(TypeError):
        DiagramObjectPoint(x_position=2.0)
        create_diagram_object_point(x_position=2.0)
    with raises(TypeError):
        DiagramObjectPoint(y_position=2.0)
        create_diagram_object_point(y_position=2.0)


# noinspection PyShadowingNames
@given(data())
def test_diagram_object_point_constructor_kwargs(data):
    verify(
        [DiagramObjectPoint, create_diagram_object_point],
        data, diagram_object_point_kwargs, verify_diagram_object_point_values
    )


def verify_diagram_object_point_values(dop, x_position, y_position):
    assert dop.x_position == x_position
    assert dop.y_position == y_position


def test_diagram_object_point_constructor_args():
    # noinspection PyArgumentList
    dop = DiagramObjectPoint(*diagram_object_point_args)

    assert dop.x_position == diagram_object_point_args[-2]
    assert dop.y_position == diagram_object_point_args[-1]
