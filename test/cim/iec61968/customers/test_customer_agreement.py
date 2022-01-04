#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds, data

from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_unordered
from test.cim.iec61968.common.test_agreement import agreement_kwargs, verify_agreement_constructor_default, verify_agreement_constructor_kwargs, \
    verify_agreement_constructor_args, agreement_args
from zepben.evolve import CustomerAgreement, Customer, PricingStructure
from zepben.evolve.model.cim.iec61968.customers.create_customers_components import create_customer_agreement

customer_agreement_kwargs = {
    **agreement_kwargs,
    "customer": builds(Customer),
    "pricing_structures": lists(builds(PricingStructure), max_size=2)
}

customer_agreement_args = [*agreement_args, Customer(), [PricingStructure()]]


def test_customer_agreement_constructor_default():
    ca = CustomerAgreement()
    ca2 = create_customer_agreement()
    verify_default_customer_agreement(ca)
    verify_default_customer_agreement(ca2)


def verify_default_customer_agreement(ca):
    verify_agreement_constructor_default(ca)
    assert not ca.customer
    assert not list(ca.pricing_structures)


# noinspection PyShadowingNames
@given(data())
def test_customer_agreement_constructor_kwargs(data):
    verify(
        [CustomerAgreement, create_customer_agreement],
        data, customer_agreement_kwargs, verify_customer_agreement_values
    )


def verify_customer_agreement_values(ca, customer, pricing_structures, **kwargs):
    verify_agreement_constructor_kwargs(ca, **kwargs)
    assert ca.customer == customer
    assert list(ca.pricing_structures) == pricing_structures


def test_customer_agreement_constructor_args():
    ca = CustomerAgreement(*customer_agreement_args)

    verify_agreement_constructor_args(ca)
    assert ca.customer == customer_agreement_args[-2]
    assert list(ca.pricing_structures) == customer_agreement_args[-1]


def test_pricing_structures_collection():
    verify_collection_unordered(CustomerAgreement,
                                lambda mrid, _: PricingStructure(mrid),
                                CustomerAgreement.num_pricing_structures,
                                CustomerAgreement.get_pricing_structure,
                                CustomerAgreement.pricing_structures,
                                CustomerAgreement.add_pricing_structure,
                                CustomerAgreement.remove_pricing_structure,
                                CustomerAgreement.clear_pricing_structures)


def test_auto_two_way_connections_for_customer_agreement_constructor():
    c = Customer()
    ca = create_customer_agreement(customer=c)

    assert c.get_agreement(ca.mrid) == ca

