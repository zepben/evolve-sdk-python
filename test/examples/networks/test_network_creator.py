from zepben.evolve import NetworkService, Junction, BaseVoltage, Terminal, EnergySource, ConductingEquipment
import unittest


class TestNetworkCreator(unittest.TestCase):

    def test_create_bus(self):
        net = NetworkService()
        bv = BaseVoltage()
        bus = net.create_bus(base_voltage=bv)
        assert isinstance(bus, Junction)
        assert bus.num_terminals() == 1, "num_terminals should be 1"
        t: Terminal = bus.get_terminal_by_sn(1)
        assert t is not None
        assert bus.get_base_voltage() is bv, f'bus.get_base_voltage() is not bv. Instead is {bus.get_base_voltage()}'
        assert t.conducting_equipment is bus, "t.conducting_equipment should be 'bus'"

    def test_create_energy_source(self):
        net = NetworkService()
        bus = net.create_bus()
        source: EnergySource = net.create_energy_source(bus=bus)
        t: Terminal = source.get_terminal_by_sn(1)
        assert source.num_terminals() == 1
        assert isinstance(t, Terminal)
        assert isinstance(source, EnergySource)
        assert t.conducting_equipment is source, "t.conducting_equipment should be 'source'"

