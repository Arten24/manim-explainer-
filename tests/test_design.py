from quonitron.design import get_theme, list_themes, register_theme, Theme
from quonitron.design.tokens import ColorPalette


def test_default_theme_registered():
    assert "quonitron_dark" in list_themes()
    theme = get_theme()
    assert theme.name == "quonitron_dark"
    assert theme.color("background").startswith("#")
    assert theme.color("text_primary") == "#F5F7FA"
    assert theme.duration("normal") == 0.5


def test_unknown_color_role_raises():
    theme = get_theme()
    try:
        theme.color("neon_soup")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "neon_soup" in str(exc)


def test_unknown_theme_raises():
    try:
        get_theme("does_not_exist")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_register_custom_theme():
    custom = Theme(
        name="test_light",
        colors=ColorPalette(background="#FFFFFF", text_primary="#111111"),
    )
    register_theme("test_light", custom)
    loaded = get_theme("test_light")
    assert loaded.color("background") == "#FFFFFF"
    assert loaded.color("text_primary") == "#111111"


def test_theme_to_dict_contains_roles():
    data = get_theme().to_dict()
    assert "colors" in data
    assert data["colors"]["accent"] == "#4F8CFF"
    assert data["pixel_width"] == 1920
    assert data["frame_rate"] == 30
