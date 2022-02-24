#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Callable

from .. import ConductingEquipment, NetworkService, PhaseCode, EnergySource, AcLineSegment, Breaker, Junction, Terminal, Feeder


def null_action(_):
    """
    An action that does nothing.

    :param _: Any item that will be ignored
    """
    pass


class TestNetworkBuilder(object):
    """
    A class for building simple test networks, often used for unit testing.
    """

    network: NetworkService = NetworkService()
    """
    The network where objects are created for this `TestNetworkBuilder`. You should not be readily required to access the network via this property,
    but should instead access it via `build` to ensure the correct tracing is applied before use.
    """

    _count = 0
    _current: Optional[ConductingEquipment] = None
    _current_terminal: Optional[int] = None

    def from_source(self, nominal_phases: PhaseCode = PhaseCode.ABC, action: Callable[[EnergySource], None] = null_action) -> 'TestNetworkBuilder':
        """
        Start a new network island from an `EnergySource`, updating the network pointer to the new `EnergySource`.

        :param nominal_phases: The `PhaseCode` for the new `EnergySource`, used as both the nominal and energising phases. Must be a subset of `PhaseCode.ABCN`.
        :param action: An action that accepts the new `EnergySource` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_external_source(nominal_phases)
        action(it)
        self._current = it
        return self

    def to_source(self, nominal_phases: PhaseCode = PhaseCode.ABC, action: Callable[[EnergySource], None] = null_action) -> 'TestNetworkBuilder':
        """
        Add a new `EnergySource` to the network and connect it to the current network pointer, updating the network pointer to the new `EnergySource`.

        :param nominal_phases: The `PhaseCode` for the new `EnergySource`, used as both the nominal and energising phases. Must be a subset of `PhaseCode.ABCN`.
        :param action: An action that accepts the new `EnergySource` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_external_source(nominal_phases)
        self._connect(self._current, it)
        action(it)
        self._current = it
        return self

    def from_acls(self, nominal_phases: PhaseCode = PhaseCode.ABC, action: Callable[[AcLineSegment], None] = null_action) -> 'TestNetworkBuilder':
        """
        Start a new network island from an `AcLineSegment`, updating the network pointer to the new `AcLineSegment`.

        :param nominal_phases: The nominal phases for the new `AcLineSegment`.
        :param action: An action that accepts the new `AcLineSegment` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_acls(nominal_phases)
        action(it)
        self._current = it
        return self

    def to_acls(self, nominal_phases: PhaseCode = PhaseCode.ABC, action: Callable[[AcLineSegment], None] = null_action) -> 'TestNetworkBuilder':
        """
        Add a new `AcLineSegment` to the network and connect it to the current network pointer, updating the network pointer to the new `AcLineSegment`.

        :param nominal_phases: The nominal phases for the new `AcLineSegment`.
        :param action: An action that accepts the new `AcLineSegment` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        acls = self._create_acls(nominal_phases)
        self._connect(self._current, acls)
        action(acls)
        self._current = acls
        return self

    def from_breaker(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        is_normally_open: bool = False,
        is_open: Optional[bool] = None,
        action: Callable[[Breaker], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from a `Breaker`, updating the network pointer to the new `Breaker`.

        :param nominal_phases: The nominal phases for the new `Breaker`.
        :param is_normally_open: The normal state of the switch. Defaults to False.
        :param is_open: The current state of the switch. Defaults to `is_normally_open`.
        :param action: An action that accepts the new `Breaker` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_breaker(nominal_phases, is_normally_open=is_normally_open, is_open=is_open if is_open is not None else is_normally_open)
        action(it)
        self._current = it
        return self

    def to_breaker(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        is_normally_open: bool = False,
        is_open: Optional[bool] = None,
        action: Callable[[Breaker], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `Breaker` to the network and connect it to the current network pointer, updating the network pointer to the new `Breaker`.

        :param nominal_phases: The nominal phases for the new `Breaker`.
        :param is_normally_open: The normal state of the switch. Defaults to False.
        :param is_open: The current state of the switch. Defaults to `is_normally_open`.
        :param action: An action that accepts the new `Breaker` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_breaker(nominal_phases, is_normally_open=is_normally_open, is_open=is_open if is_open is not None else is_normally_open)
        self._connect(self._current, it)
        action(it)
        self._current = it
        return self

    def from_junction(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        num_terminals: int = 2,
        action: Callable[[Junction], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from a `Junction`, updating the network pointer to the new `Junction`.

        :param nominal_phases: The nominal phases for the new `Junction`.
        :param num_terminals: The number of terminals to create on the new `Junction`. Defaults to 2.
        :param action: An action that accepts the new `Junction` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_junction(nominal_phases, num_terminals)
        action(it)
        self._current = it
        return self

    def to_junction(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        num_terminals: int = 2,
        action: Callable[[Junction], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `Junction` to the network and connect it to the current network pointer, updating the network pointer to the new `Junction`.

        :param nominal_phases: The nominal phases for the new `Junction`.
        :param num_terminals: The number of terminals to create on the new `Junction`. Defaults to 2.
        :param action: An action that accepts the new `Junction` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_junction(nominal_phases, num_terminals)
        self._connect(self._current, it)
        action(it)
        self._current = it
        return self

    def split_from(self, from_: str, terminal: Optional[int] = None) -> 'TestNetworkBuilder':
        """
        Move the current network pointer to the specified `from` allowing branching of the network. This has the effect of changing the current network pointer.

        :param from_: The mRID of the `ConductingEquipment` to split from.
        :param terminal: The terminal to split from. Defaults to last terminal.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        self._current = self.network.get(from_, ConductingEquipment)
        self._current_terminal = terminal
        return self

    """
    Connect the specified `from` and `to` without moving the current network pointer.
   
    :param from: The mRID of the first `ConductingEquipment` to be connected.
    :param to: The mRID of the second `ConductingEquipment` to be connected.
    :param from_terminal: The sequence number of the terminal on `from` which will be connected.
    :param to_terminal: The sequence number of the terminal on `to` which will be connected.
   
    :return: This `TestNetworkBuilder` to allow for fluent use.
    """
    def connect(self, from_: str, to: str, from_terminal: int, to_terminal: int) -> 'TestNetworkBuilder':
        self._connect(self.network.get(from_, ConductingEquipment), self.network.get(to, ConductingEquipment), from_terminal, to_terminal)
        return self

    """
    Create a new feeder with the specified terminal as the head terminal.
   
    :param head_mrid: The mRID of the head `ConductingEquipment`.
    :param sequence_number: The `Terminal` sequence number of the head terminal. Defaults to last terminal.
   
    :return: This `TestNetworkBuilder` to allow for fluent use.
    """
    def add_feeder(self, head_mrid: str, sequence_number: Optional[int] = None) -> 'TestNetworkBuilder':
        self._create_feeder(self.network.get(head_mrid, ConductingEquipment), sequence_number)
        return self

    """
    Get the `NetworkService` after apply traced phasing and feeder directions.
   
    Does not infer phasing.
   
    :return: The `NetworkService` created by this `TestNetworkBuilder`
    """
    def build(self, apply_directions_from_sources: bool = True) -> NetworkService:
        # The traces are broken, add them back in later.
        # PROJ-1945 - Tracing.setPhases().run(network)
        # PROJ-1952 - Tracing.setDirection().run(network)

        if apply_directions_from_sources:
            for es in self.network.objects(EnergySource):
                for terminal in es.terminals:
                    # PROJ-1952 - Tracing.setDirection().run(terminal)
                    pass

        return self.network

    def _next_id(self, type_: str) -> str:
        id_ = f"{type_}{self._count}"
        self._count = self._count + 1
        return id_

    def _connect(self, from_: ConductingEquipment, to: ConductingEquipment, from_terminal: Optional[int] = None, to_terminal: Optional[int] = None):
        self.network.connect_terminals(
            from_.get_terminal_by_sn(from_terminal if from_terminal else self._current_terminal if self._current_terminal else from_.num_terminals()),
            to.get_terminal_by_sn(to_terminal if to_terminal else 1)
        )
        self._current_terminal = None

    def _create_external_source(self, nominal_phases: PhaseCode) -> EnergySource:
        if any(it not in PhaseCode.ABCN for it in nominal_phases.single_phases):
            raise ValueError("EnergySource phases must be a subset of ABCN")

        es = EnergySource(mrid=self._next_id("s"), is_external_grid=True)
        self._add_terminal(es, 1, nominal_phases)

        self.network.add(es)
        return es

    def _create_acls(self, nominal_phases: PhaseCode) -> AcLineSegment:
        acls = AcLineSegment(mrid=self._next_id("c"))
        self._add_terminal(acls, 1, nominal_phases)
        self._add_terminal(acls, 2, nominal_phases)

        self.network.add(acls)
        return acls

    def _create_breaker(self, nominal_phases: PhaseCode, is_normally_open: bool, is_open: bool) -> Breaker:
        b = Breaker(mrid=self._next_id("b"))
        b.set_normally_open(is_normally_open)
        b.set_open(is_open)

        self._add_terminal(b, 1, nominal_phases)
        self._add_terminal(b, 2, nominal_phases)

        self.network.add(b)
        return b

    def _create_junction(self, nominal_phases: PhaseCode, num_terminals: int) -> Junction:
        j = Junction(mrid=self._next_id("j"))
        for i in range(1, num_terminals + 1):
            self._add_terminal(j, 1, nominal_phases)

        self.network.add(j)
        return j

    def _create_feeder(self, head_equipment: ConductingEquipment, sequence_number: Optional[int] = None) -> Feeder:
        f = Feeder(
            mrid=self._next_id("fdr"),
            normal_head_terminal=head_equipment.get_terminal_by_sn(sequence_number if sequence_number else head_equipment.num_terminals())
        )

        f.add_equipment(head_equipment)
        head_equipment.add_container(f)

        self.network.add(f)
        return f

    def _add_terminal(self, ce: ConductingEquipment, sn: int, nominal_phases: PhaseCode):
        terminal = Terminal(mrid=f"{ce.mrid}-t{sn}", phases=nominal_phases)
        ce.add_terminal(terminal)
        self.network.add(terminal)


def start_with_source(nominal_phases: PhaseCode = PhaseCode.ABC, action: Callable[[EnergySource], None] = null_action) -> TestNetworkBuilder:
    """
    Create a `TestNetworkBuilder` that starts with an `EnergySource`.

    :param nominal_phases: The nominal phases for the starting `Breaker`.
    :param action: An action that accepts the new `EnergySource` to allow for additional initialisation.

    :return: The `TestNetworkBuilder` with the current network pointer assigned to the created `EnergySource`.
    """
    builder = TestNetworkBuilder()
    builder.from_source(nominal_phases, action)
    return builder


def start_with_acls(nominal_phases: PhaseCode = PhaseCode.ABC, action: Callable[[AcLineSegment], None] = null_action) -> TestNetworkBuilder:
    """
    Create a `TestNetworkBuilder` that starts with an `AcLineSegment`.

    :param nominal_phases: The nominal phases for the starting `AcLineSegment`.
    :param action: An action that accepts the new `AcLineSegment` to allow for additional initialisation.

    :return: The `TestNetworkBuilder` with the current network pointer assigned to the created `AcLineSegment`.
    """
    builder = TestNetworkBuilder()
    builder.from_acls(nominal_phases, action)
    return builder


def start_with_breaker(
    nominal_phases: PhaseCode = PhaseCode.ABC,
    is_normally_open: bool = False,
    is_open: Optional[bool] = None,
    action: Callable[[Breaker], None] = null_action
) -> TestNetworkBuilder:
    """
    Create a `TestNetworkBuilder` that starts with a `Breaker`.

    :param nominal_phases: The nominal phases for the starting `Breaker`.
    :param is_normally_open: The normal state of the switch. Defaults to False.
    :param is_open: The current state of the switch. Defaults to `is_normally_open`.
    :param action: An action that accepts the new `Breaker` to allow for additional initialisation.

    :return: The `TestNetworkBuilder` with the current network pointer assigned to the created `Breaker`.
    """
    builder = TestNetworkBuilder()
    builder.from_breaker(nominal_phases, is_normally_open=is_normally_open, is_open=is_open, action=action)
    return builder


def start_with_junction(
    nominal_phases: PhaseCode = PhaseCode.ABC,
    num_terminals: Optional[int] = None,
    action: Callable[[Junction], None] = null_action
) -> TestNetworkBuilder:
    """
    Add a new `Junction` to the network and connect it to the current network pointer, updating the network pointer to the new `Junction`.

    :param nominal_phases: The nominal phases for the new `Junction`.
    :param num_terminals: The number of terminals to create on the new `Junction`. Defaults to 2.
    :param action: An action that accepts the new `Junction` to allow for additional initialisation.

    :return: This `TestNetworkBuilder` to allow for fluent use.
    """
    builder = TestNetworkBuilder()
    builder.from_junction(nominal_phases, num_terminals, action)
    return builder
