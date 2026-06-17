from import_csv import import_csv
from import_json import import_json
from import_xml import import_xml


class DataService:

    def import_all(self, csv_path=None, json_path=None, xml_path=None):
        data = []

        if csv_path:
            data.extend(import_csv(csv_path))

        if json_path:
            data.extend(import_json(json_path))

        if xml_path:
            data.extend(import_xml(xml_path))

        return data