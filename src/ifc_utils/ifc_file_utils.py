import ifcopenshell.util.element
import json
from src.ifc_utils.ifc_geometry_utils import IfcGeometryUtil
from .ifc_type_enum import GeometryType


class IfcUtilsFile:
    @staticmethod
    def seperate_by_category(file: ifcopenshell.file, to_json=False):
        categories = {}
        try:
            for element in file.by_type('IfcProduct'):
                element_type = element.is_a()
                if GeometryType.has_geometry_type(element):
                    print(f"Id:{element.id()}, Type: {element_type}, Representation: {element.get_info()['Representation']}")
                    print(f"full_string: {element.get_info()}")
                if element.is_a('IfcSlab'):
                    IfcGeometryUtil.extract_slab_polyline(element)
                if element_type not in categories:
                    categories[element_type] = []
                element_data = element.get_info()
                categories[element_type].append(element_data)
        except Exception as e:
            print(f"An error occurred while separating by category: {e}")

        if to_json:
            return json.dumps(categories, indent=4, default=str)
        else:
            return categories

    @staticmethod
    def load(path, is_stream=False) -> ifcopenshell.file | None:
        try:
            ifc_file = ifcopenshell.open(path=path, should_stream=is_stream)
            return ifc_file
        except Exception as e:
            print(f"An error occurred while opening the IFC file: {e}")
            return None
