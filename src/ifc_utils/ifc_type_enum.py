from enum import Enum
import ifcopenshell
import ifcopenshell.util.element

class GeometryType(Enum):
    IFC_WALL = "IfcWall"
    IFC_WALL_STANDARD_CASE = "IfcWallStandardCase"
    IFC_SLAB = "IfcSlab"
    IFC_COLUMN = "IfcColumn"
    IFC_BEAM = "IfcBeam"
    IFC_FOOTING = "IfcFooting"
    IFC_ROOF = "IfcRoof"
    IFC_STAIR = "IfcStair"
    IFC_STAIR_FLIGHT = "IfcStairFlight"
    IFC_DOOR = "IfcDoor"
    IFC_WINDOW = "IfcWindow"
    IFC_COVERING = "IfcCovering"
    IFC_RAILING = "IfcRailing"
    IFC_RAMP = "IfcRamp"
    IFC_RAMP_FLIGHT = "IfcRampFlight"
    IFC_BUILDING_ELEMENT_PROXY = "IfcBuildingElementProxy"
    IFC_PILE = "IfcPile"
    IFC_MEMBER = "IfcMember"
    IFC_PLATE = "IfcPlate"
    IFC_CURTAIN_WALL = "IfcCurtainWall"
    IFC_FURNISHING_ELEMENT = "IfcFurnishingElement"
    IFC_SHADING_DEVICE = "IfcShadingDevice"
    IFC_TRANSPORT_ELEMENT = "IfcTransportElement"
    IFC_ENERGY_CONVERSION_DEVICE = "IfcEnergyConversionDevice"
    IFC_FLOW_FITTING = "IfcFlowFitting"
    IFC_FLOW_SEGMENT = "IfcFlowSegment"
    IFC_FLOW_CONTROLLER = "IfcFlowController"
    IFC_FLOW_TERMINAL = "IfcFlowTerminal"
    IFC_FLOW_STORAGE_DEVICE = "IfcFlowStorageDevice"
    IFC_FLOW_MOVING_DEVICE = "IfcFlowMovingDevice"

    @staticmethod
    def has_geometry_type(element: ifcopenshell.entity_instance) -> bool:
        return element.is_a() in { gt.value for gt in GeometryType }

