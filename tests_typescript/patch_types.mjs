// json-schema-to-typescript turns OtherChannel.type into plain `string`, so every broken core-type
// channel would type-check as an OtherChannel. Narrow it to an http(s) template literal, which is
// what the JSON Schema pattern "^https?://" says.
import { readFileSync, writeFileSync } from "node:fs";

const path = process.argv[2] ?? "implementations/ngff_axes.from_json_schema.ts";
const source = readFileSync(path, "utf8");
const start = source.indexOf("export interface OtherChannel {");
if (start < 0) throw new Error("OtherChannel interface not found");
const end = source.indexOf("\n}\n", start);
const block = source.slice(start, end);
const patched = block.replace(/\n  type: string;/, "\n  type: `http://${string}` | `https://${string}`;");
if (patched === block) throw new Error("OtherChannel.type not found or already patched");
writeFileSync(path, source.slice(0, start) + patched + source.slice(end));
console.log(`patched OtherChannel.type in ${path}`);
