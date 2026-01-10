import json
from typing import Any, Dict, Union, Tuple

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert #FF0000 to (255, 0, 0)"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def normalize_color(color: Union[str, list, tuple]) -> tuple:
    """Handle both "#FF0000" and [255, 0, 0, 255]"""
    if isinstance(color, str) and color.startswith('#'):
        return hex_to_rgb(color)
    elif isinstance(color, (list, tuple)):
        return tuple(int(c) for c in color)
    return (0, 0, 0)

def load_template(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)