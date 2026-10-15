from quonitron.catalog import (
    CatalogError,
    check_python_references,
    get_component,
    load_catalog,
    search_catalog,
    validate_catalog,
)
from quonitron.components import BaseComponent, REGISTRY, register
from quonitron.components.base import ComponentMeta


def test_catalog_validates():
    catalog = validate_catalog()
    assert catalog["catalog_version"] == "1.0.0"
    assert len(catalog["components"]) >= 2


def test_python_references_resolve():
    errors = check_python_references()
    assert errors == []


def test_search_theme():
    hits = search_catalog("dark theme")
    ids = [item["id"] for item in hits]
    assert "design.theme.quonitron_dark" in ids


def test_search_by_category():
    hits = search_catalog("", category="base")
    assert any(item["id"] == "base.component" for item in hits)


def test_get_component_and_missing():
    item = get_component("base.component")
    assert item["class_name"] == "BaseComponent"
    try:
        get_component("no.such.component")
        assert False, "expected CatalogError"
    except CatalogError:
        pass


def test_duplicate_ids_rejected():
    catalog = load_catalog()
    catalog = {
        **catalog,
        "components": catalog["components"] + [catalog["components"][0]],
    }
    try:
        validate_catalog(catalog)
        assert False, "expected CatalogError"
    except CatalogError as exc:
        assert "Duplicate" in str(exc)


def test_registry_search_and_duplicate_guard():
    REGISTRY.clear()

    class Demo(BaseComponent):
        component_id = "test.demo.box"
        name = "Demo Box"
        category = "shape"
        tags = ["box", "demo"]
        aliases = ["sample rectangle"]
        description = "A test-only component used to exercise the registry."

    register(Demo)
    assert REGISTRY.get("test.demo.box") is Demo
    assert "test.demo.box" in REGISTRY.search("sample rectangle")
    try:
        register(Demo)
        assert False, "expected duplicate error"
    except ValueError:
        pass
    finally:
        REGISTRY.clear()


def test_invalid_test_status_rejected():
    try:
        ComponentMeta(
            component_id="x.y.z",
            name="X",
            category="base",
            test_status="probably_fine",
        )
        assert False, "expected ValueError"
    except ValueError:
        pass
