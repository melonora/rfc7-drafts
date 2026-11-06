// Writes one TypeScript module per test document, typed with `satisfies` against the types
// generated from the JSON Schema. Valid documents must compile. Broken documents are marked
// with @ts-expect-error only when listed in STATICALLY_DETECTABLE: the others break rules
// (string patterns, value ranges, empty lists) that TypeScript types cannot express.
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");
const out = join(here, "generated");
rmSync(out, { recursive: true, force: true });
mkdirSync(out);

const STATICALLY_DETECTABLE = new Set(JSON.parse(readFileSync(join(here, "statically_detectable.json"), "utf8")));

for (const file of readdirSync(join(root, "test_data")).filter((f) => f.endsWith(".json")).sort()) {
  const name = file.replace(/\.json$/, "");
  const doc = JSON.stringify(JSON.parse(readFileSync(join(root, "test_data", file), "utf8")));
  const bad = name.startsWith("bad_");
  if (bad && !STATICALLY_DETECTABLE.has(name)) continue;
  const lines = [
    'import type { OME_NGFF_Axes } from "../../implementations/ngff_axes.from_json_schema";',
    bad ? "// @ts-expect-error broken on purpose" : "",
    `export const doc = ${doc} satisfies OME_NGFF_Axes;`,
  ];
  writeFileSync(join(out, `${name}.ts`), lines.join("\n") + "\n");
}
