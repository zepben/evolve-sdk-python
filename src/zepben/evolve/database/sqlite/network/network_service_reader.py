#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import BaseServiceReader, TableCableInfo, TableOverheadWireInfo, TablePowerTransformerInfo, TableTransformerTankInfo, TableNoLoadTests, \
    TableOpenCircuitTests, TableShortCircuitTests, TableShuntCompensatorInfo, TableTransformerEndInfo, TableLocations, TableOrganisations, TableAssetOwners, \
    TablePoles, TableStreetlights, TableMeters, TableUsagePoints, TableOperationalRestrictions, TableBaseVoltages, TableConnectivityNodes, \
    TableGeographicalRegions, TableSubGeographicalRegions, TableSubstations, TableSites, TableEquivalentBranches, TableBatteryUnits, TablePhotoVoltaicUnit, \
    TablePowerElectronicsWindUnit, TableTerminals, TableFaultIndicators, TableFeeders, TableLoops, TableCircuits, TablePositionPoints, \
    TableLocationStreetAddresses, TableControls, TableRemoteControls, TableRemoteSources, TableAnalogs, TableAccumulators, TableDiscretes, TableLvFeeders, \
    TableCurrentTransformers, TablePotentialTransformers, TableCurrentRelays, TableSwitchInfo, TableEvChargingUnits, TableProtectionRelayFunctionThresholds, \
    TableDistanceRelays, TableVoltageRelays, TableProtectionRelayFunctionTimeLimits, TableProtectionRelaySystems, TableProtectionRelaySchemes
from zepben.evolve.database.sqlite.readers.network_cim_reader import NetworkCimReader
from zepben.evolve.database.sqlite.tables.associations.table_asset_organisation_roles_assets import TableAssetOrganisationRolesAssets
from zepben.evolve.database.sqlite.tables.associations.table_circuits_substations import TableCircuitsSubstations
from zepben.evolve.database.sqlite.tables.associations.table_circuits_terminals import TableCircuitsTerminals
from zepben.evolve.database.sqlite.tables.associations.table_equipment_equipment_containers import TableEquipmentEquipmentContainers
from zepben.evolve.database.sqlite.tables.associations.table_equipment_operational_restrictions import TableEquipmentOperationalRestrictions
from zepben.evolve.database.sqlite.tables.associations.table_equipment_usage_points import TableEquipmentUsagePoints
from zepben.evolve.database.sqlite.tables.associations.table_loops_substations import TableLoopsSubstations
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_protected_switches import TableProtectionRelayFunctionsProtectedSwitches
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_sensors import TableProtectionRelayFunctionsSensors
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_schemes_protection_relay_functions import \
    TableProtectionRelaySchemesProtectionRelayFunctions
from zepben.evolve.database.sqlite.tables.associations.table_usage_points_end_devices import TableUsagePointsEndDevices
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_current_transformer_info import TableCurrentTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_potential_transformer_info import TablePotentialTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_reclose_delays import TableRecloseDelays
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_relay_info import TableRelayInfo
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ac_line_segments import TableAcLineSegments
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_breakers import TableBreakers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_busbar_sections import TableBusbarSections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_disconnectors import TableDisconnectors
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumer_phases import TableEnergyConsumerPhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumers import TableEnergyConsumers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_source_phases import TableEnergySourcePhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_sources import TableEnergySources
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_fuses import TableFuses
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ground_disconnectors import TableGroundDisconnectors
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_grounds import TableGrounds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_jumpers import TableJumpers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_junctions import TableJunctions
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_linear_shunt_compensators import TableLinearShuntCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_load_break_switches import TableLoadBreakSwitches
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_sequence_impedances import TablePerLengthSequenceImpedances
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connection_phases import TablePowerElectronicsConnectionPhases
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connections import TablePowerElectronicsConnections
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_end_ratings import TablePowerTransformerEndRatings
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_ends import TablePowerTransformerEnds
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformers import TablePowerTransformers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ratio_tap_changers import TableRatioTapChangers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reclosers import TableReclosers
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_series_compensators import TableSeriesCompensators
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changer_controls import TableTapChangerControls
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_star_impedances import TableTransformerStarImpedances

__all__ = ["NetworkServiceReader"]


class NetworkServiceReader(BaseServiceReader):
    """
    Class for reading a `NetworkService` from the database.
    """

    def load(self, reader: NetworkCimReader) -> bool:
        status = self.load_name_types(reader)

        status = status and self._load_each(TableCableInfo, "cable info", reader.load_cable_info)
        status = status and self._load_each(TableOverheadWireInfo, "overhead wire info", reader.load_overhead_wire_info)
        status = status and self._load_each(TablePowerTransformerInfo, "power transformer info", reader.load_power_transformer_info)
        status = status and self._load_each(TableTransformerTankInfo, "transformer tank info", reader.load_transformer_tank_info)
        status = status and self._load_each(TableNoLoadTests, "no load tests", reader.load_no_load_test)
        status = status and self._load_each(TableOpenCircuitTests, "open circuit tests", reader.load_open_circuit_test)
        status = status and self._load_each(TableShortCircuitTests, "short circuit tests", reader.load_short_circuit_test)
        status = status and self._load_each(TableShuntCompensatorInfo, "shunt compensator info", reader.load_shunt_compensator_info)
        status = status and self._load_each(TableSwitchInfo, "switch info", reader.load_switch_info)
        status = status and self._load_each(TableTransformerEndInfo, "transformer end info", reader.load_transformer_end_info)
        status = status and self._load_each(TableCurrentTransformerInfo, "current transformer info", reader.load_current_transformer_info)
        status = status and self._load_each(TablePotentialTransformerInfo, "potential transformer info", reader.load_potential_transformer_info)
        status = status and self._load_each(TableRelayInfo, "relay info", reader.load_relay_info)
        status = status and self._load_each(TableRecloseDelays, "reclose delays", reader.load_reclose_delays)
        status = status and self._load_each(TableLocations, "locations", reader.load_location)
        status = status and self._load_each(TableOrganisations, "organisations", reader.load_organisation)
        status = status and self._load_each(TableAssetOwners, "asset owners", reader.load_asset_owner)
        status = status and self._load_each(TablePoles, "poles", reader.load_pole)
        status = status and self._load_each(TableStreetlights, "streetlights", reader.load_streetlight)
        status = status and self._load_each(TableMeters, "meters", reader.load_meter)
        status = status and self._load_each(TableUsagePoints, "usage points", reader.load_usage_point)
        status = status and self._load_each(TableOperationalRestrictions, "operational restrictions", reader.load_operational_restriction)
        status = status and self._load_each(TableBaseVoltages, "base voltages", reader.load_base_voltage)
        status = status and self._load_each(TableConnectivityNodes, "connectivity nodes", reader.load_connectivity_node)
        status = status and self._load_each(TableGeographicalRegions, "geographical regions", reader.load_geographical_region)
        status = status and self._load_each(TableSubGeographicalRegions, "sub-geographical regions", reader.load_sub_geographical_region)
        status = status and self._load_each(TableSubstations, "substations", reader.load_substation)
        status = status and self._load_each(TableSites, "sites", reader.load_site)
        status = status and self._load_each(TablePerLengthSequenceImpedances, "per length sequence impedances", reader.load_per_length_sequence_impedance)
        status = status and self._load_each(TableEquivalentBranches, "equivalent branches", reader.load_equivalent_branch)
        status = status and self._load_each(TableAcLineSegments, "AC line segments", reader.load_ac_line_segment)
        status = status and self._load_each(TableBreakers, "breakers", reader.load_breaker)
        status = status and self._load_each(TableLoadBreakSwitches, "load break switches", reader.load_load_break_switch)
        status = status and self._load_each(TableBusbarSections, "busbar sections", reader.load_busbar_section)
        status = status and self._load_each(TableCurrentRelays, "current relays", reader.load_current_relay)
        status = status and self._load_each(TableDistanceRelays, "distance relays", reader.load_distance_relay)
        status = status and self._load_each(TableVoltageRelays, "voltage relays", reader.load_voltage_relay)
        status = status and self._load_each(TableProtectionRelayFunctionThresholds, "protection relay function thresholds",
                                            reader.load_protection_relay_function_thresholds)
        status = status and self._load_each(TableProtectionRelayFunctionTimeLimits, "protection relay function time limits",
                                            reader.load_protection_relay_function_time_limits)
        status = status and self._load_each(TableProtectionRelaySystems, "protection relay system", reader.load_protection_relay_system)
        status = status and self._load_each(TableProtectionRelaySchemes, "protection relay scheme", reader.load_protection_relay_scheme)
        status = status and self._load_each(TableDisconnectors, "disconnectors", reader.load_disconnector)
        status = status and self._load_each(TableEnergyConsumers, "energy consumers", reader.load_energy_consumer)
        status = status and self._load_each(TableEnergyConsumerPhases, "energy consumer phases", reader.load_energy_consumer_phase)
        status = status and self._load_each(TableEnergySources, "energy sources", reader.load_energy_source)
        status = status and self._load_each(TableEnergySourcePhases, "energy source phases", reader.load_energy_source_phase)
        status = status and self._load_each(TableFuses, "fuses", reader.load_fuse)
        status = status and self._load_each(TableJumpers, "jumpers", reader.load_jumper)
        status = status and self._load_each(TableJunctions, "junctions", reader.load_junction)
        status = status and self._load_each(TableGrounds, "grounds", reader.load_ground)
        status = status and self._load_each(TableGroundDisconnectors, "ground disconnectors", reader.load_ground_disconnector)
        status = status and self._load_each(TableSeriesCompensators, "series compensators", reader.load_series_compensator)
        status = status and self._load_each(TableLinearShuntCompensators, "linear shunt compensators", reader.load_linear_shunt_compensator)
        status = status and self._load_each(TablePowerTransformers, "power transformers", reader.load_power_transformer)
        status = status and self._load_each(TableReclosers, "reclosers", reader.load_recloser)
        status = status and self._load_each(TablePowerElectronicsConnections, "power electronics connection", reader.load_power_electronics_connection)
        status = status and self._load_each(TableTerminals, "terminals", reader.load_terminal)
        status = status and self._load_each(TableTapChangerControls, "tap changer controls", reader.load_tap_changer_control)
        status = status and self._load_each(TablePowerElectronicsConnectionPhases, "power electronics connection phases",
                                            reader.load_power_electronics_connection_phase)
        status = status and self._load_each(TableBatteryUnits, "battery unit", reader.load_battery_unit)
        status = status and self._load_each(TablePhotoVoltaicUnit, "photo voltaic unit", reader.load_photo_voltaic_unit)
        status = status and self._load_each(TablePowerElectronicsWindUnit, "power electronics wind unit", reader.load_power_electronics_wind_unit)
        status = status and self._load_each(TableEvChargingUnits, "ev charging units", reader.load_ev_charging_unit)
        status = status and self._load_each(TableTransformerStarImpedances, "transformer star impedance", reader.load_transformer_star_impedance)
        status = status and self._load_each(TablePowerTransformerEnds, "power transformer ends", reader.load_power_transformer_end)
        status = status and self._load_each(TablePowerTransformerEndRatings, "power transformer end ratings", reader.load_power_transformer_end_ratings)
        status = status and self._load_each(TableRatioTapChangers, "ratio tap changers", reader.load_ratio_tap_changer)
        status = status and self._load_each(TableCurrentTransformers, "ratio tap changers", reader.load_current_transformer)
        status = status and self._load_each(TableFaultIndicators, "fault indicators", reader.load_fault_indicator)
        status = status and self._load_each(TablePotentialTransformers, "ratio tap changers", reader.load_potential_transformer)
        status = status and self._load_each(TableFeeders, "feeders", reader.load_feeder)
        status = status and self._load_each(TableLoops, "loops", reader.load_loop)
        status = status and self._load_each(TableCircuits, "circuits", reader.load_circuit)
        status = status and self._load_each(TableLvFeeders, "lv feeders", reader.load_lv_feeder)
        status = status and self._load_each(TablePositionPoints, "position points", reader.load_position_point)
        status = status and self._load_each(TableLocationStreetAddresses, "location street addresses", reader.load_location_street_address)
        status = status and self._load_each(
            TableAssetOrganisationRolesAssets,
            "asset organisation role to asset associations",
            reader.load_asset_organisation_role_asset
        )
        status = status and self._load_each(TableUsagePointsEndDevices, "usage point to end device associations", reader.load_usage_point_end_device)
        status = status and self._load_each(TableEquipmentUsagePoints, "equipment to usage point associations", reader.load_equipment_usage_point)
        status = status and self._load_each(
            TableEquipmentOperationalRestrictions,
            "equipment to operational restriction associations",
            reader.load_equipment_operational_restriction
        )
        status = status and self._load_each(
            TableEquipmentEquipmentContainers,
            "equipment to equipment container associations",
            reader.load_equipment_equipment_container
        )
        status = status and self._load_each(TableCircuitsSubstations, "circuit to substation associations", reader.load_circuit_substation)
        status = status and self._load_each(TableCircuitsTerminals, "circuit to terminal associations", reader.load_circuit_terminal)
        status = status and self._load_each(TableLoopsSubstations, "loop to substation associations", reader.load_loop_substation)
        status = status and self._load_each(
            TableProtectionRelayFunctionsProtectedSwitches,
            "protection equipment to protected switch associations",
            reader.load_protection_equipment_protected_switch
        )
        status = status and self._load_each(
            TableProtectionRelayFunctionsSensors,
            "protection equipment to sensor associations",
            reader.load_protection_relay_functions_sensors
        )
        status = status and self._load_each(
            TableProtectionRelaySchemesProtectionRelayFunctions,
            "protection relay scheme to protection relay function associations",
            reader.load_protection_relay_schemes_protection_relay_functions
        )
        status = status and self._load_each(TableControls, "controls", reader.load_control)
        status = status and self._load_each(TableRemoteControls, "remote controls", reader.load_remote_control)
        status = status and self._load_each(TableRemoteSources, "remote sources", reader.load_remote_source)
        status = status and self._load_each(TableAnalogs, "analogs", reader.load_analog)
        status = status and self._load_each(TableAccumulators, "accumulators", reader.load_accumulator)
        status = status and self._load_each(TableDiscretes, "discretes", reader.load_discrete)

        status = status and self.load_names(reader)

        return status
