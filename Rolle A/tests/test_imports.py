from service import DataService


def test_csv_import():
    service = DataService()
    data = service.import_all(csv_path="test.csv")

    assert isinstance(data, list)
    assert len(data) >= 0


def test_json_import_structure():
    service = DataService()
    data = service.import_all(json_path="test.json")

    if len(data) > 0:
        assert "titel" in data[0]
        assert "id" in data[0]