# Catalog schema

Files:

- `catalog/schema.json` — JSON Schema (`schema_version` **1.0.0**)
- `catalog/master.json` — searchable component index
- `catalog/categories.json` — allowed `category` values

The loader in `quonitron_manim.core.catalog` validates the master file,
rejects duplicate ids, unknown categories, broken `related_components`,
and missing Python attributes.

## Required fields (schema 1.0.0)

`id`, `name`, `version`, `category`, `subcategory`, `tags`, `aliases`,
`description`, `use_cases`, `module`, `parameters`, `dependencies`,
`compatibility`, `example`, `test_status`, `limitations`,
`related_components`, `license`, plus either `class_name` or
`function_name`.

`preview` may be a path or `null`.

`test_status` is one of `not_tested`, `passed`, `failed`.

## Evolving the schema

Change `schema_version` only when the JSON shape changes. Update
`catalog/schema.json`, the loader constant `SCHEMA_VERSION`, and this
document in the same change. Old catalogs must fail loudly rather than
be silently misread.

## Resolve

```python
from quonitron_manim.core.catalog import resolve, search_catalog

hits = search_catalog("title")
TitleCard = resolve("foundation.title_card")
```

A missing id raises `CatalogError` listing known ids.
