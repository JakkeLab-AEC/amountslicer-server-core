import ifcopenshell.util.element
import json
from src.ifc_utils.ifc_geometry_utils import IfcGeometryUtil
from src.model.model_elements import *

class IfcUtilsFile:
    @staticmethod
    def seperate_by_category(file: ifcopenshell.file, to_json=False):
        categories = {}
        try:
            for element in file.by_type('IfcProduct'):
                element_type = element.is_a()
                #Collect Slab
                if element.is_a('IfcSlab'):
                    slab = IfcGeometryUtil.parse_slab(element)
                #Collect Wall Standard Case
                if element.is_a('IfcWallStandardCase'):
                    wall = IfcGeometryUtil.parse_wall_standard(element)
                #Collections
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
