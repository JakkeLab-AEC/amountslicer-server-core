import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
from ..model.model_geometry import *

class IfcGeometryUtil:
    @staticmethod
    def get_shape(element: ifcopenshell.entity_instance):
        settings = ifcopenshell.geom.settings()
        shape = ifcopenshell.geom.create_shape(settings, element)
        return shape
    @staticmethod
    def get_shape_aspects(element: ifcopenshell.entity_instance):
        shape_aspect = ifcopenshell.util.element.get_shape_aspects(element)
        print(shape_aspect)

    @staticmethod
    def extract_slab_polyline(element: ifcopenshell.entity_instance):
        polyline_pts = list('Point3d')
        if element.is_a('IfcSlab'):
            representations = element.Representation.Representations
            for representation in representations:
                if (representation.is_a('IfcShapeRepresentation')):
                    for item in representation.Items:
                        if item.is_a('IfcExtrudedAreaSolid'):
                            for point in item.SweptArea.OuterCurve.Points:
                                coord = point.Coordinates
                                pt = Point3d(coord[0], coord[1], 0)
                                polyline_pts.append(pt)
        polyline = Polyline(polyline_pts)
        print(polyline)
        return polyline