#  Copyright 2024 Zeppelin Bend Pty Ltd
# 
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["NetworkCimReader"]

from typing import Callable, Optional

from zepben.evolve.database.sqlite.common.base_cim_reader import BaseCimReader
from zepben.evolve.database.sqlite.extensions.result_set import ResultSet
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_cable_info import TableCableInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_no_load_tests import TableNoLoadTests
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_open_circuit_tests import TableOpenCircuitTests
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_overhead_wire_info import TableOverheadWireInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_power_transformer_info import TablePowerTransformerInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_short_circuit_tests import TableShortCircuitTests
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_shunt_compensator_info import TableShuntCompensatorInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_switch_info import TableSwitchInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_end_info import TableTransformerEndInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_tank_info import TableTransformerTankInfo
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_transformer_test import TableTransformerTest
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo.table_wire_info import TableWireInfo
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_containers import TableAssetContainers
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_info import TableAssetInfo
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_organisation_roles import TableAssetOrganisationRoles
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_asset_owners import TableAssetOwners
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_assets import TableAssets
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_poles import TablePoles
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_streetlights import TableStreetlights
from zepben.evolve.database.sqlite.tables.iec61968.assets.table_structures import TableStructures
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_address_field import TableLocationStreetAddressField
from zepben.evolve.database.sqlite.tables.iec61968.common.table_location_street_addresses import TableLocationStreetAddresses
from zepben.evolve.database.sqlite.tables.iec61968.common.table_locations import TableLocations
from zepben.evolve.database.sqlite.tables.iec61968.common.table_position_points import TablePositionPoints
from zepben.evolve.database.sqlite.tables.iec61968.common.table_street_addresses import TableStreetAddresses
from zepben.evolve.database.sqlite.tables.iec61968.common.table_town_details import TableTownDetails
from zepben.evolve.model.cim.iec61968.assetinfo.no_load_test import NoLoadTest
from zepben.evolve.model.cim.iec61968.assetinfo.open_circuit_test import OpenCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
from zepben.evolve.model.cim.iec61968.assetinfo.short_circuit_test import ShortCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.shunt_compensator_info import ShuntCompensatorInfo
from zepben.evolve.model.cim.iec61968.assetinfo.switch_info import SwitchInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_test import TransformerTest
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo, WireInfo
from zepben.evolve.model.cim.iec61968.assetinfo.wire_material_kind import WireMaterialKind
from zepben.evolve.model.cim.iec61968.assets.asset import Asset, AssetContainer
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import AssetOrganisationRole, AssetOwner
from zepben.evolve.model.cim.iec61968.assets.pole import Pole
from zepben.evolve.model.cim.iec61968.assets.streetlight import Streetlight, StreetlightLampKind
from zepben.evolve.model.cim.iec61968.assets.structure import Structure
from zepben.evolve.model.cim.iec61968.common.location import Location, PositionPoint, StreetAddress, StreetDetail, TownDetail
from zepben.evolve.model.cim.iec61970.base.wires.winding_connection import WindingConnection
from zepben.evolve.services.network.network_service import NetworkService

"""
A class for reading the `NetworkService` tables from the database.

:param service: The `NetworkService` to populate from the database.
"""
class NetworkCimReader(BaseCimReader):

    def __init__(self, service: NetworkService):
        super().__init__(service)

    #######################
    # IEC61968 Asset Info #
    #######################

    def load_cable_info(self, table: TableCableInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `CableInfo` and populate its fields from `TableCableInfo`.

        :param table: The database table to read the `CableInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `CableInfo`.
        :param set_identifier: A callback to register the mRID of this `CableInfo` for logging purposes.

        :return: True if the `CableInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        cable_info = CableInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_wire_info(cable_info, table, result_set) and self._add_or_throw(cable_info)

    def load_no_load_tests(self, table: TableNoLoadTests, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `NoLoadTest` and populate its fields from `TableNoLoadTests`.

        :param table: The database table to read the `NoLoadTest` fields from.
        :param result_set: The record in the database table containing the fields for this `NoLoadTest`.
        :param set_identifier: A callback to register the mRID of this `NoLoadTest` for logging purposes.

        :return: True if the `NoLoadTest` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        no_load_test = NoLoadTest(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        no_load_test.energised_end_voltage = result_set.get_int(table.energised_end_voltage.query_index, on_none=None)
        no_load_test.exciting_current = result_set.get_double(table.exciting_current.query_index, on_none=None)
        no_load_test.exciting_current_zero = result_set.get_double(table.exciting_current_zero.query_index, on_none=None)
        no_load_test.loss = result_set.get_int(table.loss.query_index, on_none=None)
        no_load_test.loss_zero = result_set.get_int(table.loss_zero.query_index, on_none=None)

        return self._load_transformer_test(no_load_test, table, result_set) and self._add_or_throw(no_load_test)

    def load_open_circuit_tests(self, table: TableOpenCircuitTests, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `OpenCircuitTest` and populate its fields from `TableOpenCircuitTests`.

        :param table: The database table to read the `OpenCircuitTest` fields from.
        :param result_set: The record in the database table containing the fields for this `OpenCircuitTest`.
        :param set_identifier: A callback to register the mRID of this `OpenCircuitTest` for logging purposes.

        :return: True if the `OpenCircuitTest` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        open_circuit_test = OpenCircuitTest(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        open_circuit_test.energised_end_step = result_set.get_int(table.energised_end_step.query_index, on_none=None)
        open_circuit_test.energised_end_voltage = result_set.get_int(table.energised_end_voltage.query_index, on_none=None)
        open_circuit_test.open_end_step = result_set.get_int(table.open_end_step.query_index, on_none=None)
        open_circuit_test.open_end_voltage = result_set.get_int(table.open_end_voltage.query_index, on_none=None)
        open_circuit_test.phase_shift = result_set.get_double(table.phase_shift.query_index, on_none=None)

        return self._load_transformer_test(open_circuit_test, table, result_set) and self._add_or_throw(open_circuit_test)

    def load_overhead_wire_info(self, table: TableOverheadWireInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `OverheadWireInfo` and populate its fields from `TableOverheadWireInfo`.

        :param table: The database table to read the `OverheadWireInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `OverheadWireInfo`.
        :param set_identifier: A callback to register the mRID of this `OverheadWireInfo` for logging purposes.

        :return: True if the `OverheadWireInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        overhead_wire_info = OverheadWireInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_wire_info(overhead_wire_info, table, result_set) and self._add_or_throw(overhead_wire_info)

    def load_power_transformer_info(self, table: TablePowerTransformerInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `PowerTransformerInfo` and populate its fields from `TablePowerTransformerInfo`.

        :param table: The database table to read the `PowerTransformerInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `PowerTransformerInfo`.
        :param set_identifier: A callback to register the mRID of this `PowerTransformerInfo` for logging purposes.

        :return: True if the `PowerTransformerInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        power_transformer_info = PowerTransformerInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_asset_info(power_transformer_info, table, result_set) and self._add_or_throw(power_transformer_info)

    def load_short_circuit_tests(self, table: TableShortCircuitTests, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `ShortCircuitTest` and populate its fields from `TableShortCircuitTests`.

        :param table: The database table to read the `ShortCircuitTest` fields from.
        :param result_set: The record in the database table containing the fields for this `ShortCircuitTest`.
        :param set_identifier: A callback to register the mRID of this `ShortCircuitTest` for logging purposes.

        :return: True if the `ShortCircuitTest` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        short_circuit_test = ShortCircuitTest(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        short_circuit_test.current = result_set.get_double(table.current.query_index, on_none=None)
        short_circuit_test.energised_end_step = result_set.get_int(table.energised_end_step.query_index, on_none=None)
        short_circuit_test.grounded_end_step = result_set.get_int(table.grounded_end_step.query_index, on_none=None)
        short_circuit_test.leakage_impedance = result_set.get_double(table.leakage_impedance.query_index, on_none=None)
        short_circuit_test.leakage_impedance_zero = result_set.get_double(table.leakage_impedance_zero.query_index, on_none=None)
        short_circuit_test.loss = result_set.get_int(table.loss.query_index, on_none=None)
        short_circuit_test.loss_zero = result_set.get_int(table.loss_zero.query_index, on_none=None)
        short_circuit_test.power = result_set.get_int(table.power.query_index, on_none=None)
        short_circuit_test.voltage = result_set.get_double(table.voltage.query_index, on_none=None)
        short_circuit_test.voltage_ohmic_part = result_set.get_double(table.voltage_ohmic_part.query_index, on_none=None)

        return self._load_transformer_test(short_circuit_test, table, result_set) and self._add_or_throw(short_circuit_test)

    def load_shunt_compensator_info(self, table: TableShuntCompensatorInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `ShuntCompensatorInfo` and populate its fields from `TableShuntCompensatorInfo`.

        :param table: The database table to read the `ShuntCompensatorInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `ShuntCompensatorInfo`.
        :param set_identifier: A callback to register the mRID of this `ShuntCompensatorInfo` for logging purposes.

        :return: True if the `ShuntCompensatorInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        shunt_compensator_info = ShuntCompensatorInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        shunt_compensator_info.max_power_loss = result_set.get_int(table.max_power_loss.query_index, on_none=None)
        shunt_compensator_info.rated_current = result_set.get_int(table.rated_current.query_index, on_none=None)
        shunt_compensator_info.rated_reactive_power = result_set.get_int(table.rated_reactive_power.query_index, on_none=None)
        shunt_compensator_info.rated_voltage = result_set.get_int(table.rated_voltage.query_index, on_none=None)

        return self._load_asset_info(shunt_compensator_info, table, result_set) and self._add_or_throw(shunt_compensator_info)

    def load_switch_info(self, table: TableSwitchInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `SwitchInfo` and populate its fields from `TableSwitchInfo`.

        :param table: The database table to read the `SwitchInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `SwitchInfo`.
        :param set_identifier: A callback to register the mRID of this `SwitchInfo` for logging purposes.

        :return: True if the `SwitchInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        switch_info = SwitchInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        switch_info.rated_interrupting_time = result_set.get_double(table.rated_interrupting_time.query_index, on_none=None)

        return self._load_asset_info(switch_info, table, result_set) and self._add_or_throw(switch_info)

    def load_transformer_end_info(self, table: TableTransformerEndInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `TransformerEndInfo` and populate its fields from `TableTransformerEndInfo`.

        :param table: The database table to read the `TransformerEndInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `TransformerEndInfo`.
        :param set_identifier: A callback to register the mRID of this `TransformerEndInfo` for logging purposes.

        :return: True if the `TransformerEndInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        transformer_end_info = TransformerEndInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        transformer_end_info.connection_kind = WindingConnection[result_set.get_string(table.connection_kind.query_index)]
        transformer_end_info.emergency_s = result_set.get_int(table.emergency_s.query_index, on_none=None)
        transformer_end_info.end_number = result_set.get_int(table.end_number.query_index)
        transformer_end_info.insulation_u = result_set.get_int(table.insulation_u.query_index, on_none=None)
        transformer_end_info.phase_angle_clock = result_set.get_int(table.phase_angle_clock.query_index, on_none=None)
        transformer_end_info.r = result_set.get_double(table.r.query_index, on_none=None)
        transformer_end_info.rated_s = result_set.get_int(table.rated_s.query_index, on_none=None)
        transformer_end_info.rated_u = result_set.get_int(table.rated_u.query_index, on_none=None)
        transformer_end_info.short_term_s = result_set.get_int(table.short_term_s.query_index, on_none=None)

        transformer_end_info.transformer_tank_info = self._ensure_get(result_set.get_string(table.transformer_tank_info_mrid.query_index))
        transformer_end_info.energised_end_no_load_tests = self._ensure_get(result_set.get_string(table.energised_end_no_load_tests.query_index))
        transformer_end_info.energised_end_short_circuit_tests = self._ensure_get(result_set.get_string(table.energised_end_short_circuit_tests.query_index))
        transformer_end_info.grounded_end_short_circuit_tests = self._ensure_get(result_set.get_string(table.grounded_end_short_circuit_tests.query_index))
        transformer_end_info.open_end_open_circuit_tests = self._ensure_get(result_set.get_string(table.open_end_open_circuit_tests.query_index))
        transformer_end_info.energised_end_open_circuit_tests = self._ensure_get(result_set.get_string(table.energised_end_open_circuit_tests.query_index))

        if transformer_end_info.transformer_tank_info is not None:
            transformer_end_info.transformer_tank_info.add_transformer_end_info(transformer_end_info)

        return self._load_asset_info(transformer_end_info, table, result_set) and self._add_or_throw(transformer_end_info)

    def load_transformer_tank_info(self, table: TableTransformerTankInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `TransformerTankInfo` and populate its fields from `TableTransformerTankInfo`.

        :param table: The database table to read the `TransformerTankInfo` fields from.
        :param result_set: The record in the database table containing the fields for this `TransformerTankInfo`.
        :param set_identifier: A callback to register the mRID of this `TransformerTankInfo` for logging purposes.

        :return: True if the `TransformerTankInfo` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        transformer_tank_info = TransformerTankInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        transformer_tank_info.power_transformer_info = self._ensure_get(result_set.get_string(table.power_transformer_info_mrid.query_index), PowerTransformerInfo)
        if transformer_tank_info.power_transformer_info is not None:
            transformer_tank_info.power_transformer_info.add_transformer_tank_info(transformer_tank_info)

        return self._load_asset_info(transformer_tank_info, table, result_set) and self._add_or_throw(transformer_tank_info)

    def _load_transformer_test(self, transformer_test: TransformerTest, table: TableTransformerTest, result_set: ResultSet) -> bool:
        transformer_test.base_power = result_set.get_int(table.base_power.query_index, on_none=None)
        transformer_test.temperature = result_set.get_double(table.temperature.query_index, on_none=None)

        return self._load_identified_object(transformer_test, table, result_set)

    def _load_wire_info(self, wire_info: WireInfo, table: TableWireInfo, result_set: ResultSet) -> bool:
        wire_info.rated_current = result_set.get_int(table.rated_current.query_index, on_none=None)
        wire_info.material = WireMaterialKind[result_set.get_string(table.material.query_index)]

        return self._load_asset_info(wire_info, table, result_set)

    ###################
    # IEC61968 Assets #
    ###################

    def _load_asset(self, asset: Asset, table: TableAssets, result_set: ResultSet) -> bool:
        asset.location = self._ensure_get(result_set.get_string(table.location_mrid.query_index, on_none=None))

        return self._load_identified_object(asset, table, result_set)

    def _load_asset_container(self, asset_container: AssetContainer, table: TableAssetContainers, result_set: ResultSet) -> bool:
        return self._load_asset(asset_container, table, result_set)

    def _load_asset_info(self, asset_info: AssetInfo, table: TableAssetInfo, result_set: ResultSet) -> bool:
        return self._load_identified_object(asset_info, table, result_set)

    def _load_asset_organisation_role(self, asset_organisation_role: AssetOrganisationRole, table: TableAssetOrganisationRoles, result_set: ResultSet) -> bool:
        return self._load_organisation_role(asset_organisation_role, table, result_set)

    def _load_structure(self, structure: Structure, table: TableStructures, result_set: ResultSet) -> bool:
        return self._load_asset_container(structure, table, result_set)

    def load_asset_owners(self, table: TableAssetOwners, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `AssetOwner` and populate its fields from `TableAssetOwners`.

        :param table: The database table to read the `AssetOwner` fields from.
        :param result_set: The record in the database table containing the fields for this `AssetOwner`.
        :param set_identifier: A callback to register the mRID of this `AssetOwner` for logging purposes.

        :return: True if the `AssetOwner` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        asset_owner = AssetOwner(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_asset_organisation_role(asset_owner, table, result_set) and self._add_or_throw(asset_owner)

    def load_poles(self, table: TablePoles, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Pole` and populate its fields from `TablePoles`.

        :param table: The database table to read the `Pole` fields from.
        :param result_set: The record in the database table containing the fields for this `Pole`.
        :param set_identifier: A callback to register the mRID of this `Pole` for logging purposes.

        :return: True if the `Pole` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        pole = Pole(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        pole.classification = result_set.get_string(table.classification.query_index, on_none="")

        return self._load_structure(pole, table, result_set) and self._add_or_throw(pole)

    def load_streetlights(self, table: TableStreetlights, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Streetlight` and populate its fields from `TableStreetlights`.

        :param table: The database table to read the `Streetlight` fields from.
        :param result_set: The record in the database table containing the fields for this `Streetlight`.
        :param set_identifier: A callback to register the mRID of this `Streetlight` for logging purposes.

        :return: True if the `Streetlight` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        streetlight = Streetlight(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        streetlight.lamp_kind = StreetlightLampKind[result_set.get_string(table.lamp_kind.query_index)]
        streetlight.light_rating = result_set.get_int(table.light_rating.query_index, on_none=None)
        streetlight.pole = self._ensure_get(result_set.get_string(table.pole_mrid.query_index))
        if streetlight.pole is not None:
            streetlight.pole.add_streetlight(streetlight)

        return self._load_asset(streetlight, table, result_set) and self._add_or_throw(streetlight)

    ###################
    # IEC61968 Common #
    ###################

    def load_locations(self, table: TableLocations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `Location` and populate its fields from `TableLocations`.

        :param table: The database table to read the `Location` fields from.
        :param result_set: The record in the database table containing the fields for this `Location`.
        :param set_identifier: A callback to register the mRID of this `Location` for logging purposes.

        :return: True if the `Location` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        location = Location(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(location, table, result_set) and self._add_or_throw(location)

    def load_location_street_addresses(self, table: TableLocationStreetAddresses, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `set_identifier` and populate its fields from `TableLocationStreetAddresses`.

        :param table: The database table to read the `set_identifier` fields from.
        :param result_set: The record in the database table containing the fields for this `set_identifier`.
        :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

        :return: True if the `set_identifier` was successfully read from the database and added to the service.
        :raises SqlException: For any errors encountered reading from the database.
        """
        location_mrid = set_identifier(result_set.get_string(table.location_mrid.query_index))
        field = TableLocationStreetAddressField[result_set.get_string(table.address_field.query_index)]

        location = self._service.get(location_mrid, Location)

        if field == TableLocationStreetAddressField.mainAddress:
            location.mainAddress = self._load_street_address(table, result_set)

        return True

    """
    Create a `set_identifier` and populate its fields from `TablePositionPoints`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_position_points(self, table: TablePositionPoints, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        location_mrid = set_identifier(result_set.get_string(table.location_mrid.query_index))
        sequence_number = result_set.get_int(table.sequence_number.query_index)

        location = self._service.get(location_mrid, Location)

        location.insert_point(
            PositionPoint(
                result_set.get_double(table.x_position.query_index),
                result_set.get_double(table.y_position.query_index)
            ),
            sequence_number
        )

        return True

    def _load_street_address(self, table: TableStreetAddresses, result_set: ResultSet) -> StreetAddress:
        return StreetAddress(
            result_set.get_string(table.postal_code.query_index).emptyIfNull().internEmpty(),
            self._load_town_detail(table, result_set),
            result_set.get_string(table.po_box.query_index, on_none=""),
            self._load_street_detail(table, result_set)
        )

    def _load_street_detail(self, table: TableStreetAddresses, result_set: ResultSet) -> Optional[StreetDetail]:
        sd = StreetDetail(
            result_set.get_string(table.building_name.query_index, on_none=""),
            result_set.get_string(table.floor_identification.query_index, on_none=""),
            result_set.get_string(table.street_name.query_index, on_none=""),
            result_set.get_string(table.number.query_index, on_none=""),
            result_set.get_string(table.suite_number.query_index, on_none=""),
            result_set.get_string(table.type.query_index, on_none=""),
            result_set.get_string(table.display_address.query_index, on_none="")
        )

        return sd if not sd.all_fields_empty() else None

    def _load_town_detail(self, table: TableTownDetails, result_set: ResultSet) -> Optional[TownDetail]:
        td = TownDetail(
            result_set.get_string(table.town_name.query_index),
            result_set.get_string(table.state_or_province.query_index)
        )

        return td if not td.all_fields_null_or_empty() else None

up to here
    #####################################
    # IEC61968 infIEC61968 InfAssetInfo #
    #####################################

    """
    Create a `RelayInfo` and populate its fields from `TableRelayInfo`.

    :param table: The database table to read the `RelayInfo` fields from.
    :param result_set: The record in the database table containing the fields for this `RelayInfo`.
    :param set_identifier: A callback to register the mRID of this `RelayInfo` for logging purposes.

    :return: True if the `RelayInfo` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_relay_info(self, table: TableRelayInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val relayInfo = RelayInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            curveSetting = result_set.get_string(table.curve_setting.query_index, on_none=None)
            recloseFast = result_set.get_boolean(table.reclose_fast.query_index, on_none=None)

        return self._load_asset_info(relayInfo, table, result_set) and self._add_or_throw(relayInfo)

    """
    Adds a delay to a `RelayInfo` and populate its fields from `TableRecloseDelays`.

    :param table: The database table to read the delay fields from.
    :param result_set: The record in the database table containing the fields for this delay.
    :param set_identifier: A callback to register the mRID of this delay for logging purposes.

    :return: True if the delay was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_reclose_delays(self, table: TableRecloseDelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        # Note TableRecloseDelays.selectSql ensures we process ratings in the correct order.
        val relayInfoMRID = result_set.get_string(table.relay_info_mrid.query_index)
        val recloseDelay = result_set.get_double(table.reclose_delay.query_index)
        set_identifier(f"{relayInfoMRID}.s{recloseDelay}")

        val cri = self._ensure_get(relayInfoMRID, f"{relayInfoMRID}.s{recloseDelay}")
 , RelayInfo       cri?.addDelay(recloseDelay)

        return True

    """
    Create a `CurrentTransformerInfo` and populate its fields from `TableCurrentTransformerInfo`.

    :param table: The database table to read the `CurrentTransformerInfo` fields from.
    :param result_set: The record in the database table containing the fields for this `CurrentTransformerInfo`.
    :param set_identifier: A callback to register the mRID of this `CurrentTransformerInfo` for logging purposes.

    :return: True if the `CurrentTransformerInfo` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_current_transformer_info(self, table: TableCurrentTransformerInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val currentTransformerInfo = CurrentTransformerInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            accuracyClass = result_set.get_string(table.accuracy_class.query_index, on_none=None)
            accuracyLimit = result_set.get_double(table.accuracy_limit.query_index, on_none=None)
            coreCount = result_set.get_int(table.core_count.query_index, on_none=None)
            ctClass = result_set.get_string(table.ct_class.query_index, on_none=None)
            kneePointVoltage = result_set.get_int(table.knee_point_voltage.query_index, on_none=None)
            maxRatio = result_set.get_ratio(table.max_ratio_numerator.query_index, on_none=None, table.max_ratio_denominator.query_index)
            nominalRatio = result_set.get_ratio(table.nominal_ratio_numerator.query_index, on_none=None, table.nominal_ratio_denominator.query_index)
            primaryRatio = result_set.get_double(table.primary_ratio.query_index, on_none=None)
            ratedCurrent = result_set.get_int(table.rated_current.query_index, on_none=None)
            secondaryFlsRating = result_set.get_int(table.secondary_fls_rating.query_index, on_none=None)
            secondaryRatio = result_set.get_double(table.secondary_ratio.query_index, on_none=None)
            usage = result_set.get_string(table.usage.query_index, on_none=None)

        return self._load_asset_info(currentTransformerInfo, table, result_set) and self._add_or_throw(currentTransformerInfo)

    """
    Create a `PotentialTransformerInfo` and populate its fields from `TablePotentialTransformerInfo`.

    :param table: The database table to read the `PotentialTransformerInfo` fields from.
    :param result_set: The record in the database table containing the fields for this `PotentialTransformerInfo`.
    :param set_identifier: A callback to register the mRID of this `PotentialTransformerInfo` for logging purposes.

    :return: True if the `PotentialTransformerInfo` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_potential_transformer_info(self, table: TablePotentialTransformerInfo, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val potentialTransformerInfo = PotentialTransformerInfo(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            accuracyClass = result_set.get_string(table.accuracy_class.query_index, on_none=None)
            nominalRatio = result_set.get_ratio(table.nominal_ratio_numerator.query_index, on_none=None, table.nominal_ratio_denominator.query_index)
            primaryRatio = result_set.get_double(table.primary_ratio.query_index, on_none=None)
            ptClass = result_set.get_string(table.pt_class.query_index, on_none=None)
            ratedVoltage = result_set.get_int(table.rated_voltage.query_index, on_none=None)
            secondaryRatio = result_set.get_double(table.secondary_ratio.query_index, on_none=None)

        return self._load_asset_info(potentialTransformerInfo, table, result_set) and self._add_or_throw(potentialTransformerInfo)

    #####################
    # IEC61968 Metering #
    #####################

    private fun loadEndDevice(endDevice: EndDevice, table: TableEndDevices, result_set: ResultSet) -> bool:
        endDevice
            customerMRID = result_set.get_string(table.customer_mrid.query_index, on_none=None)
            serviceLocation = self._ensure_get(
                result_set.get_string(table.service_location_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )

        return self._load_asset_container(endDevice, table, result_set)

    """
    Create a `Meter` and populate its fields from `TableMeters`.

    :param table: The database table to read the `Meter` fields from.
    :param result_set: The record in the database table containing the fields for this `Meter`.
    :param set_identifier: A callback to register the mRID of this `Meter` for logging purposes.

    :return: True if the `Meter` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_meters(self, table: TableMeters, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val meter = Meter(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadEndDevice(meter, table, result_set) and self._add_or_throw(meter)

    """
    Create a `UsagePoint` and populate its fields from `TableUsagePoints`.

    :param table: The database table to read the `UsagePoint` fields from.
    :param result_set: The record in the database table containing the fields for this `UsagePoint`.
    :param set_identifier: A callback to register the mRID of this `UsagePoint` for logging purposes.

    :return: True if the `UsagePoint` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_usage_points(self, table: TableUsagePoints, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val usagePoint = UsagePoint(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            usagePointLocation = self._ensure_get(result_set.get_string(table.location_mrid.query_index, on_none=None))
            isVirtual = result_set.get_boolean(table.is_virtual.query_index)
            connectionCategory = result_set.get_string(table.connection_category.query_index, on_none=None)
            ratedPower = result_set.get_int(table.rated_power.query_index, on_none=None)
            approvedInverterCapacity = result_set.get_int(table.approved_inverter_capacity.query_index, on_none=None)

        return self._load_identified_object(usagePoint, table, result_set) and self._add_or_throw(usagePoint)

    #######################
    # IEC61968 Operations #
    #######################

    """
    Create an `OperationalRestriction` and populate its fields from `TableOperationalRestrictions`.

    :param table: The database table to read the `OperationalRestriction` fields from.
    :param result_set: The record in the database table containing the fields for this `OperationalRestriction`.
    :param set_identifier: A callback to register the mRID of this `OperationalRestriction` for logging purposes.

    :return: True if the `OperationalRestriction` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_operational_restrictions(self, table: TableOperationalRestrictions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val operationalRestriction = OperationalRestriction(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadDocument(operationalRestriction, table, result_set) and self._add_or_throw(operationalRestriction)

    #####################################
    # IEC61970 Base Auxiliary Equipment #
    #####################################

    private fun loadAuxiliaryEquipment(
        auxiliaryEquipment: AuxiliaryEquipment,
        table: TableAuxiliaryEquipment,
        result_set: ResultSet
    ) -> bool:
        auxiliaryEquipment
            terminal =
                self._ensure_get(result_set.get_string(table.terminal_mrid.query_index, on_none=None))

        return loadEquipment(auxiliaryEquipment, table, result_set)

    """
    Create a `CurrentTransformer` and populate its fields from `TableCurrentTransformers`.

    :param table: The database table to read the `CurrentTransformer` fields from.
    :param result_set: The record in the database table containing the fields for this `CurrentTransformer`.
    :param set_identifier: A callback to register the mRID of this `CurrentTransformer` for logging purposes.

    :return: True if the `CurrentTransformer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_current_transformers(self, table: TableCurrentTransformers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val currentTransformer = CurrentTransformer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            assetInfo = self._ensure_get(result_set.get_string(table.current_transformer_info_mrid.query_index, on_none=None))
            coreBurden = result_set.get_int(table.core_burden.query_index, on_none=None)

        return loadSensor(currentTransformer, table, result_set) and self._add_or_throw(currentTransformer)

    """
    Create a `FaultIndicator` and populate its fields from `TableFaultIndicators`.

    :param table: The database table to read the `FaultIndicator` fields from.
    :param result_set: The record in the database table containing the fields for this `FaultIndicator`.
    :param set_identifier: A callback to register the mRID of this `FaultIndicator` for logging purposes.

    :return: True if the `FaultIndicator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_fault_indicators(self, table: TableFaultIndicators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val faultIndicator = FaultIndicator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadAuxiliaryEquipment(faultIndicator, table, result_set) and self._add_or_throw(faultIndicator)

    """
    Create a `PotentialTransformer` and populate its fields from `TablePotentialTransformers`.

    :param table: The database table to read the `PotentialTransformer` fields from.
    :param result_set: The record in the database table containing the fields for this `PotentialTransformer`.
    :param set_identifier: A callback to register the mRID of this `PotentialTransformer` for logging purposes.

    :return: True if the `PotentialTransformer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_potential_transformers(self, table: TablePotentialTransformers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val potentialTransformer = PotentialTransformer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            assetInfo = self._ensure_get(result_set.get_string(table.potential_transformer_info_mrid.query_index, on_none=None))
            type = PotentialTransformerKind[result_set.get_string(table.type.query_index)]

        return loadSensor(potentialTransformer, table, result_set) and self._add_or_throw(potentialTransformer)

    private fun loadSensor(sensor: Sensor, table: TableSensors, result_set: ResultSet) -> bool:
        return self.loadAuxiliaryEquipment(sensor, table, result_set)

    ######################
    # IEC61970 Base Core #
    ######################

    private fun loadAcDcTerminal(acDcTerminal: AcDcTerminal, table: TableAcDcTerminals, result_set: ResultSet) -> bool:
        return self._load_identified_object(acDcTerminal, table, result_set)

    """
    Create a `BaseVoltage` and populate its fields from `TableBaseVoltages`.

    :param table: The database table to read the `BaseVoltage` fields from.
    :param result_set: The record in the database table containing the fields for this `BaseVoltage`.
    :param set_identifier: A callback to register the mRID of this `BaseVoltage` for logging purposes.

    :return: True if the `BaseVoltage` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_base_voltages(self, table: TableBaseVoltages, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val baseVoltage = BaseVoltage(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            nominalVoltage = result_set.get_int(table.nominal_voltage.query_index)

        return self._load_identified_object(baseVoltage, table, result_set) and self._add_or_throw(baseVoltage)

    private fun loadConductingEquipment(
        conductingEquipment: ConductingEquipment,
        table: TableConductingEquipment,
        result_set: ResultSet
    ) -> bool:
        conductingEquipment
            baseVoltage = self._ensure_get(
                result_set.get_string(table.base_voltage_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )

        return loadEquipment(conductingEquipment, table, result_set)

    """
    Create a `ConnectivityNode` and populate its fields from `TableConnectivityNodes`.

    :param table: The database table to read the `ConnectivityNode` fields from.
    :param result_set: The record in the database table containing the fields for this `ConnectivityNode`.
    :param set_identifier: A callback to register the mRID of this `ConnectivityNode` for logging purposes.

    :return: True if the `ConnectivityNode` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_connectivity_nodes(self, table: TableConnectivityNodes, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val connectivityNode = ConnectivityNode(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(connectivityNode, table, result_set) and self._add_or_throw(connectivityNode)

    private fun loadConnectivityNodeContainer(
        connectivityNodeContainer: ConnectivityNodeContainer,
        table: TableConnectivityNodeContainers,
        result_set: ResultSet
    ) -> bool:
        return self.loadPowerSystemResource(connectivityNodeContainer, table, result_set)

    private fun loadEquipment(equipment: Equipment, table: TableEquipment, result_set: ResultSet) -> bool:
        equipment
            normallyInService = result_set.get_boolean(table.normally_in_service.query_index)
            inService = result_set.get_boolean(table.in_service.query_index)
            commissionedDate = result_set.get_instant(table.commissioned_date.query_index)

        return loadPowerSystemResource(equipment, table, result_set)

    private fun loadEquipmentContainer(equipmentContainer: EquipmentContainer, table: TableEquipmentContainers, result_set: ResultSet) -> bool:
        return self.loadConnectivityNodeContainer(equipmentContainer, table, result_set)

    """
    Create a `Feeder` and populate its fields from `TableFeeders`.

    :param table: The database table to read the `Feeder` fields from.
    :param result_set: The record in the database table containing the fields for this `Feeder`.
    :param set_identifier: A callback to register the mRID of this `Feeder` for logging purposes.

    :return: True if the `Feeder` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_feeders(self, table: TableFeeders, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val feeder = Feeder(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            normalHeadTerminal = self._ensure_get(
                result_set.get_string(table.normal_head_terminal_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )
            normalEnergizingSubstation =
                self._ensure_get(
                    result_set.get_string(table.normal_energizing_substation_mrid.query_index, on_none=None),
                    typeNameAndMRID()
                )
            normalEnergizingSubstation?.addFeeder(this)

        return loadEquipmentContainer(feeder, table, result_set) and self._add_or_throw(feeder)

    """
    Create a `GeographicalRegion` and populate its fields from `TableGeographicalRegions`.

    :param table: The database table to read the `GeographicalRegion` fields from.
    :param result_set: The record in the database table containing the fields for this `GeographicalRegion`.
    :param set_identifier: A callback to register the mRID of this `GeographicalRegion` for logging purposes.

    :return: True if the `GeographicalRegion` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_geographical_regions(self, table: TableGeographicalRegions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val geographicalRegion = GeographicalRegion(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(geographicalRegion, table, result_set) and self._add_or_throw(geographicalRegion)

    private fun loadPowerSystemResource(
        powerSystemResource: PowerSystemResource,
        table: TablePowerSystemResources,
        result_set: ResultSet
    ) -> bool:
        powerSystemResource
            location =
                self._ensure_get(result_set.get_string(table.location_mrid.query_index, on_none=None))
            numControls = result_set.get_int(table.num_controls.query_index)

        return self._load_identified_object(powerSystemResource, table, result_set)

    """
    Create a `Site` and populate its fields from `TableSites`.

    :param table: The database table to read the `Site` fields from.
    :param result_set: The record in the database table containing the fields for this `Site`.
    :param set_identifier: A callback to register the mRID of this `Site` for logging purposes.

    :return: True if the `Site` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_sites(self, table: TableSites, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val site = Site(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadEquipmentContainer(site, table, result_set) and self._add_or_throw(site)

    """
    Create a `SubGeographicalRegion` and populate its fields from `TableSubGeographicalRegions`.

    :param table: The database table to read the `SubGeographicalRegion` fields from.
    :param result_set: The record in the database table containing the fields for this `SubGeographicalRegion`.
    :param set_identifier: A callback to register the mRID of this `SubGeographicalRegion` for logging purposes.

    :return: True if the `SubGeographicalRegion` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_sub_geographical_regions(self, table: TableSubGeographicalRegions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val subGeographicalRegion =
            SubGeographicalRegion(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
                geographicalRegion = self._ensure_get(
                    result_set.get_string(table.geographical_region_mrid.query_index, on_none=None),
                    typeNameAndMRID()
                )
                geographicalRegion?.addSubGeographicalRegion(this)

        return self._load_identified_object(subGeographicalRegion, table, result_set) and self._add_or_throw(
            subGeographicalRegion
        )

    """
    Create a `Substation` and populate its fields from `TableSubstations`.

    :param table: The database table to read the `Substation` fields from.
    :param result_set: The record in the database table containing the fields for this `Substation`.
    :param set_identifier: A callback to register the mRID of this `Substation` for logging purposes.

    :return: True if the `Substation` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_substations(self, table: TableSubstations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val substation = Substation(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            subGeographicalRegion = self._ensure_get(
                result_set.get_string(table.sub_geographical_region_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )
            subGeographicalRegion?.addSubstation(this)

        return loadEquipmentContainer(substation, table, result_set) and self._add_or_throw(substation)

    """
    Create a `Terminal` and populate its fields from `TableTerminals`.

    :param table: The database table to read the `Terminal` fields from.
    :param result_set: The record in the database table containing the fields for this `Terminal`.
    :param set_identifier: A callback to register the mRID of this `Terminal` for logging purposes.

    :return: True if the `Terminal` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_terminals(self, table: TableTerminals, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val terminal = Terminal(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            sequence_number = result_set.get_int(table.sequence_number.query_index)
            conductingEquipment = self._ensure_get(
                result_set.get_string(table.conducting_equipment_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )
            conductingEquipment?.addTerminal(this)
            phases = PhaseCode[result_set.get_string(table.phases.query_index)]

        service.connect(terminal, result_set.get_string(table.connectivity_node_mrid.query_index, on_none=None))

        return loadAcDcTerminal(terminal, table, result_set) and self._add_or_throw(terminal)

    #############################
    # IEC61970 Base Equivalents #
    #############################

    """
    Create an `EquivalentBranch` and populate its fields from `TableEquivalentBranches`.

    :param table: The database table to read the `EquivalentBranch` fields from.
    :param result_set: The record in the database table containing the fields for this `EquivalentBranch`.
    :param set_identifier: A callback to register the mRID of this `EquivalentBranch` for logging purposes.

    :return: True if the `EquivalentBranch` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_equivalent_branches(self, table: TableEquivalentBranches, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val equivalentBranch = EquivalentBranch(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            negativeR12 = result_set.get_double(table.negative_r12.query_index, on_none=None)
            negativeR21 = result_set.get_double(table.negative_r21.query_index, on_none=None)
            negativeX12 = result_set.get_double(table.negative_x12.query_index, on_none=None)
            negativeX21 = result_set.get_double(table.negative_x21.query_index, on_none=None)
            positiveR12 = result_set.get_double(table.positive_r12.query_index, on_none=None)
            positiveR21 = result_set.get_double(table.positive_r21.query_index, on_none=None)
            positiveX12 = result_set.get_double(table.positive_x12.query_index, on_none=None)
            positiveX21 = result_set.get_double(table.positive_x21.query_index, on_none=None)
            r = result_set.get_double(table.r.query_index, on_none=None)
            r21 = result_set.get_double(table.r21.query_index, on_none=None)
            x = result_set.get_double(table.x.query_index, on_none=None)
            x21 = result_set.get_double(table.x21.query_index, on_none=None)
            zeroR12 = result_set.get_double(table.zero_r12.query_index, on_none=None)
            zeroR21 = result_set.get_double(table.zero_r21.query_index, on_none=None)
            zeroX12 = result_set.get_double(table.zero_x12.query_index, on_none=None)
            zeroX21 = result_set.get_double(table.zero_x21.query_index, on_none=None)

        return loadEquivalentEquipment(equivalentBranch, table, result_set) and self._add_or_throw(equivalentBranch)

    private fun loadEquivalentEquipment(equivalentEquipment: EquivalentEquipment, table: TableEquivalentEquipment, result_set: ResultSet) -> bool:
        return self.loadConductingEquipment(equivalentEquipment, table, result_set)

    ######################
    # IEC61970 Base Meas #
    ######################

    """
    Create an `Accumulator` and populate its fields from `TableAccumulators`.

    :param table: The database table to read the `Accumulator` fields from.
    :param result_set: The record in the database table containing the fields for this `Accumulator`.
    :param set_identifier: A callback to register the mRID of this `Accumulator` for logging purposes.

    :return: True if the `Accumulator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_accumulators(self, table: TableAccumulators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val meas = Accumulator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadMeasurement(meas, table, result_set) and self._add_or_throw(meas)

    """
    Create an `Analog` and populate its fields from `TableAnalogs`.

    :param table: The database table to read the `Analog` fields from.
    :param result_set: The record in the database table containing the fields for this `Analog`.
    :param set_identifier: A callback to register the mRID of this `Analog` for logging purposes.

    :return: True if the `Analog` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_analogs(self, table: TableAnalogs, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val meas = Analog(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            positiveFlowIn = result_set.get_boolean(table.positive_flow_in.query_index)

        return loadMeasurement(meas, table, result_set) and self._add_or_throw(meas)

    """
    Create a `Control` and populate its fields from `TableControls`.

    :param table: The database table to read the `Control` fields from.
    :param result_set: The record in the database table containing the fields for this `Control`.
    :param set_identifier: A callback to register the mRID of this `Control` for logging purposes.

    :return: True if the `Control` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_controls(self, table: TableControls, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val control = Control(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            powerSystemResourceMRID = result_set.get_string(table.power_system_resource_mrid.query_index, on_none=None)

        return loadIoPoint(control, table, result_set) and self._add_or_throw(control)

    """
    Create a `Discrete` and populate its fields from `TableDiscretes`.

    :param table: The database table to read the `Discrete` fields from.
    :param result_set: The record in the database table containing the fields for this `Discrete`.
    :param set_identifier: A callback to register the mRID of this `Discrete` for logging purposes.

    :return: True if the `Discrete` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_discretes(self, table: TableDiscretes, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val meas = Discrete(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadMeasurement(meas, table, result_set) and self._add_or_throw(meas)

    private fun loadIoPoint(ioPoint: IoPoint, table: TableIoPoints, result_set: ResultSet) -> bool:
        return self._load_identified_object(ioPoint, table, result_set)

    private fun loadMeasurement(measurement: Measurement, table: TableMeasurements, result_set: ResultSet) -> bool:
        measurement
            powerSystemResourceMRID = result_set.get_string(table.power_system_resource_mrid.query_index, on_none=None)
            remoteSource = self._ensure_get(
                result_set.get_string(table.remote_source_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )
            remoteSource?.measurement = this
            terminalMRID = result_set.get_string(table.terminal_mrid.query_index, on_none=None)
            phases = PhaseCode[result_set.get_string(table.phases.query_index)]
            unitSymbol = UnitSymbol[result_set.get_string(table.unit_symbol.query_index)]
        return self._load_identified_object(measurement, table, result_set)

    ############################
    # IEC61970 Base Protection #
    ############################

    """
    Create a `CurrentRelay` and populate its fields from `TableCurrentRelays`.

    :param table: The database table to read the `CurrentRelay` fields from.
    :param result_set: The record in the database table containing the fields for this `CurrentRelay`.
    :param set_identifier: A callback to register the mRID of this `CurrentRelay` for logging purposes.

    :return: True if the `CurrentRelay` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_current_relays(self, table: TableCurrentRelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val currentRelay = CurrentRelay(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            currentLimit1 = result_set.get_double(table.current_limit_1.query_index, on_none=None)
            inverseTimeFlag = result_set.get_boolean(table.inverse_time_flag.query_index, on_none=None)
            timeDelay1 = result_set.get_double(table.time_delay_1.query_index, on_none=None)

        return loadProtectionRelayFunction(currentRelay, table, result_set) and self._add_or_throw(currentRelay)

    """
    Create a `DistanceRelay` and populate its fields from `TableDistanceRelays`.

    :param table: The database table to read the `DistanceRelay` fields from.
    :param result_set: The record in the database table containing the fields for this `DistanceRelay`.
    :param set_identifier: A callback to register the mRID of this `DistanceRelay` for logging purposes.

    :return: True if the `DistanceRelay` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_distance_relays(self, table: TableDistanceRelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val distanceRelay = DistanceRelay(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            backwardBlind = result_set.get_double(table.backward_blind.query_index, on_none=None)
            backwardReach = result_set.get_double(table.backward_reach.query_index, on_none=None)
            backwardReactance = result_set.get_double(table.backward_reactance.query_index, on_none=None)
            forwardBlind = result_set.get_double(table.forward_blind.query_index, on_none=None)
            forwardReach = result_set.get_double(table.forward_reach.query_index, on_none=None)
            forwardReactance = result_set.get_double(table.forward_reactance.query_index, on_none=None)
            operationPhaseAngle1 = result_set.get_double(table.operation_phase_angle1.query_index, on_none=None)
            operationPhaseAngle2 = result_set.get_double(table.operation_phase_angle2.query_index, on_none=None)
            operationPhaseAngle3 = result_set.get_double(table.operation_phase_angle3.query_index, on_none=None)

        return loadProtectionRelayFunction(distanceRelay, table, result_set) and self._add_or_throw(distanceRelay)

    private fun loadProtectionRelayFunction(
        protectionRelayFunction: ProtectionRelayFunction,
        table: TableProtectionRelayFunctions,
        result_set: ResultSet
    ) -> bool:
        protectionRelayFunction
            assetInfo = self._ensure_get(
                result_set.get_string(table.relay_info_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )
            model = result_set.get_string(table.model.query_index, on_none=None)
            reclosing = result_set.get_boolean(table.reclosing.query_index, on_none=None)
            relayDelayTime = result_set.get_double(table.relay_delay_time.query_index, on_none=None)
            protectionKind = ProtectionKind[result_set.get_string(table.protection_kind.query_index)]
            directable = result_set.get_boolean(table.directable.query_index, on_none=None)
            powerDirection = PowerDirectionKind[result_set.get_string(table.power_direction.query_index)]

        return loadPowerSystemResource(protectionRelayFunction, table, result_set)

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelayFunctionThresholds`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_protection_relay_function_thresholds(self, table: TableProtectionRelayFunctionThresholds, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val protectionRelayFunctionMRID = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        val sequence_number = result_set.get_int(table.sequence_number.query_index)

        val id = set_identifier(f"{protectionRelayFunctionMRID}-threshold{sequence_number}")
        val protectionRelayFunction = service.getOrThrow<ProtectionRelayFunction>(
            protectionRelayFunctionMRID,
            "ProtectionRelayFunction to RelaySetting association {id}"
        )

        protectionRelayFunction.addThreshold(
            RelaySetting(
                UnitSymbol[result_set.get_string(table.unit_symbol.query_index)],
                result_set.get_double(table.value.query_index),
                result_set.get_string(table.name.query_index, on_none=None)
            ),
            sequence_number
        )

        return True

    """
    Adds a time limit to a `ProtectionRelayFunction` and populate its fields from `TableProtectionRelayFunctionTimeLimits`.

    :param table: The database table to read the time limit fields from.
    :param result_set: The record in the database table containing the fields for this time limit.
    :param set_identifier: A callback to register the mRID of this time limit for logging purposes.

    :return: True if the time limit was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_protection_relay_function_time_limits(self, table: TableProtectionRelayFunctionTimeLimits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        # Note TableProtectionRelayFunctionTimeLimits.selectSql ensures we process ratings in the correct order.
        val protectionRelayFunctionMRID = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        val sequence_number = result_set.get_int(table.sequence_number.query_index)
        val timeLimit = result_set.get_double(table.time_limit.query_index)
        set_identifier(f"{protectionRelayFunctionMRID} time limit {sequence_number}")

        val protectionRelayFunction = service.getOrThrow<ProtectionRelayFunction>(
            protectionRelayFunctionMRID,
            f"{protectionRelayFunctionMRID} time limit {timeLimit}"
        )
        protectionRelayFunction.addTimeLimit(timeLimit)

        return True

    """
    Create a `ProtectionRelayScheme` and populate its fields from `TableProtectionRelaySchemes`.

    :param table: The database table to read the `ProtectionRelayScheme` fields from.
    :param result_set: The record in the database table containing the fields for this `ProtectionRelayScheme`.
    :param set_identifier: A callback to register the mRID of this `ProtectionRelayScheme` for logging purposes.

    :return: True if the `ProtectionRelayScheme` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_protection_relay_schemes(self, table: TableProtectionRelaySchemes, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val protectionRelayScheme = ProtectionRelayScheme(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            system = self._ensure_get(result_set.get_string(table.system_mrid.query_index))
            system?.addScheme(this)

        return self._load_identified_object(protectionRelayScheme, table, result_set) and self._add_or_throw(protectionRelayScheme)

    """
    Create a `ProtectionRelaySystem` and populate its fields from `TableProtectionRelaySystems`.

    :param table: The database table to read the `ProtectionRelaySystem` fields from.
    :param result_set: The record in the database table containing the fields for this `ProtectionRelaySystem`.
    :param set_identifier: A callback to register the mRID of this `ProtectionRelaySystem` for logging purposes.

    :return: True if the `ProtectionRelaySystem` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_protection_relay_systems(self, table: TableProtectionRelaySystems, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val protectionRelaySystem = ProtectionRelaySystem(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            protectionKind = ProtectionKind[result_set.get_string(table.protection_kind.query_index)]

        return loadEquipment(protectionRelaySystem, table, result_set) and self._add_or_throw(protectionRelaySystem)

    """
    Create a `VoltageRelay` and populate its fields from `TableVoltageRelays`.

    :param table: The database table to read the `VoltageRelay` fields from.
    :param result_set: The record in the database table containing the fields for this `VoltageRelay`.
    :param set_identifier: A callback to register the mRID of this `VoltageRelay` for logging purposes.

    :return: True if the `VoltageRelay` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_voltage_relays(self, table: TableVoltageRelays, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val voltageRelay = VoltageRelay(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadProtectionRelayFunction(voltageRelay, table, result_set) and self._add_or_throw(voltageRelay)

    #######################
    # IEC61970 Base SCADA #
    #######################

    """
    Create a `RemoteControl` and populate its fields from `TableRemoteControls`.

    :param table: The database table to read the `RemoteControl` fields from.
    :param result_set: The record in the database table containing the fields for this `RemoteControl`.
    :param set_identifier: A callback to register the mRID of this `RemoteControl` for logging purposes.

    :return: True if the `RemoteControl` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_remote_controls(self, table: TableRemoteControls, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val remoteControl = RemoteControl(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            control =
                self._ensure_get(result_set.get_string(table.control_mrid.query_index, on_none=None))
            control?.remoteControl = this

        return loadRemotePoint(remoteControl, table, result_set) and self._add_or_throw(remoteControl)

    private fun loadRemotePoint(remotePoint: RemotePoint, table: TableRemotePoints, result_set: ResultSet) -> bool:
        return self._load_identified_object(remotePoint, table, result_set)

    """
    Create a `RemoteSource` and populate its fields from `TableRemoteSources`.

    :param table: The database table to read the `RemoteSource` fields from.
    :param result_set: The record in the database table containing the fields for this `RemoteSource`.
    :param set_identifier: A callback to register the mRID of this `RemoteSource` for logging purposes.

    :return: True if the `RemoteSource` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_remote_sources(self, table: TableRemoteSources, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val remoteSource = RemoteSource(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadRemotePoint(remoteSource, table, result_set) and self._add_or_throw(remoteSource)

    #############################################
    # IEC61970 Base Wires Generation Production #
    #############################################

    """
    Create a `BatteryUnit` and populate its fields from `TableBatteryUnits`.

    :param table: The database table to read the `BatteryUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `BatteryUnit`.
    :param set_identifier: A callback to register the mRID of this `BatteryUnit` for logging purposes.

    :return: True if the `BatteryUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_battery_units(self, table: TableBatteryUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val batteryUnit = BatteryUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            batteryState = BatteryStateKind[result_set.get_string(table.battery_state.query_index)]
            ratedE = result_set.get_long(table.rated_e.query_index, on_none=None)
            storedE = result_set.get_long(table.stored_e.query_index, on_none=None)

        return loadPowerElectronicsUnit(batteryUnit, table, result_set) and self._add_or_throw(batteryUnit)

    """
    Create a `PhotoVoltaicUnit` and populate its fields from `TablePhotoVoltaicUnits`.

    :param table: The database table to read the `PhotoVoltaicUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `PhotoVoltaicUnit`.
    :param set_identifier: A callback to register the mRID of this `PhotoVoltaicUnit` for logging purposes.

    :return: True if the `PhotoVoltaicUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_photo_voltaic_units(self, table: TablePhotoVoltaicUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val photoVoltaicUnit = PhotoVoltaicUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadPowerElectronicsUnit(photoVoltaicUnit, table, result_set) and self._add_or_throw(photoVoltaicUnit)

    private fun loadPowerElectronicsUnit(powerElectronicsUnit: PowerElectronicsUnit, table: TablePowerElectronicsUnits, result_set: ResultSet) -> bool:
        powerElectronicsUnit
            powerElectronicsConnection = self._ensure_get(
                result_set.get_string(table.power_electronics_connection_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )
            powerElectronicsConnection?.addUnit(this)

            maxP = result_set.get_int(table.max_p.query_index, on_none=None)
            minP = result_set.get_int(table.min_p.query_index, on_none=None)

        return loadEquipment(powerElectronicsUnit, table, result_set)

    """
    Create a `PowerElectronicsWindUnit` and populate its fields from `TablePowerElectronicsWindUnits`.

    :param table: The database table to read the `PowerElectronicsWindUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerElectronicsWindUnit`.
    :param set_identifier: A callback to register the mRID of this `PowerElectronicsWindUnit` for logging purposes.

    :return: True if the `PowerElectronicsWindUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_power_electronics_wind_units(self, table: TablePowerElectronicsWindUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val powerElectronicsWindUnit = PowerElectronicsWindUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadPowerElectronicsUnit(powerElectronicsWindUnit, table, result_set) and self._add_or_throw(powerElectronicsWindUnit)

    #######################
    # IEC61970 Base Wires #
    #######################

    """
    Create an `AcLineSegment` and populate its fields from `TableAcLineSegments`.

    :param table: The database table to read the `AcLineSegment` fields from.
    :param result_set: The record in the database table containing the fields for this `AcLineSegment`.
    :param set_identifier: A callback to register the mRID of this `AcLineSegment` for logging purposes.

    :return: True if the `AcLineSegment` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_ac_line_segments(self, table: TableAcLineSegments, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val acLineSegment = AcLineSegment(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            perLengthSequenceImpedance =
                self._ensure_get(
                    result_set.get_string(table.per_length_sequence_impedance_mrid.query_index, on_none=None),
                    typeNameAndMRID()
                )

        return loadConductor(acLineSegment, table, result_set) and self._add_or_throw(acLineSegment)

    """
    Create a `Breaker` and populate its fields from `TableBreakers`.

    :param table: The database table to read the `Breaker` fields from.
    :param result_set: The record in the database table containing the fields for this `Breaker`.
    :param set_identifier: A callback to register the mRID of this `Breaker` for logging purposes.

    :return: True if the `Breaker` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_breakers(self, table: TableBreakers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val breaker = Breaker(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            inTransitTime = result_set.get_double(table.in_transit_time.query_index, on_none=None)

        return loadProtectedSwitch(breaker, table, result_set) and self._add_or_throw(breaker)

    """
    Create a `LoadBreakSwitch` and populate its fields from `TableLoadBreakSwitches`.

    :param table: The database table to read the `LoadBreakSwitch` fields from.
    :param result_set: The record in the database table containing the fields for this `LoadBreakSwitch`.
    :param set_identifier: A callback to register the mRID of this `LoadBreakSwitch` for logging purposes.

    :return: True if the `LoadBreakSwitch` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_load_break_switches(self, table: TableLoadBreakSwitches, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val loadBreakSwitch = LoadBreakSwitch(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadProtectedSwitch(loadBreakSwitch, table, result_set) and self._add_or_throw(loadBreakSwitch)

    """
    Create a `BusbarSection` and populate its fields from `TableBusbarSections`.

    :param table: The database table to read the `BusbarSection` fields from.
    :param result_set: The record in the database table containing the fields for this `BusbarSection`.
    :param set_identifier: A callback to register the mRID of this `BusbarSection` for logging purposes.

    :return: True if the `BusbarSection` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_busbar_sections(self, table: TableBusbarSections, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val busbarSection = BusbarSection(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadConnector(busbarSection, table, result_set) and self._add_or_throw(busbarSection)

    private fun loadConductor(conductor: Conductor, table: TableConductors, result_set: ResultSet) -> bool:
        conductor
            length = result_set.get_double(table.length.query_index, on_none=None)
            assetInfo = self._ensure_get(
                result_set.get_string(table.wire_info_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )

        return loadConductingEquipment(conductor, table, result_set)

    private fun loadConnector(connector: Connector, table: TableConnectors, result_set: ResultSet) -> bool:
        return self.loadConductingEquipment(connector, table, result_set)

    """
    Create a `Disconnector` and populate its fields from `TableDisconnectors`.

    :param table: The database table to read the `Disconnector` fields from.
    :param result_set: The record in the database table containing the fields for this `Disconnector`.
    :param set_identifier: A callback to register the mRID of this `Disconnector` for logging purposes.

    :return: True if the `Disconnector` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_disconnectors(self, table: TableDisconnectors, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val disconnector = Disconnector(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadSwitch(disconnector, table, result_set) and self._add_or_throw(disconnector)

    private fun loadEnergyConnection(
        energyConnection: EnergyConnection,
        table: TableEnergyConnections,
        result_set: ResultSet
    ) -> bool:
        return self.loadConductingEquipment(energyConnection, table, result_set)

    """
    Create an `EnergyConsumer` and populate its fields from `TableEnergyConsumers`.

    :param table: The database table to read the `EnergyConsumer` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergyConsumer`.
    :param set_identifier: A callback to register the mRID of this `EnergyConsumer` for logging purposes.

    :return: True if the `EnergyConsumer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_energy_consumers(self, table: TableEnergyConsumers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val energyConsumer = EnergyConsumer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            customerCount = result_set.get_int(table.customer_count.query_index, on_none=None)
            grounded = result_set.get_boolean(table.grounded.query_index)
            p = result_set.get_double(table.p.query_index, on_none=None)
            q = result_set.get_double(table.q.query_index, on_none=None)
            pFixed = result_set.get_double(table.p_fixed.query_index, on_none=None)
            qFixed = result_set.get_double(table.q_fixed.query_index, on_none=None)
            phaseConnection = PhaseShuntConnectionKind[result_set.get_string(table.phase_connection.query_index)]

        return loadEnergyConnection(energyConsumer, table, result_set) and self._add_or_throw(energyConsumer)

    """
    Create an `EnergyConsumerPhase` and populate its fields from `TableEnergyConsumerPhases`.

    :param table: The database table to read the `EnergyConsumerPhase` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergyConsumerPhase`.
    :param set_identifier: A callback to register the mRID of this `EnergyConsumerPhase` for logging purposes.

    :return: True if the `EnergyConsumerPhase` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_energy_consumer_phases(self, table: TableEnergyConsumerPhases, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val energyConsumerPhase = EnergyConsumerPhase(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            energyConsumer =
                self._ensure_get(result_set.get_string(table.energy_consumer_mrid.query_index))
            energyConsumer?.addPhase(this)

            phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]
            p = result_set.get_double(table.p.query_index, on_none=None)
            q = result_set.get_double(table.q.query_index, on_none=None)
            pFixed = result_set.get_double(table.p_fixed.query_index, on_none=None)
            qFixed = result_set.get_double(table.q_fixed.query_index, on_none=None)

        return loadPowerSystemResource(energyConsumerPhase, table, result_set) and self._add_or_throw(
            energyConsumerPhase
        )

    """
    Create an `EnergySource` and populate its fields from `TableEnergySources`.

    :param table: The database table to read the `EnergySource` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergySource`.
    :param set_identifier: A callback to register the mRID of this `EnergySource` for logging purposes.

    :return: True if the `EnergySource` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_energy_sources(self, table: TableEnergySources, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val energySource = EnergySource(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            activePower = result_set.get_double(table.active_power.query_index, on_none=None)
            reactivePower = result_set.get_double(table.reactive_power.query_index, on_none=None)
            voltageAngle = result_set.get_double(table.voltage_angle.query_index, on_none=None)
            voltageMagnitude = result_set.get_double(table.voltage_magnitude.query_index, on_none=None)
            pMax = result_set.get_double(table.p_max.query_index, on_none=None)
            pMin = result_set.get_double(table.p_min.query_index, on_none=None)
            r = result_set.get_double(table.r.query_index, on_none=None)
            r0 = result_set.get_double(table.r0.query_index, on_none=None)
            rn = result_set.get_double(table.rn.query_index, on_none=None)
            x = result_set.get_double(table.x.query_index, on_none=None)
            x0 = result_set.get_double(table.x0.query_index, on_none=None)
            xn = result_set.get_double(table.xn.query_index, on_none=None)
            isExternalGrid = result_set.get_boolean(table.is_external_grid.query_index)
            rMin = result_set.get_double(table.r_min.query_index, on_none=None)
            rnMin = result_set.get_double(table.rn_min.query_index, on_none=None)
            r0Min = result_set.get_double(table.r0_min.query_index, on_none=None)
            xMin = result_set.get_double(table.x_min.query_index, on_none=None)
            xnMin = result_set.get_double(table.xn_min.query_index, on_none=None)
            x0Min = result_set.get_double(table.x0_min.query_index, on_none=None)
            rMax = result_set.get_double(table.r_max.query_index, on_none=None)
            rnMax = result_set.get_double(table.rn_max.query_index, on_none=None)
            r0Max = result_set.get_double(table.r0_max.query_index, on_none=None)
            xMax = result_set.get_double(table.x_max.query_index, on_none=None)
            xnMax = result_set.get_double(table.xn_max.query_index, on_none=None)
            x0Max = result_set.get_double(table.x0_max.query_index, on_none=None)

        return loadEnergyConnection(energySource, table, result_set) and self._add_or_throw(energySource)

    """
    Create an `EnergySourcePhase` and populate its fields from `TableEnergySourcePhases`.

    :param table: The database table to read the `EnergySourcePhase` fields from.
    :param result_set: The record in the database table containing the fields for this `EnergySourcePhase`.
    :param set_identifier: A callback to register the mRID of this `EnergySourcePhase` for logging purposes.

    :return: True if the `EnergySourcePhase` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_energy_source_phases(self, table: TableEnergySourcePhases, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val energySourcePhase = EnergySourcePhase(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            energySource =
                self._ensure_get(result_set.get_string(table.energy_source_mrid.query_index))
            energySource?.addPhase(this)

            phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]

        return loadPowerSystemResource(energySourcePhase, table, result_set) and self._add_or_throw(
            energySourcePhase
        )

    """
    Create a `Fuse` and populate its fields from `TableFuses`.

    :param table: The database table to read the `Fuse` fields from.
    :param result_set: The record in the database table containing the fields for this `Fuse`.
    :param set_identifier: A callback to register the mRID of this `Fuse` for logging purposes.

    :return: True if the `Fuse` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_fuses(self, table: TableFuses, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val fuse = Fuse(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            function = self._ensure_get(result_set.get_string(table.function_mrid.query_index))

        return loadSwitch(fuse, table, result_set) and self._add_or_throw(fuse)

    """
    Create a `Ground` and populate its fields from `TableGrounds`.

    :param table: The database table to read the `Ground` fields from.
    :param result_set: The record in the database table containing the fields for this `Ground`.
    :param set_identifier: A callback to register the mRID of this `Ground` for logging purposes.

    :return: True if the `Ground` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_grounds(self, table: TableGrounds, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val ground = Ground(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadConductingEquipment(ground, table, result_set) and self._add_or_throw(ground)

    """
    Create a `GroundDisconnector` and populate its fields from `TableGroundDisconnectors`.

    :param table: The database table to read the `GroundDisconnector` fields from.
    :param result_set: The record in the database table containing the fields for this `GroundDisconnector`.
    :param set_identifier: A callback to register the mRID of this `GroundDisconnector` for logging purposes.

    :return: True if the `GroundDisconnector` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_ground_disconnectors(self, table: TableGroundDisconnectors, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val groundDisconnector = GroundDisconnector(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadSwitch(groundDisconnector, table, result_set) and self._add_or_throw(groundDisconnector)

    """
    Create a `Jumper` and populate its fields from `TableJumpers`.

    :param table: The database table to read the `Jumper` fields from.
    :param result_set: The record in the database table containing the fields for this `Jumper`.
    :param set_identifier: A callback to register the mRID of this `Jumper` for logging purposes.

    :return: True if the `Jumper` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_jumpers(self, table: TableJumpers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val jumper = Jumper(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadSwitch(jumper, table, result_set) and self._add_or_throw(jumper)

    """
    Create a `Junction` and populate its fields from `TableJunctions`.

    :param table: The database table to read the `Junction` fields from.
    :param result_set: The record in the database table containing the fields for this `Junction`.
    :param set_identifier: A callback to register the mRID of this `Junction` for logging purposes.

    :return: True if the `Junction` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_junctions(self, table: TableJunctions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val junction = Junction(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadConnector(junction, table, result_set) and self._add_or_throw(junction)

    private fun loadLine(line: Line, table: TableLines, result_set: ResultSet) -> bool:
        return self.loadEquipmentContainer(line, table, result_set)

    """
    Create a `LinearShuntCompensator` and populate its fields from `TableLinearShuntCompensators`.

    :param table: The database table to read the `LinearShuntCompensator` fields from.
    :param result_set: The record in the database table containing the fields for this `LinearShuntCompensator`.
    :param set_identifier: A callback to register the mRID of this `LinearShuntCompensator` for logging purposes.

    :return: True if the `LinearShuntCompensator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_linear_shunt_compensators(self, table: TableLinearShuntCompensators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val linearShuntCompensator =
            LinearShuntCompensator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
                b0PerSection = result_set.get_double(table.b0_per_section.query_index, on_none=None)
                bPerSection = result_set.get_double(table.b_per_section.query_index, on_none=None)
                g0PerSection = result_set.get_double(table.g0_per_section.query_index, on_none=None)
                gPerSection = result_set.get_double(table.g_per_section.query_index, on_none=None)

        return loadShuntCompensator(linearShuntCompensator, table, result_set) and self._add_or_throw(
            linearShuntCompensator
        )

    private fun loadPerLengthImpedance(perLengthImpedance: PerLengthImpedance, table: TablePerLengthImpedances, result_set: ResultSet) -> bool:
        return self.loadPerLengthLineParameter(perLengthImpedance, table, result_set)

    private fun loadPerLengthLineParameter(perLengthLineParameter: PerLengthLineParameter, table: TablePerLengthLineParameters, result_set: ResultSet) -> bool:
        return self._load_identified_object(perLengthLineParameter, table, result_set)

    """
    Create a `PerLengthSequenceImpedance` and populate its fields from `TablePerLengthSequenceImpedances`.

    :param table: The database table to read the `PerLengthSequenceImpedance` fields from.
    :param result_set: The record in the database table containing the fields for this `PerLengthSequenceImpedance`.
    :param set_identifier: A callback to register the mRID of this `PerLengthSequenceImpedance` for logging purposes.

    :return: True if the `PerLengthSequenceImpedance` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_per_length_sequence_impedances(self, table: TablePerLengthSequenceImpedances, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val perLengthSequenceImpedance =
            PerLengthSequenceImpedance(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
                r = result_set.get_double(table.r.query_index, on_none=None)
                x = result_set.get_double(table.x.query_index, on_none=None)
                r0 = result_set.get_double(table.r0.query_index, on_none=None)
                x0 = result_set.get_double(table.x0.query_index, on_none=None)
                bch = result_set.get_double(table.bch.query_index, on_none=None)
                gch = result_set.get_double(table.gch.query_index, on_none=None)
                b0ch = result_set.get_double(table.b0ch.query_index, on_none=None)
                g0ch = result_set.get_double(table.g0ch.query_index, on_none=None)

        return loadPerLengthImpedance(perLengthSequenceImpedance, table, result_set) and self._add_or_throw(
            perLengthSequenceImpedance
        )

    """
    Create a `PowerElectronicsConnection` and populate its fields from `TablePowerElectronicsConnections`.

    :param table: The database table to read the `PowerElectronicsConnection` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerElectronicsConnection`.
    :param set_identifier: A callback to register the mRID of this `PowerElectronicsConnection` for logging purposes.

    :return: True if the `PowerElectronicsConnection` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_power_electronics_connections(self, table: TablePowerElectronicsConnections, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val powerElectronicsConnection = PowerElectronicsConnection(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            maxIFault = result_set.get_int(table.max_i_fault.query_index, on_none=None)
            maxQ = result_set.get_double(table.max_q.query_index, on_none=None)
            minQ = result_set.get_double(table.min_q.query_index, on_none=None)
            p = result_set.get_double(table.p.query_index, on_none=None)
            q = result_set.get_double(table.q.query_index, on_none=None)
            ratedU = result_set.get_int(table.rated_u.query_index, on_none=None)
            ratedS = result_set.get_int(table.rated_s.query_index, on_none=None)
            inverterStandard = result_set.get_string(table.inverter_standard.query_index, on_none=None)
            sustainOpOvervoltLimit = result_set.get_int(table.sustain_op_overvolt_limit.query_index, on_none=None)
            stopAtOverFreq = result_set.get_float(table.stop_at_over_freq.query_index, on_none=None)
            stopAtUnderFreq = result_set.get_float(table.stop_at_under_freq.query_index, on_none=None)
            invVoltWattRespMode = result_set.get_boolean(table.inv_volt_watt_resp_mode.query_index, on_none=None)
            invWattRespV1 = result_set.get_int(table.inv_watt_resp_v1.query_index, on_none=None)
            invWattRespV2 = result_set.get_int(table.inv_watt_resp_v2.query_index, on_none=None)
            invWattRespV3 = result_set.get_int(table.inv_watt_resp_v3.query_index, on_none=None)
            invWattRespV4 = result_set.get_int(table.inv_watt_resp_v4.query_index, on_none=None)
            invWattRespPAtV1 = result_set.get_float(table.inv_watt_resp_p_at_v1.query_index, on_none=None)
            invWattRespPAtV2 = result_set.get_float(table.inv_watt_resp_p_at_v2.query_index, on_none=None)
            invWattRespPAtV3 = result_set.get_float(table.inv_watt_resp_p_at_v3.query_index, on_none=None)
            invWattRespPAtV4 = result_set.get_float(table.inv_watt_resp_p_at_v4.query_index, on_none=None)
            invVoltVarRespMode = result_set.get_boolean(table.inv_volt_var_resp_mode.query_index, on_none=None)
            invVarRespV1 = result_set.get_int(table.inv_var_resp_v1.query_index, on_none=None)
            invVarRespV2 = result_set.get_int(table.inv_var_resp_v2.query_index, on_none=None)
            invVarRespV3 = result_set.get_int(table.inv_var_resp_v3.query_index, on_none=None)
            invVarRespV4 = result_set.get_int(table.inv_var_resp_v4.query_index, on_none=None)
            invVarRespQAtV1 = result_set.get_float(table.inv_var_resp_q_at_v1.query_index, on_none=None)
            invVarRespQAtV2 = result_set.get_float(table.inv_var_resp_q_at_v2.query_index, on_none=None)
            invVarRespQAtV3 = result_set.get_float(table.inv_var_resp_q_at_v3.query_index, on_none=None)
            invVarRespQAtV4 = result_set.get_float(table.inv_var_resp_q_at_v4.query_index, on_none=None)
            invReactivePowerMode = result_set.get_boolean(table.inv_reactive_power_mode.query_index, on_none=None)
            invFixReactivePower = result_set.get_float(table.inv_fix_reactive_power.query_index, on_none=None)

        return loadRegulatingCondEq(powerElectronicsConnection, table, result_set) and self._add_or_throw(powerElectronicsConnection)

    """
    Create a `PowerElectronicsConnectionPhase` and populate its fields from `TablePowerElectronicsConnectionPhases`.

    :param table: The database table to read the `PowerElectronicsConnectionPhase` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerElectronicsConnectionPhase`.
    :param set_identifier: A callback to register the mRID of this `PowerElectronicsConnectionPhase` for logging purposes.

    :return: True if the `PowerElectronicsConnectionPhase` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_power_electronics_connection_phases(self, table: TablePowerElectronicsConnectionPhases, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val powerElectronicsConnectionPhase = PowerElectronicsConnectionPhase(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            powerElectronicsConnection =
                self._ensure_get(result_set.get_string(table.power_electronics_connection_mrid.query_index))
            powerElectronicsConnection?.addPhase(this)

            phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]
            p = result_set.get_double(table.p.query_index, on_none=None)
            phase = SinglePhaseKind[result_set.get_string(table.phase.query_index)]
            q = result_set.get_double(table.q.query_index, on_none=None)

        return loadPowerSystemResource(powerElectronicsConnectionPhase, table, result_set) and self._add_or_throw(powerElectronicsConnectionPhase)

    """
    Create a `PowerTransformer` and populate its fields from `TablePowerTransformers`.

    :param table: The database table to read the `PowerTransformer` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerTransformer`.
    :param set_identifier: A callback to register the mRID of this `PowerTransformer` for logging purposes.

    :return: True if the `PowerTransformer` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_power_transformers(self, table: TablePowerTransformers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val powerTransformer = PowerTransformer(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            vectorGroup = VectorGroup[result_set.get_string(table.vector_group.query_index)]
            transformerUtilisation = result_set.get_double(table.transformer_utilisation.query_index, on_none=None)
            constructionKind = TransformerConstructionKind[result_set.get_string(table.construction_kind.query_index)]
            function = TransformerFunctionKind[result_set.get_string(table.function.query_index)]
            assetInfo = self._ensure_get(
                result_set.get_string(table.power_transformer_info_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )

        return loadConductingEquipment(
            powerTransformer,
            table,
            result_set
        ) and self._add_or_throw(powerTransformer)

    """
    Create a `PowerTransformerEnd` and populate its fields from `TablePowerTransformerEnds`.

    :param table: The database table to read the `PowerTransformerEnd` fields from.
    :param result_set: The record in the database table containing the fields for this `PowerTransformerEnd`.
    :param set_identifier: A callback to register the mRID of this `PowerTransformerEnd` for logging purposes.

    :return: True if the `PowerTransformerEnd` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_power_transformer_ends(self, table: TablePowerTransformerEnds, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val powerTransformerEnd = PowerTransformerEnd(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            endNumber = result_set.get_int(table.end_number.query_index)
            powerTransformer = self._ensure_get(result_set.get_string(table.power_transformer_mrid.query_index))
            powerTransformer?.addEnd(this)

            connectionKind = WindingConnection[result_set.get_string(table.connection_kind.query_index)]
            phaseAngleClock = result_set.get_int(table.phase_angle_clock.query_index, on_none=None)
            b = result_set.get_double(table.b.query_index, on_none=None)
            b0 = result_set.get_double(table.b0.query_index, on_none=None)
            g = result_set.get_double(table.g.query_index, on_none=None)
            g0 = result_set.get_double(table.g0.query_index, on_none=None)
            r = result_set.get_double(table.r.query_index, on_none=None)
            r0 = result_set.get_double(table.r0.query_index, on_none=None)
            ratedU = result_set.get_int(table.rated_u.query_index, on_none=None)
            x = result_set.get_double(table.x.query_index, on_none=None)
            x0 = result_set.get_double(table.x0.query_index, on_none=None)

        return loadTransformerEnd(powerTransformerEnd, table, result_set) and self._add_or_throw(powerTransformerEnd)

    """
    Adds a rating to a `PowerTransformerEnd` from `TablePowerTransformerEndRatings`.

    :param table: The database table to read the rating fields from.
    :param result_set: The record in the database table containing the fields for this rating.
    :param set_identifier: A callback to register the mRID of this rating for logging purposes.

    :return: True if the rating was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_power_transformer_end_ratings(self, table: TablePowerTransformerEndRatings, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        # Note TablePowerTransformerEndRatings.selectSql ensures we process ratings in the correct order.
        val powerTransformerEndMRID = result_set.get_string(table.power_transformer_end_mrid.query_index)
        val ratedS = result_set.get_int(table.rated_s.query_index)
        set_identifier(f"{powerTransformerEndMRID}.s{ratedS}")

        val pte = self._ensure_get(powerTransformerEndMRID, f"{powerTransformerEndMRID}.s{ratedS}")
 , PowerTransformerEnd       val coolingType = TransformerCoolingType[result_set.get_string(table.cooling_type.query_index)]
        pte?.addRating(ratedS, coolingType)

        return True

    private fun loadProtectedSwitch(protectedSwitch: ProtectedSwitch, table: TableProtectedSwitches, result_set: ResultSet) -> bool:
        protectedSwitch
            breakingCapacity = result_set.get_int(table.breaking_capacity.query_index, on_none=None)

        return loadSwitch(protectedSwitch, table, result_set)

    """
    Create a `RatioTapChanger` and populate its fields from `TableRatioTapChangers`.

    :param table: The database table to read the `RatioTapChanger` fields from.
    :param result_set: The record in the database table containing the fields for this `RatioTapChanger`.
    :param set_identifier: A callback to register the mRID of this `RatioTapChanger` for logging purposes.

    :return: True if the `RatioTapChanger` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_ratio_tap_changers(self, table: TableRatioTapChangers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val ratioTapChanger = RatioTapChanger(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            transformerEnd = self._ensure_get(
                result_set.get_string(table.transformer_end_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )
            transformerEnd?.ratioTapChanger = this

            stepVoltageIncrement = result_set.get_double(table.step_voltage_increment.query_index, on_none=None)

        return loadTapChanger(ratioTapChanger, table, result_set) and self._add_or_throw(ratioTapChanger)

    """
    Create a `Recloser` and populate its fields from `TableReclosers`.

    :param table: The database table to read the `Recloser` fields from.
    :param result_set: The record in the database table containing the fields for this `Recloser`.
    :param set_identifier: A callback to register the mRID of this `Recloser` for logging purposes.

    :return: True if the `Recloser` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_reclosers(self, table: TableReclosers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val recloser = Recloser(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadProtectedSwitch(recloser, table, result_set) and self._add_or_throw(recloser)

    private fun loadRegulatingCondEq(
        regulatingCondEq: RegulatingCondEq,
        table: TableRegulatingCondEq,
        result_set: ResultSet
    ) -> bool:
        regulatingCondEq
            controlEnabled = result_set.get_boolean(table.control_enabled.query_index)
            # We use a resolver here because there is an ordering conflict between terminals, RegulatingCondEq, and RegulatingControls
            # We check this resolver has actually been resolved in the postLoad of the database read and throw there if it hasn't.
            service.resolveOrDeferReference(Resolvers.regulatingControl(this), result_set.get_string(table.regulating_control_mrid.query_index, on_none=None))

        return loadEnergyConnection(regulatingCondEq, table, result_set)

    private fun loadRegulatingControl(
        regulatingControl: RegulatingControl,
        table: TableRegulatingControls,
        result_set: ResultSet
    ) -> bool:
        regulatingControl
            discrete = result_set.get_boolean(table.discrete.query_index, on_none=None)
            mode = RegulatingControlModeKind[result_set.get_string(table.mode.query_index)]
            monitoredPhase = PhaseCode[result_set.get_string(table.monitored_phase.query_index)]
            targetDeadband = result_set.get_float(table.target_deadband.query_index, on_none=None)
            targetValue = result_set.get_double(table.target_value.query_index, on_none=None)
            enabled = result_set.get_boolean(table.enabled.query_index, on_none=None)
            maxAllowedTargetValue = result_set.get_double(table.max_allowed_target_value.query_index, on_none=None)
            minAllowedTargetValue = result_set.get_double(table.min_allowed_target_value.query_index, on_none=None)
            ratedCurrent = result_set.get_double(table.rated_current.query_index, on_none=None)
            terminal = self._ensure_get(result_set.get_string(table.terminal_mrid.query_index, on_none=None))

        return loadPowerSystemResource(regulatingControl, table, result_set)

    """
    Create a `SeriesCompensator` and populate its fields from `TableSeriesCompensators`.

    :param table: The database table to read the `SeriesCompensator` fields from.
    :param result_set: The record in the database table containing the fields for this `SeriesCompensator`.
    :param set_identifier: A callback to register the mRID of this `SeriesCompensator` for logging purposes.

    :return: True if the `SeriesCompensator` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_series_compensators(self, table: TableSeriesCompensators, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val seriesCompensator = SeriesCompensator(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            r = result_set.get_double(table.r.query_index, on_none=None)
            r0 = result_set.get_double(table.r0.query_index, on_none=None)
            x = result_set.get_double(table.x.query_index, on_none=None)
            x0 = result_set.get_double(table.x0.query_index, on_none=None)
            varistorRatedCurrent = result_set.get_int(table.varistor_rated_current.query_index, on_none=None)
            varistorVoltageThreshold = result_set.get_int(table.varistor_voltage_threshold.query_index, on_none=None)

        return loadConductingEquipment(seriesCompensator, table, result_set) and self._add_or_throw(seriesCompensator)

    private fun loadShuntCompensator(
        shuntCompensator: ShuntCompensator,
        table: TableShuntCompensators,
        result_set: ResultSet
    ) -> bool:
        shuntCompensator
            assetInfo = self._ensure_get(
                result_set.get_string(table.shunt_compensator_info_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )

            grounded = result_set.get_boolean(table.grounded.query_index)
            nomU = result_set.get_int(table.nom_u.query_index, on_none=None)
            phaseConnection = PhaseShuntConnectionKind[result_set.get_string(table.phase_connection.query_index)]
            sections = result_set.get_double(table.sections.query_index, on_none=None)

        return loadRegulatingCondEq(shuntCompensator, table, result_set)

    private fun loadSwitch(switch: Switch, table: TableSwitches, result_set: ResultSet) -> bool:
        switch
            assetInfo = self._ensure_get(result_set.get_string(table.switch_info_mrid.query_index, on_none=None))
            ratedCurrent = result_set.get_int(table.rated_current.query_index, on_none=None)
            normalOpen = result_set.get_int(table.normal_open.query_index)
            open = result_set.get_int(table.open.query_index)

        return loadConductingEquipment(switch, table, result_set)

    private fun loadTapChanger(tapChanger: TapChanger, table: TableTapChangers, result_set: ResultSet) -> bool:
        tapChanger
            controlEnabled = result_set.get_boolean(table.control_enabled.query_index)
            highStep = result_set.get_int(table.high_step.query_index, on_none=None)
            lowStep = result_set.get_int(table.low_step.query_index, on_none=None)
            neutralStep = result_set.get_int(table.neutral_step.query_index, on_none=None)
            neutralU = result_set.get_int(table.neutral_u.query_index, on_none=None)
            normalStep = result_set.get_int(table.normal_step.query_index, on_none=None)
            step = result_set.get_double(table.step.query_index, on_none=None)
            tapChangerControl = self._ensure_get(result_set.get_string(table.tap_changer_control_mrid.query_index, on_none=None))

        return loadPowerSystemResource(tapChanger, table, result_set)

    """
    Create a `TapChangerControl` and populate its fields from `TableTapChangerControls`.

    :param table: The database table to read the `TapChangerControl` fields from.
    :param result_set: The record in the database table containing the fields for this `TapChangerControl`.
    :param set_identifier: A callback to register the mRID of this `TapChangerControl` for logging purposes.

    :return: True if the `TapChangerControl` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_tap_changer_controls(self, table: TableTapChangerControls, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val tapChangerControl = TapChangerControl(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            limitVoltage = result_set.get_int(table.limit_voltage.query_index, on_none=None)
            lineDropCompensation = result_set.get_boolean(table.line_drop_compensation.query_index, on_none=None)
            lineDropR = result_set.get_double(table.line_drop_r.query_index, on_none=None)
            lineDropX = result_set.get_double(table.line_drop_x.query_index, on_none=None)
            reverseLineDropR = result_set.get_double(table.reverse_line_drop_r.query_index, on_none=None)
            reverseLineDropX = result_set.get_double(table.reverse_line_drop_x.query_index, on_none=None)
            forwardLDCBlocking = result_set.get_boolean(table.forward_ldc_blocking.query_index, on_none=None)
            timeDelay = result_set.get_double(table.time_delay.query_index, on_none=None)
            coGenerationEnabled = result_set.get_boolean(table.co_generation_enabled.query_index, on_none=None)

        return loadRegulatingControl(tapChangerControl, table, result_set) and self._add_or_throw(tapChangerControl)

    private fun loadTransformerEnd(transformerEnd: TransformerEnd, table: TableTransformerEnds, result_set: ResultSet) -> bool:
        transformerEnd
            terminal = self._ensure_get(result_set.get_string(table.terminal_mrid.query_index, on_none=None))
            baseVoltage = self._ensure_get(result_set.get_string(table.base_voltage_mrid.query_index, on_none=None))
            grounded = result_set.get_boolean(table.grounded.query_index)
            rGround = result_set.get_double(table.r_ground.query_index, on_none=None)
            xGround = result_set.get_double(table.x_ground.query_index, on_none=None)
            starImpedance = self._ensure_get(result_set.get_string(table.star_impedance_mrid.query_index, on_none=None))

        return self._load_identified_object(transformerEnd, table, result_set)

    """
    Create a `TransformerStarImpedance` and populate its fields from `TableTransformerStarImpedances`.

    :param table: The database table to read the `TransformerStarImpedance` fields from.
    :param result_set: The record in the database table containing the fields for this `TransformerStarImpedance`.
    :param set_identifier: A callback to register the mRID of this `TransformerStarImpedance` for logging purposes.

    :return: True if the `TransformerStarImpedance` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_transformer_star_impedances(self, table: TableTransformerStarImpedances, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val transformerStarImpedance = TransformerStarImpedance(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            r = result_set.get_double(table.r.query_index, on_none=None)
            r0 = result_set.get_double(table.r0.query_index, on_none=None)
            x = result_set.get_double(table.x.query_index, on_none=None)
            x0 = result_set.get_double(table.x0.query_index, on_none=None)

            transformerEndInfo = self._ensure_get(result_set.get_string(table.transformer_end_info_mrid.query_index, on_none=None))
            transformerEndInfo?.transformerStarImpedance = this

        return self._load_identified_object(transformerStarImpedance, table, result_set) and self._add_or_throw(transformerStarImpedance)

    ###############################
    # IEC61970 InfIEC61970 Feeder #
    ###############################

    """
    Create a `Circuit` and populate its fields from `TableCircuits`.

    :param table: The database table to read the `Circuit` fields from.
    :param result_set: The record in the database table containing the fields for this `Circuit`.
    :param set_identifier: A callback to register the mRID of this `Circuit` for logging purposes.

    :return: True if the `Circuit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_circuits(self, table: TableCircuits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val circuit = Circuit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            loop = self._ensure_get(result_set.get_string(table.loop_mrid.query_index, on_none=None))
            loop?.addCircuit(this)

        return loadLine(circuit, table, result_set) and self._add_or_throw(circuit)

    """
    Create a `Loop` and populate its fields from `TableLoops`.

    :param table: The database table to read the `Loop` fields from.
    :param result_set: The record in the database table containing the fields for this `Loop`.
    :param set_identifier: A callback to register the mRID of this `Loop` for logging purposes.

    :return: True if the `Loop` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_loops(self, table: TableLoops, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val loop = Loop(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(loop, table, result_set) and self._add_or_throw(loop)

    """
    Create a `LvFeeder` and populate its fields from `TableLvFeeders`.

    :param table: The database table to read the `LvFeeder` fields from.
    :param result_set: The record in the database table containing the fields for this `LvFeeder`.
    :param set_identifier: A callback to register the mRID of this `LvFeeder` for logging purposes.

    :return: True if the `LvFeeder` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_lv_feeders(self, table: TableLvFeeders, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val lvFeeder = LvFeeder(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
            normalHeadTerminal = self._ensure_get(
                result_set.get_string(table.normal_head_terminal_mrid.query_index, on_none=None),
                typeNameAndMRID()
            )

        return loadEquipmentContainer(lvFeeder, table, result_set) and self._add_or_throw(lvFeeder)

    ####################################################
    # IEC61970 InfIEC61970 Wires Generation Production #
    ####################################################

    """
    Create an `EvChargingUnit` and populate its fields from `TableEvChargingUnits`.

    :param table: The database table to read the `EvChargingUnit` fields from.
    :param result_set: The record in the database table containing the fields for this `EvChargingUnit`.
    :param set_identifier: A callback to register the mRID of this `EvChargingUnit` for logging purposes.

    :return: True if the `EvChargingUnit` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_ev_charging_units(self, table: TableEvChargingUnits, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val evChargingUnit = EvChargingUnit(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return loadPowerElectronicsUnit(evChargingUnit, table, result_set) and self._add_or_throw(evChargingUnit)

    ################
    # Associations #
    ################

    """
    Create a `set_identifier` and populate its fields from `TableAssetOrganisationRolesAssets`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_asset_organisation_roles_assets(self, table: TableAssetOrganisationRolesAssets, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val assetOrganisationRoleMRID = set_identifier(result_set.get_string(table.asset_organisation_role_mrid.query_index))
        set_identifier(f"{assetOrganisationRoleMRID}-to-UNKNOWN")

        val assetMRID = result_set.get_string(table.asset_mrid.query_index)
        val id = set_identifier(f"{assetOrganisationRoleMRID}-to-{assetMRID}")

        val typeNameAndMRID = "AssetOrganisationRole to Asset association {id}"
        val assetOrganisationRole = service.getOrThrow<AssetOrganisationRole>(assetOrganisationRoleMRID, typeNameAndMRID)
        val asset = service.getOrThrow<Asset>(assetMRID, typeNameAndMRID)

        asset.addOrganisationRole(assetOrganisationRole)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableEquipmentEquipmentContainers`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_equipment_equipment_containers(self, table: TableEquipmentEquipmentContainers, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val equipmentMRID = set_identifier(result_set.get_string(table.equipment_mrid.query_index))
        set_identifier(f"{equipmentMRID}-to-UNKNOWN")

        val equipmentContainerMRID = result_set.get_string(table.equipment_container_mrid.query_index)
        val id = set_identifier(f"{equipmentMRID}-to-{equipmentContainerMRID}")

        val typeNameAndMRID = "Equipment to EquipmentContainer association {id}"
        val equipment = service.getOrThrow<Equipment>(equipmentMRID, typeNameAndMRID)
        val equipmentContainer = service.getOrThrow<EquipmentContainer>(equipmentContainerMRID, typeNameAndMRID)

        equipmentContainer.addEquipment(equipment)
        equipment.addContainer(equipmentContainer)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableEquipmentOperationalRestrictions`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_equipment_operational_restrictions(self, table: TableEquipmentOperationalRestrictions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val equipmentMRID = set_identifier(result_set.get_string(table.equipment_mrid.query_index))
        set_identifier(f"{equipmentMRID}-to-UNKNOWN")

        val operationalRestrictionMRID = result_set.get_string(table.operational_restriction_mrid.query_index)
        val id = set_identifier(f"{equipmentMRID}-to-{operationalRestrictionMRID}")

        val typeNameAndMRID = "Equipment to OperationalRestriction association {id}"
        val equipment = service.getOrThrow<Equipment>(equipmentMRID, typeNameAndMRID)
        val operationalRestriction = service.getOrThrow<OperationalRestriction>(operationalRestrictionMRID, typeNameAndMRID)

        operationalRestriction.addEquipment(equipment)
        equipment.addOperationalRestriction(operationalRestriction)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableEquipmentUsagePoints`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_equipment_usage_points(self, table: TableEquipmentUsagePoints, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val equipmentMRID = set_identifier(result_set.get_string(table.equipment_mrid.query_index))
        set_identifier(f"{equipmentMRID}-to-UNKNOWN")

        val usagePointMRID = result_set.get_string(table.usage_point_mrid.query_index)
        val id = set_identifier(f"{equipmentMRID}-to-{usagePointMRID}")

        val typeNameAndMRID = "Equipment to UsagePoint association {id}"
        val equipment = service.getOrThrow<Equipment>(equipmentMRID, typeNameAndMRID)
        val usagePoint = service.getOrThrow<UsagePoint>(usagePointMRID, typeNameAndMRID)

        usagePoint.addEquipment(equipment)
        equipment.addUsagePoint(usagePoint)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableUsagePointsEndDevices`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_usage_points_end_devices(self, table: TableUsagePointsEndDevices, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val usagePointMRID = set_identifier(result_set.get_string(table.usage_point_mrid.query_index))
        set_identifier(f"{usagePointMRID}-to-UNKNOWN")

        val endDeviceMRID = result_set.get_string(table.end_device_mrid.query_index)
        val id = set_identifier(f"{usagePointMRID}-to-{endDeviceMRID}")

        val typeNameAndMRID = "UsagePoint to EndDevice association {id}"
        val usagePoint = service.getOrThrow<UsagePoint>(usagePointMRID, typeNameAndMRID)
        val endDevice = service.getOrThrow<EndDevice>(endDeviceMRID, typeNameAndMRID)

        endDevice.addUsagePoint(usagePoint)
        usagePoint.addEndDevice(endDevice)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableCircuitsSubstations`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_circuits_substations(self, table: TableCircuitsSubstations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val circuitMRID = set_identifier(result_set.get_string(table.circuit_mrid.query_index))
        set_identifier(f"{circuitMRID}-to-UNKNOWN")

        val substationMRID = result_set.get_string(table.substation_mrid.query_index)
        val id = set_identifier(f"{circuitMRID}-to-{substationMRID}")

        val typeNameAndMRID = "Circuit to Substation association {id}"
        val circuit = service.getOrThrow<Circuit>(circuitMRID, typeNameAndMRID)
        val substation = service.getOrThrow<Substation>(substationMRID, typeNameAndMRID)

        substation.addCircuit(circuit)
        circuit.addEndSubstation(substation)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableCircuitsTerminals`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_circuits_terminals(self, table: TableCircuitsTerminals, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val circuitMRID = set_identifier(result_set.get_string(table.circuit_mrid.query_index))
        set_identifier(f"{circuitMRID}-to-UNKNOWN")

        val terminalMRID = result_set.get_string(table.terminal_mrid.query_index)
        val id = set_identifier(f"{circuitMRID}-to-{terminalMRID}")

        val typeNameAndMRID = "Circuit to Terminal association {id}"
        val circuit = service.getOrThrow<Circuit>(circuitMRID, typeNameAndMRID)
        val terminal = service.getOrThrow<Terminal>(terminalMRID, typeNameAndMRID)

        circuit.addEndTerminal(terminal)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableLoopsSubstations`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_loops_substations(self, table: TableLoopsSubstations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val assetOrganisationRoleMRID = set_identifier(result_set.get_string(table.loop_mrid.query_index))
        set_identifier(f"{assetOrganisationRoleMRID}-to-UNKNOWN")

        val assetMRID = result_set.get_string(table.substation_mrid.query_index)
        val id = set_identifier(f"{assetOrganisationRoleMRID}-to-{assetMRID}")

        val typeNameAndMRID = "Loop to Substation association {id}"
        val loop = service.getOrThrow<Loop>(assetOrganisationRoleMRID, typeNameAndMRID)
        val substation = service.getOrThrow<Substation>(assetMRID, typeNameAndMRID)

        when (LoopSubstationRelationship[result_set.get_string(table.relationship.query_index)]) {
            LoopSubstationRelationship.LOOP_ENERGIZES_SUBSTATION -> {
                substation.addLoop(loop)
                loop.addSubstation(substation)

            LoopSubstationRelationship.SUBSTATION_ENERGIZES_LOOP -> {
                substation.addEnergizedLoop(loop)
                loop.addEnergizingSubstation(substation)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelayFunctionsProtectedSwitches`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_protection_relay_functions_protected_switches(self, table: TableProtectionRelayFunctionsProtectedSwitches, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val protectionRelayFunctionMRID = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        set_identifier(f"{protectionRelayFunctionMRID}-to-UNKNOWN")

        val protectedSwitchMRID = result_set.get_string(table.protected_switch_mrid.query_index)
        val id = set_identifier(f"{protectionRelayFunctionMRID}-to-{protectedSwitchMRID}")

        val typeNameAndMRID = "ProtectionRelayFunction to ProtectedSwitch association {id}"
        val protectionRelayFunction = service.getOrThrow<ProtectionRelayFunction>(protectionRelayFunctionMRID, typeNameAndMRID)
        val protectedSwitch = service.getOrThrow<ProtectedSwitch>(protectedSwitchMRID, typeNameAndMRID)

        protectionRelayFunction.addProtectedSwitch(protectedSwitch)
        protectedSwitch.addRelayFunction(protectionRelayFunction)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelayFunctionsSensors`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_protection_relay_functions_sensors(self, table: TableProtectionRelayFunctionsSensors, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val protectionRelayFunctionMRID = set_identifier(result_set.get_string(table.protection_relay_function_mrid.query_index))
        set_identifier(f"{protectionRelayFunctionMRID}-to-UNKNOWN")

        val sensorMRID = result_set.get_string(table.sensor_mrid.query_index)
        val id = set_identifier(f"{protectionRelayFunctionMRID}-to-{sensorMRID}")

        val typeNameAndMRID = "ProtectionRelayFunction to Sensor association {id}"
        val protectionRelayFunction = service.getOrThrow<ProtectionRelayFunction>(protectionRelayFunctionMRID, typeNameAndMRID)
        val sensor = service.getOrThrow<Sensor>(sensorMRID, typeNameAndMRID)

        protectionRelayFunction.addSensor(sensor)
        sensor.addRelayFunction(protectionRelayFunction)

        return True

    """
    Create a `set_identifier` and populate its fields from `TableProtectionRelaySchemesProtectionRelayFunctions`.

    :param table: The database table to read the `set_identifier` fields from.
    :param result_set: The record in the database table containing the fields for this `set_identifier`.
    :param set_identifier: A callback to register the mRID of this `set_identifier` for logging purposes.

    :return: True if the `set_identifier` was successfully read from the database and added to the service.
    :raises SqlException: For any errors encountered reading from the database.
    """
    def load_protection_relay_schemes_protection_relay_functions(self, table: TableProtectionRelaySchemesProtectionRelayFunctions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        val protectionRelaySchemeMRID = set_identifier(result_set.get_string(table.protection_relay_scheme_mrid.query_index))
        set_identifier(f"{protectionRelaySchemeMRID}-to-UNKNOWN")

        val protectionRelayFunctionMRID = result_set.get_string(table.protection_relay_function_mrid.query_index)
        val id = set_identifier(f"{protectionRelaySchemeMRID}-to-{protectionRelayFunctionMRID}")

        val typeNameAndMRID = "ProtectionRelayScheme to ProtectionRelayFunction association {id}"
        val protectionRelayScheme = service.getOrThrow<ProtectionRelayScheme>(protectionRelaySchemeMRID, typeNameAndMRID)
        val protectionRelayFunction = service.getOrThrow<ProtectionRelayFunction>(protectionRelayFunctionMRID, typeNameAndMRID)

        protectionRelayScheme.addFunction(protectionRelayFunction)
        protectionRelayFunction.addScheme(protectionRelayScheme)

        return True
