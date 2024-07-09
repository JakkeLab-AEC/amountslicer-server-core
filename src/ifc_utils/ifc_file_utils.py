import ifcopenshell

class IfcUtilsFile:
    @staticmethod
    def load(path, is_stream=False) -> ifcopenshell.file:
        try:
            ifc_file = ifcopenshell.open(path=path, should_stream=is_stream)
            return ifc_file
        except Exception as e:
            print(f"An error occurred while opening the IFC file: {e}")
            return None