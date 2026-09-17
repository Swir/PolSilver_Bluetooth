import asyncio

from polsilver import ble as ble_module


class FakePairClient:
    instances = []

    def __init__(self, address, timeout):
        self.address = address
        self.timeout = timeout
        self.is_connected = True
        self.pair_called = False
        self.disconnect_called = False
        type(self).instances.append(self)

    async def pair(self):
        self.pair_called = True
        return True

    async def disconnect(self):
        self.disconnect_called = True
        self.is_connected = False


def test_pair_device_uses_one_selected_address_and_disconnects(monkeypatch):
    FakePairClient.instances.clear()
    monkeypatch.setattr(ble_module, "BleakClient", FakePairClient)

    result = asyncio.run(ble_module.pair_device("AA:BB:CC:DD:EE:FF", timeout=20))

    assert result is True
    assert len(FakePairClient.instances) == 1
    client = FakePairClient.instances[0]
    assert client.address == "AA:BB:CC:DD:EE:FF"
    assert client.timeout == 20
    assert client.pair_called is True
    assert client.disconnect_called is True
