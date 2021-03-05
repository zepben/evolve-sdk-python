#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import defaultdict
from enum import Enum
from functools import reduce
from typing import Set, Tuple, FrozenSet, Dict, Callable, Union, TypeVar, Optional

from zepben.evolve import NetworkService, ConnectivityNode, Terminal, Switch, AcLineSegment, ConductingEquipment, \
    PowerTransformer, \
    EnergySource, EnergyConsumer, IdentifiedObject, ShuntCompensator, Junction, BusbarSection, Jumper, \
    PerLengthSequenceImpedance, WireInfo

__all__ = ["create_bus_branch_model", "CreationResult", "ErrorInfo", "ErrorType"]

BBN = TypeVar('BBN')  # Bus-Branch Network
TN = TypeVar('TN')  # Topological Node
PTT = TypeVar('PTT')  # PowerTransformer Type
TBT = TypeVar('TBT')  # Topological Branch Type


class ErrorType(Enum):
    invalid_number_of_terminals = "invalid_number_of_terminals"
    unsupported_class = "unsupported_class"
    missing_required_data = "missing_required_data"


class ErrorInfo:
    """
    Error information for an identified object that failed a validation test when trying to generate a bus-branch model.
    """

    def __init__(self, error_type: ErrorType, io: IdentifiedObject):
        self.error_type = error_type
        self.io = io


class CreationResult:
    """
    Represents the results of creating a bus-branch model from a network service (node-breaker-model)
    """

    def __init__(self, bus_branch_model: Optional[BBN] = None, errors: Dict[ErrorType, Set[ErrorInfo]] = defaultdict(set)):
        self.bus_branch_model = bus_branch_model,
        self.errors = errors

    @property
    def succeed(self) -> bool:
        """True if no errors were found while trying to create the bus-branch model, False otherwise."""
        return len(self.errors) == 0

    def _add_error(self, error_type: ErrorType, io: IdentifiedObject):
        self.errors[error_type].add(ErrorInfo(error_type, io))


def create_bus_branch_model(
        network_service: NetworkService,
        bus_branch_network_creator: Callable[[NetworkService], BBN],
        topological_node_creator: Callable[[BBN, int, FrozenSet[ConductingEquipment], FrozenSet[Terminal], FrozenSet[Terminal], NetworkService], TN],
        topological_branch_creator: Callable[
            [BBN, Tuple[TN, TN], float, TBT, FrozenSet[AcLineSegment], FrozenSet[Terminal], FrozenSet[Terminal], NetworkService], None],
        topological_branch_type_creator: Callable[[BBN, PerLengthSequenceImpedance, WireInfo], TBT],
        get_topological_branch_type_id: Callable[[PerLengthSequenceImpedance, WireInfo], str],
        two_winding_power_transformer_creator: Callable[[BBN, PowerTransformer, Tuple[TN, TN], PTT, NetworkService], None],
        power_transformer_type_creator: Callable[[BBN, PowerTransformer], PTT],
        get_power_transformer_type_id: Callable[[PowerTransformer], str],
        infeed_creator: Callable[[BBN, EnergySource, TN, NetworkService], None],
        energy_consumer_creator: Callable[[BBN, EnergyConsumer, TN, NetworkService], None],
        use_normal_state: bool = True) -> CreationResult:
    """
    Computes the values needed to generate a bus-branch model from a source `zepben.evolve.services.network.network.NetworkService` object and calls the appropriate bus-branch model element creator callbacks passing in those values.

    Generic Types:
    BBN := The object you are using to represent the bus-branch network.
    TN := The object used to represent a topological node.
    PTT := The object used to represent a transformer datasheet information needed to run a loadflow.
    TBT := The object used to represent a topological branch's datasheet information needed to run a loadflow.

    :param network_service: Source `zepben.evolve.services.network.network.NetworkService` used for the computation of the bus-branch model.
    :param bus_branch_network_creator: Creates target bus-branch model instance of type BBN.
    :param topological_node_creator: Callback used to create a topological node instance of type TN.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param base_voltage: Base voltage value to be used for the topological node in Volts.
        :param collapsed_conducting_equipment: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.conducting_equipment.ConductingEquipment` being collapsed in this topological node. e.g. closed switches.
        :param border_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` that connect this topological node to other equipment.
        :param inner_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` collapsed in this topological node.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :return: Instance of type TN that represents a topological node in your target bus-branch network. This instance will be passed into the appropriate bus-branch model element creators for the elements that are connected to this topological node.

    :param topological_branch_creator: Callback used to create a topological branch instance in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param connected_topological_nodes: Instances of type TN connected to this topological branch.
        :param length: Length of the topological branch in meters.
        :param topological_branch_type: Instance of type TBT for this topological branch. The instace passed in is determined by the id generated with `get_topological_branch_type_id` function with the `zepben.evolve.model.cim.iec61970.base.wires.per_length.PerLengthSequenceImpedance` and `zepben.evolve.model.cim.iec61968.assetinfo.wire_info.WireInfo` for this topological branch being used as arguments.
        :param collapsed_ac_line_segments: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.wires.aclinesegment.AcLineSegment` being collapsed in this topological branch. e.g. connected lines with the same impedance values.
        :param border_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` that connect this topological branch to other equipment.
        :param inner_terminals: Set that contains all instances of `zepben.evolve.model.cim.iec61970.base.core.terminal.Terminal` collapsed in this topological branch.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :return: None

    :param topological_branch_type_creator: Callback used to create a topological branch type in target bus-branch network that is uniquely identified by the id generated with the `get_topological_branch_type_id` function.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param per_length_sequence_impedance: Instance of `zepben.evolve.model.cim.iec61970.base.wires.per_length.PerLengthSequenceImpedance` used to generate this topological branch type.
        :param wire_info: Instance of `zepben.evolve.model.cim.iec61968.assetinfo.wire_info.WireInfo` used to generate this topological branch type.
        :return: Instace of type TBT that represents a topological branch's datasheet information needed to run a loadflow.

    :param get_topological_branch_type_id: Function that returns a unique identifier for the topological branch type.
        :param per_length_sequence_impedance: Instance of `zepben.evolve.model.cim.iec61970.base.wires.per_length.PerLengthSequenceImpedance` used to generate this topological branch type id.
        :param wire_info: Instance of `zepben.evolve.model.cim.iec61968.assetinfo.wire_info.WireInfo` used to generate this topological branch type id.
        :return: String that serves as an id that uniquely identifies this topological branch type.

    :param two_winding_power_transformer_creator: Callback used to create a two-winding transformer instance in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param power_transformer: Instance of `zepben.evolve.model.cim.iec61970.base.wires.power_transformer.PowerTransformer` used to generate two-winding transformer in target bus-branch network.
        :param connedted_topological_nodes: 2-tuple holding the topological nodes of type TN that are connected to the two-winding transformer. The first element in the tuple holds the HV topological node and the second holds the LV one.
        :param power_transformer_type: Instance of type PTT for this power transformer. The instance passed in is determined by the id generated with `get_power_transformer_type_id` function with the `zepben.evolve.model.cim.iec61970.base.wires.power_transformer.PowerTransformer` for this two-winding transformer being used as an argument.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :return: None

    :param power_transformer_type_creator: Callback used to create a power transformer type in target bus-branch network that is uniquely identified by the id generated with the `get_power_transformer_type_id` function.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param power_transformer: Instance of `zepben.evolve.model.cim.iec61970.base.wires.power_transformer.PowerTransformer` used to generate this power transformer type.
        :return: Instace of type PTT that represents a power transformerf's datasheet information needed to run a loadflow.

    :param get_power_transformer_type_id: Function that returns a unique identifier for the power transformer type.
        :param power_transformer: Instance of `zepben.evolve.model.cim.iec61970.base.wires.power_transformer.PowerTransformer` used to generate this power transformer type id.
        :return: String that serves as an id that uniquely identifies this power transformer type.

    :param infeed_creator: Callback used to create an infeed instance in target bus-branch network.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param energy_source: Instance of `zepben.evolve.model.cim.iec61970.base.wires.energy_source.EnergySource` used to generate infeed in target bus-branch network.
        :param connected_topological_node: Topological node of type TN that is connected to this infeed.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :return: None

    :param energy_consumer_creator: Callback used to pass all the required values to generate an energy consumer object.
        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param energy_consumer: Instance of `zepben.evolve.model.cim.iec61970.base.wires.energy_consumer.EnergyConsumer` used to generate energy consumer in target bus-branch network.
        :param connected_topological_node: Topological node of type TN that is connected to this energy consumer.
        :param node_breaker_network: Instance of type `zepben.evolve.services.network.network.NetworkService` being used as a source node-breaker network.
        :return: None

    :param use_normal_state: Flag to determine the network state used when checking switch states. Uses 'normal state' if True, 'current state' otherwise. default: True
    :return: `CreationResult`
    """
    result = CreationResult()
    _validate_node_breaker_model(network_service, result)

    if len(result.errors.values()) != 0:
        return result

    bus_branch_network = bus_branch_network_creator(network_service)

    def get_is_open(sw: Switch):
        return sw.is_normally_open() if use_normal_state else sw.is_open()

    tb_types: Dict[str, TBT] = {}
    pt_types: Dict[str, PTT] = {}
    tns: Dict[str, TN] = {}
    processed_cn_ids = set()
    for cn in network_service.objects(ConnectivityNode):
        if cn.mrid not in processed_cn_ids:
            closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn, get_is_open)
            rated_u = next((_get_base_voltage(t.conducting_equipment, t) for t in border_terms), None)
            tn = topological_node_creator(bus_branch_network, rated_u, closed_switches, border_terms, inner_terms, network_service)

            for t in border_terms:
                tns[t.mrid] = tn

            processed_cn_ids.update({t.connectivity_node.mrid for t in inner_terms})
            processed_cn_ids.update({t.connectivity_node.mrid for t in border_terms})

    processed_acls_ids = set()
    for acls in network_service.objects(AcLineSegment):
        if acls.mrid not in processed_acls_ids:
            common_acls, inner_terms, border_terms = _group_common_ac_line_segment_terminals(acls)
            acls_tns = [tns[t.mrid] for t in border_terms]
            total_length = reduce(lambda s, l: l.length + s, (acls for acls in common_acls), 0.0)
            psli = next((common_acl for common_acl in common_acls)).per_length_sequence_impedance
            wire_info = next((common_acl for common_acl in common_acls)).wire_info
            tb_type_id = get_topological_branch_type_id(psli, wire_info)

            tb_type = tb_types.get(tb_type_id)
            if tb_type is None:
                tb_type = topological_branch_type_creator(bus_branch_network, psli, wire_info)
                tb_types[tb_type_id] = tb_type

            topological_branch_creator(
                bus_branch_network,
                (acls_tns[0], acls_tns[1]),
                total_length,
                tb_type,
                common_acls,
                border_terms,
                inner_terms,
                network_service
            )

            processed_acls_ids.update({acls.mrid for acls in common_acls})

    for pt in network_service.objects(PowerTransformer):
        pt_tns = [tns[t.mrid] for t in (e.terminal for e in pt.ends)]

        pt_type_id = get_power_transformer_type_id(pt)
        pt_type = pt_types.get(pt_type_id)
        if pt_type is None:
            pt_type = power_transformer_type_creator(bus_branch_network, pt)
            pt_types[pt_type_id] = pt_type

        if len(pt_tns) == 2:
            two_winding_power_transformer_creator(bus_branch_network, pt, (pt_tns[0], pt_tns[1]), pt_type, network_service)
        else:
            result._add_error(ErrorType.invalid_number_of_terminals, pt)
            return result

    for es in network_service.objects(EnergySource):
        es_tn = tns[next((t for t in es.terminals)).mrid]
        infeed_creator(bus_branch_network, es, es_tn, network_service)

    for ec in network_service.objects(EnergyConsumer):
        ec_tn = tns[next((t for t in ec.terminals)).mrid]
        energy_consumer_creator(bus_branch_network, ec, ec_tn, network_service)

    result.bus_branch_model = bus_branch_network
    return result


def _get_base_voltage(ce: ConductingEquipment, t: Terminal) -> Union[int, None]:
    # TODO: This should ideally come from the voltage_level container for the conducting equipment and in the absence of that we should use the base_voltage \
    #  for the upstream power_transformer end.
    if isinstance(ce, PowerTransformer):
        return next((e for e in ce.ends if e.terminal is t)).rated_u
    else:
        return ce.base_voltage.nominal_voltage


def _validate_node_breaker_model(network: NetworkService, result: CreationResult):
    for acl in network.objects(AcLineSegment):
        if acl.num_terminals() != 2:
            result._add_error(ErrorType.invalid_number_of_terminals, acl)

        if acl.per_length_sequence_impedance is None or acl.wire_info is None:
            result._add_error(ErrorType.missing_required_data, acl)

    for sw in network.objects(Switch):
        if sw.num_terminals() != 2:
            result._add_error(ErrorType.invalid_number_of_terminals, sw)

    for tx in network.objects(PowerTransformer):
        if tx.num_terminals() != 2:
            result._add_error(ErrorType.invalid_number_of_terminals, tx)

        if tx.power_transformer_info is None:
            result._add_error(ErrorType.missing_required_data, tx)

    for es in network.objects(EnergySource):
        if es.num_terminals() != 1:
            result._add_error(ErrorType.invalid_number_of_terminals, es)

    for ec in network.objects(EnergyConsumer):
        if ec.num_terminals() != 1:
            result._add_error(ErrorType.invalid_number_of_terminals, ec)

    for sc in network.objects(ShuntCompensator):
        result._add_error(ErrorType.unsupported_class, sc)


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
                                           and ot.conducting_equipment.per_length_sequence_impedance is ac_line.per_length_sequence_impedance):
            _group_common_ac_line_segment_terminals(adjacent_common_ac_line, ac_line_segments)

    all_terminals = {t for ts in (acl.terminals for acl in ac_line_segments) for t in ts}
    inner_terminals = {t for t in all_terminals if t.connectivity_node is not None
                       for ot in t.connectivity_node.terminals if ot is not t and ot in all_terminals}
    border_terminals = {t for t in all_terminals if t not in inner_terminals}

    return frozenset(ac_line_segments), frozenset(inner_terminals), frozenset(border_terminals)
