#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import text, lists, builds, data

from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_unordered
from test.cim.iec61968.assets.test_structure import structure_kwargs, verify_structure_constructor_default, \
    verify_structure_constructor_kwargs, verify_structure_constructor_args, structure_args
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import Pole, Streetlight
from zepben.evolve.model.cim.iec61968.assets.create_assets_components import create_pole

pole_kwargs = {
    **structure_kwargs,
    "classification": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "streetlights": lists(builds(Streetlight), max_size=2)
}

pole_args = [*structure_args, "a", [Streetlight()]]


def test_pole_constructor_default():
    p = Pole()
    p2 = create_pole()
    verify_default_pole(p)
    verify_default_pole(p2)


def verify_default_pole(p):
    verify_structure_constructor_default(p)
    assert p.classification == ""
    assert not list(p.streetlights)


# noinspection PyShadowingNames
@given(data())
def test_pole_constructor_kwargs(data):
    verify(
        [Pole, create_pole],
        data, pole_kwargs, verify_pole_values
    )


def verify_pole_values(p, classification, streetlights, **kwargs):
    verify_structure_constructor_kwargs(p, **kwargs)
    assert p.classification == classification
    assert list(p.streetlights) == streetlights


def test_pole_constructor_args():
    p = Pole(*pole_args)

    verify_structure_constructor_args(p)
    assert p.classification == pole_args[-2]
    assert list(p.streetlights) == pole_args[-1]


def test_streetlights_collection():
    verify_collection_unordered(Pole,
                                  lambda mrid, _: Streetlight(mrid),
                                  Pole.num_streetlights,
                                  Pole.get_streetlight,
                                  Pole.streetlights,
                                  Pole.add_streetlight,
                                  Pole.remove_streetlight,
                                  Pole.clear_streetlights)


def test_auto_two_way_connections_for_pole_constructor():
    s = Streetlight()
    p = create_pole(streetlights=[s])

    assert s.pole == p
