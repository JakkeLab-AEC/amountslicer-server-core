import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape

class IfcGeometryUtil:
    @staticmethod
    def get_shape(element:ifcopenshell.entity_instance):
        settings = ifcopenshell.geom.settings()
        shape = ifcopenshell.geom.create_shape(settings, element)
        print(shape)
        matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
        print(matrix)