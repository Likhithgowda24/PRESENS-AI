"""
Custom Camera Selector Component for PRESENS AI
Allows users to explicitly select between System Camera, Iriun, or any external USB webcam.
"""

import os
import base64
import io
from PIL import Image
import streamlit.components.v1 as components

_COMPONENT_DIR = os.path.dirname(os.path.abspath(__file__))
_camera_component = components.declare_component(
    "camera_selector_widget",
    path=_COMPONENT_DIR
)


def render_camera_selector(key=None):
    """
    Renders an HTML5 camera capture component with explicit device selection dropdown.
    Returns: BytesIO object of captured image or None.
    """
    raw_base64 = _camera_component(key=key, default=None)

    if raw_base64 and isinstance(raw_base64, str) and "data:image" in raw_base64:
        try:
            header, encoded = raw_base64.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            return io.BytesIO(img_bytes)
        except Exception as e:
            print(f"Error decoding base64 image: {e}")
            return None

    return None
