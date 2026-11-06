"""Run every test document through the generated JSON Schema and the generated Pydantic models.

Documents named bad_*.json must be rejected; all others must be accepted.

The JSON Schema is the reference and must get every document right. The Pydantic models are generated with
the template overrides in templates/pydantic, which add the constraints LinkML 1.12 drops. Any remaining known
gap goes into PYDANTIC_GAPS as an expected failure (strict, so the test reports it once the gap is closed).
"""
import json
import sys
from pathlib import Path

import jsonschema
import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "implementations"))
from ngff_axes import Axes  # noqa: E402

DOCUMENTS = sorted((ROOT / "test_data").glob("*.json"))
SCHEMA = json.loads((ROOT / "schemas" / "ngff_axes.schema.json").read_text())

PYDANTIC_GAPS: dict[str, str] = {}


def expected_valid(path: Path) -> bool:
    return not path.name.startswith("bad_")


def pydantic_param(path: Path):
    marks = []
    if path.stem in PYDANTIC_GAPS:
        marks.append(pytest.mark.xfail(reason=PYDANTIC_GAPS[path.stem], strict=True))
    return pytest.param(path, id=path.stem, marks=marks)


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda p: p.stem)
def test_json_schema(path: Path) -> None:
    data = json.loads(path.read_text())
    if expected_valid(path):
        jsonschema.validate(data, SCHEMA)
    else:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, SCHEMA)


@pytest.mark.parametrize("path", [pydantic_param(p) for p in DOCUMENTS])
def test_pydantic(path: Path) -> None:
    data = json.loads(path.read_text())
    if expected_valid(path):
        Axes.model_validate(data)
    else:
        with pytest.raises(ValidationError):
            Axes.model_validate(data)
