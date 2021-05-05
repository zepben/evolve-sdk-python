#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import field, dataclass
from typing import Set, FrozenSet, Tuple, Any, List, Iterable

from zepben.evolve import Terminal, NetworkService, AcLineSegment, PerLengthSequenceImpedance, \
    WireInfo, PowerTransformer, EnergySource, EnergyConsumer, ConductingEquipment, PowerElectronicsConnection, BusBranchNetworkCreator, \
    BusBranchNetworkCreationLogger, PowerTransformerEnd

TN = Tuple[int, FrozenSet[ConductingEquipment], FrozenSet[Terminal], FrozenSet[Terminal], NetworkService, BusBranchNetworkCreationLogger]
TBT = Tuple[PerLengthSequenceImpedance, WireInfo, int, NetworkService, BusBranchNetworkCreationLogger]
TB = Tuple[Tuple[TN, TN], float, TBT, FrozenSet[AcLineSegment], FrozenSet[Terminal], FrozenSet[Terminal], NetworkService, BusBranchNetworkCreationLogger]
PTT = Tuple[PowerTransformer, NetworkService, BusBranchNetworkCreationLogger]
PT = Tuple[PowerTransformer, List[Tuple[PowerTransformerEnd, TN]], PTT, NetworkService, BusBranchNetworkCreationLogger]
ES = Tuple[EnergySource, TN, NetworkService, BusBranchNetworkCreationLogger]
EC = Tuple[EnergyConsumer, TN, NetworkService, BusBranchNetworkCreationLogger]
PEC = Tuple[PowerElectronicsConnection, TN, NetworkService, BusBranchNetworkCreationLogger]


@dataclass()
class ArgsContainer:
    bus: Set[Tuple[int, Set[TN]]] = field(default_factory=set)

    branch: Set[Tuple[int, Set[TB]]] = field(default_factory=set)

    branch_type: Set[Tuple[int, Set[TBT]]] = field(default_factory=set)

    transformer: Set[Tuple[int, Set[PT]]] = field(default_factory=set)

    transformer_type: Set[Tuple[int, Set[PTT]]] = field(default_factory=set)

    energy_source: Set[Tuple[int, Set[ES]]] = field(default_factory=set)

    energy_consumer: Set[Tuple[int, Set[EC]]] = field(default_factory=set)

    power_electronics_connection: Set[Tuple[int, Set[PEC]]] = field(default_factory=set)


class TestBusBranchCreator(BusBranchNetworkCreator[ArgsContainer, TN, TB, TBT, PT, PTT, ES, EC, PEC]):

    def bus_branch_network_creator(self, node_breaker_network: NetworkService) -> ArgsContainer:
        return ArgsContainer()

    def topological_node_creator(self, bus_branch_network: ArgsContainer, *args) -> (int, TN):
        id_args = (create_terminal_based_id(args[2]), args)
        bus_branch_network.bus.add(id_args)
        return id_args

    def topological_branch_creator(self, bus_branch_network: ArgsContainer, *args) -> (Any, TB):
        id_args = (f"tb_{next(iter(args[3])).mrid}", args)
        bus_branch_network.branch.add(id_args)
        return id_args

    def topological_branch_type_creator(self, bus_branch_network: ArgsContainer, *args) -> (Any, TBT):
        id_args = (f"tbt_{args[1].mrid}", args)
        bus_branch_network.branch_type.add(id_args)
        return id_args

    def power_transformer_creator(self, bus_branch_network: ArgsContainer, *args) -> (Any, PT):
        id_args = (f"pt_{args[0].mrid}", tuple(tuple(e for e in arg) if isinstance(arg, list) else arg for arg in args))
        bus_branch_network.transformer.add(id_args)
        return id_args

    def power_transformer_type_creator(self, bus_branch_network: ArgsContainer, *args) -> (Any, PTT):
        id_args = (f"ptt_{args[0].asset_info.mrid}", args)
        bus_branch_network.transformer_type.add(id_args)
        return id_args

    def energy_source_creator(self, bus_branch_network: ArgsContainer, *args) -> (Any, ES):
        id_args = (f"es_{args[0].mrid}", args)
        bus_branch_network.energy_source.add(id_args)
        return id_args

    def energy_consumer_creator(self, bus_branch_network: ArgsContainer, *args) -> (Any, EC):
        id_args = (f"ec_{args[0].mrid}", args)
        bus_branch_network.energy_consumer.add(id_args)
        return id_args

    def power_electronics_connection_creator(self, bus_branch_network: ArgsContainer, *args) -> (Any, PEC):
        id_args = (f"pec_{args[0].mrid}", args)
        bus_branch_network.power_electronics_connection.add(id_args)
        return id_args


def create_terminal_based_id(terminals: Iterable[Terminal]) -> str:
    return "_".join(sorted([t.mrid for t in terminals]))
