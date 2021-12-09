#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_asset_owner(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, organisation: Organisation = None) -> AssetOwner:
    """
    AssetOwner(AssetOrganisationRole(OrganisationRole(IdentifiedObject)))
    IdentifiedObject: mrid, name, description, names
    OrganisationRole: organisation
    AssetOrganisationRole: 
    AssetOwner:
    """
    return AssetOwner(**locals())


def create_pole(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None, 
                organisation_roles: List[AssetOrganisationRole] = None, classification: str = "", streetlights: List[Streetlight] = None) -> Pole:
    """
    Pole(Structure(AssetContainer(Asset(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    Asset: location, organisation_roles
    AssetContainer:
    Structure:
    Pole: classification, streetlights
    """
    return Pole(**locals())


def create_streetlight(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                       organisation_roles: List[AssetOrganisationRole] = None, pole: Pole = None, light_rating: int = None,
                       lamp_kind: StreetlightLampKind = StreetlightLampKind.UNKNOWN) -> Streetlight:
    """
    Streetlight(Asset(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    Asset: location, organisation_roles
    Streetlight: pole, light_rating, lamp_kind
    """
    return Streetlight(**locals())
