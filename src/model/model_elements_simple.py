from abc import ABC, abstractmethod
from ..element_type.ifc_type_enum import *
from typing import Any, Union
import logging

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
from ifcopenshell import ifcopenshell_wrapper
import numpy as np
from stl import mesh

# 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#region Base class
class ElementSimple(ABC):
    """
    Base class for elements like Slab, Wall, Columns.
    Simply record element type and Geometry
    """

    def __init__(self, element: ifcopenshell.entity_instance):
        self.element_geometry: Union[ifcopenshell_wrapper.BRepElement, ifcopenshell_wrapper.TriangulationElement, ifcopenshell_wrapper.SerializedElement, None] = None
        self.element_type = None
        self.set_element_type()
        self.set_geometry(element)

    @abstractmethod
    def set_element_type(self):
        pass

    def get_geometry_element(self) -> Union[ifcopenshell_wrapper.BRepElement, ifcopenshell_wrapper.TriangulationElement, ifcopenshell_wrapper.SerializedElement, None]:
        return self.geometry_element

    def set_geometry(self, element: ifcopenshell.entity_instance):
        try:
            settings = ifcopenshell.geom.settings()
            shape = ifcopenshell.geom.create_shape(settings, element)
            if isinstance(shape, ifcopenshell_wrapper.BRepElement):
                self.geometry_element = shape
            elif isinstance(shape, ifcopenshell_wrapper.TriangulationElement):
                self.geometry_element = shape
            elif isinstance(shape, ifcopenshell_wrapper.SerializedElement):
                self.geometry_element = shape
            else:
                logger.error(f"Unsupported geometry type for element {element.GlobalId}")
        except Exception as e:
            logger.error(f"Failed to create geometry for element {element.GlobalId}: {e}")
#endregion

#region Sub Classes

class SlabSimple(ElementSimple):
    def __init__(self, element: ifcopenshell.entity_instance):
        super().__init__(element)

    def set_element_type(self):
        self.element_type = ElementType.IFC_SLAB

#endregion
