import json
import os

def write_json(data, output_path: str):
    """Serialize ``data`` to a JSON file.

    Parameters
    ----------
    data : Any
        JSON-serializable Python object.
    output_path : str
        Destination path for the JSON file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
