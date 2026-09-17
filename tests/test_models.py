from polsilver.models import DeviceSnapshot, normalize_uuid, rssi_quality


def test_rssi_quality_boundaries():
    assert rssi_quality(-45) == "excellent"
    assert rssi_quality(-60) == "good"
    assert rssi_quality(-70) == "fair"
    assert rssi_quality(-90) == "weak"
    assert rssi_quality(None) == "unknown"


def test_snapshot_serializes_derived_signal_quality():
    row = DeviceSnapshot(address="AA:BB", name="Sensor", rssi=-62, service_uuids=["ABC"])
    payload = row.to_dict()
    assert payload["signal_quality"] == "good"
    assert payload["address"] == "AA:BB"
    assert normalize_uuid(" ABC ") == "abc"
