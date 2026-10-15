"""Load, validate, and search the master JSON catalog."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

SCHEMA_PATH = Path(__file__).with_name("schema.json")
CATALOG_PATH = Path(__file__).with_name("catalog.json")


class CatalogError(ValueError):
    """Raised when the catalog or a query is invalid."""


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise CatalogError(f"Missing JSON file: {path}")
    with path.open(encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError as exc:
            raise CatalogError(f"Invalid JSON in {path}: {exc}") from exc


def load_schema(path: Path = SCHEMA_PATH) -> Dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, dict):
        raise CatalogError("Schema root must be an object")
    return data


def load_catalog(path: Path = CATALOG_PATH) -> Dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, dict):
        raise CatalogError("Catalog root must be an object")
    return data


def _require_jsonschema():
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover
        raise CatalogError(
            "The jsonschema package is required to validate the catalog. "
            "Install with: pip install jsonschema"
        ) from exc
    return jsonschema


def validate_catalog(
    catalog: Optional[Dict[str, Any]] = None,
    schema: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Validate catalog JSON against the schema and internal consistency rules."""
    catalog = catalog if catalog is not None else load_catalog()
    schema = schema if schema is not None else load_schema()
    jsonschema = _require_jsonschema()
    try:
        jsonschema.validate(instance=catalog, schema=schema)
    except jsonschema.ValidationError as exc:
        raise CatalogError(f"Catalog schema validation failed: {exc.message}") from exc

    components = catalog.get("components", [])
    seen: Dict[str, int] = {}
    for index, item in enumerate(components):
        cid = item["id"]
        if cid in seen:
            raise CatalogError(
                f"Duplicate component id {cid!r} at index {index} "
                f"(first seen at {seen[cid]})"
            )
        seen[cid] = index
        status = item.get("test_status", "untested")
        if status == "tested" and not item.get("module"):
            raise CatalogError(
                f"{cid}: entries marked tested must declare a module path"
            )

    catalog_prefixes = {
        "design",
        "motion",
        "transition",
        "text",
        "shape",
        "chart",
        "math",
        "physics",
        "code",
        "data_structure",
        "ml",
        "diagram",
        "camera",
        "effect",
        "spatial",
        "timing",
        "template",
        "utility",
        "base",
    }
    for item in components:
        for related in item.get("related_ids", []):
            if related not in seen:
                raise CatalogError(
                    f"{item['id']}: related_ids references unknown id {related!r}"
                )
        for dep in item.get("dependencies", []):
            prefix = dep.split(".", 1)[0]
            if prefix in catalog_prefixes and dep not in seen:
                raise CatalogError(
                    f"{item['id']}: dependencies references unknown catalog id {dep!r}"
                )
    return catalog


def check_python_references(catalog: Optional[Dict[str, Any]] = None) -> List[str]:
    """Import declared modules and confirm class names exist.

    Returns a list of error strings. Empty means all references resolved.
    """
    import importlib

    catalog = catalog if catalog is not None else load_catalog()
    errors: List[str] = []
    for item in catalog.get("components", []):
        module_name = item.get("module") or ""
        class_name = item.get("class_name") or ""
        if not module_name:
            continue
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{item['id']}: cannot import {module_name}: {exc}")
            continue
        if class_name and not hasattr(module, class_name):
            errors.append(
                f"{item['id']}: {module_name} has no attribute {class_name}"
            )
    return errors


def _blob(item: Dict[str, Any]) -> str:
    fields: List[str] = [
        str(item.get("id", "")),
        str(item.get("name", "")),
        str(item.get("category", "")),
        str(item.get("description", "")),
        str(item.get("module", "")),
        str(item.get("class_name", "")),
        str(item.get("example", "")),
        str(item.get("limitations", "")),
    ]
    for key in ("tags", "aliases", "dependencies", "related_ids"):
        fields.extend(str(v) for v in item.get(key, []) or [])
    return " ".join(fields).lower()


def search_catalog(
    query: str,
    *,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    test_status: Optional[str] = None,
    catalog: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Search by free text across id, name, tags, aliases, and description."""
    catalog = catalog if catalog is not None else load_catalog()
    tokens = [t for t in query.lower().split() if t]
    results: List[Dict[str, Any]] = []
    for item in catalog.get("components", []):
        if category and item.get("category") != category:
            continue
        if tag and tag not in (item.get("tags") or []):
            continue
        if test_status and item.get("test_status") != test_status:
            continue
        blob = _blob(item)
        if tokens and not all(token in blob for token in tokens):
            continue
        results.append(item)
    return results


def get_component(
    component_id: str,
    catalog: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    catalog = catalog if catalog is not None else load_catalog()
    for item in catalog.get("components", []):
        if item["id"] == component_id:
            return item
    raise CatalogError(f"Unknown component id: {component_id}")


@lru_cache(maxsize=1)
def default_catalog() -> Dict[str, Any]:
    return validate_catalog()


def iter_ids(catalog: Optional[Dict[str, Any]] = None) -> Iterable[str]:
    catalog = catalog if catalog is not None else load_catalog()
    for item in catalog.get("components", []):
        yield item["id"]
