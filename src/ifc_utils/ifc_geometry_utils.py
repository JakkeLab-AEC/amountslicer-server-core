from typing import  List, Union, Any

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element

from ..data_structure.utils import DataStructureHelper
from ..model.model_geometry import *
from ..model.model_elements import *

class IfcGeometryUtil:
    """
    Utility for extracting or parsing Geometric datas from IFC Files.
    """
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
    def extract_slab_profile(element: ifcopenshell.entity_instance) -> SlabProfile:
        if element.is_a('IfcSlab'):
            representations = element.Representation.Representations
            swept_solid = list(filter(lambda x : x.RepresentationType == 'SweptSolid', representations))[0]
            item = swept_solid.Items[0]

            #Create Polyline
            points = [point for point in item.SweptArea.OuterCurve.Points]
            polyline_pts = IfcGeometryHelper.extract_points(points)
            polyline = Polyline(polyline_pts)

            #Get Depth
            depth = item.Depth
            profile = SlabProfile(polyline, depth)
            return profile
        else:
            return None
    @staticmethod
    def parse_slab(element) -> Slab:
        if element.is_a('IfcSlab'):
            profile = IfcGeometryUtil.extract_slab_profile(element)
            return Slab(profile)
        else:
            return None
    @staticmethod
    def extract_wall_standard_profile(element: ifcopenshell.entity_instance, thickness: float) -> WallStandardProfile:
        if element.is_a('IfcWallStandardCase'):
            representations = element.Representation.Representations
            crv = list(filter(lambda x: x.RepresentationType == 'Curve2D', representations))[0]
            crv_points = crv.Items[0].Points
            point_start = crv_points[0].Coordinates
            point_start_3d = Point3d(point_start[0], point_start[1], 0)
            point_end = crv_points[1].Coordinates
            point_end_3d = Point3d(point_end[0], point_end[1], 0)

            line = Line(point_start_3d, point_end_3d)
            return WallStandardProfile(line, thickness)
        else:
            return None

    @staticmethod
    def extract_wall_standard_layers(element: ifcopenshell.entity_instance) -> WallLayerSet:
        if element.is_a('IfcWallStandardCase'):
            layer_set = element.HasAssociations[0].RelatingMaterial.ForLayerSet
            layer_set_name = layer_set.LayerSetName
            layers = []
            for item in layer_set.MaterialLayers:
                thickness = item.LayerThickness
                name = item.Name
                layer = WallLayer(name, thickness)
                layers.append(layer)
            return WallLayerSet(layer_set_name, layers)
        else:
            return None

    @staticmethod
    def parse_wall_standard(element: ifcopenshell.entity_instance) -> WallStandard:
        if element.is_a('IfcWallStandardCase'):
            layer_set = IfcGeometryUtil.extract_wall_standard_layers(element)
            profile = IfcGeometryUtil.extract_wall_standard_profile(element, layer_set.total_thickness())
            return WallStandard(profile, layer_set)
        else:
            return None

class IfcGeometryHelper:
    @staticmethod
    def extract_points(input: Any) -> Union[List[Point3d], None]:
        points = []

        if all(hasattr(item, 'Coordinates') for item in input):
            input = [point.Coordinates for point in input]

        flat_list = DataStructureHelper.flatten_as_points(input)
        for item in flat_list:
            if isinstance(item, tuple) and all(isinstance(coord, (int, float)) for coord in item):
                if len(item) == 2:
                    points.append(Point3d(item[0], item[1], 0))
                elif len(item) == 3:
                    points.append(Point3d(item[0], item[1], item[2]))
            elif hasattr(item, 'Coordinates'):
                coords = item.Coordinates
                if len(coords) == 2:
                    points.append(Point3d(coords[0], coords[1], 0))
                elif len(coords) == 3:
                    points.append(Point3d(coords[0], coords[1], coords[2]))
        return points if points else None