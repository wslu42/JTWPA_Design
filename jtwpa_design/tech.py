"""Technology definitions."""

import gdsfactory as gf
import yaml
from gdsfactory.technology import LayerViews
from gdsfactory.typings import Layer

from jtwpa_design.config import PATH


class LayerMapQPDK(gf.technology.LayerMap):
    """Layer map for QPDK technology.

    Simplified version for 2D layout only - no simulation features.
    """

    # Basic metal layers
    MAIN_METAL: Layer = (1, 0)
    JJ: Layer = (2, 0)
    AIR_BRIDGE_CONTACT: Layer = (3, 0)
    AIR_BRIDGE: Layer = (3, 1)
    GROUND_MASK: Layer = (1, 1)
    WG: Layer = (102, 0)  # Waveguide layer


# Load layer views from yaml
with open(PATH.lyp_yaml) as f:
    layer_data = yaml.safe_load(f)

LAYER_VIEWS = LayerViews(layer_views=layer_data)

# Use class directly for layer access
L = LAYER = LayerMapQPDK
