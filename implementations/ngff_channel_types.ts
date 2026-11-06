export type ChannelId = string;
export type FluorescenceChannelId = string;
export type OpticalChannelId = string;
export type ElectronChannelId = string;
export type ScanningProbeChannelId = string;
export type SpectroscopicChannelId = string;
export type DiffractionChannelId = string;
export type XrayChannelId = string;
export type ComputedChannelId = string;
export type GenericChannelId = string;
export type OtherChannelId = string;

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

export enum FluorescenceMeasurement {
    
    /** Emission intensity. The default. */
    intensity = "intensity",
    /** Fluorescence lifetime, e.g. in nanoseconds. */
    lifetime = "lifetime",
    /** G coordinate of a FLIM phasor. */
    phasor_g = "phasor_g",
    /** S coordinate of a FLIM phasor. */
    phasor_s = "phasor_s",
    /** Fluorescence anisotropy. */
    anisotropy = "anisotropy",
};
/**
* Values of the OME model's AcquisitionMode enumeration, kept so OME-XML round-trips are lossless.
*/
export enum AcquisitionMode {
    
    WideField = "WideField",
    LaserScanningConfocalMicroscopy = "LaserScanningConfocalMicroscopy",
    SpinningDiskConfocal = "SpinningDiskConfocal",
    SlitScanConfocal = "SlitScanConfocal",
    SweptFieldConfocal = "SweptFieldConfocal",
    MultiPhotonMicroscopy = "MultiPhotonMicroscopy",
    StructuredIllumination = "StructuredIllumination",
    SingleMoleculeImaging = "SingleMoleculeImaging",
    TotalInternalReflection = "TotalInternalReflection",
    FluorescenceLifetime = "FluorescenceLifetime",
    SpectralImaging = "SpectralImaging",
    FluorescenceCorrelationSpectroscopy = "FluorescenceCorrelationSpectroscopy",
    NearFieldScanningOpticalMicroscopy = "NearFieldScanningOpticalMicroscopy",
    SecondHarmonicGenerationImaging = "SecondHarmonicGenerationImaging",
    PALM = "PALM",
    STORM = "STORM",
    STED = "STED",
    TIRF = "TIRF",
    FSM = "FSM",
    LCM = "LCM",
    SPIM = "SPIM",
    BrightField = "BrightField",
    Other = "Other",
};

export enum ContrastMethod {
    
    brightfield = "brightfield",
    darkfield = "darkfield",
    phase_contrast = "phase_contrast",
    /** Differential interference contrast. */
    DIC = "DIC",
    oblique = "oblique",
    /** Hoffman modulation contrast. */
    hoffman = "hoffman",
    polarized = "polarized",
    quantitative_phase = "quantitative_phase",
    interference = "interference",
    /** Second-harmonic generation. */
    SHG = "SHG",
    /** Third-harmonic generation. */
    THG = "THG",
};

export enum Illumination {
    
    transmitted = "transmitted",
    /** Reflected light, e.g. metallography or wafer inspection. */
    reflected = "reflected",
    oblique = "oblique",
};

export enum ElectronSignal {
    
    /** Secondary electrons. */
    SE = "SE",
    /** Backscattered electrons. */
    BSE = "BSE",
    TEM_BF = "TEM_BF",
    TEM_DF = "TEM_DF",
    STEM_BF = "STEM_BF",
    STEM_ABF = "STEM_ABF",
    STEM_ADF = "STEM_ADF",
    STEM_HAADF = "STEM_HAADF",
    /** Differential phase contrast. */
    DPC = "DPC",
    /** Integrated differential phase contrast. */
    iDPC = "iDPC",
    /** Electron-beam-induced current. */
    EBIC = "EBIC",
    absorbed_current = "absorbed_current",
};

export enum ScanningProbeTechnique {
    
    AFM = "AFM",
    STM = "STM",
    KPFM = "KPFM",
    MFM = "MFM",
    EFM = "EFM",
    c_AFM = "c-AFM",
    PFM = "PFM",
    s_SNOM = "s-SNOM",
    SThM = "SThM",
    SICM = "SICM",
};

export enum ScanningProbeMode {
    
    contact = "contact",
    tapping = "tapping",
    non_contact = "non_contact",
    peak_force = "peak_force",
    lift = "lift",
};

export enum ScanningProbeSignal {
    
    height = "height",
    deflection = "deflection",
    amplitude = "amplitude",
    phase = "phase",
    frequency_shift = "frequency_shift",
    lateral_force = "lateral_force",
    adhesion = "adhesion",
    modulus = "modulus",
    deformation = "deformation",
    dissipation = "dissipation",
    current = "current",
    surface_potential = "surface_potential",
    piezo_amplitude = "piezo_amplitude",
    piezo_phase = "piezo_phase",
    near_field_amplitude = "near_field_amplitude",
    near_field_phase = "near_field_phase",
};

export enum ScanDirection {
    
    /** Forward line of the fast scan axis. */
    trace = "trace",
    /** Backward line of the fast scan axis. */
    retrace = "retrace",
};

export enum ScanPass {
    
    main = "main",
    /** Interleaved second pass at a lift height, used in MFM and KPFM. */
    lift = "lift",
};

export enum SpectroscopicTechnique {
    
    EDS = "EDS",
    WDS = "WDS",
    EELS = "EELS",
    XRF = "XRF",
    XPS = "XPS",
    AES = "AES",
    /** Cathodoluminescence. */
    CL = "CL",
    Raman = "Raman",
    IR = "IR",
    CARS = "CARS",
    SRS = "SRS",
    MALDI = "MALDI",
    DESI = "DESI",
    /** Secondary-ion mass spectrometry, including MIBI. */
    SIMS = "SIMS",
    /** Laser-ablation ICP mass spectrometry, including imaging mass cytometry. */
    LA_ICP_MS = "LA-ICP-MS",
    LIBS = "LIBS",
};

export enum DiffractionTechnique {
    
    EBSD = "EBSD",
    TKD = "TKD",
    number_4D_STEM = "4D-STEM",
    XRD = "XRD",
    ED = "ED",
};

export enum DiffractionSignal {
    
    euler_phi1 = "euler_phi1",
    euler_Phi = "euler_Phi",
    euler_phi2 = "euler_phi2",
    quaternion_a = "quaternion_a",
    quaternion_b = "quaternion_b",
    quaternion_c = "quaternion_c",
    quaternion_d = "quaternion_d",
    /** Categorical phase map; use quantity.categories. */
    phase = "phase",
    band_contrast = "band_contrast",
    band_slope = "band_slope",
    confidence_index = "confidence_index",
    image_quality = "image_quality",
    /** Mean angular deviation. */
    MAD = "MAD",
    /** Kernel average misorientation. */
    KAM = "KAM",
    strain_xx = "strain_xx",
    strain_yy = "strain_yy",
    strain_zz = "strain_zz",
    strain_xy = "strain_xy",
    strain_xz = "strain_xz",
    strain_yz = "strain_yz",
    virtual_BF = "virtual_BF",
    virtual_ADF = "virtual_ADF",
};

export enum XrayContrast {
    
    absorption = "absorption",
    phase = "phase",
    darkfield = "darkfield",
};

export enum ComputedKind {
    
    probability = "probability",
    prediction = "prediction",
    classification = "classification",
    ratio = "ratio",
    difference = "difference",
    /** Normalized signal, e.g. delta F over F. */
    normalized = "normalized",
    feature = "feature",
    distance = "distance",
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


/**
 * A spectral position or window. Either `center` (with an optional full `width`) or both `min` and `max` MUST be given. The unit is nanometer, electronvolt, kiloelectronvolt, 1/centimeter for Raman shift and wavenumber, or the literal "m/z" for mass-to-charge.

 */
export interface Band {
    center?: number,
    /** Full width of the window around `center`. */
    width?: number,
    min?: number,
    max?: number,
    unit: string,
}


/**
 * A number with a unit.
 */
export interface Value {
    value: number,
    unit: string,
}


/**
 * A closed interval with a unit, e.g. a STEM detector collection angle.
 */
export interface Interval {
    min: number,
    max: number,
    unit: string,
}


/**
 * The model that produced a computed channel.
 */
export interface Model {
    name: string,
    version?: string,
    /** Link to the model, e.g. its page in a model zoo. */
    uri?: string,
}


/**
 * What a predicted channel stands in for, written like a channel without `id` and `name`, e.g. { "type": "fluorescence", "entities": [...] } for virtual staining. It MAY carry the attributes of that type.

 */
export interface EmulatedChannel {
    type: string,
    entities?: Entity[],
}


/**
 * Provenance of a channel that MUST be derived.
 */
export interface DerivedProvenance extends Provenance {
}


/**
 * Emission from a fluorophore, under any excitation scheme. The fluorophore itself is an `entities` entry with role signal.

 */
export interface FluorescenceChannel extends Channel {
    /** Excitation band; for multiphoton excitation, the laser wavelength. */
    excitation?: Band,
    /** Detection window. */
    emission?: Band,
    /** Photons absorbed per excitation event. Defaults to 1. */
    photons?: number,
    /** What is measured from the emission. Defaults to intensity. A lifetime channel pairs with a `quantity` of lifetime in nanoseconds.
 */
    measurement?: string,
    acquisition_mode?: string,
}


/**
 * Non-fluorescent light microscopy, transmitted or reflected, in biology and materials science.
 */
export interface OpticalChannel extends Channel {
    contrast_method?: string,
    illumination?: string,
    /** Illumination band. */
    wavelength?: Band,
    /** Polarization setting, e.g. "crossed" or "analyzer 45 degree". */
    polarization?: string,
    acquisition_mode?: string,
}


/**
 * A detector signal in SEM, TEM or STEM, including cryo-EM and FIB-SEM. Energy-resolved signals (EDS, EELS, cathodoluminescence) use SpectroscopicChannel.

 */
export interface ElectronChannel extends Channel {
    signal: string,
    /** Detector name, e.g. "Everhart-Thornley", "in-lens", "HAADF", "segment A". */
    detector?: string,
    beam_energy?: Value,
    /** Collection angle of a STEM detector, typically in milliradian. */
    collection_angle?: Interval,
}


/**
 * AFM and related probe techniques. Each recorded signal and scan direction is one channel; the physical unit goes in `quantity`. Force-volume and spectroscopy grids add a non-spatial axis, not channels.

 */
export interface ScanningProbeChannel extends Channel {
    technique?: string,
    mode?: string,
    signal: string,
    scan_direction?: string,
    /** Main pass, or the interleaved lift pass of MFM and KPFM. */
    pass?: string,
    /** Demodulation order, e.g. 2 or 3 in s-SNOM. */
    harmonic?: number,
}


/**
 * A map of one band, line or species from a spectral technique: X-ray, electron, vibrational, luminescence or mass spectrometry. The analyte is an `entities` entry (role signal for an isotope tag, target for an element or molecule). A continuous spectral dimension is better stored as an axis; one unbound spectroscopic channel then describes the image.

 */
export interface SpectroscopicChannel extends Channel {
    technique: string,
    /** Energy window, Raman shift, wavenumber or m/z window. */
    band?: Band,
    /** X-ray line or absorption edge, e.g. "Ka", "La", "L2,3". */
    line?: string,
    /** Laser wavelength for Raman, beam energy for EDS. */
    excitation?: string,
}


/**
 * Quantities derived from diffraction patterns, mostly in materials science. A phase map is categorical and uses `quantity.categories`; an inverse-pole-figure map is three channels with `component` R, G, B.

 */
export interface DiffractionChannel extends Channel {
    technique?: string,
    signal: string,
    /** Sample reference frame convention for orientations. */
    reference_frame?: string,
}


/**
 * X-ray imaging and tomography that is not resolved by energy; energy-resolved maps use SpectroscopicChannel.
 */
export interface XrayChannel extends Channel {
    contrast?: string,
    /** Monochromatic energy or spectrum window. */
    energy?: string,
}


/**
 * A channel with no physical modality of its own: model outputs, ratios, feature maps. A deconvolved or projected channel keeps its physical type and only sets `provenance.origin` to derived.

 */
export interface ComputedChannel extends Channel {
    kind?: string,
    /** The formula or method, as text or a URI. */
    operation?: string,
    model?: Model,
    /** What a prediction stands in for. */
    emulates?: EmulatedChannel,
}


/**
 * A channel no core type fits. It has only the base attributes.
 */
export interface GenericChannel extends Channel {
}


/**
 * Fallback for a channel with an extension type. Its type MUST be a namespaced http(s) URI, so a misspelled core type does not fall back. It MUST be valid as a base channel and MAY carry extension attributes. Core type names are not URIs, so a core-type channel never validates as OtherChannel and must pass its own class.

 */
export interface OtherChannel extends Channel {
}



