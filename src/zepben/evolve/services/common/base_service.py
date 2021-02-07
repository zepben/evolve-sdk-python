#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
from abc import ABCMeta
from collections import OrderedDict
from dataclassy import dataclass
from typing import Dict, Generator, Callable, Optional, List, Union, Sized, Set

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.services.common.reference_resolvers import BoundReferenceResolver, UnresolvedReference

__all__ = ["BaseService"]


_GET_DEFAULT = (1,)


@dataclass(slots=True)
class BaseService(object, metaclass=ABCMeta):
    name: str
    _objectsByType: Dict[type, Dict[str, IdentifiedObject]] = OrderedDict()
    _unresolved_references_to: Dict[str, Set[UnresolvedReference]] = OrderedDict()
    """
    A dictionary of references between mRID's that as yet have not been resolved - typically when transferring services between systems.
    The key is the to_mrid of the `UnresolvedReference`s, and the value is a list of `UnresolvedReference`s for that specific object.
    For example, if an AcLineSegment with mRID 'acls1' is present in the service, but the service is missing its `location` with mRID 'location-l1' 
    and `perLengthSequenceImpedance` with mRID 'plsi-1', the following key value pairs would be present:
    {
        "plsi-1": [
          UnresolvedReference(from_ref=AcLineSegment('acls1'), to_mrid='plsi-1', resolver=ReferenceResolver(from_class=AcLineSegment, to_class=PerLengthSequenceImpedance, resolve=...))
        ],
        "location-l1": [
          UnresolvedReference(from_ref=AcLineSegment('acls1'), to_mrid='location-l1', resolver=ReferenceResolver(from_class=AcLineSegment, to_class=Location, resolve=...))
        ]
    }
    
    `resolve` in `ReferenceResolver` will be the function used to populate the relationship between the `IdentifiedObject`s either when 
    `resolveOrDeferReference() is called if the other side of the reference exists in the service, or otherwise when the second object is added to the service.
    """

    _unresolved_references_from: Dict[str, Set[UnresolvedReference]] = OrderedDict()
    """ 
    An index of the unresolved references by their `from_ref.mrid`. For the above example this will be a dictionary of the form:
    {
        "acls1": [
          UnresolvedReference(from_ref=AcLineSegment('acls1'), to_mrid='location-l1', resolver=ReferenceResolver(from_class=AcLineSegment, to_class=Location, resolve=...)),
          UnresolvedReference(from_ref=AcLineSegment('acls1'), to_mrid='plsi-1', resolver=ReferenceResolver(from_class=AcLineSegment, to_class=PerLengthSequenceImpedance, resolve=...))
        ]
    }
    """

    def __contains__(self, mrid: str) -> bool:
        """
        Check if `mrid` has any associated object.

        `mrid` The mRID to search for.
        Returns True if there is an object associated with the specified `mrid`, False otherwise.
        """
        for type_map in self._objectsByType.values():
            if mrid in type_map:
                return True
        return False

    def __str__(self):
        return f"{type.__name__}{f' {self.name}' if self.name else ''}"

    def has_unresolved_references(self):
        """
        Returns True if this service has unresolved references, False otherwise.
        """
        return self.num_unresolved_references() > 0

    def len_of(self, t: type = None) -> int:
        """
        Get the len of objects of type `t` in the service.
        `t` The type of object to get the len of. If None (default), will get the len of all objects in the service.
        """
        if t is None:
            return sum([len(vals) for vals in self._objectsByType.values()])
        else:
            try:
                return len(self._objectsByType[t].values())
            except KeyError:
                count = 0
                for c, obj_map in self._objectsByType.items():
                    if issubclass(c, t):
                        try:
                            count += len(self._objectsByType[c].values())
                        except KeyError:
                            pass
                return count

    def num_unresolved_references(self):
        """
        Get the total number of unresolved references.
        Returns The number of references in the network that have not already been resolved.
        """
        return sum([len(r) for r in self._unresolved_references_to.copy().values()])

    def unresolved_references(self) -> Generator[UnresolvedReference, None, None]:
        """
        Returns a generator over all the `UnresolvedReferences` that are known to this service. This should typically be avoided when resolving references in
        favour of `get_unresolved_reference_mrids_by_resolver()`, `get_unresolved_reference_mrids_from()`, and `get_unresolved_reference_mrids_to()`
        """
        for unresolved_refs in self._unresolved_references_to.copy().values():
            for ur in unresolved_refs:
                yield ur

    def get(self, mrid: str, type_: type = None, default=_GET_DEFAULT,
            generate_error: Callable[[str, str], str] = lambda mrid, typ: f"Failed to find {typ}[{mrid}]") -> IdentifiedObject:
        """
        Get an object associated with this service.

        `mrid` The mRID of the `iec61970.base.core.identified_object.IdentifiedObject` to retrieve.
        `type_` The `iec61970.base.core.identified_object.IdentifiedObject` subclass type of the object
                      with `mrid`. If None, will check all types stored in the service.
        `default` The default to return if `mrid` can't be found in the service.
        `generate_error` Function to call for an error message. Will be passed the mrid and _type (if set).
        Returns The `iec61970.base.core.identified_object.IdentifiedObject` associated with `mrid`, or default
                 if it is set.
        Raises `KeyError` if `mrid` was not found in the service with `_type` or if no objects of `_type` are
                 stored by the service and default was not set.
        """
        if not mrid:
            raise KeyError("You must specify an mRID to get. Empty/None is invalid.")
        mrid = str(mrid)
        if type_:
            try:
                return self._objectsByType[type_][mrid]
            except KeyError:
                for c, obj_map in self._objectsByType.items():
                    if issubclass(c, type_):
                        try:
                            return obj_map[mrid]
                        except KeyError:
                            pass
                if default is _GET_DEFAULT:
                    raise KeyError(generate_error(mrid, type_.__name__))
                else:
                    return default
        else:
            for object_map in self._objectsByType.values():
                if mrid in object_map:
                    return object_map[mrid]

            if default is _GET_DEFAULT:
                raise KeyError(generate_error(mrid, ""))
            return default

    def __getitem__(self, mrid):
        """
        Get an object associated with this service.
        Note that you should use `get` directly where the type of the desired object is known.
        `mrid` The mRID of the `iec61970.base.core.identified_object.IdentifiedObject` to retrieve.
        Returns The `iec61970.base.core.identified_object.IdentifiedObject` associated with `mrid`.
        Raises `KeyError` if `mrid` was not found in the service with `type`.
        """
        return self.get(mrid)

    def add(self, identified_object: IdentifiedObject) -> bool:
        """
        Associate an object with this service.
        `identified_object` The object to associate with this service.
        Returns True if the object is associated with this service, False otherwise.
        """
        mrid = identified_object.mrid
        if not mrid:
            return False
        # TODO: Only allow supported types

        objs = self._objectsByType.get(identified_object.__class__, dict())
        if mrid in objs:
            return False

        # Check other types and make sure this mRID is unique
        for obj_map in self._objectsByType.values():
            if mrid in obj_map:
                return False

        unresolved_refs = self._unresolved_references_to.get(mrid, None)
        if unresolved_refs:
            for ref in unresolved_refs:
                ref.resolver.resolve(ref.from_ref, identified_object)
                self._unresolved_references_from[ref.from_ref.mrid].remove(ref)
                if not self._unresolved_references_from[ref.from_ref.mrid]:
                    del self._unresolved_references_from[ref.from_ref.mrid]
            del self._unresolved_references_to[mrid]

        objs[mrid] = identified_object
        self._objectsByType[identified_object.__class__] = objs
        return True

    def resolve_or_defer_reference(self, bound_resolver: BoundReferenceResolver, to_mrid: str) -> bool:
        """
        Resolves a property reference between two types by looking up the `to_mrid` in the service and
        using the provided `bound_resolver` to resolve the reference relationships (including any reverse relationship).

        If the `to_mrid` object has not yet been added to the service, the reference resolution will be deferred until the
        object with `to_mrid` is added to the service, which will then use the resolver from the `bound_resolver` at that
        time to resolve the reference relationship.


        `bound_resolver`
        `to_mrid` The MRID of an object that is the subclass of the to_class of `bound_resolver`.
        Returns true if the reference was resolved, otherwise false if it has been deferred.
        """
        if not to_mrid:
            return True
        to_mrid = to_mrid
        from_ = bound_resolver.from_obj
        resolver = bound_resolver.resolver
        reverse_resolver = bound_resolver.reverse_resolver
        try:
            # If to_mrid is present in the service, we resolve any references immediately.
            to = self.get(to_mrid, resolver.to_class)
            resolver.resolve(from_, to)
            if reverse_resolver:
                reverse_resolver.resolve(to, from_)

                # Clean up any reverse resolvers now that the reference has been resolved
                if from_.mrid in self._unresolved_references_to:
                    to_remove = UnresolvedReference(from_ref=to, to_mrid=from_.mrid, resolver=reverse_resolver)
                    self._unresolved_references_to[from_.mrid].remove(to_remove)
                    self._unresolved_references_from[to_remove.from_ref.mrid].remove(to_remove)
                    if not self._unresolved_references_from[to_remove.from_ref.mrid]:
                        del self._unresolved_references_from[to_remove.from_ref.mrid]
                    if not self._unresolved_references_to[from_.mrid]:
                        del self._unresolved_references_to[from_.mrid]

            return True
        except KeyError:
            # to_mrid didn't exist in the service, populate the reference caches for resolution when it is added.
            urefs = self._unresolved_references_to.get(to_mrid, set())
            uref = UnresolvedReference(from_ref=from_, to_mrid=to_mrid, resolver=resolver)
            urefs.add(uref)
            self._unresolved_references_to[to_mrid] = urefs
            rev_urefs = self._unresolved_references_from.get(from_.mrid, set())
            rev_urefs.add(uref)
            self._unresolved_references_from[from_.mrid] = rev_urefs
            return False

    def get_unresolved_reference_mrids_by_resolver(self, bound_resolvers: Union[BoundReferenceResolver, Sized[BoundReferenceResolver]]) -> Generator[str, None, None]:
        """
        Gets a set of MRIDs that are referenced by the from_obj held by `bound_resolver` that are unresolved.
        `bound_resolver` The `BoundReferenceResolver` to retrieve unresolved references for.
        Returns Set of mRIDs that have unresolved references.
        """
        seen = set()
        try:
            len(bound_resolvers)
            resolvers = bound_resolvers
        except TypeError:
            resolvers = [bound_resolvers]

        for resolver in resolvers:
            if resolver.from_obj.mrid not in self._unresolved_references_from:
                continue
            for ref in self._unresolved_references_from[resolver.from_obj.mrid]:
                if ref.to_mrid not in seen and ref.resolver == resolver.resolver:
                    seen.add(ref.to_mrid)
                    yield ref.to_mrid

    def get_unresolved_references_from(self, mrid: str) -> Generator[UnresolvedReference, None, None]:
        """
        Get the mRIDs that are unresolved that `mrid` has to other objects.
        `mrid` The mRID to get unresolved references for.
        Returns a generator over the mRIDs that need to be resolved for `mrid`.
        """
        if mrid in self._unresolved_references_from:
            for ref in self._unresolved_references_from[mrid]:
                yield ref

    def get_unresolved_references_to(self, mrid: str, exclude_types: Set[Relationship] = None) -> Generator[UnresolvedReference, None, None]:
        """
        Get the mRIDs that are unresolved that other objects have to `mrid`.
        `mrid` The mRID to fetch unresolved references for that are pointing to it.
        Returns a generator over the mRIDs that need to be resolved for `mrid`.
        """
        if mrid in self._unresolved_references_to:
            for ref in self._unresolved_references_to[mrid]:
                yield ref

    def remove(self, identified_object: IdentifiedObject) -> bool:
        """
        Disassociate an object from this service.

        `identified_object` THe object to disassociate from the service.
        Raises `KeyError` if `identified_object` or its type was not present in the service.
        """
        del self._objectsByType[identified_object.__class__][identified_object.mrid]
        return True

    def objects(self, obj_type: Optional[type] = None, exc_types: Optional[List[type]] = None) -> Generator[IdentifiedObject, None, None]:
        """
        Generator for the objects in this service of type `obj_type`.
        `obj_type` The type of object to yield. If this is a base class it will yield all subclasses.
        Returns Generator over
        """
        if obj_type is None:
            for typ, obj_map in self._objectsByType.items():
                if exc_types:
                    if typ in exc_types:
                        continue
                for obj in obj_map.values():
                    yield obj
            return
        else:
            try:
                for obj in self._objectsByType[obj_type].values():
                    yield obj
            except KeyError:
                for _type, object_map in self._objectsByType.items():
                    if issubclass(_type, obj_type):
                        for obj in object_map.values():
                            yield obj
