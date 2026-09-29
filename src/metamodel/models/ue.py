"""User Equipment (UE) models."""

from enum import StrEnum, auto
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Any, Literal, Self

from pydantic import (
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from metamodel.models.base import StrictBaseModel
from metamodel.models.common import (
    BitRate,
    Category5G,
    Component5G,
)
from metamodel.utils import (
    parse_hex_int,
    serialize_hex_int,
)


class UEType(StrEnum):
    """Supported UE types."""

    CONTAINERIZED = auto()
    """Software-based UE stack (can be simulated or real RF)."""

    COTS = auto()
    """Physical Commercial Off-The-Shelf (COTS) UE."""


class SSCMode(StrEnum):
    """
    Session and Service Continuity (SSC) mode.

    3GPP References:
        - 3GPP TS 23.501 clause 5.6.9
    """

    SSC_MODE_1 = auto()
    """SSC mode 1: The core network maintains the established user plane connectivity."""

    SSC_MODE_2 = auto()
    """SSC mode 2: User plane connectivity is released before establishing new connectivity."""

    SSC_MODE_3 = auto()
    """SSC mode 3: Make-before-break; new connectivity is established before releasing old."""


class AuthenticationMethod(StrEnum):
    """
    Authentication method used for 5GS access.

    3GPP References:
        - 3GPP TS 23.501 clause 5.16.2
        - 3GPP TS 33.501 clause 6
        - 3GPP TS 24.501
    """

    FIVE_G_AKA = "5G_AKA"
    """5G Authentication and Key Agreement."""

    EAP_AKA_PRIME = "EAP_AKA_PRIME"
    """Extensible Authentication Protocol-AKA'."""

    EAP_TLS = "EAP_TLS"
    """Extensible Authentication Protocol-Transport Layer Security."""


class UESubscriptionData(StrictBaseModel):
    """
    UE subscription data.

    Represents subscription information associated with a UE/SUPI,
    independent of an individual PDU Session.

    3GPP References:
        - 3GPP TS 23.501 clause 5.15
        - 3GPP TS 23.502
        - 3GPP TS 29.503
    """

    snssai: str = Field(default="internet")
    """Name reference to a defined slice associated with this PDU session."""

    dnn: str = Field(default="internet")
    """Name reference to DNN associated with this PDU session, defined in the given slice."""


class UEAuthenticationData(StrictBaseModel):
    """
    UE authentication subscription data.

    Contains authentication parameters required for 5G Authentication
    and Key Agreement (5G-AKA) and related authentication methods.

    3GPP References:
        - 3GPP TS 33.501 clause 6
        - 3GPP TS 31.102
        - 3GPP TS 35.206
        - 3GPP TS 29.503
    """

    k: str = Field(default="fec86ba6eb707ed08905757b1bb44b8f", min_length=32, max_length=32)
    """Subscriber permanent key (K). 128-bit value."""

    opc: str = Field(default="C42449363BBAD02B66D16BC975D77CC1", min_length=32, max_length=32)
    """Operator Variant Algorithm Configuration Field (OPc). 128-bit value."""

    op: str | None = Field(default=None, min_length=16, max_length=16)
    """Operator Code (OP). 128-bit value."""

    amf: int = Field(default=0x8000, ge=0, le=0xFFFF)
    """Authentication Management Field (AMF). 16-bit value."""

    sqn: int = Field(default=0, ge=0, le=0xFFFFFFFFFFFF)
    """Sequence Number (SQN). 48-bit value."""

    authenticationMethod: AuthenticationMethod = Field(default=AuthenticationMethod.FIVE_G_AKA)
    """Authentication method used for 5GS access."""


    @field_validator("amf", "sqn", mode="before")
    @classmethod
    def normalize_hex_int(cls, value) -> int | Any:
        """Convert hexadecimal strings to integers."""

        return parse_hex_int(value)


    @field_serializer("amf")
    def serialize_amf(self, value: int | None) -> str | None:
        """Serialize AMF as a four-digit hexadecimal string."""

        return serialize_hex_int(value, 4)


    @field_serializer("sqn")
    def serialize_sqn(self, value: int) -> str | None:
        """Serialize SQN as a twelve-digit hexadecimal string."""

        return serialize_hex_int(value, 12)


class UEPDUSession(StrictBaseModel):
    """
    UE PDU Session configuration.

    Defines a UE-associated PDU Session towards a Data Network.

    3GPP References:
        - 3GPP TS 23.501 clause 5.6
        - 3GPP TS 24.501
    """

    subscriptionIndex: int = Field(ge=0, default=0)
    """
    Index of the UE subscription data used by this PDU Session.
    The referenced subscription provides the S-NSSAI and DNN.
    """

    sscMode: SSCMode = Field(default=SSCMode.SSC_MODE_1)
    """SSC mode for this PDU Session."""

    ueIPv4Address: IPv4Address | None = Field(default=None)
    """UE IPv4 address allocated to this PDU Session."""

    ueIPv6Address: IPv6Address | None = Field(default=None)
    """UE IPv6 address allocated to this PDU Session."""

    ipAllocationMethod: Literal["DYNAMIC", "STATIC"] = Field(default="DYNAMIC")
    """UE IP address allocation method."""

    sessionAmbr: BitRate | None = Field(default=None)
    """
    Session-AMBR applicable to this PDU Session.
    If omitted, the applicable value may be inherited from subscription/DNN configuration.
    """


class UEConfiguration(StrictBaseModel):
    """
    User Equipment (UE) configuration.

    Represents a 5G subscriber equipment profile.

    3GPP References:
        - 3GPP TS 23.003
        - 3GPP TS 23.501
        - 3GPP TS 24.501
    """

    timeZone: str = Field(default="Europe/Paris")
    """UE timezone."""

    supi: str = Field(default="001010000000100", pattern=r"^[0-9]{15}$")
    """UE Subscription Permanent Identifier (SUPI). For IMSI-based SUPI, this contains the IMSI digits."""

    pei: str = Field(default="356938035643803", pattern=r"^[0-9]{14,16}$")
    """
    Permanent Equipment Identifier (PEI).
    For an IMEI/IMEISV-based PEI, this contains the corresponding decimal identifier.
    """

    authenticationData: UEAuthenticationData = Field(default_factory=UEAuthenticationData)
    """UE authentication subscription data."""

    subscriptions: list[UESubscriptionData] = Field(default_factory=lambda: [UESubscriptionData()])
    """S-NSSAI/DNN subscription data available to the UE."""

    pduSessions: list[UEPDUSession] = Field(default_factory=lambda: [UEPDUSession()])
    """List of UE PDU Sessions."""

    ueAmbr: BitRate = Field(default_factory= lambda: BitRate(uplink="1Gbps", downlink="1Gbps")) # type: ignore
    """UE AMBR."""

    gnbs: list[str] = Field(default_factory= lambda: ["gnb"])
    """List of name reference to defined GNB/DU components to connect the UE to."""

    ru: str | None = Field(default="sim_ru")
    """Name reference to a defined RU to be used by the UE (only relevant for containerized UEs)."""

    nrBands: list[Annotated[int, Field(ge=1, le=303)]] = Field(default_factory=lambda: [78])
    """NR operating bands used by the UE."""


    @model_validator(mode="after")
    def validate_pdu_session_subscription_indexes(self) -> Self:
        """Ensure that PDU sessions 'subscriptionIndex' reference valid subscriptions."""

        if self.pduSessions:
            max_index = max(session.subscriptionIndex for session in self.pduSessions)

            if max_index >= len(self.subscriptions):
                raise ValueError(
                    f"UE 'pduSessions' references out of range 'subscriptionIndex' "
                    f"({max_index} > {len(self.subscriptions) - 1})."
                )

        return self


class UE(Component5G):
    """User Equipment."""

    category: Literal[Category5G.UE] = Field(default=Category5G.UE, frozen=True)

    type: UEType = Field(default=UEType.CONTAINERIZED)
    """UE type."""

    config: UEConfiguration = Field(default_factory=UEConfiguration)
    """UE configuration."""


    @model_validator(mode="after")
    def validate_ru(self) -> Self:
        """Ensure that 'ru' is set for containerized UEs and None for COTS UEs."""

        if self.type is UEType.CONTAINERIZED and self.config.ru is None:
            raise ValueError("'ru' is required for containerized UE.")

        if self.type is UEType.COTS:
            self.config.ru = None

        return self


    @model_validator(mode="after")
    def validate_pdu_sessions(self) -> Self:
        """Ensure that containerized UEs have at least one PDU session."""

        if self.type is UEType.CONTAINERIZED and not self.config.pduSessions:
                raise ValueError("Containerized UE needs at least one PDU session.")

        return self
