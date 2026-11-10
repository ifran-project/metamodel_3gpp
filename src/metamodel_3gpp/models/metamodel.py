"""Full 3GPP 5G/6G metamodel."""

from typing import Any

from pydantic import Field, field_validator

from metamodel_3gpp.models.base import StrictBaseModel
from metamodel_3gpp.models.core import Core
from metamodel_3gpp.models.ran import RAN
from metamodel_3gpp.models.ric import RIC
from metamodel_3gpp.models.ru import RU
from metamodel_3gpp.models.slice import Slice
from metamodel_3gpp.models.ue import UE


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
