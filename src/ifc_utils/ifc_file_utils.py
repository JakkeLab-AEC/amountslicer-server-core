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
    @Logger.log_method
    def get_geometry(ifc_file: ifcopenshell.file, entity_name="IfcSlab", to_json=True, yz_swap=True):
        elements = ifc_file.by_type('IfcProduct')
        if elements is None:
            Logger.log_error("No IfcProduct elements found.")

        elements = ifc_file.by_type(entity_name)
        all_geometry_data = []

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
                    geometry_type = slab.get_geometry_element().geometry.__class__.__name__

                    shape = slab.get_geometry_element()
                    matrix = np.array(shape.transformation.matrix).reshape(-1, 4)[-1][0:3]
                    location = []

                    vertices = slab.get_geometry_element().geometry.verts
                    vertices = np.array(vertices).reshape(-1, 3)

                    if yz_swap:
                        vertices = vertices[:, [0, 2, 1]].tolist()
                        location = [matrix[0], matrix[2], matrix[1]]
                    else:
                        vertices = vertices.tolist()
                        location = [matrix[0], matrix[1], matrix[2]]

                    faces = slab.get_geometry_element().geometry.faces
                    faces = np.array(faces).reshape(-1, 3).tolist()

                    normals = slab.get_geometry_element().geometry.normals

                    edges = slab.get_geometry_element().geometry.edges
                    edges = np.array(edges).reshape(-1, 2).tolist()

                    geometry_data = {
                        "id": element.id(),
                        "type": "IfcSlab",
                        "geometryType": geometry_type,
                        "vertices": vertices,
                        "vertices_count": len(vertices),
                        "faces": faces,
                        "faces_count": len(faces),
                        "normals": normals,
                        "normals_count": len(normals),
                        "edges": edges,
                        "edges_count": len(edges),
                        "location": location,
                    }
                    all_geometry_data.append(geometry_data)

            except Exception as e:
                Logger.log_error(f"An error occurred while separating by category: {e}")
                Logger.log_error(f"Current Element : {element}")
            finally:
                continue

        if to_json:
            return json.dumps(all_geometry_data, indent=4, default=str)
        else:
            return all_geometry_data

    @staticmethod
    @Logger.log_method
    def get_element_location(element: ifcopenshell.entity_instance) -> dict:
        """
        Get the local placement of an element and convert it to a dictionary.
        """
        if element.ObjectPlacement is None:
            return {"x": 0, "y": 0, "z": 0}

        coords = element.ObjectPlacement.RelativePlacement.Location.Coordinates
        return {"x": coords[0], "y": coords[1], "z": coords[2]}

    @staticmethod
    def load(path, is_stream=False) -> ifcopenshell.file | None:
        try:
            ifc_file = ifcopenshell.open(path=path, should_stream=is_stream)
            return ifc_file
        except Exception as e:
            print(f"An error occurred while opening the IFC file: {e}")
            return None
