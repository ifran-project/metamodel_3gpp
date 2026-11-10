"""Radio Unit (RU) models."""

from enum import StrEnum, auto
from typing import Literal

from pydantic import Field

from metamodel_3gpp.models.base import StrictBaseModel


class RUType(StrEnum):
    """Radio Unit vendor types."""

    SIMULATED = auto()
    """Simulated Radio Unit."""

    REAL = auto()
    """Real Radio Unit."""


class RU(StrictBaseModel):
    """Radio Unit."""

    type: RUType = Field(default=RUType.SIMULATED)
    """RU type."""

    clockSource: Literal["internal", "external"] = Field(default="internal")
    """Clock synchronization source."""

    timeSource: Literal["internal", "external"] = Field(default="internal")
    """Time synchronization source."""

    numberOfTxPorts: int = Field(default=1, ge=1)
    """Number of transmit antenna ports to be used."""

    numberOfRxPorts: int = Field(default=1, ge=1)
    """Number of receive antenna ports to be used."""

    txAttenuationDB: int = Field(default=0, ge=0)
    """Transmit attenuation in dB."""

    rxAttenuationDB: int = Field(default=0, ge=0)
    """Receive attenuation in dB."""

    txGainDB: int = Field(default=35)
    """Transmit gain in dB."""

    rxGainDB: int = Field(default=75)
    """Receive gain in dB."""
