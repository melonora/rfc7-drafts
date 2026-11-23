import type { OME_NGFF_Axes } from "../../implementations/ngff_axes.from_json_schema";

export const doc = {"axes":[{"name":"c","type":"channel","channels":[{"id":"ch-gfp","name":"EGFP","type":"fluorescence","excitation":{"center":488,"unit":"nanometer"},"emission":{"min":500,"max":550,"unit":"nanometer"},"acquisition_mode":"WideField","entities":[{"name":"EGFP","role":"signal"}],"quantity":{"name":"photon_count","value_scale":0.575,"value_offset":-57.5}}]},{"name":"y","type":"space","unit":"micrometer"},{"name":"x","type":"space","unit":"micrometer"}]} satisfies OME_NGFF_Axes;
