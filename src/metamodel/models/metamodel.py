"""Full meta model."""

from typing import Any

from pydantic import Field, field_validator

from metamodel.models.base import StrictBaseModel
from metamodel.models.core import Core
from metamodel.models.ran import RAN
from metamodel.models.ric import RIC
from metamodel.models.ru import RU
from metamodel.models.slice import Slice
from metamodel.models.ue import UE


class MetaModel(StrictBaseModel):
    """Meta Model describing the 5G network to be deployed."""

    core: Core = Field(default_factory=Core)
    """5G core."""

    ran: RAN = Field(default_factory=RAN)
    """RAN."""

    rus: dict[str, RU] = Field(default_factory=lambda: {"sim_ru": RU()})
    """RUs."""

    ues: dict[str, UE] = Field(default_factory=lambda: {"sim_ue": UE()})
    """UEs."""

    slices: dict[str, Slice] = Field(default_factory=lambda: {"internet": Slice()})
    """Slices."""

    ric: RIC = Field(default_factory=RIC)
    """RIC."""


    @field_validator("slices", mode="before")
    @classmethod
    def populate_slice_names(cls, value) -> dict[str, Any] | Any:
        """Populate slice names with slices dict keys after validation."""

        if isinstance(value, dict):
            for slice_name, slice_data in value.items():
                if isinstance(slice_data, dict):
                    slice_data["name"] = slice_name
                value[slice_name] = slice_data

        return value
