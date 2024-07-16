from src.server_utils.method_loggers import *
import ifcopenshell.util.element
import json
from src.ifc_utils.ifc_geometry_utils import IfcGeometryUtil

from src.model.model_elements import *
from src.model.model_elements_simple import *

class IfcUtilsFile:
    """
    Utility for loaded IFC File.
    """
    @staticmethod
    @Logger.log_method
    def seperate_by_category(file: ifcopenshell.file, to_json=False):
        """
        Sperate items by Amount Slicer defined models. (Slab, Wall, Roof, ... etc)
        :param file:
        :param to_json:
        :return:
        """
        categories = {}
        elements = file.by_type('IfcProduct')
        if elements is None:
            Logger.log_error("No IfcProduct elements found.")
            return categories if not to_json else json.dumps(categories, indent=4, default=str)

        for element in elements:
            try:
                if element is None:
                    Logger.log_error("Encountered a NoneType element.")
                    continue

                # Get Element Type
                element_type = element.is_a()

                # Collect Slab
                if element.is_a('IfcSlab'):
                    slab = SlabSimple(element)

                # Collections
                if element_type not in categories:
                    categories[element_type] = []

                element_data = element.get_info()
                if element_data is None:
                    Logger.log_error(f"Failed to get info for element: {element.id()}")
                    continue

                categories[element_type].append(element_data)
            except Exception as e:
                Logger.log_error(f"An error occurred while separating by category: {e}")
                Logger.log_error(f"Current Element : {element}")
            finally:
                continue

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
