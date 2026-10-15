"""Load, validate, search, and resolve the master JSON catalog."""

from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCHEMA_VERSION = "1.0.0"


class CatalogError(ValueError):
    """Invalid catalog data or a failed resolve."""


def find_repo_root(start: Optional[Path] = None) -> Path:
    env = os.environ.get("QUONITRON_ROOT")
    if env:
        candidate = Path(env).expanduser().resolve()
        if (candidate / "catalog" / "master.json").is_file():
            return candidate
    cwd = Path.cwd()
    if (cwd / "catalog" / "master.json").is_file():
        return cwd
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / "catalog" / "master.json").is_file():
            return parent
        if (parent / "catalog" / "schema.json").is_file() and (
            parent / "pyproject.toml"
        ).is_file():
            return parent
    return cwd


def catalog_paths(root: Optional[Path] = None) -> Dict[str, Path]:
    base = find_repo_root(root)
    return {
        "root": base,
        "master": base / "catalog" / "master.json",
        "schema": base / "catalog" / "schema.json",
        "categories": base / "catalog" / "categories.json",
    }


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise CatalogError(f"Missing JSON file: {path}")
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise CatalogError(f"Invalid JSON in {path}: {exc}") from exc


def _jsonschema():
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover
        raise CatalogError(
            "The jsonschema package is required. Install with: pip install jsonschema"
        ) from exc
    return jsonschema


def load_master(root: Optional[Path] = None) -> Dict[str, Any]:
    path = catalog_paths(root)["master"]
    data = load_json(path)
    if not isinstance(data, dict):
        raise CatalogError("master.json root must be an object")
    return data


def load_schema(root: Optional[Path] = None) -> Dict[str, Any]:
    data = load_json(catalog_paths(root)["schema"])
    if not isinstance(data, dict):
        raise CatalogError("schema.json root must be an object")
    return data


def load_categories(root: Optional[Path] = None) -> Dict[str, Any]:
    data = load_json(catalog_paths(root)["categories"])
    if not isinstance(data, dict):
        raise CatalogError("categories.json root must be an object")
    return data


def validate_catalog(root: Optional[Path] = None) -> Dict[str, Any]:
    """Schema-validate master.json and enforce referential integrity."""
    jsonschema = _jsonschema()
    master = load_master(root)
    schema = load_schema(root)
    categories = load_categories(root)

    try:
        jsonschema.validate(instance=master, schema=schema)
    except jsonschema.ValidationError as exc:
        path = "/".join(str(p) for p in exc.path) or "<root>"
        raise CatalogError(
            f"Catalog schema validation failed at {path}: {exc.message}"
        ) from exc

    declared_schema = master.get("schema_version")
    if declared_schema != SCHEMA_VERSION:
        raise CatalogError(
            f"Unsupported catalog schema_version {declared_schema!r}. "
            f"Loader supports {SCHEMA_VERSION}."
        )

    category_ids = {item["id"] for item in categories.get("categories", [])}
    components = master.get("components") or []
    seen: Dict[str, int] = {}
    for index, item in enumerate(components):
        cid = item["id"]
        if cid in seen:
            raise CatalogError(
                f"Duplicate component id {cid!r} at index {index} "
                f"(first seen at {seen[cid]})"
            )
        seen[cid] = index
        cat = item.get("category")
        if cat not in category_ids:
            raise CatalogError(
                f"{cid}: category {cat!r} is not in catalog/categories.json"
            )
        if not item.get("class_name") and not item.get("function_name"):
            raise CatalogError(
                f"{cid}: either class_name or function_name is required"
            )
        status = item.get("test_status")
        if status == "passed" and not item.get("module"):
            raise CatalogError(f"{cid}: passed entries must declare a module")

    for item in components:
        cid = item["id"]
        for related in item.get("related_components") or []:
            if related not in seen:
                raise CatalogError(
                    f"{cid}: related_components references unknown id {related!r}"
                )
    return master


def check_python_references(
    master: Optional[Dict[str, Any]] = None,
    root: Optional[Path] = None,
) -> List[str]:
    """Import each declared module and confirm the class or function exists."""
    master = master if master is not None else load_master(root)
    errors: List[str] = []
    for item in master.get("components") or []:
        module_name = item.get("module") or ""
        if not module_name:
            errors.append(f"{item['id']}: missing module")
            continue
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{item['id']}: cannot import {module_name}: {exc}")
            continue
        attr = item.get("class_name") or item.get("function_name")
        if attr and not hasattr(module, attr):
            errors.append(f"{item['id']}: {module_name} has no attribute {attr}")
    return errors


def resolve_entry(item: Dict[str, Any]) -> Any:
    """Return the Python class or function named by a catalog entry."""
    module_name = item.get("module") or ""
    attr = item.get("class_name") or item.get("function_name")
    if not module_name or not attr:
        raise CatalogError(
            f"{item.get('id', '<unknown>')}: catalog entry is missing module "
            "or class_name/function_name"
        )
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001
        raise CatalogError(
            f"{item.get('id')}: cannot import {module_name}: {exc}"
        ) from exc
    if not hasattr(module, attr):
        raise CatalogError(
            f"{item.get('id')}: {module_name} has no attribute {attr!r}"
        )
    return getattr(module, attr)


def get_component(
    component_id: str,
    master: Optional[Dict[str, Any]] = None,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    master = master if master is not None else load_master(root)
    for item in master.get("components") or []:
        if item["id"] == component_id:
            return item
    known = ", ".join(iter_ids(master)) or "(empty catalog)"
    raise CatalogError(
        f"Unknown component id {component_id!r}. Known ids: {known}"
    )


def resolve(component_id: str, root: Optional[Path] = None) -> Any:
    return resolve_entry(get_component(component_id, root=root))


def _blob(item: Dict[str, Any]) -> str:
    parts: List[str] = [
        str(item.get("id", "")),
        str(item.get("name", "")),
        str(item.get("category", "")),
        str(item.get("subcategory", "")),
        str(item.get("description", "")),
        str(item.get("module", "")),
        str(item.get("class_name", "") or ""),
        str(item.get("function_name", "") or ""),
        str(item.get("example", "")),
        str(item.get("limitations", "")),
    ]
    for key in ("tags", "aliases", "use_cases", "related_components"):
        parts.extend(str(v) for v in item.get(key, []) or [])
    return " ".join(parts).lower()


def search_catalog(
    query: str,
    *,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    test_status: Optional[str] = None,
    master: Optional[Dict[str, Any]] = None,
    root: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    master = master if master is not None else load_master(root)
    tokens = [t for t in query.lower().split() if t]
    hits: List[Dict[str, Any]] = []
    for item in master.get("components") or []:
        if category and item.get("category") != category:
            continue
        if tag and tag not in (item.get("tags") or []):
            continue
        if test_status and item.get("test_status") != test_status:
            continue
        blob = _blob(item)
        if tokens and not all(token in blob for token in tokens):
            continue
        hits.append(item)
    return hits


def iter_ids(master: Optional[Dict[str, Any]] = None) -> Iterable[str]:
    master = master if master is not None else load_master()
    for item in master.get("components") or []:
        yield item["id"]


def unique_ids(master: Optional[Dict[str, Any]] = None) -> Tuple[List[str], List[str]]:
    ids = list(iter_ids(master))
    dupes = sorted({cid for cid in ids if ids.count(cid) > 1})
    return ids, dupes
