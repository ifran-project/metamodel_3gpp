"""3GPP-based 5G/6G RAN Intelligent Controller (RIC) models."""

from enum import StrEnum, auto
from typing import Annotated, Literal

from pydantic import Field

from metamodel_3gpp.models.common import (
    E2,
    Category5G,
    Component5G,
    Network5G,
    StrictBaseModel,
)


class RICComponentType(StrEnum):
    """RIC component types."""

    RIC = auto()
    """Core Near-Real-Time RAN Intelligent Controller platform."""

    DBAAS = auto()
    """Database as a Service (Shared Data Layer) for shared state storage."""

    E2MGR = auto()
    """E2 Manager for managing E2 node setups, connections, and resets."""

    E2TERM = auto()
    """E2 Termination handling SCTP protocol and E2AP messaging with E2 nodes."""

    RTMGR = auto()
    """Route Manager for generating and distributing RMR routing tables."""

    SUBMGR = auto()
    """Subscription Manager for handling E2 subscriptions between xApps and E2 nodes."""

    APPMGR = auto()
    """App Manager for managing xApp lifecycles (deployment, status, and deletion)."""

    CHARTMUSEUM = auto()
    """Helm chart repository for hosting xApp deployment packages."""

    XAPP_ONBOARDER = auto()
    """xApp Onboarder for parsing, validating, and uploading xApp charts to ChartMuseum."""

    A1MEDIATOR = auto()
    """A1 Mediator for terminating the A1 interface and managing policy guidance."""


class RICComponentConfig(StrictBaseModel):
    """Generic RIC component configuration."""


class SingleRICConfig(RICComponentConfig):
    """Single RIC component configuration exposing E2 interface."""

    e2: E2 = Field(default_factory=E2)
    """E2 endpoint used to reach the RAN."""


class RICComponent(Component5G):
    """Generic RIC component."""

    category: Literal[Category5G.RIC] = Field(default=Category5G.RIC, frozen=True)

    type: RICComponentType = Field()
    """RIC component type."""

    config: RICComponentConfig = Field(default_factory=RICComponentConfig)
    """RIC configuration."""


class SingleRICComponent(RICComponent):
    """Single RIC component."""

    type: Literal[RICComponentType.RIC] = Field(frozen=True)
    config: SingleRICConfig = Field(default_factory=SingleRICConfig)


class E2TermComponent(RICComponent):
    """O-RAN SC E2 Termination component."""

    type: Literal[RICComponentType.E2TERM] = Field(frozen=True)
    config: SingleRICConfig = Field(default_factory=SingleRICConfig)


# type used to tell pydantic which ran component to chose for validation based on the type
type ValidatedRICComponent = Annotated[SingleRICComponent | E2TermComponent, Field(discriminator="type")]


class RIC(Network5G):
    """5G RAN Intelligent Controller network."""

    components: dict[str, ValidatedRICComponent | RICComponent] = Field(
        default_factory=lambda: {
            "ric": SingleRICComponent(type=RICComponentType.RIC),
        }
    )
    """RIC components."""
