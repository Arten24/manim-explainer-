import pytest

from quonitron_manim.core.catalog import get_component, resolve, validate_catalog
from quonitron_manim.motion import ALL_MOTION_RECIPES
from quonitron_manim.motion.base import MotionError
from quonitron_manim.motion.appearance import FadeInMotion
from quonitron_manim.motion.position import MoveToMotion, ShiftMotion
from quonitron_manim.motion.rotation import ScaleMotion
from quonitron_manim.motion.transform import MorphPropertyMotion


def test_every_motion_recipe_validates_defaults():
    for cls in ALL_MOTION_RECIPES:
        recipe = cls()
        recipe.validate()
        assert recipe.component_id.startswith("motion.")
        assert recipe.manim_api
        assert recipe.run_time() > 0


def test_invalid_run_time_and_easing():
    try:
        FadeInMotion(run_time=0).validate()
        raise AssertionError("expected MotionError")
    except MotionError:
        pass
    try:
        FadeInMotion(easing="bounce_the_moon").validate()
        raise AssertionError("expected MotionError")
    except MotionError:
        pass


def test_move_to_requires_well_formed_point():
    try:
        MoveToMotion(target=[0]).validate()
        raise AssertionError("expected MotionError")
    except MotionError:
        pass
    MoveToMotion(target=[1.0, 2.0]).validate()


def test_scale_factor_must_be_positive():
    try:
        ScaleMotion(factor=0).validate()
        raise AssertionError("expected MotionError")
    except MotionError:
        pass
    ScaleMotion(factor=1.2).validate()


def test_opacity_bounds():
    try:
        MorphPropertyMotion(opacity=1.5).validate()
        raise AssertionError("expected MotionError")
    except MotionError:
        pass
    MorphPropertyMotion(opacity=0.4, color="accent").validate()


def test_shift_vector():
    ShiftMotion(vector=[0.5, 0, 0]).validate()


def test_motion_ids_are_in_the_catalog(repo_root):
    master = validate_catalog(repo_root)
    ids = {item["id"] for item in master["components"]}
    for cls in ALL_MOTION_RECIPES:
        assert cls.component_id in ids
        entry = get_component(cls.component_id, root=repo_root)
        assert resolve(cls.component_id, root=repo_root) is cls
        assert entry["module"]
        assert entry["class_name"] == cls.__name__


def test_unknown_motion_id_is_a_catalog_error(repo_root):
    from quonitron_manim.core.catalog import CatalogError

    try:
        get_component("motion.appearance.does_not_exist", root=repo_root)
        raise AssertionError("expected CatalogError")
    except CatalogError as exc:
        assert "Unknown component id" in str(exc)
