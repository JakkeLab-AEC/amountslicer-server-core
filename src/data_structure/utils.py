from typing import List, Union, Any

class DataStructureHelper:
    @staticmethod
    def flatten_as_points(input: Any) -> List[Any]:
        print("flatten_as_points called")
        flat_list = []

        def _flatten(item):
            if isinstance(item, list) or isinstance(item, tuple):
                if all(isinstance(sub_item, (int, float)) for sub_item in item):
                    flat_list.append(item)
                else:
                    for sub_item in item:
                        _flatten(sub_item)
        _flatten(input)
        return flat_list