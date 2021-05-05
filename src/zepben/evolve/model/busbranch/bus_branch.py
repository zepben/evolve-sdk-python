#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import abc
from dataclasses import dataclass, field
from functools import reduce
from typing import Set, Tuple, FrozenSet, Dict, Callable, Union, TypeVar, Any, List, Generic

from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import WireInfo
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
from zepben.evolve.model.cim.iec61970.base.wires.connectors import Junction, BusbarSection
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd
from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch, Jumper
from zepben.evolve.services.network.network import NetworkService

__all__ = [
    "BusBranchNetworkCreationLogger",
    "BusBranchNetworkCreator",
    "ListBackedLogger",
    "BusBranchNetworkCreationMappings",
    "BusBranchNetworkCreationResult",
    "_create_bus_branch_network"
]


class BusBranchNetworkCreationLogger(metaclass=abc.ABCMeta):
    """
    Logger for information captured while creating a bus-branch network from a node-breaker network.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "error") and
                callable(subclass.error) and
                hasattr(subclass, "warning") and
                callable(subclass.warning) and
                hasattr(subclass, "info") and
                callable(subclass.info) and
                hasattr(subclass, "debug") and
                callable(subclass.debug) or
                NotImplemented)

    @abc.abstractmethod
    def error(self, message: str):
        raise NotImplementedError

    @abc.abstractmethod
    def warning(self, message: str):
        raise NotImplementedError

    @abc.abstractmethod
    def info(self, message: str):
        raise NotImplementedError

    @abc.abstractmethod
    def debug(self, message: str):
        raise NotImplementedError


BBN = TypeVar('BBN')  # Bus-Branch Network
TN = TypeVar('TN')  # Topological Node
TB = TypeVar('TB')  # Topological Branch
TBT = TypeVar('TBT')  # Topological Branch Type
PT = TypeVar('PT')  # Power Transformer
PTT = TypeVar('PTT')  # Power Transformer Type
ES = TypeVar('ES')  # Energy Source
EC = TypeVar('EC')  # Energy Consumer
PEC = TypeVar('PEC')  # Power Electronics Connection


class BusBranchNetworkCreator(Generic[BBN, TN, TB, TBT, PT, PTT, ES, EC, PEC], metaclass=abc.ABCMeta):
    """Contains the logic needed to generate a target bus-branch network from a source `zepben.evolve.services.network.network.NetworkService`.

    Generic Types:
    BBN := Type for the object used to represent the bus-branch network.
    TN := Type for the object used to represent a topological node in the bus-branch network.
    TB := Type for the object used to represent a topological branch in the bus-branch network.
    TBT := Type for the object used to represent a topological branch's datasheet information in the bus-branch network.
    PT := Type for the object used to represent a power transformer in the bus-branch network.
    PTT := Type for the object used to represent a transformer' datasheet information in the bus-branch network.
    ES := Type for the object used to represent an energy source in the bus-branch network.
    EC := Type for the object used to represent an energy consumer in the bus-branch network.
    PEC := Type for the object used to represent a power electronics connection in the bus-branch network.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "bus_branch_network_creator") and
                callable(subclass.bus_branch_network_creator) and
                hasattr(subclass, "topological_node_creator") and
                callable(subclass.topological_node_creator) and
                hasattr(subclass, "topological_branch_creator") and
                callable(subclass.topological_branch_creator) and
                hasattr(subclass, "topological_branch_type_creator") and
                callable(subclass.topological_branch_type_creator) and
                hasattr(subclass, "power_transformer_creator") and
                callable(subclass.power_transformer_creator) and
                hasattr(subclass, "power_transformer_type_creator") and
                callable(subclass.power_transformer_type_creator) and
                hasattr(subclass, "energy_source_creator") and
                callable(subclass.energy_source_creator) and
                hasattr(subclass, "energy_consumer_creator") and
                callable(subclass.energy_consumer_creator) and
                hasattr(subclass, "power_electronics_connection_creator") and
                callable(subclass.power_electronics_connection_creator) or
                NotImplemented)

    @abc.abstractmethod
    def bus_branch_network_creator(self, node_breaker_network: NetworkService) -> BBN:
        """
        Creates an empty target bus-branch network instance of type BBN.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :return: Target bus-branch network of type BBN.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def topological_node_creator(
        self,
        bus_branch_network: BBN,
        base_voltage: int,
        collapsed_conducting_equipment: FrozenSet[ConductingEquipment],
        border_terminals: FrozenSet[Terminal],
        inner_terminals: FrozenSet[Terminal],
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, TN):
        """
        Callback used to create a topological node instance of type TN.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param base_voltage: Base voltage value to be used for the topological node in Volts.
        :param collapsed_conducting_equipment: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.conducting_equipment.ConductingEquipment` being collapsed in this topological node. e.g. closed switches.
        :param border_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` that connect this topological node to other equipment.
        :param inner_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` collapsed in this topological node.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the topological node and the second element being an instance of type TN that represents a topological node in the target bus-branch network. This instance will be passed into the appropriate bus-branch model element creators for the elements that are connected to this topological node.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def topological_branch_creator(
        self,
        bus_branch_network: BBN,
        connected_topological_nodes: Tuple[TN, TN],
        length: float,
        topological_branch_type: TBT,
        collapsed_ac_line_segments: FrozenSet[AcLineSegment],
        border_terminals: FrozenSet[Terminal],
        inner_terminals: FrozenSet[Terminal],
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, TB):
        """
        Callback used to create a topological branch instance in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param connected_topological_nodes: Instances of type TN connected to this topological branch.
        :param length: Length of the topological branch in meters.
        :param topological_branch_type: Instance of type TBT for this topological branch.
        :param collapsed_ac_line_segments: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.wires.aclinesegment.AcLineSegment` being collapsed in this topological branch. e.g. connected lines with the same impedance values.
        :param border_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` that connect this topological branch to other equipment.
        :param inner_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` collapsed in this topological branch.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the topological branch and the second element being an instance of type TB that represents a topological branch in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def topological_branch_type_creator(
        self,
        bus_branch_network: BBN,
        per_length_sequence_impedance: PerLengthSequenceImpedance,
        wire_info: WireInfo,
        base_voltage: int,
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, TBT):
        """
        Callback used to create a topological branch type in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param per_length_sequence_impedance: Instance of `zepben.evolve.model.cim.iec61970.base.wires.per_length.PerLengthSequenceImpedance` used to generate this topological branch type.
        :param wire_info: Instance of `zepben.evolve.model.cim.iec61968.assetinfo.wire_info.WireInfo` used to generate this topological branch type.
        :param base_voltage: Base voltage value to be used for the topological branch type in Volts.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the topological branch type and the second element being an instance of type TBT that represents a topological branch type in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def power_transformer_creator(
        self,
        bus_branch_network: BBN,
        power_transformer: PowerTransformer,
        ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, TN]],
        power_transformer_type: PTT,
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, PT):
        """
        Callback used to create a power transformer instance in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param power_transformer: Instance of `zepben.evolve.model.cim.iec61970.base.wires.power_transformer.PowerTransformer` used to generate power transformer in target bus-branch network.
        :param ends_to_topological_nodes: List holding power transformer ends with the topological nodes they are connected to.
        :param power_transformer_type: Instance of type PTT for this power transformer.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the power transformer and the second element being an instance of type PT that represents a power transformer in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def power_transformer_type_creator(
        self,
        bus_branch_network: BBN,
        power_transformer: PowerTransformer,
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, PTT):
        """
        Callback used to create a power transformer type in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param power_transformer: Instance of `zepben.evolve.model.cim.iec61970.base.wires.power_transformer.PowerTransformer` used to generate this power transformer type.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the power transformer type and the second element being an instance of type PTT that represents a power transformer type in the target bus-branch network..
        """
        raise NotImplementedError

    @abc.abstractmethod
    def energy_source_creator(
        self,
        bus_branch_network: BBN,
        energy_source: EnergySource,
        connected_topological_node: TN,
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, ES):
        """
        Callback used to create an energy source instance in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param energy_source: Instance of `zepben.evolve.model.cim.iec61970.base.wires.energy_source.EnergySource` used to generate energy source in target bus-branch network.
        :param connected_topological_node: Topological node of type TN that is connected to this energy source.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the energy source and the second element being an instance of type ES that represents an energy source in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def energy_consumer_creator(
        self,
        bus_branch_network: BBN,
        energy_consumer: EnergyConsumer,
        connected_topological_node: TN,
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, EC):
        """
        Callback used to pass all the required values to generate an energy consumer object.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param energy_consumer: Instance of `zepben.evolve.model.cim.iec61970.base.wires.energy_consumer.EnergyConsumer` used to generate energy consumer in target bus-branch network.
        :param connected_topological_node: Topological node of type TN that is connected to this energy consumer.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the energy consumer and the second element being an instance of type EC that represents an energy consumer in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def power_electronics_connection_creator(
        self,
        bus_branch_network: BBN,
        power_electronics_connection: PEC,
        connected_topological_node: TN,
        node_breaker_network: NetworkService,
        logger: BusBranchNetworkCreationLogger
    ) -> (Any, PEC):
        """
        Callback used to pass all the required values to generate a power electronics connection object.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param power_electronics_connection: Instance of `zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection.PowerElectronicsConnection` used to generate power electronics connection in target bus-branch network.
        :param connected_topological_node: Topological node of type TN that is connected to this power electronics connection.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :param logger: Logger instance to capture any runtime messages while creating the bus-branch network.
        :return: A 2-tuple with the first element being an id for the power electronics connection and the second element being an instance of type PEC that represents a power eletronics connection in the target bus-branch network.
        """
        raise NotImplementedError

    def create(
        self,
        node_breaker_network: NetworkService,
        use_normal_state: bool = True,
        logger: BusBranchNetworkCreationLogger = None
    ) -> 'BusBranchNetworkCreationResult[BBN]':
        return _create_bus_branch_network(self, node_breaker_network, use_normal_state, logger)


@dataclass()
class ListBackedLogger(BusBranchNetworkCreationLogger):
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    infos: List[str] = field(default_factory=list)
    debugs: List[str] = field(default_factory=list)

    def error(self, message: str):
        self.errors.append(message)

    def warning(self, message: str):
        self.warnings.append(message)

    def info(self, message: str):
        self.infos.append(message)

    def debug(self, message: str):
        self.debugs.append(message)


@dataclass
class BusBranchNetworkCreationMappings:
    """
    Holds mappings between a bus-branch network and a node-breaker network.
    """
    topological_nodes: Dict[Any, FrozenSet[ConnectivityNode]] = field(default_factory=dict)
    topological_branches: Dict[Any, FrozenSet[AcLineSegment]] = field(default_factory=dict)
    topological_branch_types: Dict[Any, Tuple[PerLengthSequenceImpedance, WireInfo, int]] = field(default_factory=dict)
    power_transformers: Dict[Any, PowerTransformer] = field(default_factory=dict)
    power_transformer_types: Dict[Any, FrozenSet[PowerTransformer]] = field(default_factory=dict)
    energy_sources: Dict[Any, EnergySource] = field(default_factory=dict)
    energy_consumers: Dict[Any, EnergyConsumer] = field(default_factory=dict)
    power_electronics_connections: Dict[Any, PowerElectronicsConnection] = field(default_factory=dict)
    from_identified_object: Dict[str, Any] = field(default_factory=dict)


BBN_1 = TypeVar('BBN_1')  # Bus-Branch Network


@dataclass
class BusBranchNetworkCreationResult(Generic[BBN_1]):
    """
    Represents the results of creating a bus-branch network from a node-breaker network.
    """
    logger: BusBranchNetworkCreationLogger
    mappings: BusBranchNetworkCreationMappings = field(default_factory=BusBranchNetworkCreationMappings)
    network: BBN_1 = None


BBN_2 = TypeVar('BBN_2')  # Bus-Branch Network
TN_2 = TypeVar('TN_2')  # Topological Node
TB_2 = TypeVar('TB_2')  # Topological Branch
TBT_2 = TypeVar('TBT_2')  # Topological Branch Type
PT_2 = TypeVar('PT_2')  # Power Transformer
PTT_2 = TypeVar('PTT_2')  # Power Transformer Type
ES_2 = TypeVar('ES_2')  # Energy Source
EC_2 = TypeVar('EC_2')  # Energy Consumer
PEC_2 = TypeVar('PEC_2')  # Power Electronics Connection


def _create_bus_branch_network(
    bus_branch_network_creator: BusBranchNetworkCreator[BBN_2, TN_2, TB_2, TBT_2, PT_2, PTT_2, ES_2, EC_2, PEC_2],
    node_breaker_network: NetworkService,
    use_normal_state: bool = True,
    logger: BusBranchNetworkCreationLogger = None
) -> BusBranchNetworkCreationResult[BBN_2]:
    """
    :param bus_branch_network_creator: Instance of type BusBranchNetworkCreator used to generate the target bus-branch network.
    :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
    :param use_normal_state: Flag to determine the network state used when checking switch states. Uses 'normal state' if True, 'current state' otherwise. default: True
    :param logger: logger instance passed into the bus_branch_network_creator methods.
    :return: `CreationResult`
    """
    _validate_number_of_terminals(node_breaker_network)

    if logger is None:
        logger = ListBackedLogger()

    result: BusBranchNetworkCreationResult[BBN_2] = BusBranchNetworkCreationResult(logger)
    bus_branch_network = bus_branch_network_creator.bus_branch_network_creator(node_breaker_network)

    def get_is_open(sw: Switch):
        return sw.is_normally_open() if use_normal_state else sw.is_open()

    terminals_to_tns = _create_topological_nodes(node_breaker_network, bus_branch_network, bus_branch_network_creator, result, get_is_open, logger)
    _create_topological_branches(node_breaker_network, bus_branch_network, bus_branch_network_creator, result, terminals_to_tns, logger)
    _create_power_transformers(node_breaker_network, bus_branch_network, bus_branch_network_creator, result, terminals_to_tns, logger)
    _create_energy_sources(node_breaker_network, bus_branch_network, bus_branch_network_creator, result, terminals_to_tns, logger)
    _create_energy_consumers(node_breaker_network, bus_branch_network, bus_branch_network_creator, result, terminals_to_tns, logger)
    _create_power_electronics_connections(node_breaker_network, bus_branch_network, bus_branch_network_creator, result, terminals_to_tns, logger)

    result.network = bus_branch_network
    return result


BBN_3 = TypeVar('BBN_3')  # Bus-Branch Network
TN_3 = TypeVar('TN_3')  # Topological Node
TB_3 = TypeVar('TB_3')  # Topological Branch
TBT_3 = TypeVar('TBT_3')  # Topological Branch Type
PT_3 = TypeVar('PT_3')  # Power Transformer
PTT_3 = TypeVar('PTT_3')  # Power Transformer Type
ES_3 = TypeVar('ES_3')  # Energy Source
EC_3 = TypeVar('EC_3')  # Energy Consumer
PEC_3 = TypeVar('PEC_3')  # Power Electronics Connection


def _create_topological_nodes(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN_3,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN_3, TN_3, TB_3, TBT_3, PT_3, PTT_3, ES_3, EC_3, PEC_3],
    result: BusBranchNetworkCreationResult[BBN_3],
    get_is_open: Callable[[Switch], bool],
    logger: BusBranchNetworkCreationLogger
) -> Dict[str, TN_3]:
    terminals_to_tns: Dict[str, TN_3] = {}
    processed_cn_ids = set()
    for cn in node_breaker_network.objects(ConnectivityNode):
        if cn.mrid not in processed_cn_ids:
            # group terminals connected by negligible impedance equipment
            negligible_impedance_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn, get_is_open)
            rated_u = next((_get_base_voltage(t.conducting_equipment, t) for t in border_terms), None)

            # create topological node
            tn_id, tn = bus_branch_network_creator.topological_node_creator(
                bus_branch_network,
                rated_u,
                negligible_impedance_equipment,
                border_terms,
                inner_terms,
                node_breaker_network,
                logger
            )

            # map border terminals to associated topological nodes for easy lookup when creating connected equipment
            for t in border_terms:
                terminals_to_tns[t.mrid] = tn

            # populate result mappings
            tn_connectivity_nodes: Set[ConnectivityNode] = set()
            tn_connectivity_nodes.update({t.connectivity_node for t in inner_terms})
            tn_connectivity_nodes.update({t.connectivity_node for t in border_terms})
            result.mappings.topological_nodes[tn_id] = frozenset(tn_connectivity_nodes)

            for tn_cn in tn_connectivity_nodes:
                result.mappings.from_identified_object[tn_cn.mrid] = tn
                for tn_cn_t in tn_cn.terminals:
                    result.mappings.from_identified_object[tn_cn_t.mrid] = tn
            for eq in negligible_impedance_equipment:
                result.mappings.from_identified_object[eq.mrid] = tn

            # flag processed connectivity nodes
            processed_cn_ids.update(tn_connectivity_nodes)
    return terminals_to_tns


BBN_4 = TypeVar('BBN_4')  # Bus-Branch Network
TN_4 = TypeVar('TN_4')  # Topological Node
TB_4 = TypeVar('TB_4')  # Topological Branch
TBT_4 = TypeVar('TBT_4')  # Topological Branch Type
PT_4 = TypeVar('PT_4')  # Power Transformer
PTT_4 = TypeVar('PTT_4')  # Power Transformer Type
ES_4 = TypeVar('ES_4')  # Energy Source
EC_4 = TypeVar('EC_4')  # Energy Consumer
PEC_4 = TypeVar('PEC_4')  # Power Electronics Connection


def _create_topological_branches(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN_4,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN_4, TN_4, TB_4, TBT_4, PT_4, PTT_4, ES_4, EC_4, PEC_4],
    result: BusBranchNetworkCreationResult[BBN_4],
    terminals_to_tns: Dict[str, TN_4],
    logger: BusBranchNetworkCreationLogger
):
    processed_acls_ids = set()
    for acls in node_breaker_network.objects(AcLineSegment):
        if acls.mrid not in processed_acls_ids:
            # group ac-line-segments with common characteristics (per_length_sequence_impedance)
            # TODO: group by both wire_info and per_length_sequence_impedance
            common_acls, inner_terms, border_terms = _group_common_ac_line_segment_terminals(acls)

            # retrieve connected topological nodes
            acls_tns = [terminals_to_tns[t.mrid] for t in border_terms]

            total_length = reduce(lambda s, l: l.length + s, (common_acl for common_acl in common_acls), 0.0)
            plsi = next((common_acl for common_acl in common_acls)).per_length_sequence_impedance
            wire_info = next((common_acl for common_acl in common_acls)).wire_info
            voltage = [acls.base_voltage.nominal_voltage for acls in common_acls][0]

            # create topological branch type
            tb_type_id, tb_type = bus_branch_network_creator.topological_branch_type_creator(
                bus_branch_network,
                plsi,
                wire_info,
                voltage,
                node_breaker_network,
                logger
            )

            # create topological branch
            tb_id, tb = bus_branch_network_creator.topological_branch_creator(
                bus_branch_network,
                (acls_tns[0], acls_tns[1]),
                total_length,
                tb_type,
                common_acls,
                border_terms,
                inner_terms,
                node_breaker_network,
                logger
            )

            # populate result mappings
            result.mappings.topological_branch_types[tb_type_id] = (plsi, wire_info, voltage)
            result.mappings.topological_branches[tb_id] = frozenset(common_acls)

            result.mappings.from_identified_object[f"{plsi.mrid}:{wire_info.mrid}:{voltage}"] = tb_type

            for common_acl in common_acls:
                result.mappings.from_identified_object[common_acl.mrid] = tb

            for t in inner_terms:
                result.mappings.from_identified_object[t] = tb

            # flag processed ac-line-segments
            processed_acls_ids.update({acls.mrid for acls in common_acls})


BBN_5 = TypeVar('BBN_5')  # Bus-Branch Network
TN_5 = TypeVar('TN_5')  # Topological Node
TB_5 = TypeVar('TB_5')  # Topological Branch
TBT_5 = TypeVar('TBT_5')  # Topological Branch Type
PT_5 = TypeVar('PT_5')  # Power Transformer
PTT_5 = TypeVar('PTT_5')  # Power Transformer Type
ES_5 = TypeVar('ES_5')  # Energy Source
EC_5 = TypeVar('EC_5')  # Energy Consumer
PEC_5 = TypeVar('PEC_5')  # Power Electronics Connection


def _create_power_transformers(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN_5,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN_5, TN_5, TB_5, TBT_5, PT_5, PTT_5, ES_5, EC_5, PEC_5],
    result: BusBranchNetworkCreationResult[BBN_5],
    terminals_to_tns: Dict[str, TN_5],
    logger: BusBranchNetworkCreationLogger
):
    for pt in node_breaker_network.objects(PowerTransformer):
        # create list of ends with their connected topological nodes
        ends_to_topological_nodes = [(e, None) if e.terminal is None else (e, terminals_to_tns.get(e.terminal.mrid)) for e in pt.ends]

        # create power transformer type
        tx_type_id, tx_type = bus_branch_network_creator.power_transformer_type_creator(bus_branch_network, pt, node_breaker_network, logger)

        # create power transformer
        tx_id, tx = bus_branch_network_creator.power_transformer_creator(
            bus_branch_network,
            pt,
            ends_to_topological_nodes,
            tx_type,
            node_breaker_network,
            logger
        )

        # populate result mappings
        pts = result.mappings.power_transformer_types.get(tx_type_id, set())
        pts.add(pt)
        result.mappings.power_transformer_types[tx_type_id] = pts

        result.mappings.power_transformers[tx_id] = pt

        result.mappings.from_identified_object[pt.mrid] = tx
        for end in pt.ends:
            result.mappings.from_identified_object[end.mrid] = tx


BBN_6 = TypeVar('BBN_6')  # Bus-Branch Network
TN_6 = TypeVar('TN_6')  # Topological Node
TB_6 = TypeVar('TB_6')  # Topological Branch
TBT_6 = TypeVar('TBT_6')  # Topological Branch Type
PT_6 = TypeVar('PT_6')  # Power Transformer
PTT_6 = TypeVar('PTT_6')  # Power Transformer Type
ES_6 = TypeVar('ES_6')  # Energy Source
EC_6 = TypeVar('EC_6')  # Energy Consumer
PEC_6 = TypeVar('PEC_6')  # Power Electronics Connection


def _create_energy_sources(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN_6,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN_6, TN_6, TB_6, TBT_6, PT_6, PTT_6, ES_6, EC_6, PEC_6],
    result: BusBranchNetworkCreationResult[BBN_6],
    terminals_to_tns: Dict[str, TN_6],
    logger: BusBranchNetworkCreationLogger
):
    for es in node_breaker_network.objects(EnergySource):
        es_tn = terminals_to_tns[next((t for t in es.terminals)).mrid]
    bb_es_id, bb_es = bus_branch_network_creator.energy_source_creator(bus_branch_network, es, es_tn, node_breaker_network, logger)

    # populate result mappings
    result.mappings.energy_sources[bb_es_id] = es
    result.mappings.from_identified_object[es.mrid] = bb_es


BBN_7 = TypeVar('BBN_7')  # Bus-Branch Network
TN_7 = TypeVar('TN_7')  # Topological Node
TB_7 = TypeVar('TB_7')  # Topological Branch
TBT_7 = TypeVar('TBT_7')  # Topological Branch Type
PT_7 = TypeVar('PT_7')  # Power Transformer
PTT_7 = TypeVar('PTT_7')  # Power Transformer Type
ES_7 = TypeVar('ES_7')  # Energy Source
EC_7 = TypeVar('EC_7')  # Energy Consumer
PEC_7 = TypeVar('PEC_7')  # Power Electronics Connection


def _create_energy_consumers(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN_7,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN_7, TN_7, TB_7, TBT_7, PT_7, PTT_7, ES_7, EC_7, PEC_7],
    result: BusBranchNetworkCreationResult[BBN_7],
    terminals_to_tns: Dict[str, TN_7],
    logger: BusBranchNetworkCreationLogger
):
    for ec in node_breaker_network.objects(EnergyConsumer):
        ec_tn = terminals_to_tns[next((t for t in ec.terminals)).mrid]
    bb_ec_id, bb_ec = bus_branch_network_creator.energy_consumer_creator(bus_branch_network, ec, ec_tn, node_breaker_network, logger)

    # populate result mappings
    result.mappings.energy_consumers[bb_ec_id] = ec
    result.mappings.from_identified_object[ec.mrid] = bb_ec


BBN_8 = TypeVar('BBN_8')  # Bus-Branch Network
TN_8 = TypeVar('TN_8')  # Topological Node
TB_8 = TypeVar('TB_8')  # Topological Branch
TBT_8 = TypeVar('TBT_8')  # Topological Branch Type
PT_8 = TypeVar('PT_8')  # Power Transformer
PTT_8 = TypeVar('PTT_8')  # Power Transformer Type
ES_8 = TypeVar('ES_8')  # Energy Source
EC_8 = TypeVar('EC_8')  # Energy Consumer
PEC_8 = TypeVar('PEC_8')  # Power Electronics Connection


def _create_power_electronics_connections(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN_8,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN_8, TN_8, TB_8, TBT_8, PT_8, PTT_8, ES_8, EC_8, PEC_8],
    result: BusBranchNetworkCreationResult[BBN_8],
    terminals_to_tns: Dict[str, TN_8],
    logger: BusBranchNetworkCreationLogger
):
    for pec in node_breaker_network.objects(PowerElectronicsConnection):
        pec_tn = terminals_to_tns[next((t for t in pec.terminals)).mrid]
    bb_pec_id, bb_pec = bus_branch_network_creator.power_electronics_connection_creator(bus_branch_network, pec, pec_tn, node_breaker_network, logger)

    # populate result mappings
    result.mappings.energy_consumers[bb_pec_id] = pec
    result.mappings.from_identified_object[pec.mrid] = bb_pec


def _get_base_voltage(ce: ConductingEquipment, t: Terminal) -> Union[int, None]:
    # TODO: This should ideally come from the voltage_level container for the conducting equipment and in the absence of that we should use the base_voltage \
    #  for the upstream power_transformer end.
    if isinstance(ce, PowerTransformer):
        return next((e for e in ce.ends if e.terminal is t)).rated_u
    else:
        return ce.base_voltage.nominal_voltage


def _validate_number_of_terminals(network: NetworkService):
    illegal_acls = []
    for acl in network.objects(AcLineSegment):
        if acl.num_terminals() != 2:
            illegal_acls.append(acl)

    if len(illegal_acls) != 0:
        raise ValueError(f"NetworkService contains the following AcLineSegments with an invalid number of terminals: {[acl.mrid for acl in illegal_acls]}")

    illegal_es = []
    for es in network.objects(EnergySource):
        if es.num_terminals() != 1:
            illegal_es.append(es)

    if len(illegal_es) != 0:
        raise ValueError(f"NetworkService contains the following EnergySources with an invalid number of terminals: {[es.mrid for es in illegal_es]}")

    illegal_ec = []
    for ec in network.objects(EnergyConsumer):
        if ec.num_terminals() != 1:
            illegal_ec.append(ec)

    if len(illegal_ec) != 0:
        raise ValueError(f"NetworkService contains the following EnergyConsumers with an invalid number of terminals: {[ec.mrid for ec in illegal_ec]}")

    illegal_pec = []
    for pec in network.objects(PowerElectronicsConnection):
        if pec.num_terminals() != 1:
            illegal_pec.append(pec)

    if len(illegal_pec) != 0:
        raise ValueError(
            f"NetworkService contains the following PowerElectronicsConnections with an invalid number of terminals: {[pec.mrid for pec in illegal_pec]}")


def _group_negligible_impedance_terminals(
    cnn: ConnectivityNode,
    get_is_open: Callable[[Switch], bool],
    negligible_impedance_equipment: Set[Union[Switch, Junction, BusbarSection, Jumper]] = None,
    inner_terminals: Set[Terminal] = None,
    border_terminals: Set[Terminal] = None
) -> Tuple[FrozenSet[Union[Switch, Junction, BusbarSection, Jumper]], FrozenSet[Terminal], FrozenSet[Terminal]]:
    if negligible_impedance_equipment is None:
        negligible_impedance_equipment = set()
    if inner_terminals is None:
        inner_terminals = set()
    if border_terminals is None:
        border_terminals = set()

    for t in cnn.terminals:

        if isinstance(t.conducting_equipment, Switch) and not get_is_open(t.conducting_equipment) \
            or isinstance(t.conducting_equipment, Junction) \
            or isinstance(t.conducting_equipment, BusbarSection):
            ni_equipment = t.conducting_equipment
            negligible_impedance_equipment.add(ni_equipment)
            other_terminals = {nie_t for nie_t in ni_equipment.terminals
                               if nie_t is not t and nie_t not in border_terminals and nie_t not in inner_terminals}

            if len(other_terminals) == 0:
                if ni_equipment.num_terminals() >= 2:
                    inner_terminals.add(t)
                else:
                    border_terminals.add(t)
                continue

            inner_terminals.add(t)
            for other_t in other_terminals:
                if other_t.connectivity_node is None:
                    border_terminals.add(other_t)
                else:
                    _group_negligible_impedance_terminals(
                        other_t.connectivity_node,
                        get_is_open,
                        negligible_impedance_equipment,
                        inner_terminals,
                        border_terminals
                    )
        else:
            border_terminals.add(t)

    return frozenset(negligible_impedance_equipment), frozenset(inner_terminals), frozenset(border_terminals)


def _group_common_ac_line_segment_terminals(
    ac_line: AcLineSegment,
    ac_line_segments: Set[AcLineSegment] = None
) -> Tuple[FrozenSet[AcLineSegment], FrozenSet[Terminal], FrozenSet[Terminal]]:
    if ac_line_segments is None:
        ac_line_segments = set()

    ac_line_segments.add(ac_line)
    for t in ac_line.terminals:
        if t.connectivity_node is None or t.connectivity_node.num_terminals() > 2:
            continue

        for adjacent_common_ac_line in (ot.conducting_equipment for ot in t.connectivity_node.terminals
                                        if ot is not t
                                           and ot.conducting_equipment not in ac_line_segments
                                           and isinstance(ot.conducting_equipment, AcLineSegment)
                                           # TODO: we should a include check to make sure the wire_info is also the same between ac-line-segments
                                           and ot.conducting_equipment.per_length_sequence_impedance is ac_line.per_length_sequence_impedance):
            _group_common_ac_line_segment_terminals(adjacent_common_ac_line, ac_line_segments)

    all_terminals = {t for ts in (acl.terminals for acl in ac_line_segments) for t in ts}
    inner_terminals = {t for t in all_terminals if t.connectivity_node is not None
                       for ot in t.connectivity_node.terminals if ot is not t and ot in all_terminals}
    border_terminals = {t for t in all_terminals if t not in inner_terminals}

    return frozenset(ac_line_segments), frozenset(inner_terminals), frozenset(border_terminals)
