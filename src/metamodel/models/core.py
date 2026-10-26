"""5G core models."""

from enum import StrEnum, auto
from typing import Annotated, Any, Literal

from pydantic import (
    Field,
    TypeAdapter,
    computed_field,
    field_serializer,
    field_validator,
)

from metamodel.models.base import (
    StrictBaseModel,
    TolerantBaseModel,
)
from metamodel.models.common import (
    NGAP,
    PFCP,
    TLS,
    Category5G,
    Component5G,
    GTPUEndpoint,
    N6Endpoint,
    Network5G,
    SecurityAlgorithmConfiguration,
    TransportEndpoint,
)
from metamodel.utils import (
    URL,
    parse_hex_int,
    serialize_hex_int,
)


class CoreComponentType(StrEnum):
    """5G core components."""

    AMF = auto()
    """Access and Mobility Management Function."""

    SMF = auto()
    """Session Management Function."""

    UPF = auto()
    """User Plane Function."""

    AUSF = auto()
    """Authentication Server Function."""

    UDM = auto()
    """Unified Data Management."""

    UDR = auto()
    """Unified Data Repository."""

    PCF = auto()
    """Policy Control Function."""

    CHF = auto()
    """Charging Function."""

    NRF = auto()
    """Network Repository Function."""

    NSSF = auto()
    """Network Slice Selection Function."""

    NEF = auto()
    """Network Exposure Function."""

    NWDAF = auto()
    """Network Data Analytics Function."""

    BSF = auto()
    """Binding Support Function."""

    SEPP = auto()
    """Security Edge Protection Proxy."""

    SCP = auto()
    """Service Communication Proxy."""

    LMF = auto()
    """Location Management Function."""


class SBI(TransportEndpoint):
    """
    Service-Based Interface (SBI) configuration.

    Defines the transport endpoint used by a Network Function (NF)
    to expose SBI services.

    3GPP References:
        - 3GPP TS 29.500
        - 3GPP TS 29.501
        - 3GPP TS 29.510
    """

    protocol: Literal["TCP"] = Field(default="TCP")

    scheme: Literal["http", "https"] = Field(default="http")
    """URI scheme used for the SBI endpoint."""

    port: int = Field(default=80, ge=1,le=65535)
    """TCP port of the SBI endpoint."""

    apiVersion: str = Field(default="v1", pattern=r"^v\d+$")
    """Service API version."""

    tls: TLS = Field(default_factory=TLS)
    """Transport Layer Security (TLS) configuration."""


# NOTE after serialization and deserialization, the mncLength and plmnId might be given as input but should be tolerated
class PLMN(TolerantBaseModel):
    """
    Public Land Mobile Network (PLMN) Identity.

    3GPP References:
        - 3GPP TS 23.003, clause 2.2 (PLMN Identity)
        - 3GPP TS 24.501
        - 3GPP TS 29.571
    """

    mcc: int = Field(default=1, ge=0, le=999)
    """Mobile Country Code (MCC) (3 digits)."""

    mnc: int = Field(default=1, ge=0, le=999)
    """Mobile Network Code (MNC) (2 to 3 digits)."""

    @computed_field
    @property
    def mncLength(self) -> int:
        """Length of the MNC field (2 or 3)."""

        return 2 if self.mnc < 100 else 3  # noqa: PLR2004

    @computed_field
    @property
    def plmnId(self) -> str:
        """PLMN identity (MCC + MNC)."""

        return f"{self.mcc:03d}{self.mnc:02d}" if self.mnc < 100 else f"{self.mcc:03d}{self.mnc:03d}"  # noqa: PLR2004


    @field_validator("mcc", "mnc", mode="before")
    @classmethod
    def parse_code(cls, value) -> int | Any:
        """Convert string MCC and MNC values to integers."""

        if isinstance(value, str):
            if not value.isdigit():
                raise ValueError("MCC and MNC must contain only digits.")
            return int(value)
        return value


    @field_serializer("mcc")
    def serialize_mcc(self, value: int) -> str:
        """Serialize MCC as a three-digit string."""

        return f"{value:03d}"


    @field_serializer("mnc")
    def serialize_mnc(self, value: int) -> str:
        """Serialize MNC as a two or three-digit string."""

        return f"{value:02d}" if value < 100 else f"{value:03d}"  # noqa: PLR2004


class PLMNSupportItem(StrictBaseModel):
    """
    Association between a PLMN Identity and supported S-NSSAIs.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 29.510
        - 3GPP TS 29.571
    """

    plmnId: PLMN = Field(default_factory=PLMN)
    """PLMN Identity."""

    snssaiList: list[str] = Field(default_factory=lambda: ["internet"])
    """List of name references to defined slices to be supported by this PLMN."""


class TAI(StrictBaseModel):
    """
    Tracking Area Identity (TAI).

    3GPP References:
        - 3GPP TS 23.003, clause 19.4
        - 3GPP TS 24.501
        - 3GPP TS 38.413
    """

    plmnId: PLMN = Field(default_factory=PLMN)
    """PLMN Identity."""

    tac: int = Field(default=1, ge=0, le=65535)
    """Tracking Area Code (16 bits)."""


# NOTE after serialization and deserialization, the computed amfId be given as input but should be tolerated
class GUAMI(TolerantBaseModel):
    """
    Globally Unique AMF Identifier (GUAMI).

    3GPP References:
        - 3GPP TS 23.003, clause 2.10
        - 3GPP TS 23.501
        - 3GPP TS 38.413
    """

    plmnId: PLMN = Field(default_factory=PLMN)
    """PLMN Identity."""

    amfRegionId: int = Field(default=0x02, ge=0, le=0xFF)
    """AMF Region Identifier (8 bits)."""

    amfSetId: int = Field(default=0x001, ge=0, le=0x3FF)
    """AMF Set Identifier (10 bits)."""

    amfPointer: int = Field(default=0x00, ge=0, le=0x3F)
    """AMF Pointer (6 bits)."""

    @computed_field
    @property
    def amfId(self) -> int:
        """
        AMF Identifier (24-bit integer).

        Concatenates the fields into a single 24-bit value:
        [ Region ID (8 bits) ] [ Set ID (10 bits) ] [ Pointer (6 bits) ]

        - Region ID shifts left by 16 bits (10 + 6) to occupy bits 16-23.
        - Set ID shifts left by 6 bits to occupy bits 6-15.
        - Pointer occupies the lowest 6 bits (bits 0-5).
        """
        return (self.amfRegionId << 16) | (self.amfSetId << 6) | self.amfPointer

    @field_validator("amfRegionId", "amfSetId", "amfPointer", mode="before")
    @classmethod
    def normalize_hex_values(cls, value) -> int | Any:
        """Convert hexadecimal strings to integers."""

        return parse_hex_int(value)

    @field_serializer("amfRegionId")
    def serialize_amf_region_id(self, value: int) -> str | None:
        """Serialize AMF Region ID as hexadecimal."""

        return serialize_hex_int(value, 2)

    @field_serializer("amfSetId")
    def serialize_amf_set_id(self, value: int) -> str | None:
        """Serialize AMF Set ID as hexadecimal."""

        return serialize_hex_int(value, 3)

    @field_serializer("amfPointer")
    def serialize_amf_pointer(self, value: int) -> str | None:
        """Serialize AMF Pointer as hexadecimal."""

        return serialize_hex_int(value, 2)

    @field_serializer("amfId")
    def serialize_amf_id(self, value: int) -> str | None:
        """Serialize AMF ID as hexadecimal."""

        return serialize_hex_int(value, 6)


class NetworkName(StrictBaseModel):
    """
    Network Name.

    Broadcast network names provided by the AMF.

    3GPP References:
        - 3GPP TS 23.003
        - 3GPP TS 24.501
    """

    fullNetworkName: str = Field(default="5G_network")
    """Full Network Name."""

    shortNetworkName: str | None = Field(default=None)
    """Short Network Name."""


class NSIInformation(StrictBaseModel):
    """
    Network Slice Instance information.

    3GPP References:
        - 3GPP TS 29.531
        - 3GPP TS 29.571
    """

    nrfId: URL = Field(default=TypeAdapter(URL).validate_python("http://cn5g-nrf:8080/nnrf-disc/v1/nf-instances"))
    """NRF discovery URI used to discover Network Functions."""

    nsiId: int = Field(default=1)
    """Network Slice Instance identifier."""

    nrfNfMgtUri: URL | None = Field(default=TypeAdapter(URL).validate_python("http://cn5g-nrf:8080/nnrf-nfm/v1/nf-instances"))
    """NRF NF management URI."""


class NSIInfo(StrictBaseModel):
    """
    Network Slice Instance information associated with an S-NSSAI.

    3GPP References:
        - 3GPP TS 29.531
    """

    snssai: str = Field(default="internet")
    """Name reference to a defined slice associated with this Network Slice Instance."""

    nsiInformationList: list[NSIInformation] = Field(default_factory=lambda: [NSIInformation()])
    """Network Slice Instance information."""


class RestrictedSNSSAIList(StrictBaseModel):
    """
    Restricted S-NSSAI list associated with a home PLMN.

    3GPP References:
        - 3GPP TS 29.531
    """

    homePlmnId: PLMN = Field(default_factory=PLMN)
    """Home PLMN identity for which the S-NSSAI restriction applies."""

    snssaiList: list[str] = Field(default_factory=lambda: ["internet"])
    """List of name references to defined slices to be restricted."""


class SupportedTAIItem(StrictBaseModel):
    """
    S-NSSAI information supported by a Tracking Area.

    3GPP References:
        - 3GPP TS 29.531
    """

    tai: TAI = Field(default_factory=TAI)
    """Tracking Area Identity."""

    snssaiList: list[str] = Field(default_factory=lambda: ["internet"])
    """List of name references to defined slices to be supported."""


class ExtendedSupportedTAIItem(SupportedTAIItem):
    """
    S-NSSAI information supported by a Tracking Area.

    3GPP References:
        - 3GPP TS 29.531
    """

    restrictedSnssaiList: list[RestrictedSNSSAIList] = Field(default_factory=list)
    """List of name references to defined slices to be restricted."""


class SupportedNSSAIAvailabilityData(StrictBaseModel):
    """
    Supported S-NSSAI availability information for an AMF.

    3GPP References:
        - 3GPP TS 29.531
    """

    tai: TAI = Field(default_factory=TAI)
    """Tracking Area Identity for the supported S-NSSAI availability information."""

    snssaiList: list[str] = Field(default_factory=lambda: ["internet"])
    """List of name references to defined slices to be supported in the given Tracking Area."""

    taiList: list[SupportedTAIItem] | None = Field(default=None)
    """Additional list of TAIs supported by the AMF."""


class AMFInfo(StrictBaseModel):
    """
    AMF information associated with an AMF Set.

    3GPP References:
        - 3GPP TS 29.531
        - 3GPP TS 29.571
    """

    nfId: str = Field(default="405e8251-cc5a-45dd-a494-efb9eaf1cd58")
    """NF Instance ID of the AMF."""

    supportedNssaiAvailabilityData: SupportedNSSAIAvailabilityData = Field(
        default_factory=SupportedNSSAIAvailabilityData)
    """S-NSSAI availability information advertised by the AMF."""


class AMFInfoSet(StrictBaseModel):
    """
    AMF Set information used by the NSSF.

    3GPP References:
        - 3GPP TS 29.531
    """

    targetAmfSet: int = Field(default=0x001, ge=0, le=0x3FF)
    """Target AMF Set identifier."""

    nrfAmfSet: URL = Field(default=TypeAdapter(URL).validate_python("http://nrf/nnrf-nfm/v1/nf-instances"))
    """NRF discovery URI for the AMF Set."""

    nrfAmfSetNfMgtUri: URL = Field(default=TypeAdapter(URL).validate_python("http://nrf/nnrf-nfm/v1/nf-instances"))
    """NRF NF management URI for the AMF Set."""

    amfList: list[AMFInfo] = Field(default_factory=lambda: [AMFInfo()])
    """List of AMFs belonging to the AMF Set."""


    @field_validator("targetAmfSet", mode="before")
    @classmethod
    def normalize_hex_values(cls, value) -> int | Any:
        """Convert hexadecimal strings to integers."""

        return parse_hex_int(value)


    @field_serializer("targetAmfSet")
    def serialize_target_amf_set_id(self, value: int) -> str | None:
        """Serialize target AMF Set ID as hexadecimal."""

        return serialize_hex_int(value, 3)


class PLMNInfo(StrictBaseModel):
    """
    PLMN information configured in the NSSF.

    3GPP References:
        - 3GPP TS 29.531
        - 3GPP TS 29.571
    """

    operatorName: str = Field(default="")
    """Operator name."""

    homePlmnId: PLMN = Field(default_factory=PLMN)
    """Home PLMN identity."""


class CoreComponentConfig(StrictBaseModel):
    """
    Generic 5G Core Network Function configuration.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 29.500
    """

    sbi: SBI = Field(default_factory=SBI)
    """Service-Based Interface configuration."""

    nrfUri: URL | None = Field(default=None)
    """URI of the NRF."""


class AMFConfig(CoreComponentConfig):
    """
    Access and Mobility Management Function (AMF) configuration.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 23.502
        - 3GPP TS 24.501
        - 3GPP TS 29.518
        - 3GPP TS 38.413
    """

    n2: NGAP = Field(default_factory=NGAP)
    """N2 reference point endpoint. Used for NGAP signalling between AMF and NG-RAN."""

    guamiList: list[GUAMI] = Field(default_factory=lambda: [GUAMI()])
    """List of Globally Unique AMF Identifiers (GUAMI) supported by this AMF."""

    taiList: list[TAI] = Field(default_factory=lambda: [TAI()])
    """List of Tracking Area Identities (TAI) served by this AMF."""

    plmnList: list[PLMNSupportItem] = Field(default_factory=lambda: [PLMNSupportItem()])
    """List of supported PLMN identities and associated S-NSSAIs."""

    securityAlgorithmConfiguration: SecurityAlgorithmConfiguration = Field(
        default_factory=SecurityAlgorithmConfiguration)
    """Security algorithm preference configuration."""

    networkName: NetworkName = Field(default_factory=NetworkName)
    """Network Name broadcast by the AMF."""


class AUSFConfig(CoreComponentConfig):
    """
    Authentication Server Function (AUSF) configuration.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 29.510
    """

    plmnList: list[PLMN] = Field(default_factory=lambda: [PLMN()])
    """List of PLMN identities (MCC/MNC) served by this AUSF instance for authentication."""


class SMFConfig(CoreComponentConfig):
    """
    Session Management Function (SMF) configuration.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 23.502
        - 3GPP TS 29.510
        - 3GPP TS 29.502
        - 3GPP TS 29.244
    """

    n4: PFCP = Field(default_factory=PFCP)
    """N4 reference point endpoint. Used for PFCP signalling between SMF and UPF."""

    snssaiList: list[str] = Field(default_factory=lambda: ["internet"])
    """List of name references to defined slices to be supported by this SMF."""

    plmnList: list[PLMN] = Field(default_factory=lambda: [PLMN()])
    """List of PLMN identities (MCC/MNC) served by this SMF instance."""

    taiList: list[TAI] = Field(default_factory=lambda: [TAI()])
    """List of Tracking Area Identities (TAI) served by this SMF."""

    upfs: list[str] = Field(default_factory=lambda: ["upf"])
    """List of name references to defined UPFs to connect to."""


class UPFConfig(CoreComponentConfig):
    """
    User Plane Function (UPF) configuration.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 29.244
        - 3GPP TS 29.281
    """

    snssaiList: list[str] = Field(default_factory=lambda: ["internet"])
    """List of name references to defined slices to be supported by this UPF."""

    n3: GTPUEndpoint = Field(default_factory=GTPUEndpoint)
    """N3 reference point endpoint. GTP-U user-plane tunnel endpoint towards NG-RAN."""

    n4: PFCP = Field(default_factory=PFCP)
    """N4 reference point endpoint. PFCP endpoint towards SMF."""

    n6: N6Endpoint = Field(default_factory=N6Endpoint)
    """N6 reference point endpoint. User-plane connection towards the Data Network (DN)."""

    # chose port 2153 for n9 and keep default 2152 to n3 interface
    n9: GTPUEndpoint = Field(default_factory=lambda: GTPUEndpoint(port=2153))
    """N9 reference point endpoint. GTP-U endpoint used between UPFs."""


class NRFConfig(CoreComponentConfig):
    """
    Network Repository Function (NRF) configuration.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 29.500
        - 3GPP TS 29.510
    """

    plmnList: list[PLMNSupportItem] = Field(default_factory=lambda: [PLMNSupportItem()])
    """List of supported PLMN identities and S-NSSAIs."""


class NSSFConfig(CoreComponentConfig):
    """
    Network Slice Selection Function configuration.

    3GPP References:
        - 3GPP TS 23.501
        - 3GPP TS 29.531
        - 3GPP TS 29.571
    """

    nsiInfoList: list[NSIInfo] = Field(default_factory=lambda: [NSIInfo()])
    """List of Network Slice Instance information."""

    taInfoList: list[ExtendedSupportedTAIItem] = Field(default_factory=lambda: [ExtendedSupportedTAIItem()])
    """List of Tracking Area and S-NSSAI information."""

    amfInfoList: list[AMFInfoSet] = Field(default_factory=lambda: [AMFInfoSet()])
    """List of AMF Set information."""

    plmnInfoList: list[PLMNInfo] = Field(default_factory=lambda: [PLMNInfo()])
    """List of PLMN information."""


class CoreComponent(Component5G):
    """Base class for 5G core component."""

    category: Literal[Category5G.CORE] = Field(default=Category5G.CORE, frozen=True)

    type: CoreComponentType = Field()
    """Core component type."""

    config: CoreComponentConfig = Field(default_factory=CoreComponentConfig)
    """Core component configuration."""


class AMFComponent(CoreComponent):
    """AMF component."""

    type: Literal[CoreComponentType.AMF] = Field(frozen=True)
    config: AMFConfig = Field(default_factory=AMFConfig)


class AUSFComponent(CoreComponent):
    """AUSF component."""

    type: Literal[CoreComponentType.AUSF] = Field(frozen=True)
    config: AUSFConfig = Field(default_factory=AUSFConfig)


class SMFComponent(CoreComponent):
    """SMF component."""

    type: Literal[CoreComponentType.SMF] = Field(frozen=True)
    config: SMFConfig = Field(default_factory=SMFConfig)


class UPFComponent(CoreComponent):
    """UPF component."""

    type: Literal[CoreComponentType.UPF] = Field(frozen=True)
    config: UPFConfig = Field(default_factory=UPFConfig)


class NRFComponent(CoreComponent):
    """NRF component."""

    type: Literal[CoreComponentType.NRF] = Field(frozen=True)
    config: NRFConfig = Field(default_factory=NRFConfig)


class NSSFComponent(CoreComponent):
    """NSSF component."""

    type: Literal[CoreComponentType.NSSF] = Field(frozen=True)
    config: NSSFConfig = Field(default_factory=NSSFConfig)


# type used to tell pydantic which ran component to chose for validation based on the type
type ValidatedCoreComponent = Annotated[
    AMFComponent |
    AUSFComponent |
    SMFComponent |
    UPFComponent |
    NRFComponent |
    NSSFComponent,
    Field(discriminator="type")
]


class Core(Network5G):
    """5G core."""

    components: dict[str, ValidatedCoreComponent | CoreComponent] = Field(default_factory=lambda: {
        "amf": AMFComponent(type=CoreComponentType.AMF),
        "ausf": AUSFComponent(type=CoreComponentType.AUSF),
        "bsf": CoreComponent(type=CoreComponentType.BSF),
        "nssf": NSSFComponent(type=CoreComponentType.NSSF),
        "nrf": NRFComponent(type=CoreComponentType.NRF),
        "pcf": CoreComponent(type=CoreComponentType.PCF),
        "smf": SMFComponent(type=CoreComponentType.SMF),
        "upf": UPFComponent(type=CoreComponentType.UPF),
        "udm": CoreComponent(type=CoreComponentType.UDM),
        "udr": CoreComponent(type=CoreComponentType.UDR),
    })
    """Core components."""
