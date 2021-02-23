from hypothesis import given

from cim.constructor_validation import ps_kwargs, ps_args, verify_connector_constructor, \
    verify_protected_switch_constructor, verify_ps_args
from zepben.evolve import LoadBreakSwitch

lbs_kwargs = ps_kwargs

lbs_args = ps_args


@given(**lbs_kwargs)
def test_protected_switch_constructor_kwargs(**kwargs):
    verify_protected_switch_constructor(LoadBreakSwitch, **kwargs)


def test_loadbreakswitch_constructor_args():
    lbs = LoadBreakSwitch(*lbs_args)
    verify_ps_args(lbs)


def test_set_open():
    # TODO
    pass


def test_set_normal_open():
    # TODO
    pass