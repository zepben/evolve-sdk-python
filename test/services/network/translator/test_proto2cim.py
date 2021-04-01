#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.pb_creators import terminal, connectivitynode, basevoltage, feeder, substation, geographicalregion, analog, \
    discrete, accumulator, remotecontrol, busbarsection, junction, energysource, energyconsumer, aclinesegment, disconnector, \
    fuse, jumper, breaker, loadbreakswitch, powertransformer, powertransformerend, linearshuntcompensator, ratiotapchanger, \
    remotesource, perlengthsequenceimpedance, batteryunit
from zepben.evolve import NetworkService, WindingConnection, VectorGroup, phasecode_by_id, unit_symbol_from_id, PhaseShuntConnectionKind, Terminal, \
    ConnectivityNode, \
    BaseVoltage, Feeder, Substation, GeographicalRegion, Analog, Discrete, Accumulator, RemoteControl, BusbarSection, Junction, \
    EnergySource, EnergyConsumer, AcLineSegment, Disconnector, Fuse, Jumper, Breaker, LoadBreakSwitch, PowerTransformer, \
    PowerTransformerEnd, LinearShuntCompensator, RatioTapChanger, RemoteSource, PerLengthSequenceImpedance, BatteryUnit, \
    BatteryStateKind


# Core
def verify_identifiedobject_to_cim(pb, cim):
    ## Top of inheritance hierarchy
    assert cim.mrid == pb.mRID
    assert cim.name == pb.name
    assert cim.description == pb.description


def verify_acdcterminal_to_cim(pb, cim):
    verify_identifiedobject_to_cim(pb.io, cim)


def verify_assetinfo_to_cim(pb, cim):
    verify_identifiedobject_to_cim(pb.io, cim)


def verify_asset_to_cim(pb, cim):
    verify_assetinfo_to_cim(pb.ai, cim)


def verify_assetcontainer_to_cim(pb, cim):
    verify_asset_to_cim(pb.at, cim)


def verify_enddevice_to_cim(pb, cim):
    verify_assetcontainer_to_cim(pb.ac, cim)


@given(te=terminal())
def test_terminal_to_cim(te):
    cim = te.to_cim(NetworkService())
    assert cim.mrid == te.mrid()
    assert isinstance(cim, Terminal)
    assert cim.phases == phasecode_by_id(te.phases)
    verify_acdcterminal_to_cim(te.ad, cim)


@given(cnn=connectivitynode())
def test_connectivitynode_to_cim(cnn):
    cim = cnn.to_cim(NetworkService())
    assert cim.mrid == cnn.mrid()
    assert isinstance(cim, ConnectivityNode)
    verify_identifiedobject_to_cim(cnn.io, cim)


@given(bv=basevoltage())
def test_basevoltage_to_cim(bv):
    cim = bv.to_cim(NetworkService())
    assert cim.mrid == bv.mrid()
    assert isinstance(cim, BaseVoltage)
    assert cim.nominal_voltage == bv.nominalVoltage
    verify_identifiedobject_to_cim(bv.io, cim)


def verify_connectivitynodecontainer_to_cim(pb, cim):
    verify_powersystemsresource_to_cim(pb.psr, cim)


def verify_equipmentcontainer_to_cim(pb, cim):
    verify_connectivitynodecontainer_to_cim(pb.cnc, cim)


@given(fe=feeder())
def test_feeder_to_cim(fe):
    cim = fe.to_cim(NetworkService())
    assert cim.mrid == fe.mrid()
    assert isinstance(cim, Feeder)
    verify_equipmentcontainer_to_cim(fe.ec, cim)


@given(sub=substation())
def test_substation_to_cim(sub):
    cim = sub.to_cim(NetworkService())
    assert cim.mrid == sub.mrid()
    assert isinstance(cim, Substation)
    verify_equipmentcontainer_to_cim(sub.ec, cim)


@given(ger=geographicalregion())
def test_geographicalregion_to_cim(ger):
    cim = ger.to_cim(NetworkService())
    assert cim.mrid == ger.mrid()
    assert isinstance(cim, GeographicalRegion)
    verify_identifiedobject_to_cim(ger.io, cim)


# Meas
def verify_measurement_to_cim(pb, cim):
    assert cim.phases == phasecode_by_id(pb.phases)
    assert cim.unit_symbol == unit_symbol_from_id(pb.unitSymbol)


@given(ana=analog())
def test_analog_to_cim(ana):
    cim = ana.to_cim(NetworkService())
    assert cim.mrid == ana.mrid()
    assert isinstance(cim, Analog)
    assert cim.positive_flow_in == ana.positiveFlowIn
    verify_measurement_to_cim(ana.measurement, cim)


@given(dis=discrete())
def test_discrete_to_cim(dis):
    cim = dis.to_cim(NetworkService())
    assert cim.mrid == dis.mrid()
    assert isinstance(cim, Discrete)
    verify_measurement_to_cim(dis.measurement, cim)


@given(acc=accumulator())
def test_accumulator_to_cim(acc):
    cim = acc.to_cim(NetworkService())
    assert cim.mrid == acc.mrid()
    assert isinstance(cim, Accumulator)
    verify_measurement_to_cim(acc.measurement, cim)


# SCADA
def verify_remotepoint_to_cim(pb, cim):
    verify_identifiedobject_to_cim(pb.io, cim)


@given(rs=remotesource())
def test_remotesource_to_cim(rs):
    cim = rs.to_cim(NetworkService())
    assert cim.mrid == rs.mrid()
    assert isinstance(cim, RemoteSource)
    verify_remotepoint_to_cim(rs.rp, cim)


@given(rc=remotecontrol())
def test_remotecontrol_to_cim(rc):
    cim = rc.to_cim(NetworkService())
    assert cim.mrid == rc.mrid()
    assert isinstance(cim, RemoteControl)
    verify_remotepoint_to_cim(rc.rp, cim)


# Wires
def verify_powersystemsresource_to_cim(pb, cim):
    verify_identifiedobject_to_cim(pb.io, cim)


def verify_equipment_to_cim(pb, cim):
    assert cim.in_service == pb.inService
    assert cim.normally_in_service == pb.normallyInService
    verify_powersystemsresource_to_cim(pb.psr, cim)


def verify_conductingequipment_to_cim(pb, cim):
    verify_equipment_to_cim(pb.eq, cim)


def verify_conductor_to_cim(pb, cim):
    assert cim.length == pb.length
    verify_conductingequipment_to_cim(pb.ce, cim)


def verify_connector_to_cim(pb, cim):
    verify_conductingequipment_to_cim(pb.ce, cim)


@given(bbs=busbarsection())
def test_busbarsection_to_cim(bbs):
    cim = bbs.to_cim(NetworkService())
    assert cim.mrid == bbs.mrid()
    assert isinstance(cim, BusbarSection)
    verify_connector_to_cim(bbs.cn, cim)


def verify_perlengthlineparameter_to_pb(pb, cim):
    verify_identifiedobject_to_cim(pb.io, cim)


def verify_perlengthimpedance_to_pb(pb, cim):
    verify_perlengthlineparameter_to_pb(pb.lp, cim)


@given(plsi=perlengthsequenceimpedance())
def test_perlengthsequenceimpedance_to_cim(plsi):
    cim = plsi.to_cim(NetworkService())
    assert cim.mrid == plsi.mrid()
    assert isinstance(cim, PerLengthSequenceImpedance)
    assert cim.b0ch == plsi.b0ch
    assert cim.bch == plsi.bch
    assert cim.g0ch == plsi.g0ch
    assert cim.gch == plsi.gch
    assert cim.r == plsi.r
    assert cim.r0 == plsi.r0
    assert cim.x == plsi.x
    assert cim.x0 == plsi.x0
    verify_perlengthimpedance_to_pb(plsi.pli, cim)


def verify_switch_to_cim(pb, cim):
    if not cim.is_open():
        assert not pb.open
    if not cim.is_normally_open():
        assert not pb.normalOpen

    if cim.is_open():
        assert pb.open
    if cim.is_normally_open():
        assert pb.normalOpen

    verify_conductingequipment_to_cim(pb.ce, cim)


def verify_protectedswitch_to_cim(pb, cim):
    verify_switch_to_cim(pb.sw, cim)


@given(dis=disconnector())
def test_disconnector_to_cim(dis):
    cim = dis.to_cim(NetworkService())
    assert cim.mrid == dis.mrid()
    assert isinstance(cim, Disconnector)
    verify_switch_to_cim(dis.sw, cim)


@given(fus=fuse())
def test_fuse_to_cim(fus):
    cim = fus.to_cim(NetworkService())
    assert cim.mrid == fus.mrid()
    assert isinstance(cim, Fuse)
    verify_switch_to_cim(fus.sw, cim)


@given(jum=jumper())
def test_jumper_to_cim(jum):
    cim = jum.to_cim(NetworkService())
    assert cim.mrid == jum.mrid()
    assert isinstance(cim, Jumper)
    verify_switch_to_cim(jum.sw, cim)


@given(brk=breaker())
def test_breaker_to_cim(brk):
    cim = brk.to_cim(NetworkService())
    assert cim.mrid == brk.mrid()
    assert isinstance(cim, Breaker)
    verify_protectedswitch_to_cim(brk.sw, cim)


@given(lbs=loadbreakswitch())
def test_loadbreakswitch_to_cim(lbs):
    cim = lbs.to_cim(NetworkService())
    assert cim.mrid == lbs.mrid()
    assert isinstance(cim, LoadBreakSwitch)
    verify_protectedswitch_to_cim(lbs.ps, cim)


@given(jnc=junction())
def test_junction_to_cim(jnc):
    cim = jnc.to_cim(NetworkService())
    assert cim.mrid == jnc.mrid()
    assert isinstance(cim, Junction)
    verify_connector_to_cim(jnc.cn, cim)


@given(acl=aclinesegment())
def test_aclinesegment_to_cim(acl):
    cim = acl.to_cim(NetworkService())
    assert cim.mrid == acl.mrid()
    assert isinstance(cim, AcLineSegment)
    verify_conductor_to_cim(acl.cd, cim)


@given(ens=energysource())
def test_energysource_to_cim(ens):
    cim = ens.to_cim(NetworkService())
    assert cim.mrid == ens.mrid()
    assert isinstance(cim, EnergySource)
    assert cim.active_power == ens.activePower
    assert cim.r == ens.r
    assert cim.x == ens.x
    assert cim.reactive_power == ens.reactivePower
    assert cim.voltage_angle == ens.voltageAngle
    assert cim.voltage_magnitude == ens.voltageMagnitude
    assert cim.p_max == ens.pMax
    assert cim.p_min == ens.pMin
    assert cim.r0 == ens.r0
    assert cim.rn == ens.rn
    assert cim.x0 == ens.x0
    assert cim.xn == ens.xn
    verify_energyconnection_to_cim(ens.ec, cim)


@given(enc=energyconsumer())
def test_energyconsumer_to_cim(enc):
    cim = enc.to_cim(NetworkService())
    assert cim.mrid == enc.mrid()
    assert isinstance(cim, EnergyConsumer)
    assert cim.customer_count == enc.customerCount
    assert cim.grounded == enc.grounded
    assert cim.phase_connection == PhaseShuntConnectionKind(enc.phaseConnection)
    assert cim.p == enc.p
    assert cim.q == enc.q
    assert cim.p_fixed == enc.pFixed
    assert cim.q_fixed == enc.qFixed
    verify_energyconnection_to_cim(enc.ec, cim)


@given(lsc=linearshuntcompensator())
def test_linearshuntcompensator_to_cim(lsc):
    cim = lsc.to_cim(NetworkService())
    assert cim.mrid == lsc.mrid()
    assert isinstance(cim, LinearShuntCompensator)
    assert cim.b0_per_section == lsc.b0PerSection
    assert cim.b_per_section == lsc.bPerSection
    assert cim.g0_per_section == lsc.g0PerSection
    assert cim.g_per_section == lsc.gPerSection
    verify_shuntcompensator_to_cim(lsc.sc, cim)


def verify_energyconnection_to_cim(pb, cim):
    verify_conductingequipment_to_cim(pb.ce, cim)


def verify_regulatingcondeq_to_cim(pb, cim):
    assert cim.control_enabled == pb.controlEnabled
    verify_energyconnection_to_cim(pb.ec, cim)


def verify_shuntcompensator_to_cim(pb, cim):
    assert cim.grounded == pb.grounded
    assert cim.nom_u == pb.nomU
    assert cim.phase_connection == PhaseShuntConnectionKind(pb.phaseConnection)
    assert cim.sections == pb.sections
    verify_regulatingcondeq_to_cim(pb.rce, cim)


def verify_transformerend_to_cim(pb, cim):
    assert cim.end_number == pb.endNumber
    assert cim.grounded == pb.grounded
    assert cim.r_ground == pb.rGround
    assert cim.x_ground == pb.xGround
    verify_identifiedobject_to_cim(pb.io, cim)


@given(pwt=powertransformer())
def test_powertransformer_to_cim(pwt):
    cim = pwt.to_cim(NetworkService())
    assert cim.mrid == pwt.mrid()
    assert isinstance(cim, PowerTransformer)
    assert cim.vector_group == VectorGroup(pwt.vectorGroup)
    assert cim.transformer_utilisation == pwt.transformerUtilisation
    verify_conductingequipment_to_cim(pwt.ce, cim)


@given(pte=powertransformerend())
def test_powertransformerend_to_cim(pte):
    cim = pte.to_cim(NetworkService())
    assert cim.mrid == pte.mrid()
    assert isinstance(cim, PowerTransformerEnd)
    assert cim.b == pte.b
    assert cim.b0 == pte.b0
    assert cim.connection_kind == WindingConnection(pte.connectionKind)
    assert cim.g == pte.g
    assert cim.g0 == pte.g0
    assert cim.phase_angle_clock == pte.phaseAngleClock
    assert cim.r == pte.r
    assert cim.r0 == pte.r0
    assert cim.rated_s == pte.ratedS
    assert cim.rated_u == pte.ratedU
    assert cim.x == pte.x
    assert cim.x0 == pte.x0
    verify_transformerend_to_cim(pte.te, cim)


def verify_tapchanger_to_cim(pb, cim):
    assert cim.control_enabled == pb.controlEnabled
    assert cim.high_step == pb.highStep
    assert cim.low_step == pb.lowStep
    assert cim.neutral_step == pb.neutralStep
    assert cim.neutral_u == pb.neutralU
    assert cim.normal_step == pb.normalStep
    assert cim.step == pb.step
    verify_powersystemsresource_to_cim(pb.psr, cim)


@given(rtc=ratiotapchanger())
def test_ratiotapchanger_to_cim(rtc):
    cim = rtc.to_cim(NetworkService())
    assert cim.mrid == rtc.mrid()
    assert isinstance(cim, RatioTapChanger)
    assert cim.step_voltage_increment == rtc.stepVoltageIncrement
    verify_tapchanger_to_cim(rtc.tc, cim)


# Generation
def verify_powerelectronicsunit_to_cim(pb, cim):
    assert cim.max_p == pb. maxP
    assert cim.min_p == pb.minP
    verify_equipment_to_cim(pb.eq, cim)


@given(bu=batteryunit())
def test_batteryunit_to_cim(bu):
    cim = bu.to_cim(NetworkService())
    assert cim.mrid == bu.mrid()
    assert isinstance(cim, BatteryUnit)
    assert cim.battery_state == BatteryStateKind(bu.batteryState)
    assert cim.rated_e == bu.ratedE
    assert cim.stored_e == bu.storedE
    verify_powerelectronicsunit_to_cim(bu.peu, cim)
