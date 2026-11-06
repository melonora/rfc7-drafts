import type { OME_NGFF_Axes } from "../../implementations/ngff_axes.from_json_schema";
// @ts-expect-error broken on purpose
export const doc = {"axes":[{"name":"c","type":"channel","channels":[{"id":"a","name":"A","type":"scanning_probe","signal":"height","scan_direction":"forward"}]},{"name":"y","type":"space","unit":"micrometer"},{"name":"x","type":"space","unit":"micrometer"}]} satisfies OME_NGFF_Axes;
