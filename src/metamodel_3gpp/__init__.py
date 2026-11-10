"""3GPP-based 5G/6G metamodel."""

from .models import (
    RAN,
    RIC,
    RU,
    UE,
    Core,
    MetaModel,
    Slice,
)

__all__ = [
    "MetaModel",
    "Core",
    "RAN",
    "RU",
    "RIC",
    "Slice",
    "UE",
]
