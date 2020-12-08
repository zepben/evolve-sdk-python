#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import abstractmethod, ABC
from asyncio import get_event_loop
from typing import TypeVar, Union, List, Dict, Generic, Type

from dataclassy import dataclass
from grpc import Channel
from zepben.cimbend import NetworkService, BaseService, DiagramService, CustomerService
from zepben.cimbend.network.translator.network_cim2proto import CimTranslationException
from zepben.cimbend.streaming.exceptions import UnsupportedOperationException
from zepben.cimbend.streaming.grpc import GrpcClient, GrpcResult
from zepben.cimbend.streaming.network_rpc import network_rpc_map
from zepben.cimbend.streaming.streaming import NoSuchRPCException, ProtoAttributeError
from zepben.protobuf.cp.cp_pb2_grpc import CustomerProducerStub
from zepben.protobuf.cp.cp_requests_pb2 import CreateCustomerServiceRequest, CompleteCustomerServiceRequest
from zepben.protobuf.dp.dp_pb2_grpc import DiagramProducerStub
from zepben.protobuf.dp.dp_requests_pb2 import CompleteDiagramServiceRequest, CreateDiagramServiceRequest
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub
from zepben.protobuf.np.np_requests_pb2 import CreateNetworkRequest, CompleteNetworkRequest

__all__ = ["CimProducerClient", "CustomerProducerClient", "NetworkProducerClient", "DiagramProducerClient", "ProducerClient", "SyncProducerClient",
           "SyncCustomerProducerClient"]
T = TypeVar("T", bound=BaseService)


async def _send(stub, service, rpc_map):
    if not service:
        return

    for obj in service.objects():
        try:
            pb = obj.to_pb()
        except Exception as e:
            raise CimTranslationException(f"Failed to translate {obj} to protobuf.") from e

        try:
            rpc = getattr(stub, rpc_map[type(pb)][0])
        except AttributeError as e:
            raise NoSuchRPCException(f"RPC {rpc_map[type(pb)][0]} could not be found in {stub.__class__.__name__}") from e

        try:
            attrname = f"{obj.__class__.__name__[:1].lower()}{obj.__class__.__name__[1:]}"
            req = rpc_map[type(pb)][1]()
            getattr(req, attrname).CopyFrom(pb)
        except AttributeError as e:
            raise ProtoAttributeError() from e

        rpc(req)


class CimProducerClient(GrpcClient):
    """Base class that defines some helpful functions when producer clients are sending to the server."""

    @abstractmethod
    def send(self, service: T = None):
        """
        Sends objects within the given `service` to the producer server.
                                                                                                                 
        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        raise NotImplementedError()


class NetworkProducerClient(CimProducerClient):
    _stub: NetworkProducerStub = None

    def __init__(self, channel=None, stub: NetworkProducerStub = None):
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = NetworkProducerStub(channel)

    async def send(self, service: NetworkService = None):
        """
        Sends objects within the given `service` to the producer server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        await self.try_rpc(lambda: self._stub.CreateNetwork(CreateNetworkRequest()))

        await _send(self._stub, service, network_rpc_map)

        await self.try_rpc(lambda: self._stub.CompleteNetwork(CompleteNetworkRequest()))


class DiagramProducerClient(CimProducerClient):
    _stub: DiagramProducerStub = None

    def __init__(self, channel=None, stub: DiagramProducerStub = None):
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = DiagramProducerStub(channel)

    async def send(self, service: DiagramService = None):
        """
        Sends objects within the given `service` to the producer server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        await self.try_rpc(lambda: self._stub.CreateDiagramService(CreateDiagramServiceRequest()))

        await _send(self._stub, service, network_rpc_map)

        await self.try_rpc(lambda: self._stub.CompleteDiagramService(CompleteDiagramServiceRequest()))


class CustomerProducerClient(CimProducerClient):
    _stub: CustomerProducerStub = None

    def __init__(self, channel=None, stub: CustomerProducerStub = None):
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = CustomerProducerStub(channel)

    async def send(self, service: CustomerService = None):
        """
        Sends objects within the given `service` to the producer server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        await self.try_rpc(lambda: self._stub.CreateCustomerService(CreateCustomerServiceRequest()))

        await _send(self._stub, service, network_rpc_map)

        await self.try_rpc(lambda: self._stub.CompleteCustomerService(CompleteCustomerServiceRequest()))


class ProducerClient(CimProducerClient):
    _channel: Channel = None
    _clients: Dict[Type[BaseService], CimProducerClient] = None

    def __init__(self, channel: Channel, clients: Dict[Type[BaseService], CimProducerClient] = None):
        self._channel = channel
        if clients is not None:
            self._clients = clients.copy()
        else:
            self._clients = {
                NetworkService: NetworkProducerClient(self._channel),
                DiagramService: DiagramProducerClient(self._channel),
                CustomerService: CustomerProducerClient(self._channel)
            }

    async def send(self, services: Union[List[BaseService], BaseService] = None):
        """
        Send each service in `services` to the server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        if not services:
            return GrpcResult(UnsupportedOperationException("No services were provided"))

        sent = []
        for service in services:
            client = self._clients[type(service)]
            await client.send(service)
            sent.append(type(service))

        for s in self._clients.keys():
            if s not in sent:
                client = self._clients[s]
                await client.send()


class SyncProducerClient(ProducerClient):

    def send(self, services: Union[List[BaseService], BaseService] = None):
        return get_event_loop().run_until_complete(super().send(services))


class SyncCustomerProducerClient(CimProducerClient):

    def send(self, service: CustomerService = None):
        return get_event_loop().run_until_complete(super().send(service))


class SyncNetworkProducerClient(CimProducerClient):

    def send(self, service: NetworkService = None):
        return get_event_loop().run_until_complete(super().send(service))


class SyncDiagramProducerClient(CimProducerClient):

    def send(self, service: DiagramService = None):
        return get_event_loop().run_until_complete(super().send(service))
