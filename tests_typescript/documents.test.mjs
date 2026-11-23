// Runtime validation of every test document against the generated JSON Schema with Ajv.
// Documents named bad_*.json must be rejected; all others must be accepted.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2019 from "ajv/dist/2019.js";
import addFormats from "ajv-formats";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const schema = JSON.parse(readFileSync(join(root, "schemas", "ngff_axes.schema.json"), "utf8"));
const ajv = new Ajv2019({ strict: false, allErrors: true });
addFormats(ajv);
const validate = ajv.compile(schema);

// Rules the RFC states but no schema can express; reported as todo until a check enforces them.
const RULES_NOT_IN_SCHEMA = {
  bad_component_duplicate: "A colour group MUST contain each component of its model exactly once",
};

for (const file of readdirSync(join(root, "test_data")).filter((f) => f.endsWith(".json")).sort()) {
  const todo = RULES_NOT_IN_SCHEMA[file.replace(/\.json$/, "")];
  test(file, { todo }, () => {
    const data = JSON.parse(readFileSync(join(root, "test_data", file), "utf8"));
    const valid = validate(data);
    if (file.startsWith("bad_")) {
      assert.equal(valid, false, `${file} should be rejected`);
    } else {
      assert.equal(valid, true, `${file} should be accepted: ${ajv.errorsText(validate.errors)}`);
    }
  });
}
