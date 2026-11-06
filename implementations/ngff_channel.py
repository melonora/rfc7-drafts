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
     'created_on': '2026-11-04T00:00:00+00:00',
     'default_prefix': 'ngff',
     'default_range': 'string',
     'description': 'This schema defines the base channel of the draft OME-NGFF '
                    'channel metadata RFC. The `channels` list of a multiscale '
                    '(defined in the main OME-NGFF schema) holds one channel per '
                    'index of its channel axis. Every channel has an id, a name '
                    'and a type, and can state what its values measure, what it '
                    'reports on, where it came from and whether it is a plane of a '
                    'colour image. Typed channels are defined in the channel types '
                    'schema.',
     'id': 'https://w3id.org/ome/ngff/channel',
     'imports': ['linkml:types'],
     'name': 'OME_NGFF_Channel',
     'prefixes': {'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'ngff': {'prefix_prefix': 'ngff',
                           'prefix_reference': 'https://w3id.org/ome/ngff/'},
                  'ome': {'prefix_prefix': 'ome',
                          'prefix_reference': 'https://w3id.org/ome/'},
                  'orcid': {'prefix_prefix': 'orcid',
                            'prefix_reference': 'https://orcid.org/'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'source_file': 'schemas\\ngff_channel.yaml'} )

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
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'Quantity', 'Category', 'Entity', 'Component']} })
    type: str = Field(default=..., description="""The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), \"generic\", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the channel for humans and language models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    quantity: Optional[Quantity] = Field(default=None, description="""What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
    entities: Optional[list[Entity]] = Field(default=None, description="""What the channel reports on, each with its role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel']} })
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
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'Quantity', 'Category', 'Entity', 'Component']} })
    unit: Optional[str] = Field(default=None, description="""Unit of the physical value, spelled as for axes (e.g. nanometer, volt, degree, nanosecond). This attribute is OPTIONAL; if it is absent, the values are in arbitrary units.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity']} })
    value_scale: Optional[float] = Field(default=1.0, description="""Linear calibration, physical = stored * value_scale + value_offset. Defaults to 1.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity'], 'ifabsent': 'float(1.0)'} })
    value_offset: Optional[float] = Field(default=0.0, description="""Linear calibration, physical = stored * value_scale + value_offset. Defaults to 0.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity'], 'ifabsent': 'float(0.0)'} })
    categories: Optional[list[Category]] = Field(default=None, description="""For categorical channels such as EBSD phase maps or classifier outputs, a map from stored value to the category it stands for, serialized as { \"<stored value>\": { \"name\": ..., \"term\": ... } }.
""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity']} })


class Category(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/ome/ngff/channel'})

    value: int = Field(default=..., description="""The stored pixel value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Category']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'Quantity', 'Category', 'Entity', 'Component']} })
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

    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'Quantity', 'Category', 'Entity', 'Component']} })
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

    model: ColorModel = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Component']} })
    name: ColorComponent = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Channel', 'Quantity', 'Category', 'Entity', 'Component']} })
    group: str = Field(default=..., description="""Identifier shared by the channels of one colour image.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Component']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Channel.model_rebuild()
Quantity.model_rebuild()
Category.model_rebuild()
Entity.model_rebuild()
Provenance.model_rebuild()
Component.model_rebuild()
