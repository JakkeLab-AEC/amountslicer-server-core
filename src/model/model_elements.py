from abc import ABC, abstractmethod
from ..model.model_geometry import *
from typing import List
from ..element_type.ifc_type_enum import *

#Base class
class Element(ABC):
    """
    Base class for elements like Slab, Wall, Columns
    """

    def __init__(self):
        self.element_type = None
        self.set_element_type()

    @abstractmethod
    def set_element_type(self):
        pass
    @abstractmethod
    def get_geometry(self) -> 'ElementGeometry':
        pass

class ElementGeometry(ABC):
    pass

#region Slab
class Slab(Element):
    def __init__(self, profile: 'SlabProfile'):
        super().__init__()
        self.geometry = profile

    def set_element_type(self):
        self.element_type = ElementType.IFC_SLAB

    def get_geometry(self) -> ElementGeometry:
        return self.geometry

class SlabProfile(ElementGeometry):
    def __init__(self, boundary: Polyline, depth: float):
        self.boundary_curve = boundary
        self.depth = depth
#endregion

#region Wall
class WallStandard(Element):
    def __init__(self, profile: 'WallStandardProfile', layer_set: 'WallLayerSet'):
        super().__init__()
        self.layer_set = layer_set
        self.geometry = profile

    def set_element_type(self):
        self.element_type = ElementType.IFC_WALL_STANDARD_CASE

    def get_geometry(self) -> 'ElementGeometry':
        return self.geometry

class WallStandardProfile(ElementGeometry):
    def __init__(self, line: Line, thickness: float):
        super().__init__()
        self.center_line = line
        self.thickness = thickness

class WallLayer:
    def __init__(self, name: str, thickness: float):
        self.name = name
        self.thickness = thickness

class WallLayerSet:
    def __init__(self, name: str, layers: List[WallLayer]):
        self.name = name
        self.layers = layers

    def total_thickness(self) -> float:
        return sum(layer.thickness for layer in self.layers)
#endregion
