import json
from polsilver.export import export_csv, export_json
from polsilver.models import DeviceSnapshot


def test_exports_json_and_csv(tmp_path):
    rows = [DeviceSnapshot(address="AA:BB", name="Demo", rssi=-50, service_uuids=["180f"], manufacturer_ids=[76])]
    json_path = export_json(tmp_path / "scan.json", rows)
    csv_path = export_csv(tmp_path / "scan.csv", rows)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload[0]["name"] == "Demo"
    text = csv_path.read_text(encoding="utf-8-sig")
    assert "AA:BB" in text and "excellent" in text
