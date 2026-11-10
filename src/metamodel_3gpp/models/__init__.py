"""3GPP-based 5G/6G models."""

from .core import Core
from .metamodel import MetaModel
from .ran import RAN
from .ric import RIC
from .ru import RU
from .slice import Slice
from .ue import UE

__all__ = [
    "MetaModel",
    "Core",
    "RAN",
    "RU",
    "RIC",
    "Slice",
    "UE",
]
