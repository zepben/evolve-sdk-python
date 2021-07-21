#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import field, dataclass
from typing import Set, FrozenSet, Tuple, List, Iterable, Optional, Dict

from zepben.evolve import Terminal, NetworkService, AcLineSegment, PowerTransformer, EnergySource, EnergyConsumer, ConductingEquipment, \
    PowerElectronicsConnection, BusBranchNetworkCreator, \
    BusBranchNetworkCreationValidator, PowerTransformerEnd
from zepben.evolve.model.busbranch.bus_branch import BBN

TN = Tuple[int, FrozenSet[ConductingEquipment], FrozenSet[Terminal], FrozenSet[Terminal], NetworkService, BusBranchNetworkCreationValidator]
TB = Tuple[Tuple[TN, TN], float, FrozenSet[AcLineSegment], FrozenSet[Terminal], FrozenSet[Terminal], NetworkService, BusBranchNetworkCreationValidator]
PT = Tuple[PowerTransformer, List[Tuple[PowerTransformerEnd, TN]], NetworkService, BusBranchNetworkCreationValidator]
ES = Tuple[EnergySource, TN, NetworkService, BusBranchNetworkCreationValidator]
EC = Tuple[EnergyConsumer, TN, NetworkService, BusBranchNetworkCreationValidator]
PEC = Tuple[PowerElectronicsConnection, TN, NetworkService, BusBranchNetworkCreationValidator]


@dataclass()
class ArgsContainer:
    bus: Set[Tuple[str, TN]] = field(default_factory=set)

    branch: Set[Tuple[str, TB]] = field(default_factory=set)

    transformer: Set[Tuple[str, Set[PT]]] = field(default_factory=set)

    energy_source: Set[Tuple[str, Set[ES]]] = field(default_factory=set)

    energy_consumer: Set[Tuple[str, Set[EC]]] = field(default_factory=set)

    power_electronics_connection: Set[Tuple[str, Set[PEC]]] = field(default_factory=set)


class TestValidator(BusBranchNetworkCreationValidator[ArgsContainer, TN, TB, PT, ES, EC, PEC]):
    network_data_count: int
    topological_node_data_count: int
    topological_branch_data_count: int
    power_transformer_data_count: int
    energy_source_data_count: int
    energy_consumer_data_count: int
    power_electronics_connection_data_count: int

    def __init__(self):
        self.network_data_count = 0
        self.topological_node_data_count = 0
        self.topological_branch_data_count = 0
        self.power_transformer_data_count = 0
        self.energy_source_data_count = 0
        self.energy_consumer_data_count = 0
        self.power_electronics_connection_data_count = 0

    def is_valid_network_data(self, node_breaker_network: NetworkService) -> bool:
        self.network_data_count += 1
        return True

    def is_valid_topological_node_data(self, bus_branch_network: BBN, base_voltage: Optional[int],
                                       collapsed_conducting_equipment: FrozenSet[ConductingEquipment], border_terminals: FrozenSet[Terminal],
                                       inner_terminals: FrozenSet[Terminal], node_breaker_network: NetworkService) -> bool:
        self.topological_node_data_count += 1
        return True

    def is_valid_topological_branch_data(self, bus_branch_network: BBN, connected_topological_nodes: Tuple[TN, TN], length: Optional[float],
                                         collapsed_ac_line_segments: FrozenSet[AcLineSegment], border_terminals: FrozenSet[Terminal],
                                         inner_terminals: FrozenSet[Terminal], node_breaker_network: NetworkService) -> bool:
        self.topological_branch_data_count += 1
        return True

    def is_valid_power_transformer_data(self, bus_branch_network: BBN, power_transformer: PowerTransformer,
                                        ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, TN]], node_breaker_network: NetworkService) -> bool:
        self.power_transformer_data_count += 1
        return True

    def is_valid_energy_source_data(self, bus_branch_network: BBN, energy_source: EnergySource, connected_topological_node: TN,
                                    node_breaker_network: NetworkService) -> bool:
        self.energy_source_data_count += 1
        return True

    def is_valid_energy_consumer_data(self, bus_branch_network: BBN, energy_consumer: EnergyConsumer, connected_topological_node: TN,
                                      node_breaker_network: NetworkService) -> bool:
        self.energy_consumer_data_count += 1
        return True

    def is_valid_power_electronics_connection_data(self, bus_branch_network: BBN, power_electronics_connection: PEC, connected_topological_node: TN,
                                                   node_breaker_network: NetworkService) -> bool:
        self.power_electronics_connection_data_count += 1
        return True


class TestBusBranchCreator(BusBranchNetworkCreator[ArgsContainer, TN, TB, PT, ES, EC, PEC, TestValidator]):

    def validator_creator(self) -> TestValidator:
        return TestValidator()

    def bus_branch_network_creator(self, node_breaker_network: NetworkService) -> ArgsContainer:
        return ArgsContainer()

    def topological_node_creator(self, bus_branch_network: ArgsContainer, *args) -> Tuple[str, TN]:
        id_args = (create_terminal_based_id(args[2]), args)
        bus_branch_network.bus.add(id_args)
        return id_args

    def topological_branch_creator(self, bus_branch_network: ArgsContainer, *args) -> Tuple[str, TB]:
        id_args = (f"tb_{next(iter(args[2])).mrid}", args)
        bus_branch_network.branch.add(id_args)
        return id_args

    def power_transformer_creator(self, bus_branch_network: ArgsContainer, *args) -> Dict[str, PT]:
        id_args = (f"pt_{args[0].mrid}", tuple(tuple(e for e in arg) if isinstance(arg, list) else arg for arg in args))
        bus_branch_network.transformer.add(id_args)
        return {id_args[0]: id_args[1]}

    def energy_source_creator(self, bus_branch_network: ArgsContainer, *args) -> Dict[str, ES]:
        id_args = (f"es_{args[0].mrid}", args)
        bus_branch_network.energy_source.add(id_args)
        return {id_args[0]: id_args[1]}

    def energy_consumer_creator(self, bus_branch_network: ArgsContainer, *args) -> Dict[str, EC]:
        id_args = (f"ec_{args[0].mrid}", args)
        bus_branch_network.energy_consumer.add(id_args)
        return {id_args[0]: id_args[1]}

    def power_electronics_connection_creator(self, bus_branch_network: ArgsContainer, *args) -> Dict[str, PEC]:
        id_args = (f"pec_{args[0].mrid}", args)
        bus_branch_network.power_electronics_connection.add(id_args)
        return {id_args[0]: id_args[1]}


def create_terminal_based_id(terminals: Iterable[Terminal]) -> str:
    return "_".join(sorted([t.mrid for t in terminals]))
