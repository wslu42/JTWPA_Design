from .tech import LAYER

__all__ = [
    "LAYER",
    "PDK",
    "get_pdk",
]


def __getattr__(name: str):
    if name in {"PDK", "get_pdk"}:
        from . import pdk

        return getattr(pdk, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")
