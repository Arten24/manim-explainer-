"""Pure layout arithmetic plus optional real Pango/Manim regression checks."""
import importlib.util
from pathlib import Path

import pytest

from quonitron_manim.design.layout import (
    LayoutError, LayoutItem, LayoutValidator, SafeArea, bounds, layout_regions,
    place_in, stack_in,
)


class Box:
    """Only the public geometry operations used by the layout module."""
    def __init__(self, left=-1, right=1, bottom=0, top=1):
        self.coords = [left, right, bottom, top]
    def get_left(self): return [self.coords[0], 0, 0]
    def get_right(self): return [self.coords[1], 0, 0]
    def get_bottom(self): return [0, self.coords[2], 0]
    def get_top(self): return [0, self.coords[3], 0]
    def shift(self, delta):
        self.coords = [self.coords[0] + delta[0], self.coords[1] + delta[0],
                       self.coords[2] + delta[1], self.coords[3] + delta[1]]


def test_safe_frame_and_subtitle_violations():
    validator = LayoutValidator(scene="BoundsDemo")
    issues = validator.validate([LayoutItem("paragraph", Box(-8, 8, -3, 1))])
    assert len(issues) == 1
    assert issues[0].severity == "ERROR"
    assert "paragraph" in str(issues[0]) and "BoundsDemo" in str(issues[0])
    assert "subtitle-safe" in issues[0].message


def test_accidental_containment_is_not_implicitly_allowed():
    validator = LayoutValidator()
    items = [LayoutItem("panel", Box(-2, 2, -1, 2)), LayoutItem("text", Box())]
    assert validator.validate(items)[0].severity == "ERROR"
    validator.allow("panel", "text", reason="documented panel background")
    assert validator.validate(items)[0].severity == "INFO"


def test_tolerant_edge_contact_and_gap_warning():
    v = LayoutValidator()
    assert not any(i.severity == "ERROR" for i in v.validate([
        LayoutItem("a", Box()), LayoutItem("b", Box(0, 1, 1 - 1e-7, 2))]))
    assert any(i.severity == "WARNING" for i in v.validate([
        LayoutItem("a", Box()), LayoutItem("b", Box(0, 1, 1.04, 2))]))


def test_unrelated_text_collision():
    issues = LayoutValidator().validate([LayoutItem("heading", Box()),
                                         LayoutItem("body", Box())])
    assert [i.severity for i in issues] == ["ERROR"]


def test_region_geometry_and_stack():
    regions = layout_regions()
    assert regions["content"].bottom - regions["subtitle"].top == pytest.approx(0.16)
    a, b = Box(), Box()
    stack_in([a, b], regions["content"], gap=0.4)
    assert bounds(a).bottom - bounds(b).top == pytest.approx(0.4)
    assert not LayoutValidator(regions).validate([LayoutItem("a", a), LayoutItem("b", b)])


def test_oversize_is_atomic_not_silent_shrinking():
    a, b = Box(), Box()
    before = a.coords.copy()
    with pytest.raises(LayoutError, match="split"):
        stack_in([a, b], SafeArea(-1, 1, 0, 1))
    assert a.coords == before
    with pytest.raises(LayoutError):
        place_in(Box(-10, 10), layout_regions()["content"])


def test_stable_ids_and_reasons_required():
    v = LayoutValidator()
    with pytest.raises(ValueError): v.allow("a", "b", reason="")
    with pytest.raises(ValueError): v.validate([LayoutItem("a", Box()), LayoutItem("a", Box())])


def require_manim():
    from quonitron_manim.core.manim_compat import manim_available
    if not manim_available():
        pytest.skip("Real Manim/Pango unavailable; not a rendered/geometry verification")


@pytest.mark.render
def test_real_long_text_and_subtitle_geometry():
    require_manim()
    from quonitron_manim.core.text import measured_text, subtitle_text
    from quonitron_manim.design.theme import get_theme
    theme = get_theme()
    band = layout_regions()["subtitle"]
    caption = subtitle_text("A stable name identifies a slot while its value can change.", theme)
    assert not LayoutValidator().validate([LayoutItem("caption", caption, "subtitle")])
    assert bounds(caption).bottom == pytest.approx(band.bottom)
    with pytest.raises(LayoutError, match="Split"):
        subtitle_text("Long explanations need separate timed cues. " * 80, theme)
    body = measured_text("WIDE " * 20, theme=theme, max_width=4)
    assert body.width <= 4 + 1e-6


@pytest.mark.render
@pytest.mark.parametrize("file,scene", [
    ("foundation_demo.py", "VariableStoresAValue"),
    ("motion_timeline_demo.py", "VariableMemoryTimeline"),
    ("journey_demo.py", "CodeToMemoryJourney"),
    ("text_typography_demo.py", "AssignmentInType"),
])
def test_demo_endpoint_geometry(file, scene):
    """Dry-render existing demos; capture registered endpoint collisions, not pixels."""
    require_manim()
    from manim import tempconfig
    path = Path(__file__).resolve().parents[1] / "examples" / file
    spec = importlib.util.spec_from_file_location("audit_demo", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Resolve Part 2 name without guessing the public scene class.
    if file == "motion_timeline_demo.py":
        scene = "VariableMemoryTimeline"  # public demo scene
    with tempconfig({"dry_run": True, "disable_caching": True}):
        instance = getattr(module, scene)()
        failures = []
        original = instance.check_layout
        def capture(**kwargs):
            issues = original(**kwargs)
            failures.extend(i for i in issues if i.severity == "ERROR")
            return issues
        instance.check_layout = capture
        instance.render()
        # Close-up cropping in the journey is intentional and still emits diagnostics.
        if file != "journey_demo.py":
            assert not failures, "\n".join(map(str, failures))


def test_horizontal_connector_cannot_evade_collision_check():
    class Connector(Box):
        def get_start(self): return [-1, 0.5, 0]
        def get_end(self): return [1, 0.5, 0]
    arrow = Connector(-1, 1, 0.5, 0.5)
    issues = LayoutValidator().validate([LayoutItem("arrow", arrow),
                                         LayoutItem("label", Box())])
    assert any(i.severity == "ERROR" and set(i.ids) == {"arrow", "label"} for i in issues)


def test_subtitle_box_must_fit_its_own_band():
    band = layout_regions()["subtitle"]
    good = Box(band.left, band.right, band.bottom, band.top)
    assert not LayoutValidator().validate([LayoutItem("caption", good, "subtitle")])
    bad = Box(band.left, band.right, band.bottom, band.top + 0.2)
    assert LayoutValidator().validate([LayoutItem("caption", bad, "subtitle")])[0].severity == "ERROR"


def test_notebook_is_valid_and_render_gated(repo_root):
    import json
    notebook = json.loads((repo_root / "notebooks/overlap_repair_lab.ipynb").read_text())
    assert notebook["nbformat"] == 4
    source = "\n".join("".join(c["source"]) for c in notebook["cells"])
    assert "if not READY" in source
    assert "embed=True" in source
    assert "LayoutRepairExercise" in source
