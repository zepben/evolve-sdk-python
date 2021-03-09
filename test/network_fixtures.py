#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Dict, List, Optional

from pytest import fixture
from zepben.evolve import NetworkService, Feeder, PhaseCode, EnergySource, EnergySourcePhase, Junction, ConductingEquipment, Breaker, PowerTransformer, \
    UsagePoint, Terminal, PowerTransformerEnd, Meter, AssetOwner, CustomerService, Organisation, AcLineSegment, \
    PerLengthSequenceImpedance, WireInfo, EnergyConsumer, GeographicalRegion, SubGeographicalRegion, Substation, PowerSystemResource, Location, PositionPoint, \
    SetPhases, OverheadWireInfo, OperationalRestriction, Equipment, ConnectivityNode

__all__ = ["create_terminals", "create_junction_for_connecting", "create_source_for_connecting", "create_switch_for_connecting", "create_acls_for_connecting",
           "create_energy_consumer_for_connecting", "create_feeder", "create_substation", "create_power_transformer_for_connecting", "create_terminals",
           "create_geographical_region", "create_subgeographical_region", "create_asset_owner", "create_meter", "create_power_transformer_end",
           "basic_network_hierarchy", "feeder_network", "feeder_start_point_between_conductors_network", "feeder_start_point_to_open_point_network",
           "feeder_with_current", "operational_restriction_with_equipment", "create_connectivitynode_with_terminals", "single_connectivitynode_network",
           "create_terminal", "network_service"]

from zepben.evolve.services.network.tracing.feeder.assign_to_feeders import AssignToFeeders
from zepben.evolve.util import CopyableUUID


def create_terminals(network: NetworkService, ce: ConductingEquipment, num_terms: int, phases: PhaseCode = PhaseCode.ABCN) -> List[Terminal]:
    terms = []
    for i in range(1, num_terms + 1):
        term = Terminal(mrid=f"{ce.mrid}_t{i}", conducting_equipment=ce, phases=phases, sequence_number=i)
        ce.add_terminal(term)
        assert network.add(term)
        terms.append(term)

    return terms


def create_terminal(network: NetworkService, ce: Optional[ConductingEquipment], phases: PhaseCode = PhaseCode.ABCN, sequence_number: int = 1) -> Terminal:
    terminal = None
    try:
        terminal = ce.get_terminal_by_sn(sequence_number) if ce is not None else None
    except IndexError:
        pass

    if terminal is None:
        terminal = Terminal(conducting_equipment=ce, phases=phases, sequence_number=sequence_number)
        if ce:
            ce.add_terminal(terminal)
        network.add(terminal)
    return terminal


def create_connectivitynode_with_terminals(ns: NetworkService, mrid: str, *terminal_phases: PhaseCode):
    cn = ConnectivityNode(mrid)
    ns.add(cn)
    for i, phase in enumerate(terminal_phases, start=1):
        t = create_terminal(ns, None, phase, i)
        ns.connect_by_mrid(t, mrid)


def create_junction_for_connecting(network: NetworkService, mrid: str = "", num_terms: int = 0, phases: PhaseCode = PhaseCode.ABCN) -> Junction:
    if not mrid:
        mrid = str(CopyableUUID())

    junction = Junction(mrid, name="test junction")
    create_terminals(network, junction, num_terms, phases)
    network.add(junction)
    return junction


def create_source_for_connecting(network: NetworkService, mrid: str = "", num_terms: int = 0, phases: PhaseCode = PhaseCode.ABCN) -> EnergySource:
    if not mrid:
        mrid = str(CopyableUUID())

    source = EnergySource(mrid)
    for phase in phases.single_phases:
        esp = EnergySourcePhase(energy_source=source, phase=phase)

        source.add_phase(esp)
        network.add(esp)

    create_terminals(network, source, num_terms, phases)
    network.add(source)
    return source


def create_switch_for_connecting(network: NetworkService, mrid: str = "", num_terms: int = 0, phases: PhaseCode = PhaseCode.ABC,
                                 normal_phase_states: List[bool] = None, current_phase_states: List[bool] = None) -> Breaker:
    if not mrid:
        mrid = str(CopyableUUID())

    cb = Breaker(mrid, name="test breaker")
    create_terminals(network, cb, num_terms, phases)

    cb.set_open(False)
    cb.set_normally_open(False)
    if normal_phase_states:
        for i, state in enumerate(normal_phase_states):
            cb.set_normally_open(state, phases.single_phases[i])
    if current_phase_states:
        for i, state in enumerate(current_phase_states):
            cb.set_open(state, phases.single_phases[i])

    network.add(cb)
    return cb


def create_power_transformer_end(network: NetworkService, pt: PowerTransformer, t: Terminal, end_number: int = 0, **kwargs) -> PowerTransformerEnd:
    en = end_number if end_number > 0 else t.sequence_number
    te = PowerTransformerEnd(mrid=f"{pt.mrid}_e{en}", power_transformer=pt, terminal=t, end_number=en,
                             **kwargs)
    pt.add_end(te)
    network.add(te)
    return te


def create_asset_owner(network: NetworkService, company: str, customer_service: Optional[CustomerService] = None) -> AssetOwner:
    ao = AssetOwner(mrid=f"{company}-owner-role")
    org = Organisation(mrid=company, name=company)
    ao.organisation = org
    network.add(org)
    network.add(ao)

    if customer_service is not None:
        customer_service.add(org)

    return ao


def create_meter(network: NetworkService, id: str = "") -> Meter:
    if not id:
        id = str(CopyableUUID())

    meter = Meter(id, name=f"companyMeterId{id}")
    meter.add_organisation_role(create_asset_owner(network, f"company{id}"))
    network.add(meter)
    return meter


def create_power_transformer_for_connecting(network: NetworkService, mrid: str = "", num_terms: int = 0, phases: PhaseCode = PhaseCode.ABCN,
                                            num_usagepoints: int = 0, num_meters: int = 0, end_args: List[Dict] = None) -> PowerTransformer:
    """
    `end_args` A list of dictionaries, each of which is passed to `create_power_transformer_end` for every terminal created. Possible kwargs are anything that
               can be passed to the `PowerTransformerEnd` constructor. Keep in mind CIM recommends the HV end is first in the list.
    """
    if not mrid:
        mrid = str(CopyableUUID())

    pt = PowerTransformer(mrid, name="test powertransformer")
    terminals = create_terminals(network, pt, num_terms, phases)

    for eargs, t in zip(end_args, terminals):
        create_power_transformer_end(network, pt, t, **eargs)

    for i in range(num_usagepoints):
        up = UsagePoint(f"{mrid}-up{i}")
        pt.add_usage_point(up)
        up.add_equipment(pt)
        for j in range(num_meters):
            meter = create_meter(network, f"{mrid}-up{i}-m{j}")
            up.add_end_device(meter)
            meter.add_usage_point(up)
        network.add(up)

    network.add(pt)
    return pt


def create_acls_for_connecting(network: NetworkService, mrid: str = "", phases: PhaseCode = PhaseCode.ABCN, length: float = 0.0,
                               plsi_mrid: str = "perLengthSequenceImepedance",
                               wi_mrid: str = "wireInfo") -> AcLineSegment:
    if not mrid:
        mrid = str(CopyableUUID())

    try:
        plsi = network.get(plsi_mrid, PerLengthSequenceImpedance)
    except KeyError:
        plsi = PerLengthSequenceImpedance(plsi_mrid)
        network.add(plsi)

    try:
        wi = network.get(wi_mrid, WireInfo)
    except KeyError:
        wi = OverheadWireInfo(wi_mrid)
        network.add(wi)

    acls = AcLineSegment(mrid, name=f"{mrid} name", per_length_sequence_impedance=plsi, asset_info=wi, length=length)
    create_terminals(network, acls, 2, phases)
    network.add(acls)
    return acls


def create_energy_consumer_for_connecting(network: NetworkService, mrid: str = "", num_terms: int = 0, phases: PhaseCode = PhaseCode.ABCN) -> EnergyConsumer:
    if not mrid:
        mrid = str(CopyableUUID())

    ec = EnergyConsumer(mrid, name=f"{mrid}-name")
    create_terminals(network, ec, num_terms, phases)
    network.add(ec)
    return ec


def create_geographical_region(network: NetworkService, mrid: str = "", name: str = "") -> GeographicalRegion:
    if not mrid:
        mrid = str(CopyableUUID())

    gr = GeographicalRegion(mrid, name=name)
    network.add(gr)
    return gr


def create_subgeographical_region(network: NetworkService, mrid: str = "", name: str = "", gr: GeographicalRegion = None) -> SubGeographicalRegion:
    if not mrid:
        mrid = str(CopyableUUID())

    sgr = SubGeographicalRegion(mrid, name=name)
    if gr is not None:
        sgr.geographical_region = gr
        gr.add_sub_geographical_region(sgr)

    network.add(sgr)
    return sgr


def create_substation(network: NetworkService, mrid: str = "", name: str = "", sgr: SubGeographicalRegion = None) -> Substation:
    if not mrid:
        mrid = str(CopyableUUID())

    sub = Substation(mrid, name=name, sub_geographical_region=sgr)
    if sgr is not None:
        sgr.add_substation(sub)

    network.add(sub)
    return sub


def create_feeder(network: NetworkService, mrid: str = "", name: str = "", sub: Substation = None, head_terminal: Terminal = None,
                  *equipment_mrids: str) -> Feeder:
    """
    `equipment_mrids` Equipment to fetch from the network and add to this feeder.
    """
    if not mrid:
        mrid = str(CopyableUUID())
    feeder = Feeder(mrid, name=name, normal_head_terminal=head_terminal, normal_energizing_substation=sub)
    sub.add_feeder(feeder)
    network.add(feeder)

    for mrid in equipment_mrids:
        ce = network.get(mrid, ConductingEquipment)
        ce.add_container(feeder)
        feeder.add_equipment(ce)

    return feeder


def create_operational_restriction(network: NetworkService, mrid: str = "", name: str = "", *equipment_mrids: str, **document_kwargs):
    if not mrid:
        mrid = str(CopyableUUID())
    restriction = OperationalRestriction(mrid, name, **document_kwargs)
    network.add(restriction)

    for mrid in equipment_mrids:
        eq = network.get(mrid, Equipment)
        restriction.add_equipment(eq)
        eq.add_restriction(restriction)

    return restriction


def add_location(network: NetworkService, psr: PowerSystemResource, *coords: float):
    """
    `coords` XY/longlats to use for the PositionPoint for this location. Must be an even number of coords.
    :return:
    """
    loc = Location()
    for i in range(0, len(coords), 2):
        loc.add_point(PositionPoint(coords[i], coords[i + 1]))
    psr.location = loc
    network.add(loc)


@fixture()
async def feeder_network():
    """
                c1       c2
    source-fcb------fsp------tx
    """
    network_service = NetworkService()

    source = create_source_for_connecting(network_service, "source", 1, PhaseCode.AB)
    fcb = create_switch_for_connecting(network_service, "fcb", 2, PhaseCode.AB)
    fsp = create_junction_for_connecting(network_service, "fsp", 2, PhaseCode.AB)
    tx = create_power_transformer_for_connecting(network_service, "tx", 2, PhaseCode.AB, end_args=[{"rated_u": 22000}, {"rated_u": 415}])

    c1 = create_acls_for_connecting(network_service, "c1", PhaseCode.AB)
    c2 = create_acls_for_connecting(network_service, "c2", PhaseCode.AB)

    sub = create_substation(network_service, "f", "f")
    create_feeder(network_service, "f001", "f001", sub, fsp.get_terminal_by_sn(2))

    add_location(network_service, source, 1.0, 1.0)
    add_location(network_service, fcb, 1.0, 1.0)
    add_location(network_service, fsp, 5.0, 1.0)
    add_location(network_service, tx, 10.0, 2.0)
    add_location(network_service, c1, 1.0, 1.0, 5.0, 1.0)
    add_location(network_service, c2, 5.0, 1.0, 10.0, 2.0)

    network_service.connect_terminals(source.get_terminal_by_sn(1), fcb.get_terminal_by_sn(1))
    network_service.connect_terminals(fcb.get_terminal_by_sn(2), c1.get_terminal_by_sn(1))
    network_service.connect_terminals(c1.get_terminal_by_sn(2), fsp.get_terminal_by_sn(1))
    network_service.connect_terminals(fsp.get_terminal_by_sn(2), c2.get_terminal_by_sn(1))
    network_service.connect_terminals(c2.get_terminal_by_sn(2), tx.get_terminal_by_sn(1))

    await SetPhases().run(network_service)
    await AssignToFeeders().run(network_service)
    return network_service


@fixture()
async def feeder_with_current():
    """
                c1       c2      c3       c4
    source-fcb------fsp------tx------sw--------tx2
                                   (open)
    """
    network_service = NetworkService()

    source = create_source_for_connecting(network_service, "source", 1, PhaseCode.AB)
    fcb = create_switch_for_connecting(network_service, "fcb", 2, PhaseCode.AB)
    fsp = create_junction_for_connecting(network_service, "fsp", 2, PhaseCode.AB)
    tx = create_power_transformer_for_connecting(network_service, "tx", 2, PhaseCode.AB, end_args=[{"rated_u": 22000}, {"rated_u": 415}])
    sw = create_switch_for_connecting(network_service, "sw", 2, PhaseCode.AB, current_phase_states=[True, True])
    tx2 = create_power_transformer_for_connecting(network_service, "tx2", 2, PhaseCode.AB, end_args=[{"rated_u": 415}, {"rated_u": 22000}])

    c1 = create_acls_for_connecting(network_service, "c1", PhaseCode.AB)
    c2 = create_acls_for_connecting(network_service, "c2", PhaseCode.AB)
    c3 = create_acls_for_connecting(network_service, "c3", PhaseCode.AB)
    c4 = create_acls_for_connecting(network_service, "c4", PhaseCode.AB)

    sub = create_substation(network_service, "f", "f")
    create_feeder(network_service, "f001", "f001", sub, fsp.get_terminal_by_sn(2))

    add_location(network_service, source, 1.0, 1.0)
    add_location(network_service, fcb, 1.0, 1.0)
    add_location(network_service, fsp, 5.0, 1.0)
    add_location(network_service, tx, 10.0, 2.0)
    add_location(network_service, sw, 15.0, 3.0)
    add_location(network_service, tx2, 20.0, 4.0)
    add_location(network_service, c1, 1.0, 1.0, 5.0, 1.0)
    add_location(network_service, c2, 5.0, 1.0, 10.0, 2.0)
    add_location(network_service, c3, 10.0, 1.0, 15.0, 3.0)
    add_location(network_service, c4, 15.0, 1.0, 20.0, 4.0)

    network_service.connect_terminals(source.get_terminal_by_sn(1), fcb.get_terminal_by_sn(1))
    network_service.connect_terminals(fcb.get_terminal_by_sn(2), c1.get_terminal_by_sn(1))
    network_service.connect_terminals(c1.get_terminal_by_sn(2), fsp.get_terminal_by_sn(1))
    network_service.connect_terminals(fsp.get_terminal_by_sn(2), c2.get_terminal_by_sn(1))
    network_service.connect_terminals(c2.get_terminal_by_sn(2), tx.get_terminal_by_sn(1))
    network_service.connect_terminals(tx.get_terminal_by_sn(2), c3.get_terminal_by_sn(1))
    network_service.connect_terminals(c3.get_terminal_by_sn(2), sw.get_terminal_by_sn(1))
    network_service.connect_terminals(sw.get_terminal_by_sn(2), c4.get_terminal_by_sn(1))
    network_service.connect_terminals(c4.get_terminal_by_sn(2), tx2.get_terminal_by_sn(1))

    await SetPhases().run(network_service)
    await AssignToFeeders().run(network_service)
    return network_service


@fixture()
def feeder_start_point_between_conductors_network():
    network_service = NetworkService()

    sub = create_substation(network_service)

    c1 = create_acls_for_connecting(network_service, "c1", PhaseCode.A)
    fsp = create_junction_for_connecting(network_service, "fsp", 2)
    c2 = create_acls_for_connecting(network_service, "c2", PhaseCode.A)

    network_service.connect_terminals(c1.get_terminal_by_sn(2), fsp.get_terminal_by_sn(1))
    network_service.connect_terminals(c2.get_terminal_by_sn(1), fsp.get_terminal_by_sn(2))

    create_feeder(network_service, "f", "f", sub, fsp.get_terminal_by_sn(2))
    return network_service


@fixture()
def operational_restriction_with_equipment():
    network_service = NetworkService()
    source = create_source_for_connecting(network_service, "source", 1, PhaseCode.AB)
    fcb = create_switch_for_connecting(network_service, "fcb", 2, PhaseCode.AB)
    fsp = create_junction_for_connecting(network_service, "fsp", 2, PhaseCode.AB)
    c1 = create_acls_for_connecting(network_service, "c1", PhaseCode.AB)
    c2 = create_acls_for_connecting(network_service, "c2", PhaseCode.AB)
    tx = create_power_transformer_for_connecting(network_service, "tx", 2, PhaseCode.AB, end_args=[{"rated_u": 22000}, {"rated_u": 415}])
    create_operational_restriction(network_service, "or1", "test_or1", "fsp", "c2", "tx", title="test title")

    network_service.connect_terminals(source.get_terminal_by_sn(1), fcb.get_terminal_by_sn(1))
    network_service.connect_terminals(fcb.get_terminal_by_sn(2), c1.get_terminal_by_sn(1))
    network_service.connect_terminals(c1.get_terminal_by_sn(2), fsp.get_terminal_by_sn(1))
    network_service.connect_terminals(c1.get_terminal_by_sn(2), fsp.get_terminal_by_sn(1))
    network_service.connect_terminals(fsp.get_terminal_by_sn(2), c2.get_terminal_by_sn(1))
    network_service.connect_terminals(c2.get_terminal_by_sn(2), tx.get_terminal_by_sn(1))

    return network_service


@fixture()
def single_connectivitynode_network():
    network_service = NetworkService()
    create_connectivitynode_with_terminals(network_service, "cn1", PhaseCode.A, PhaseCode.B, PhaseCode.C)
    return network_service


@fixture()
def feeder_start_point_to_open_point_network(request):
    normally_open = request.param[0]
    currently_open = request.param[1]
    network_service = NetworkService()
    sub = create_substation(network_service)
    fsp = create_junction_for_connecting(network_service, "fsp", 1)
    c1 = create_acls_for_connecting(network_service, "c1", PhaseCode.A)
    op = create_switch_for_connecting(network_service, "op", 2, PhaseCode.A)
    c2 = create_acls_for_connecting(network_service, "c2", PhaseCode.A)

    op.set_normally_open(normally_open)
    op.set_open(currently_open)

    network_service.connect_terminals(c1.get_terminal_by_sn(1), fsp.get_terminal_by_sn(1))
    network_service.connect_terminals(c1.get_terminal_by_sn(2), op.get_terminal_by_sn(1))
    network_service.connect_terminals(c2.get_terminal_by_sn(1), op.get_terminal_by_sn(2))

    create_feeder(network_service, "f", "f", sub, fsp.get_terminal_by_sn(1))
    return network_service


@fixture()
def basic_network_hierarchy():
    service = NetworkService()
    feeder = Feeder(name="basic-feeder")
    create_switch_for_connecting(service, "test_breaker", 2, PhaseCode.ABCN, normal_phase_states=[True] * 4, current_phase_states=[True] * 4)


@fixture()
def network_service():
    # An empty network.
    yield NetworkService()
