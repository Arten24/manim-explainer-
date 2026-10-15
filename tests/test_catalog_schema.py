from quonitron_manim.core.catalog import (
    SCHEMA_VERSION,
    CatalogError,
    check_python_references,
    get_component,
    resolve,
    search_catalog,
    unique_ids,
    validate_catalog,
)


def test_master_validates_against_schema(repo_root):
    master = validate_catalog(repo_root)
    assert master["schema_version"] == SCHEMA_VERSION
    assert master["components"], "Part 1 catalog must list real components"


def test_component_ids_are_unique(repo_root):
    master = validate_catalog(repo_root)
    ids, dupes = unique_ids(master)
    assert dupes == []
    assert len(ids) == len(set(ids))


def test_python_references_resolve(repo_root):
    master = validate_catalog(repo_root)
    errors = check_python_references(master, repo_root)
    assert errors == [], errors
    for item in master["components"]:
        obj = resolve(item["id"], root=repo_root)
        expected = item.get("class_name") or item.get("function_name")
        assert obj.__name__ == expected


def test_unknown_component_error_lists_known_ids(repo_root):
    try:
        get_component("motion.does.not.exist", root=repo_root)
        raise AssertionError("expected CatalogError")
    except CatalogError as exc:
        message = str(exc)
        assert "Unknown component id" in message
        assert "foundation.title_card" in message


def test_search_by_concept(repo_root):
    hits = search_catalog("variable", root=repo_root)
    ids = [item["id"] for item in hits]
    assert "foundation.variable_store" in ids
    theme_hits = search_catalog("dark theme", root=repo_root)
    assert any(item["id"] == "design.theme.quonitron_dark" for item in theme_hits)


def test_every_component_category_is_registered(repo_root):
    from quonitron_manim.core.catalog import load_categories, load_master

    cats = {item["id"] for item in load_categories(repo_root)["categories"]}
    master = load_master(repo_root)
    for item in master["components"]:
        assert item["category"] in cats, item["id"]
