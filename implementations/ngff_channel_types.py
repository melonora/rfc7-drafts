from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)

from pydantic import model_validator  # added by templates/pydantic (class-level any_of)

metamodel_version = "1.12.0"
version = "0.1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'created_by': 'orcid:0000-0003-1666-5421',
     'created_on': '2026-11-05T00:00:00+00:00',
     'default_prefix': 'ngff',
     'default_range': 'string',
     'description': 'This schema defines the core channel types of the draft '
                    'OME-NGFF channel metadata RFC7. Each type is a subclass of '
                    'the base Channel that pins `type` with equals_string and adds '
                    'only the attributes needed to interpret its values. '
                    'Enumerated attributes accept the listed core values or an '
                    'extension value given as an http(s) URI. A channel whose type '
                    'is not a core type validates as OtherChannel, which accepts '
                    'extension attributes.',
     'id': 'https://w3id.org/ome/ngff/channel_types',
     'imports': ['linkml:types', 'ngff_channel'],
     'name': 'OME_NGFF_Channel_Types',
     'prefixes': {'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'ngff': {'prefix_prefix': 'ngff',
                           'prefix_reference': 'https://w3id.org/ome/ngff/'},
                  'ome': {'prefix_prefix': 'ome',
                          'prefix_reference': 'https://w3id.org/ome/'},
                  'orcid': {'prefix_prefix': 'orcid',
                            'prefix_reference': 'https://orcid.org/'}},
     'source_file': 'schemas\\ngff_channel_types.yaml',
     'types': {'ExtensionValue': {'description': 'An extension value for an '
                                                 'enumerated attribute, given as '
                                                 'an http(s) URI.',
                                  'from_schema': 'https://w3id.org/ome/ngff/channel_types',
                                  'name': 'ExtensionValue',
                                  'pattern': '^https?://',
                                  'typeof': 'string'}}} )

class EntityRole(str, Enum):
    signal = "signal"
    """
    What produces the measured signal, e.g. a fluorophore, a metal isotope tag or a stain.
    """
    target = "target"
    """
    What the signal is bound to or reports on, e.g. a protein, DNA or an element.
    """
    observed_entity = "observed_entity"
    """
    The structure or material seen, e.g. a nucleus, the nuclear lamina or ferrite grains.
    """


class Origin(str, Enum):
    acquired = "acquired"
    """
    The channel was recorded by an instrument. This is the default.
    """
    derived = "derived"
    """
    The channel was computed from other channels, e.g. a projection, a deconvolution or a model output.
    """
    simulated = "simulated"
    """
    The channel was produced by a simulation.
    """


class ColorModel(str, Enum):
    RGB = "RGB"
    """
    Red, green and blue planes.
    """
    RGBA = "RGBA"
    """
    Red, green, blue and alpha planes.
    """


class ColorComponent(str, Enum):
    R = "R"
    """
    Red plane.
    """
    G = "G"
    """
    Green plane.
    """
    B = "B"
    """
    Blue plane.
    """
    A = "A"
    """
    Alpha plane.
    """


class FluorescenceMeasurement(str, Enum):
    intensity = "intensity"
    """
    Emission intensity. The default.
    """
    lifetime = "lifetime"
    """
    Fluorescence lifetime, e.g. in nanoseconds.
    """
    phasor_g = "phasor_g"
    """
    G coordinate of a FLIM phasor.
    """
    phasor_s = "phasor_s"
    """
    S coordinate of a FLIM phasor.
    """
    anisotropy = "anisotropy"
    """
    Fluorescence anisotropy.
    """


class AcquisitionMode(str, Enum):
    """
    Values of the OME model's AcquisitionMode enumeration, kept so OME-XML round-trips are lossless.
    """
    WideField = "WideField"
    LaserScanningConfocalMicroscopy = "LaserScanningConfocalMicroscopy"
    SpinningDiskConfocal = "SpinningDiskConfocal"
    SlitScanConfocal = "SlitScanConfocal"
    SweptFieldConfocal = "SweptFieldConfocal"
    MultiPhotonMicroscopy = "MultiPhotonMicroscopy"
    StructuredIllumination = "StructuredIllumination"
    SingleMoleculeImaging = "SingleMoleculeImaging"
    TotalInternalReflection = "TotalInternalReflection"
    FluorescenceLifetime = "FluorescenceLifetime"
    SpectralImaging = "SpectralImaging"
    FluorescenceCorrelationSpectroscopy = "FluorescenceCorrelationSpectroscopy"
    NearFieldScanningOpticalMicroscopy = "NearFieldScanningOpticalMicroscopy"
    SecondHarmonicGenerationImaging = "SecondHarmonicGenerationImaging"
    PALM = "PALM"
    STORM = "STORM"
    STED = "STED"
    TIRF = "TIRF"
    FSM = "FSM"
    LCM = "LCM"
    SPIM = "SPIM"
    BrightField = "BrightField"
    Other = "Other"


class ContrastMethod(str, Enum):
    brightfield = "brightfield"
    darkfield = "darkfield"
    phase_contrast = "phase_contrast"
    DIC = "DIC"
    """
    Differential interference contrast.
    """
    oblique = "oblique"
    hoffman = "hoffman"
    """
    Hoffman modulation contrast.
    """
    polarized = "polarized"
    quantitative_phase = "quantitative_phase"
    interference = "interference"
    SHG = "SHG"
    """
    Second-harmonic generation.
    """
    THG = "THG"
    """
    Third-harmonic generation.
    """


class Illumination(str, Enum):
    transmitted = "transmitted"
    reflected = "reflected"
    """
    Reflected light, e.g. metallography or wafer inspection.
    """
    oblique = "oblique"


class ElectronSignal(str, Enum):
    SE = "SE"
    """
    Secondary electrons.
    """
    BSE = "BSE"
    """
    Backscattered electrons.
    """
    TEM_BF = "TEM_BF"
    TEM_DF = "TEM_DF"
    STEM_BF = "STEM_BF"
    STEM_ABF = "STEM_ABF"
    STEM_ADF = "STEM_ADF"
    STEM_HAADF = "STEM_HAADF"
    DPC = "DPC"
    """
    Differential phase contrast.
    """
    iDPC = "iDPC"
    """
    Integrated differential phase contrast.
    """
    EBIC = "EBIC"
    """
    Electron-beam-induced current.
    """
    absorbed_current = "absorbed_current"


class ScanningProbeTechnique(str, Enum):
    AFM = "AFM"
    STM = "STM"
    KPFM = "KPFM"
    MFM = "MFM"
    EFM = "EFM"
    c_AFM = "c-AFM"
    PFM = "PFM"
    s_SNOM = "s-SNOM"
    SThM = "SThM"
    SICM = "SICM"


class ScanningProbeMode(str, Enum):
    contact = "contact"
    tapping = "tapping"
    non_contact = "non_contact"
    peak_force = "peak_force"
    lift = "lift"


class ScanningProbeSignal(str, Enum):
    height = "height"
    deflection = "deflection"
    amplitude = "amplitude"
    phase = "phase"
    frequency_shift = "frequency_shift"
    lateral_force = "lateral_force"
    adhesion = "adhesion"
    modulus = "modulus"
    deformation = "deformation"
    dissipation = "dissipation"
    current = "current"
    surface_potential = "surface_potential"
    piezo_amplitude = "piezo_amplitude"
    piezo_phase = "piezo_phase"
    near_field_amplitude = "near_field_amplitude"
    near_field_phase = "near_field_phase"


class ScanDirection(str, Enum):
    trace = "trace"
    """
    Forward line of the fast scan axis.
    """
    retrace = "retrace"
    """
    Backward line of the fast scan axis.
    """


class ScanPass(str, Enum):
    main = "main"
    lift = "lift"
    """
    Interleaved second pass at a lift height, used in MFM and KPFM.
    """


class SpectroscopicTechnique(str, Enum):
    EDS = "EDS"
    WDS = "WDS"
    EELS = "EELS"
    XRF = "XRF"
    XPS = "XPS"
    AES = "AES"
    CL = "CL"
    """
    Cathodoluminescence.
    """
    Raman = "Raman"
    IR = "IR"
    CARS = "CARS"
    SRS = "SRS"
    MALDI = "MALDI"
    DESI = "DESI"
    SIMS = "SIMS"
    """
    Secondary-ion mass spectrometry, including MIBI.
    """
    LA_ICP_MS = "LA-ICP-MS"
    """
    Laser-ablation ICP mass spectrometry, including imaging mass cytometry.
    """
    LIBS = "LIBS"


class DiffractionTechnique(str, Enum):
    EBSD = "EBSD"
    TKD = "TKD"
    number_4D_STEM = "4D-STEM"
    XRD = "XRD"
    ED = "ED"


class DiffractionSignal(str, Enum):
    euler_phi1 = "euler_phi1"
    euler_Phi = "euler_Phi"
    euler_phi2 = "euler_phi2"
    quaternion_a = "quaternion_a"
    quaternion_b = "quaternion_b"
    quaternion_c = "quaternion_c"
    quaternion_d = "quaternion_d"
    phase = "phase"
    """
    Categorical phase map; use quantity.categories.
    """
    band_contrast = "band_contrast"
    band_slope = "band_slope"
    confidence_index = "confidence_index"
    image_quality = "image_quality"
    MAD = "MAD"
    """
    Mean angular deviation.
    """
    KAM = "KAM"
    """
    Kernel average misorientation.
    """
    strain_xx = "strain_xx"
    strain_yy = "strain_yy"
    strain_zz = "strain_zz"
    strain_xy = "strain_xy"
    strain_xz = "strain_xz"
    strain_yz = "strain_yz"
    virtual_BF = "virtual_BF"
    virtual_ADF = "virtual_ADF"


class XrayContrast(str, Enum):
    absorption = "absorption"
    phase = "phase"
    darkfield = "darkfield"


class ComputedKind(str, Enum):
    probability = "probability"
    prediction = "prediction"
    classification = "classification"
    ratio = "ratio"
    difference = "difference"
    normalized = "normalized"
    """
    Normalized signal, e.g. delta F over F.
    """
    feature = "feature"
    distance = "distance"



class Channel(ConfiguredBaseModel):
    """
    The base channel. Every channel, whatever its type, MUST be valid as a base channel. Readers that do not recognise `type` MUST treat the channel as a base channel and MUST ignore attributes they do not know. Writers MUST NOT put rendering attributes (colour, window, lookup table) on a channel.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel',
         'unique_keys': {'name_key': {'description': 'Channel names are unique within '
                                                     'the channels list.',
                                      'unique_key_name': 'name_key',
                                      'unique_key_slots': ['name']}}})

    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: str = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class Quantity(ConfiguredBaseModel):
    """
    The physical quantity the stored values represent and how to calibrate them. The calibration applies to pixel values, not to coordinates, and is unrelated to RFC-5 scale transformations.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel'})

    name: str = Field(default=..., description="""The measured quantity, e.g. intensity, counts, height, phase, potential, force, modulus, lifetime, probability, angle, concentration. Values from the recommended vocabulary SHOULD be used; other values are allowed.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    unit: Optional[str] = Field(default=None, description="""Unit of the physical value, spelled as for axes (e.g. nanometer, volt, degree, nanosecond). This attribute is OPTIONAL; if it is absent, the values are in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity', 'Band', 'Value', 'Interval']} })
    value_scale: Optional[float] = Field(default=1.0, description="""Linear calibration, physical = stored * value_scale + value_offset. Defaults to 1.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity'], 'ifabsent': 'float(1.0)'} })
    value_offset: Optional[float] = Field(default=0.0, description="""Linear calibration, physical = stored * value_scale + value_offset. Defaults to 0.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity'], 'ifabsent': 'float(0.0)'} })
    categories: Optional[list[Category]] = Field(default=None, description="""For categorical channels such as EBSD phase maps or classifier outputs, a map from stored value to the category it stands for, serialized as { \"<stored value>\": { \"name\": ..., \"term\": ... } }.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity']} })


class Category(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel'})

    value: int = Field(default=..., description="""The stored pixel value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Category', 'Value']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    term: Optional[str] = Field(default=None, description="""Ontology term for the category as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Category', 'Entity']} })

    @field_validator('term')
    def pattern_term(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid term format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid term format: {v}"
            raise ValueError(err_msg)
        return v


class Entity(ConfiguredBaseModel):
    """
    Something the channel reports on. The same roles apply across domains: a DAPI channel (DAPI, DNA, nucleus), an imaging mass cytometry channel (165Ho, CD3, T cell) and an EDS map (iron in a steel matrix).

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel'})

    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    term: Optional[str] = Field(default=None, description="""Ontology or database term for the entity as a CURIE. Prefixes SHOULD follow bioregistry.io.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Category', 'Entity']} })
    role: EntityRole = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Entity']} })

    @field_validator('term')
    def pattern_term(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid term format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid term format: {v}"
            raise ValueError(err_msg)
        return v


class Provenance(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel'})

    origin: Optional[Origin] = Field(default=Origin("acquired"), json_schema_extra = { "linkml_meta": {'domain_of': ['Provenance'], 'ifabsent': 'string(acquired)'} })
    sources: Optional[list[str]] = Field(default=None, description="""Ids of the channels this channel was derived from. Channels in other documents will be referenced with RFC-8 References once RFC-8 is settled.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Provenance']} })
    method: Optional[str] = Field(default=None, description="""Short description of, or URI for, the method that produced the channel.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Provenance']} })


class Component(ConfiguredBaseModel):
    """
    Channels with the same `group` together form one colour image. A group MUST contain each component of its colour model exactly once.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel'})

    model: ColorModel = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Component', 'ComputedChannel']} })
    name: ColorComponent = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    group: str = Field(default=..., description="""Identifier shared by the channels of one colour image.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component']} })


class Band(ConfiguredBaseModel):
    """
    A spectral position or window. Either `center` (with an optional full `width`) or both `min` and `max` MUST be given. The unit is nanometer, electronvolt, kiloelectronvolt, 1/centimeter for Raman shift and wavenumber, or the literal \"m/z\" for mass-to-charge.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'center': {'name': 'center',
                                                    'required': True}}},
                    {'slot_conditions': {'max': {'name': 'max', 'required': True},
                                         'min': {'name': 'min', 'required': True}}}],
         'from_schema': 'https://w3id.org/ome/ngff/channel_types'})

    center: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Band']} })
    width: Optional[float] = Field(default=None, description="""Full width of the window around `center`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Band']} })
    min: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Band', 'Interval']} })
    max: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Band', 'Interval']} })
    unit: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity', 'Band', 'Value', 'Interval']} })

    @model_validator(mode="after")
    def check_any_of(self):
        groups = [["center", ], ["min", "max", ], ]
        if not any(all(getattr(self, s, None) is not None for s in group) for group in groups):
            raise ValueError(f"Band needs one of these sets of attributes: {groups}")
        return self


class Value(ConfiguredBaseModel):
    """
    A number with a unit.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types'})

    value: float = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Category', 'Value']} })
    unit: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity', 'Band', 'Value', 'Interval']} })


class Interval(ConfiguredBaseModel):
    """
    A closed interval with a unit, e.g. a STEM detector collection angle.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types'})

    min: float = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Band', 'Interval']} })
    max: float = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Band', 'Interval']} })
    unit: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity', 'Band', 'Value', 'Interval']} })


class Model(ConfiguredBaseModel):
    """
    The model that produced a computed channel.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types'})

    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    version: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Model']} })
    uri: Optional[str] = Field(default=None, description="""Link to the model, e.g. its page in a model zoo.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Model']} })

    @field_validator('uri')
    def pattern_uri(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid uri format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid uri format: {v}"
            raise ValueError(err_msg)
        return v


class EmulatedChannel(ConfiguredBaseModel):
    """
    What a predicted channel stands in for, written like a channel without `id` and `name`, e.g. { \"type\": \"fluorescence\", \"entities\": [...] } for virtual staining. It MAY carry the attributes of that type.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'extra_slots': {'allowed': True},
         'from_schema': 'https://w3id.org/ome/ngff/channel_types'})

    model_config = ConfigDict(extra="allow")

    type: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    entities: Optional[list[Entity]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })


class DerivedProvenance(Provenance):
    """
    Provenance of a channel that MUST be derived.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'origin': {'equals_string': 'derived',
                                   'name': 'origin',
                                   'required': True}}})

    origin: Literal["derived"] = Field(default=Origin("acquired"), json_schema_extra = { "linkml_meta": {'domain_of': ['Provenance'],
         'equals_string': 'derived',
         'ifabsent': 'string(acquired)'} })
    sources: Optional[list[str]] = Field(default=None, description="""Ids of the channels this channel was derived from. Channels in other documents will be referenced with RFC-8 References once RFC-8 is settled.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Provenance']} })
    method: Optional[str] = Field(default=None, description="""Short description of, or URI for, the method that produced the channel.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Provenance']} })


class FluorescenceChannel(Channel):
    """
    Emission from a fluorophore, under any excitation scheme. The fluorophore itself is an `entities` entry with role signal.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'fluorescence', 'name': 'type'}}})

    excitation: Optional[Band] = Field(default=None, description="""Excitation band; for multiphoton excitation, the laser wavelength.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FluorescenceChannel', 'SpectroscopicChannel']} })
    emission: Optional[Band] = Field(default=None, description="""Detection window.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FluorescenceChannel']} })
    photons: Optional[int] = Field(default=1, description="""Photons absorbed per excitation event. Defaults to 1.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['FluorescenceChannel'], 'ifabsent': 'int(1)'} })
    measurement: Optional[Union[FluorescenceMeasurement, str]] = Field(default="intensity", description="""What is measured from the emission. Defaults to intensity. A lifetime channel pairs with a `quantity` of lifetime in nanoseconds.
""", json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'FluorescenceMeasurement'}, {'range': 'ExtensionValue'}],
         'domain_of': ['FluorescenceChannel'],
         'ifabsent': 'string(intensity)'} })
    @field_validator("measurement")
    def check_measurement_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in FluorescenceMeasurement} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"measurement must be a value of FluorescenceMeasurement or an http(s) URI, got {value!r}")
        return v
    acquisition_mode: Optional[Union[AcquisitionMode, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'AcquisitionMode'}, {'range': 'ExtensionValue'}],
         'domain_of': ['FluorescenceChannel', 'OpticalChannel']} })
    @field_validator("acquisition_mode")
    def check_acquisition_mode_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in AcquisitionMode} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"acquisition_mode must be a value of AcquisitionMode or an http(s) URI, got {value!r}")
        return v
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["fluorescence"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'fluorescence'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class OpticalChannel(Channel):
    """
    Non-fluorescent light microscopy, transmitted or reflected, in biology and materials science.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'optical', 'name': 'type'}}})

    contrast_method: Optional[Union[ContrastMethod, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'ContrastMethod'}, {'range': 'ExtensionValue'}],
         'domain_of': ['OpticalChannel']} })
    @field_validator("contrast_method")
    def check_contrast_method_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in ContrastMethod} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"contrast_method must be a value of ContrastMethod or an http(s) URI, got {value!r}")
        return v
    illumination: Optional[Union[Illumination, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'Illumination'}, {'range': 'ExtensionValue'}],
         'domain_of': ['OpticalChannel']} })
    @field_validator("illumination")
    def check_illumination_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in Illumination} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"illumination must be a value of Illumination or an http(s) URI, got {value!r}")
        return v
    wavelength: Optional[Band] = Field(default=None, description="""Illumination band.""", json_schema_extra = { "linkml_meta": {'domain_of': ['OpticalChannel']} })
    polarization: Optional[str] = Field(default=None, description="""Polarization setting, e.g. \"crossed\" or \"analyzer 45 degree\".""", json_schema_extra = { "linkml_meta": {'domain_of': ['OpticalChannel']} })
    acquisition_mode: Optional[Union[AcquisitionMode, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'AcquisitionMode'}, {'range': 'ExtensionValue'}],
         'domain_of': ['FluorescenceChannel', 'OpticalChannel']} })
    @field_validator("acquisition_mode")
    def check_acquisition_mode_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in AcquisitionMode} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"acquisition_mode must be a value of AcquisitionMode or an http(s) URI, got {value!r}")
        return v
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["optical"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'optical'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class ElectronChannel(Channel):
    """
    A detector signal in SEM, TEM or STEM, including cryo-EM and FIB-SEM. Energy-resolved signals (EDS, EELS, cathodoluminescence) use SpectroscopicChannel.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'electron', 'name': 'type'}}})

    signal: Union[ElectronSignal, str] = Field(default=..., json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'ElectronSignal'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ElectronChannel', 'ScanningProbeChannel', 'DiffractionChannel']} })
    @field_validator("signal")
    def check_signal_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in ElectronSignal} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"signal must be a value of ElectronSignal or an http(s) URI, got {value!r}")
        return v
    detector: Optional[str] = Field(default=None, description="""Detector name, e.g. \"Everhart-Thornley\", \"in-lens\", \"HAADF\", \"segment A\".""", json_schema_extra = { "linkml_meta": {'domain_of': ['ElectronChannel']} })
    beam_energy: Optional[Value] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ElectronChannel']} })
    collection_angle: Optional[Interval] = Field(default=None, description="""Collection angle of a STEM detector, typically in milliradian.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ElectronChannel']} })
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["electron"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'electron'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class ScanningProbeChannel(Channel):
    """
    AFM and related probe techniques. Each recorded signal and scan direction is one channel; the physical unit goes in `quantity`. Force-volume and spectroscopy grids add a non-spatial axis, not channels.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'scanning_probe', 'name': 'type'}}})

    technique: Optional[Union[ScanningProbeTechnique, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'ScanningProbeTechnique'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ScanningProbeChannel',
                       'SpectroscopicChannel',
                       'DiffractionChannel']} })
    @field_validator("technique")
    def check_technique_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in ScanningProbeTechnique} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"technique must be a value of ScanningProbeTechnique or an http(s) URI, got {value!r}")
        return v
    mode: Optional[Union[ScanningProbeMode, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'ScanningProbeMode'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ScanningProbeChannel']} })
    @field_validator("mode")
    def check_mode_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in ScanningProbeMode} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"mode must be a value of ScanningProbeMode or an http(s) URI, got {value!r}")
        return v
    signal: Union[ScanningProbeSignal, str] = Field(default=..., json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'ScanningProbeSignal'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ElectronChannel', 'ScanningProbeChannel', 'DiffractionChannel']} })
    @field_validator("signal")
    def check_signal_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in ScanningProbeSignal} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"signal must be a value of ScanningProbeSignal or an http(s) URI, got {value!r}")
        return v
    scan_direction: Optional[ScanDirection] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ScanningProbeChannel']} })
    pass_: Optional[ScanPass] = Field(default=None, alias="pass", description="""Main pass, or the interleaved lift pass of MFM and KPFM.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ScanningProbeChannel']} })
    harmonic: Optional[int] = Field(default=None, description="""Demodulation order, e.g. 2 or 3 in s-SNOM.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['ScanningProbeChannel']} })
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["scanning_probe"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'scanning_probe'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class SpectroscopicChannel(Channel):
    """
    A map of one band, line or species from a spectral technique: X-ray, electron, vibrational, luminescence or mass spectrometry. The analyte is an `entities` entry (role signal for an isotope tag, target for an element or molecule). A continuous spectral dimension is better stored as an axis; one unbound spectroscopic channel then describes the image.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'spectroscopic', 'name': 'type'}}})

    technique: Union[SpectroscopicTechnique, str] = Field(default=..., json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'SpectroscopicTechnique'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ScanningProbeChannel',
                       'SpectroscopicChannel',
                       'DiffractionChannel']} })
    @field_validator("technique")
    def check_technique_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in SpectroscopicTechnique} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"technique must be a value of SpectroscopicTechnique or an http(s) URI, got {value!r}")
        return v
    band: Optional[Band] = Field(default=None, description="""Energy window, Raman shift, wavenumber or m/z window.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpectroscopicChannel']} })
    line: Optional[str] = Field(default=None, description="""X-ray line or absorption edge, e.g. \"Ka\", \"La\", \"L2,3\".""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpectroscopicChannel']} })
    excitation: Optional[Union[Band, Value]] = Field(default=None, description="""Laser wavelength for Raman, beam energy for EDS.""", json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'Band'}, {'range': 'Value'}],
         'domain_of': ['FluorescenceChannel', 'SpectroscopicChannel']} })
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["spectroscopic"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'spectroscopic'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class DiffractionChannel(Channel):
    """
    Quantities derived from diffraction patterns, mostly in materials science. A phase map is categorical and uses `quantity.categories`; an inverse-pole-figure map is three channels with `component` R, G, B.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'diffraction', 'name': 'type'}}})

    technique: Optional[Union[DiffractionTechnique, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'DiffractionTechnique'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ScanningProbeChannel',
                       'SpectroscopicChannel',
                       'DiffractionChannel']} })
    @field_validator("technique")
    def check_technique_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in DiffractionTechnique} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"technique must be a value of DiffractionTechnique or an http(s) URI, got {value!r}")
        return v
    signal: Union[DiffractionSignal, str] = Field(default=..., json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'DiffractionSignal'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ElectronChannel', 'ScanningProbeChannel', 'DiffractionChannel']} })
    @field_validator("signal")
    def check_signal_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in DiffractionSignal} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"signal must be a value of DiffractionSignal or an http(s) URI, got {value!r}")
        return v
    reference_frame: Optional[str] = Field(default=None, description="""Sample reference frame convention for orientations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiffractionChannel']} })
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["diffraction"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'diffraction'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class XrayChannel(Channel):
    """
    X-ray imaging and tomography that is not resolved by energy; energy-resolved maps use SpectroscopicChannel.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'xray', 'name': 'type'}}})

    contrast: Optional[Union[XrayContrast, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'XrayContrast'}, {'range': 'ExtensionValue'}],
         'domain_of': ['XrayChannel']} })
    @field_validator("contrast")
    def check_contrast_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in XrayContrast} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"contrast must be a value of XrayContrast or an http(s) URI, got {value!r}")
        return v
    energy: Optional[Union[Band, Value]] = Field(default=None, description="""Monochromatic energy or spectrum window.""", json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'Band'}, {'range': 'Value'}],
         'domain_of': ['XrayChannel']} })
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["xray"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'xray'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class ComputedChannel(Channel):
    """
    A channel with no physical modality of its own: model outputs, ratios, feature maps. A deconvolved or projected channel keeps its physical type and only sets `provenance.origin` to derived.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'provenance': {'description': 'Inputs and method. Computed '
                                                      'channels MUST have origin '
                                                      'derived.',
                                       'name': 'provenance',
                                       'range': 'DerivedProvenance',
                                       'required': True},
                        'type': {'equals_string': 'computed', 'name': 'type'}}})

    kind: Optional[Union[ComputedKind, str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'ComputedKind'}, {'range': 'ExtensionValue'}],
         'domain_of': ['ComputedChannel']} })
    @field_validator("kind")
    def check_kind_enum_or_uri(cls, v):
        for item in (v if isinstance(v, list) else [v]):
            if item is None:
                continue
            value = item.value if isinstance(item, Enum) else item
            if value not in {e.value for e in ComputedKind} and not re.match(r"^https?://", str(value)):
                raise ValueError(f"kind must be a value of ComputedKind or an http(s) URI, got {value!r}")
        return v
    operation: Optional[str] = Field(default=None, description="""The formula or method, as text or a URI.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputedChannel']} })
    model: Optional[Model] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Component', 'ComputedChannel']} })
    emulates: Optional[EmulatedChannel] = Field(default=None, description="""What a prediction stands in for.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputedChannel']} })
    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["computed"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'computed'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: DerivedProvenance = Field(default=..., description="""Inputs and method. Computed channels MUST have origin derived.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class GenericChannel(Channel):
    """
    A channel no core type fits. It has only the base attributes.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'equals_string': 'generic', 'name': 'type'}}})

    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: Literal["generic"] = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel'], 'equals_string': 'generic'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


class OtherChannel(Channel):
    """
    Fallback for a channel with an extension type. Its type MUST be a namespaced http(s) URI, so a misspelled core type does not fall back. It MUST be valid as a base channel and MAY carry extension attributes. Core type names are not URIs, so a core-type channel never validates as OtherChannel and must pass its own class.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'extra_slots': {'allowed': True},
         'from_schema': 'https://w3id.org/ome/ngff/channel_types',
         'slot_usage': {'type': {'name': 'type', 'pattern': '^https?://'}}})

    model_config = ConfigDict(extra="allow")

    id: str = Field(default=..., description="""Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    name: str = Field(default=..., description="""Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel',
                       'Quantity',
                       'Category',
                       'Entity',
                       'Component',
                       'Model']} })
    type: str = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'EmulatedChannel']} })
    provenance: Optional[Provenance] = Field(default=None, description="""Whether the channel was acquired, derived or simulated, and from what.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    component: Optional[Component] = Field(default=None, description="""Membership of a colour image stored as separate planes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    terms: Optional[list[str]] = Field(default=None, description="""Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9\-_.]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('type')
    def pattern_type(cls, v):
        pattern=re.compile(r"^https?://")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('terms')
    def pattern_terms(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9._+-]*:\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid terms format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid terms format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Channel.model_rebuild()
Quantity.model_rebuild()
Category.model_rebuild()
Entity.model_rebuild()
Provenance.model_rebuild()
Component.model_rebuild()
Band.model_rebuild()
Value.model_rebuild()
Interval.model_rebuild()
Model.model_rebuild()
EmulatedChannel.model_rebuild()
DerivedProvenance.model_rebuild()
FluorescenceChannel.model_rebuild()
OpticalChannel.model_rebuild()
ElectronChannel.model_rebuild()
ScanningProbeChannel.model_rebuild()
SpectroscopicChannel.model_rebuild()
DiffractionChannel.model_rebuild()
XrayChannel.model_rebuild()
ComputedChannel.model_rebuild()
GenericChannel.model_rebuild()
OtherChannel.model_rebuild()
