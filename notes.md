# Notes: channel metadata schemas

Working notes on the LinkML schemas in `schemas/`, the decisions behind them, the limits of the generated code, and
questions that are still open. The RFC text itself is kept as a separate draft; this file is for whoever works on the
schemas and the tests.

## Layout

| File | Contents |
| --- | --- |
| `schemas/ngff_axes.yaml` | Entry point. Axes, with an optional `channels` list on the axis of type `channel`. Imports the channel types. |
| `schemas/ngff_channel_types.yaml` | The nine core channel types, the `OtherChannel` fallback, shared value classes (`Band`, `Value`, `Interval`) and their enums. Imports the base channel. |
| `schemas/ngff_channel.yaml` | The base `Channel` and its parts: `Quantity`, `Category`, `Entity`, `Provenance`, `Component`. |
| `templates/pydantic/` | Overrides of LinkML's gen-pydantic templates. |
| `test_data/` | 26 test documents: 7 `ex*` must validate, 19 `bad_*` must not. |
| `tests_python/`, `tests_typescript/` | Tests of the generated JSON Schema, Pydantic models and TypeScript types. |

Imported files must keep the `.yaml` extension: LinkML resolves `imports: [ngff_channel]` to `ngff_channel.yaml`.

## Design decisions

- **Channels live on the channel axis.** `{"name": "c", "type": "channel", "channels": [...]}`, following current
  OME-NGFF, where channels are an axis type. Consequences: an image without a channel axis cannot declare its channel,
  and the list is repeated wherever the axis is repeated (it MUST then be identical).
- **Axis and channel types are pinned with `equals_string`, not `designates_type`.** `designates_type` makes the
  serialized value the class name (`"SpaceAxis"`), which rejects real data such as `"type": "space"`, and cannot
  accept extension types given as URIs. The class `time` cannot be named after its value either: it clashes with
  LinkML's built-in `time` type. Will discuss with Damien.
- **Core types are closed, extension types are open.** A channel whose `type` is a core name must pass that type's
  class, which rejects unknown keys and so catches typos. A channel whose `type` is an http(s) URI validates as
  `OtherChannel`, which accepts extra keys. Any other `type` string is invalid, so a misspelled core type does not
  silently fall back. We could allow for extra slots to make core channels still freely extensible, but that would 
  also risk people just doing what they want
- **Writers strict, readers lenient.** The RFC says writers MUST NOT add undefined keys to core types, and readers
  MUST ignore keys they do not know. Validation follows the writer rule.
- **`generic` and `OtherChannel` are different.** `generic` is a core, closed type for a channel nothing fits;
  `OtherChannel` is for extension types with their own keys.
- **Enumerated keys accept a listed value or an http(s) URI.** Other strings are invalid. `scan_direction` keeps
  `trace`/`retrace`; software that says forward/backward maps to them.
- **Categories are a list,** `[{"value": 1, "name": "ferrite"}]`, not a dict keyed by value. `value` stays an integer
  that matches the pixel data, and gen-pydantic cannot read the dict form.
- **Patterns sit on slots, not on custom types.** gen-pydantic ignores patterns on types. The term pattern is
  therefore repeated on `terms` and both `term` slots.
- **Calibration is `value_scale` / `value_offset`.** It calibrates pixel values, not coordinates, and is named so it
  is not mistaken for an RFC-5 `scale` transformation.

## Tooling

| Output | How it is produced | Status |
| --- | --- | --- |
| JSON Schema | `gen-json-schema` | Reference. Gets all 26 test documents right, in Python (`jsonschema`) and JavaScript (Ajv). |
| Pydantic | `gen-pydantic --template-dir templates/pydantic` | Gets all 26 right with the template overrides. |
| TypeScript | `json-schema-to-typescript` on the JSON Schema, plus `tests_typescript/patch_types.mjs` | All 7 valid documents compile; 15 of 19 broken ones fail to compile, the other 4 need runtime checks. |
| TypeScript (LinkML) | `gen-typescript` | Not usable: `axes` and `channels` become `string[]`. Kept only for reference. |

The Pydantic template overrides add what gen-pydantic 1.12 drops:

- `extra_slots: {allowed: true}` becomes `extra="allow"` (`class.py.jinja`);
- a class-level `any_of` of `slot_conditions` becomes a model validator, e.g. the "center, or min and max" rule on
  `Band` (`class.py.jinja`);
- an enum-or-`ExtensionValue` slot gets a validator accepting a listed value or a URI (`attribute.py.jinja`);
- `module.py.jinja` adds the `model_validator` import.

The overrides are copies of LinkML 1.12's templates with additions. After a LinkML upgrade, diff them against the new
defaults.

Rules no generated validator checks yet, so readers or a custom check must:

- the number of channels equals the size of the channel axis;
- channel names are unique within the list (declared as a LinkML `unique_keys`, which `linkml-validate` ignores);
- axis names are unique;
- an RGB(A) `component` group contains each component exactly once.

`linkml-validate` also drops empty lists before validating, so it accepts `channels: []`; the JSON Schema rejects it.

## Considerations

- **Mass spectrometry.** MALDI, DESI, SIMS and LA-ICP-MS (imaging mass cytometry) fit `spectroscopic` with `band` in
  `m/z`. Polarity, adduct, ion source, analyzer and matrix have no channel keys; Thyra keeps them per dataset in its
  own LinkML schema (`msi_metadata.linkml.yaml`), which could become the acquisition extension. A separate
  `mass_spectrometry` type is only needed if polarity can differ between channels of one image.
- **Thyra output.** Its TIC image is one `spectroscopic` channel with the full m/z range and `origin: derived`; its
  optical image is three `optical` channels with `component` R, G, B. The spectra themselves are a table, not channels.
- **`AcquisitionMode` values** in `ngff_channel_types.yaml` follow the OME model's enumeration from memory; check them
  against the current OME XSD.
- **Zod.** ngff-zarr's TypeScript package and zod-ome-ngff validate with Zod. Converting the JSON Schema with
  `json-schema-to-zod` works (after inlining `$ref`s and removing an `enum` that duplicates a `const`) but produces one
  inlined expression with no named schemas. A LinkML-to-Zod generator would give named schemas and types per class;
  worth building once ngff-zarr or zod-ome-ngff would use it. Update: I will create a zod generator based on discussion
  with Matt.
- **Upstream LinkML issues worth filing:** gen-typescript's handling of `any_of`; gen-pydantic ignoring
  `extra_slots`, class-level `any_of`, type patterns and enum-or-pattern unions; `linkml-validate` ignoring
  `unique_keys` and cardinality in rules.

## Open questions

- **Implicit channel.** How does an image without a channel axis declare its channel: require a channel axis of size 1,
  or allow one channel elsewhere only in that case?
- **Several channel axes.** The axes schema fixes the channel axis name to `c`, so only one is possible. Revisit with
  RFC-3.
- **Same channel across arrays** (user stories 2 to 4): shared id across documents, or a `same_as` Reference?
- **Prototype alignment.** Agree with @lubianat on replacing the prototype's `coordinates` entries.
- **Core types.** Merge `xray` into `spectroscopic`/`optical`? Add `mass_spectrometry`, MRI, ultrasound, neutron?
- **Vocabularies.** Should `quantity.name` values be normative? How are units without a good UDUNITS-2 name spelled
  (m/z, Raman shift, arbitrary units)?
- **Required keys.** `signal` (electron, scanning probe, diffraction) and `technique` (spectroscopic) are required.
  Is that right for every converter, or should some become recommended?
- **Reviewers.** SPM, EM, EBSD and mass-spectrometry people (FAIRmat/NeXus, Thyra); Matt McCormick (ngff-zarr) and
  Trevor Manz (zod-ome-ngff) for the TypeScript side. Quarep limi.
- **RGB.** What about RGB, is it one channel or not. Think about pixel type.
Colour space of RGB channels. component.model: "RGB" says which planes form a colour image, but not their colour space. 
- Camera, slide-scanner and histology images are almost always sRGB (gamma-encoded), while some computed or scientific 
RGB data is linear. A viewer that assumes the wrong one shows colours too dark or washed out, and colour deconvolution 
or stain quantification gives wrong values. Should the RFC:

  - add an optional color_space to component (e.g. sRGB, linear_sRGB, or an ICC profile reference), defaulting to sRGB
  - define RGB as sRGB, with no field, and leave other colour spaces to an extension
  - Leave colour space to the rendering or acquisition layer?
- **MassSpec** Add specific channel axis with at least polarity.
- **Name** Should name be required or not? Most likely just do whatever rfc8 does.