export type ChannelId = string;

export enum EntityRole {
    
    /** What produces the measured signal, e.g. a fluorophore, a metal isotope tag or a stain. */
    signal = "signal",
    /** What the signal is bound to or reports on, e.g. a protein, DNA or an element. */
    target = "target",
    /** The structure or material seen, e.g. a nucleus, the nuclear lamina or ferrite grains. */
    observed_entity = "observed_entity",
};

export enum Origin {
    
    /** The channel was recorded by an instrument. This is the default. */
    acquired = "acquired",
    /** The channel was computed from other channels, e.g. a projection, a deconvolution or a model output. */
    derived = "derived",
    /** The channel was produced by a simulation. */
    simulated = "simulated",
};

export enum ColorModel {
    
    /** Red, green and blue planes. */
    RGB = "RGB",
    /** Red, green, blue and alpha planes. */
    RGBA = "RGBA",
};

export enum ColorComponent {
    
    /** Red plane. */
    R = "R",
    /** Green plane. */
    G = "G",
    /** Blue plane. */
    B = "B",
    /** Alpha plane. */
    A = "A",
};


/**
 * The base channel. Every channel, whatever its type, MUST be valid as a base channel. Readers that do not recognise `type` MUST treat the channel as a base channel and MUST ignore attributes they do not know. Writers MUST NOT put rendering attributes (colour, window, lookup table) on a channel.

 */
export interface Channel {
    /** Identifier of the channel, unique for the multiscale. Other metadata (rendering, biological annotation, statistics, transformations) references the channel by this id. Follows the RFC-8 id pattern; UUIDs are allowed but not required.
 */
    id: string,
    /** Human-readable name of the channel. It MUST be unique within the `channels` list, so that a channel can be looked up by name.
 */
    name: string,
    /** The channel type: one of the core types (fluorescence, optical, electron, scanning_probe, spectroscopic, diffraction, xray, computed), "generic", or an extension type given as a namespaced http(s) URI. Typed subclasses pin this value with equals_string; other values are invalid.
 */
    type: string,
    /** Free-text description of the channel for humans and language models. */
    description?: string,
    /** What the stored values measure. This attribute is OPTIONAL. When absent, values are intensities in arbitrary units.
 */
    quantity?: Quantity,
    /** What the channel reports on, each with its role. */
    entities?: Entity[],
    /** Whether the channel was acquired, derived or simulated, and from what. */
    provenance?: Provenance,
    /** Membership of a colour image stored as separate planes. */
    component?: Component,
    /** Ontology terms for the channel as a whole, e.g. an imaging-method term, as CURIEs. Prefixes SHOULD follow bioregistry.io.
 */
    terms?: string[],
}


/**
 * The physical quantity the stored values represent and how to calibrate them. The calibration applies to pixel values, not to coordinates, and is unrelated to RFC-5 scale transformations.

 */
export interface Quantity {
    /** The measured quantity, e.g. intensity, counts, height, phase, potential, force, modulus, lifetime, probability, angle, concentration. Values from the recommended vocabulary SHOULD be used; other values are allowed.
 */
    name: string,
    /** Unit of the physical value, spelled as for axes (e.g. nanometer, volt, degree, nanosecond). This attribute is OPTIONAL; if it is absent, the values are in arbitrary units.
 */
    unit?: string,
    /** Linear calibration, physical = stored * value_scale + value_offset. Defaults to 1. */
    value_scale?: number,
    /** Linear calibration, physical = stored * value_scale + value_offset. Defaults to 0. */
    value_offset?: number,
    /** For categorical channels such as EBSD phase maps or classifier outputs, a map from stored value to the category it stands for, serialized as { "<stored value>": { "name": ..., "term": ... } }.
 */
    categories?: Category[],
}



export interface Category {
    /** The stored pixel value. */
    value: number,
    name: string,
    /** Ontology term for the category as a CURIE. */
    term?: string,
}


/**
 * Something the channel reports on. The same roles apply across domains: a DAPI channel (DAPI, DNA, nucleus), an imaging mass cytometry channel (165Ho, CD3, T cell) and an EDS map (iron in a steel matrix).

 */
export interface Entity {
    name: string,
    /** Ontology or database term for the entity as a CURIE. Prefixes SHOULD follow bioregistry.io. */
    term?: string,
    role: string,
}



export interface Provenance {
    origin?: string,
    /** Ids of the channels this channel was derived from. Channels in other documents will be referenced with RFC-8 References once RFC-8 is settled.
 */
    sources?: string[],
    /** Short description of, or URI for, the method that produced the channel. */
    method?: string,
}


/**
 * Channels with the same `group` together form one colour image. A group MUST contain each component of its colour model exactly once.

 */
export interface Component {
    model: string,
    name: string,
    /** Identifier shared by the channels of one colour image. */
    group: string,
}



