#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

import pytest
from hypothesis import given, settings, Phase
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetEquipmentForContainerRequest, GetCurrentEquipmentForFeederRequest, \
    GetEquipmentForRestrictionRequest
from zepben.protobuf.nc.nc_responses_pb2 import GetIdentifiedObjectsResponse, GetEquipmentForContainerResponse, GetCurrentEquipmentForFeederResponse, \
    GetEquipmentForRestrictionResponse
from unittest.mock import MagicMock

from test.pb_creators import networkidentifiedobjects, aclinesegment
from zepben.evolve import NetworkConsumerClient, NetworkService, IdentifiedObject, CableInfo, ConductingEquipment, AcLineSegment, Breaker, EnergySource, \
    EnergySourcePhase, Junction, PowerTransformer, PowerTransformerEnd, ConnectivityNode, Feeder, Location, OverheadWireInfo, PerLengthSequenceImpedance, \
    Substation, Terminal, EquipmentContainer, Equipment, BaseService, OperationalRestriction


# TODO: Test behaviour of "failures" with get_feeder/get_identified_objects

@pytest.mark.asyncio
@given(networkidentifiedobjects())
@settings(max_examples=1, phases=(Phase.explicit, Phase.reuse, Phase.generate))
async def test_retrieve_supported_types(networkidentifiedobjects):
    network_service = NetworkService()
    for nio in networkidentifiedobjects:
        response = GetIdentifiedObjectsResponse(identifiedObject=nio)
        stub = MagicMock(**{"getIdentifiedObjects.return_value": [response]})
        client = NetworkConsumerClient(stub=stub)
        pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
        result = await client.get_identified_objects(network_service, [pbio.mrid()])
        assert result.was_successful
        if pbio.mrid():
            assert result.result.value[pbio.mrid()] is not None, f"type: {nio.WhichOneof('identifiedObject')} mrid: {pbio.mrid()}"
            assert network_service.get(pbio.mrid()) is result.result.value[pbio.mrid()]
        else:
            assert pbio.mrid() in result.result.failed


@pytest.mark.asyncio
@given(aclinesegment())
async def test_get_identifiedobject(aclinesegment):
    network_service = NetworkService()
    nio = NetworkIdentifiedObject(acLineSegment=aclinesegment)
    response = GetIdentifiedObjectsResponse(identifiedObject=nio)
    stub = MagicMock(**{"getIdentifiedObjects.return_value": [response]})
    client = NetworkConsumerClient(stub=stub)
    pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
    result = await client.get_identified_object(network_service, pbio.mrid())
    assert result.was_successful
    assert result.result is not None
    assert result.result.mrid == pbio.mrid()

    stub = MagicMock(**{"getIdentifiedObjects.return_value": []})
    client = NetworkConsumerClient(stub=stub)
    pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
    result = await client.get_identified_object(network_service, "fakemrid")
    assert result.was_successful
    assert result.result is None


@pytest.mark.asyncio
async def test_get_network_hierarchy(feeder_network):
    pass


@pytest.mark.asyncio
async def test_retrieve_network():
    pass


@pytest.mark.asyncio
async def test_get_feeder(feeder_network):
    ns = NetworkService()
    feeder_mrid = "f001"

    def create_feeder_response(request: GetIdentifiedObjectsRequest, *args, **kwargs):
        for mrid in request.mrids:
            io = feeder_network.get(mrid)
            yield response_of(io, GetIdentifiedObjectsResponse)

    stub = MagicMock(
        **{"getIdentifiedObjects.side_effect": create_feeder_response, "getEquipmentForContainer.side_effect": create_container_equipment_func(feeder_network)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_feeder(ns, feeder_mrid)
    assert len(objects.result.value) == ns.len_of() == 21
    assert objects.was_successful
    assert feeder_mrid in objects.result.value
    for io in objects.result.value.values():
        assert ns.get(io.mrid) == io

    for io in ns.objects():
        assert objects.result.value[io.mrid] == io
    assert len(objects.result.failed) == 0


@pytest.mark.asyncio
async def test_get_equipment_for_container(feeder_network):
    ns = NetworkService()
    feeder_mrid = "f001"

    stub = MagicMock(**{"getEquipmentForContainer.side_effect": create_container_equipment_func(feeder_network)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_container(ns, feeder_mrid)
    assert len(objects.result.value) == ns.len_of(Equipment) == 3
    assert_contains_mrids(ns, "fsp", "c2", "tx")


@pytest.mark.asyncio
async def test_get_current_equipment_for_feeder(feeder_with_current):
    ns = NetworkService()
    feeder_mrid = "f001"
    stub = MagicMock(**{"getEquipmentForContainer.side_effect": create_container_equipment_func(feeder_with_current), "getCurrentEquipmentForFeeder.side_effect": create_container_current_equipment_func(feeder_with_current)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_container(ns, feeder_mrid)
    assert len(objects.result.value) == ns.len_of(Equipment) == 7
    assert_contains_mrids(ns, "fsp", "c2", "tx", "c3", "sw", "c4", "tx2")
    ns2 = NetworkService()
    objects = await client.get_current_equipment_for_feeder(ns2, feeder_mrid)
    assert len(objects.result.value) == ns2.len_of(Equipment) == 5
    assert_contains_mrids(ns2, "fsp", "c2", "tx", "c3", "sw")


@pytest.mark.asyncio
async def test_get_equipment_for_operational_restriction(operational_restriction_with_equipment):
    ns = NetworkService()
    or_mrid = "or1"
    stub = MagicMock(**{"getEquipmentForRestriction.side_effect": create_restriction_equipment_func(operational_restriction_with_equipment)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_restriction(ns, or_mrid)
    assert len(objects.result.value) == ns.len_of(Equipment) == 3
    assert_contains_mrids(ns, "fsp", "c2", "tx")


def assert_contains_mrids(service: BaseService, *mrids):
    for mrid in mrids:
        assert service.get(mrid)


def response_of(object: IdentifiedObject, response_type):
    return response_type(identifiedObject=to_networkidentifiedobject(object))


def to_networkidentifiedobject(obj) -> NetworkIdentifiedObject:
    if isinstance(obj, CableInfo):
        nio = NetworkIdentifiedObject(cableInfo=obj.to_pb())
    elif isinstance(obj, ConductingEquipment):
        if isinstance(obj, AcLineSegment):
            nio = NetworkIdentifiedObject(acLineSegment=obj.to_pb())
        elif isinstance(obj, Breaker):
            nio = NetworkIdentifiedObject(breaker=obj.to_pb())
        elif isinstance(obj, EnergySource):
            nio = NetworkIdentifiedObject(energySource=obj.to_pb())
        elif isinstance(obj, EnergySourcePhase):
            nio = NetworkIdentifiedObject(energySourcePhase=obj.to_pb())
        elif isinstance(obj, Junction):
            nio = NetworkIdentifiedObject(junction=obj.to_pb())
        elif isinstance(obj, PowerTransformer):
            nio = NetworkIdentifiedObject(powerTransformer=obj.to_pb())
        else:
            raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
    elif isinstance(obj, ConnectivityNode):
        nio = NetworkIdentifiedObject(connectivityNode=obj.to_pb())
    elif isinstance(obj, EnergySourcePhase):
        nio = NetworkIdentifiedObject(energySourcePhase=obj.to_pb())
    elif isinstance(obj, Feeder):
        nio = NetworkIdentifiedObject(feeder=obj.to_pb())
    elif isinstance(obj, Location):
        nio = NetworkIdentifiedObject(location=obj.to_pb())
    elif isinstance(obj, OverheadWireInfo):
        nio = NetworkIdentifiedObject(overheadWireInfo=obj.to_pb())
    elif isinstance(obj, PerLengthSequenceImpedance):
        nio = NetworkIdentifiedObject(perLengthSequenceImpedance=obj.to_pb())
    elif isinstance(obj, PowerTransformerEnd):
        nio = NetworkIdentifiedObject(powerTransformerEnd=obj.to_pb())
    elif isinstance(obj, Substation):
        nio = NetworkIdentifiedObject(substation=obj.to_pb())
    elif isinstance(obj, Terminal):
        nio = NetworkIdentifiedObject(terminal=obj.to_pb())
    else:
        raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
    return nio


def create_container_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetEquipmentForContainerRequest, *args, **kwargs):
        ec = network.get(request.mrid, EquipmentContainer)
        for equip in ec.equipment:
            yield response_of(equip, GetEquipmentForContainerResponse)

    return create_equipment_response


def create_restriction_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetEquipmentForRestrictionRequest, *args, **kwargs):
        or1 = network.get(request.mrid, OperationalRestriction)
        for equip in or1.equipment:
            yield response_of(equip, GetEquipmentForRestrictionResponse)

    return create_equipment_response


def create_container_current_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetCurrentEquipmentForFeederRequest, *args, **kwargs):
        ec = network.get(request.mrid, Feeder)
        for equip in ec.current_equipment:
            yield response_of(equip, GetCurrentEquipmentForFeederResponse)

    return create_equipment_response
