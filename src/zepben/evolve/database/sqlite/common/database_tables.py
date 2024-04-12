#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Dict, TypeVar, Type

from dataclassy import dataclass
from zepben.evolve.database.sqlite.prepared_statement import PreparedStatement

from zepben.evolve.database.sqlite.tables.exceptions import MissingTableConfigException
from zepben.evolve.database.sqlite.tables.sqlite_table import *
from zepben.evolve.database.sqlite.tables.table_metadata_data_sources import *
from zepben.evolve.database.sqlite.tables.table_version import *
from zepben.evolve.database.sqlite.tables.associations.loop_substation_relationship import *
from zepben.evolve.database.sqlite.tables.associations.table_asset_organisation_roles_assets import *
from zepben.evolve.database.sqlite.tables.associations.table_circuits_substations import *
from zepben.evolve.database.sqlite.tables.associations.table_circuits_terminals import *
from zepben.evolve.database.sqlite.tables.associations.table_customer_agreements_pricing_structures import *
from zepben.evolve.database.sqlite.tables.associations.table_equipment_equipment_containers import *
from zepben.evolve.database.sqlite.tables.associations.table_equipment_operational_restrictions import *
from zepben.evolve.database.sqlite.tables.associations.table_equipment_usage_points import *
from zepben.evolve.database.sqlite.tables.associations.table_loops_substations import *
from zepben.evolve.database.sqlite.tables.associations.table_pricing_structures_tariffs import *
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_protected_switches import *
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_functions_sensors import *
from zepben.evolve.database.sqlite.tables.associations.table_protection_relay_schemes_protection_relay_functions import *
from zepben.evolve.database.sqlite.tables.associations.table_usage_points_end_devices import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_cable_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_no_load_tests import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_open_circuit_tests import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_overhead_wire_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_power_transformer_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_short_circuit_tests import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_shunt_compensator_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_switch_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_end_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_tank_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_test import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_wire_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_containers import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_organisation_roles import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_owners import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_assets import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_poles import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_streetlights import *
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_structures import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_agreements import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_documents import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_address_field import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_addresses import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_locations import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisation_roles import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisations import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_position_points import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_street_addresses import *
from zepben.evolve.database.sqlite.tables.iec61968.common.table_town_details import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customer_agreements import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_customers import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_pricing_structures import *
from zepben.evolve.database.sqlite.tables.iec61968.customers.table_tariffs import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_current_transformer_info import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_potential_transformer_info import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_reclose_delays import *
from zepben.evolve.database.sqlite.tables.iec61968.infiec61968.infassetinfo.table_relay_info import *
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_end_devices import *
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_meters import *
from zepben.evolve.database.sqlite.tables.iec61968.metering.table_usage_points import *
from zepben.evolve.database.sqlite.tables.iec61968.operations.table_operational_restrictions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_auxiliary_equipment import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_current_transformers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_fault_indicators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_potential_transformers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment.table_sensors import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_ac_dc_terminals import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_base_voltages import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_conducting_equipment import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_connectivity_node_containers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_connectivity_nodes import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_equipment_containers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_feeders import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_geographical_regions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_name_types import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_names import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_power_system_resources import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sites import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_sub_geographical_regions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_substations import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_terminals import *
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_object_points import *
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagram_objects import *
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout.table_diagrams import *
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalents.table_equivalent_branches import *
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalents.table_equivalent_equipment import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_accumulators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_analogs import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_controls import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_discretes import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_io_points import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas.table_measurements import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_current_relays import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_distance_relays import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_thresholds import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_function_time_limits import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_functions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_schemes import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_protection_relay_systems import *
from zepben.evolve.database.sqlite.tables.iec61970.base.protection.table_voltage_relays import *
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_controls import *
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_points import *
from zepben.evolve.database.sqlite.tables.iec61970.base.scada.table_remote_sources import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_battery_units import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_photo_voltaic_unit import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_power_electronics_units import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production.table_power_electronics_wind_unit import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ac_line_segments import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_breakers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_busbar_sections import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_conductors import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_connectors import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_disconnectors import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_connections import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumer_phases import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_consumers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_source_phases import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_energy_sources import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_fuses import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ground_disconnectors import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_grounds import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_jumpers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_junctions import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_linear_shunt_compensators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_lines import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_load_break_switches import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_impedances import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_line_parameters import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_sequence_impedances import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connection_phases import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_electronics_connections import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_end_ratings import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformer_ends import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_power_transformers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_protected_switches import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_ratio_tap_changers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_reclosers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_cond_eq import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_regulating_controls import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_series_compensators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_shunt_compensators import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_switches import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changer_controls import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_tap_changers import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_ends import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_transformer_star_impedances import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_circuits import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_loops import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.feeder.table_lv_feeders import *
from zepben.evolve.database.sqlite.tables.iec61970.infiec61970.wires.generation.production.table_ev_charging_units import *

__all__ = ["DatabaseTables"]

from zepben.evolve.database.sqlite.tables.table_metadata_data_sources import TableMetadataDataSources
from zepben.evolve.database.sqlite.tables.table_version import TableVersion

T = TypeVar("T", bound=SqliteTable)


def _create_tables() -> Dict[Type[T], T]:
    return {
        TableAcLineSegments: TableAcLineSegments(),
        TableAccumulators: TableAccumulators(),
        TableAnalogs: TableAnalogs(),
        TableAssetOrganisationRolesAssets: TableAssetOrganisationRolesAssets(),
        TableAssetOwners: TableAssetOwners(),
        TableBaseVoltages: TableBaseVoltages(),
        TableBatteryUnits: TableBatteryUnits(),
        TableBreakers: TableBreakers(),
        TableBusbarSections: TableBusbarSections(),
        TableCableInfo: TableCableInfo(),
        TableCircuits: TableCircuits(),
        TableCircuitsSubstations: TableCircuitsSubstations(),
        TableCircuitsTerminals: TableCircuitsTerminals(),
        TableConnectivityNodes: TableConnectivityNodes(),
        TableControls: TableControls(),
        TableCurrentRelays: TableCurrentRelays(),
        TableCurrentTransformerInfo: TableCurrentTransformerInfo(),
        TableCurrentTransformers: TableCurrentTransformers(),
        TableCustomerAgreements: TableCustomerAgreements(),
        TableCustomerAgreementsPricingStructures: TableCustomerAgreementsPricingStructures(),
        TableCustomers: TableCustomers(),
        TableDiagramObjectPoints: TableDiagramObjectPoints(),
        TableDiagramObjects: TableDiagramObjects(),
        TableDiagrams: TableDiagrams(),
        TableDisconnectors: TableDisconnectors(),
        TableDiscretes: TableDiscretes(),
        TableDistanceRelays: TableDistanceRelays(),
        TableEnergyConsumerPhases: TableEnergyConsumerPhases(),
        TableEnergyConsumers: TableEnergyConsumers(),
        TableEnergySourcePhases: TableEnergySourcePhases(),
        TableEnergySources: TableEnergySources(),
        TableEquipmentEquipmentContainers: TableEquipmentEquipmentContainers(),
        TableEquipmentOperationalRestrictions: TableEquipmentOperationalRestrictions(),
        TableEquipmentUsagePoints: TableEquipmentUsagePoints(),
        TableEquivalentBranches: TableEquivalentBranches(),
        TableEvChargingUnits: TableEvChargingUnits(),
        TableFaultIndicators: TableFaultIndicators(),
        TableFeeders: TableFeeders(),
        TableFuses: TableFuses(),
        TableGeographicalRegions: TableGeographicalRegions(),
        TableGrounds: TableGrounds(),
        TableGroundDisconnectors: TableGroundDisconnectors(),
        TableJumpers: TableJumpers(),
        TableJunctions: TableJunctions(),
        TableLinearShuntCompensators: TableLinearShuntCompensators(),
        TableLoadBreakSwitches: TableLoadBreakSwitches(),
        TableLocationStreetAddresses: TableLocationStreetAddresses(),
        TableLocations: TableLocations(),
        TableLoops: TableLoops(),
        TableLoopsSubstations: TableLoopsSubstations(),
        TableLvFeeders: TableLvFeeders(),
        TableMetadataDataSources: TableMetadataDataSources(),
        TableMeters: TableMeters(),
        TableNameTypes: TableNameTypes(),
        TableNames: TableNames(),
        TableNoLoadTests: TableNoLoadTests(),
        TableOpenCircuitTests: TableOpenCircuitTests(),
        TableOperationalRestrictions: TableOperationalRestrictions(),
        TableOrganisations: TableOrganisations(),
        TableOverheadWireInfo: TableOverheadWireInfo(),
        TablePerLengthSequenceImpedances: TablePerLengthSequenceImpedances(),
        TablePhotoVoltaicUnit: TablePhotoVoltaicUnit(),
        TablePoles: TablePoles(),
        TablePositionPoints: TablePositionPoints(),
        TablePotentialTransformerInfo: TablePotentialTransformerInfo(),
        TablePotentialTransformers: TablePotentialTransformers(),
        TablePowerElectronicsConnections: TablePowerElectronicsConnections(),
        TablePowerElectronicsConnectionsPhases: TablePowerElectronicsConnectionsPhases(),
        TablePowerElectronicsWindUnit: TablePowerElectronicsWindUnit(),
        TablePowerTransformerEnds: TablePowerTransformerEnds(),
        TablePowerTransformerEndRatings: TablePowerTransformerEndRatings(),
        TablePowerTransformerInfo: TablePowerTransformerInfo(),
        TablePowerTransformers: TablePowerTransformers(),
        TablePricingStructures: TablePricingStructures(),
        TablePricingStructuresTariffs: TablePricingStructuresTariffs(),
        TableProtectionRelayFunctionThresholds: TableProtectionRelayFunctionThresholds(),
        TableProtectionRelayFunctionTimeLimits: TableProtectionRelayFunctionTimeLimits(),
        TableProtectionRelayFunctionsProtectedSwitches: TableProtectionRelayFunctionsProtectedSwitches(),
        TableProtectionRelayFunctionsSensors: TableProtectionRelayFunctionsSensors(),
        TableProtectionRelaySchemes: TableProtectionRelaySchemes(),
        TableProtectionRelaySchemesProtectionRelayFunctions: TableProtectionRelaySchemesProtectionRelayFunctions(),
        TableProtectionRelaySystems: TableProtectionRelaySystems(),
        TableRatioTapChangers: TableRatioTapChangers(),
        TableReclosers: TableReclosers(),
        TableRecloseDelays: TableRecloseDelays(),
        TableRelayInfo: TableRelayInfo(),
        TableRemoteControls: TableRemoteControls(),
        TableRemoteSources: TableRemoteSources(),
        TableSeriesCompensators: TableSeriesCompensators(),
        TableShortCircuitTests: TableShortCircuitTests(),
        TableShuntCompensatorInfo: TableShuntCompensatorInfo(),
        TableSites: TableSites(),
        TableStreetlights: TableStreetlights(),
        TableSubGeographicalRegions: TableSubGeographicalRegions(),
        TableSubstations: TableSubstations(),
        TableSwitchInfo: TableSwitchInfo(),
        TableTapChangerControls: TableTapChangerControls(),
        TableTariffs: TableTariffs(),
        TableTerminals: TableTerminals(),
        TableTransformerEndInfo: TableTransformerEndInfo(),
        TableTransformerStarImpedances: TableTransformerStarImpedances(),
        TableTransformerTankInfo: TableTransformerTankInfo(),
        TableUsagePoints: TableUsagePoints(),
        TableUsagePointsEndDevices: TableUsagePointsEndDevices(),
        TableVersion: TableVersion(),
        TableVoltageRelays: TableVoltageRelays(),
    }


@dataclass(slots=True)
class DatabaseTables(object):
    _tables: Dict[Type[T], T] = _create_tables()
    _insert_statements: Dict[Type[T], PreparedStatement] = dict()

    def __init__(self):
        self._insert_statements.clear()
        for t, table in self._tables.items():
            self._insert_statements[t] = PreparedStatement(table.prepared_insert_sql)

    def get_table(self, clazz: Type[T]) -> T:
        try:
            return self._tables[clazz]
        except KeyError:
            raise MissingTableConfigException(f"No table has been registered for {clazz}. Add the table to database_tables.py")

    def get_insert(self, clazz: Type[T]) -> PreparedStatement:
        try:
            return self._insert_statements[clazz]
        except KeyError:
            raise MissingTableConfigException(f"No prepared insert statement has been registered for {clazz}. Add the to database_tables.py")

    @property
    def tables(self):
        for t in self._tables.values():
            yield t

    @staticmethod
    def copy():
        return DatabaseTables()
