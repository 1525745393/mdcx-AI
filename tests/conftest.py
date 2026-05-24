"""
Test skipping utilities for PyQt6-dependent tests.
"""
import os
import sys

import pytest


def is_ci() -> bool:
    """判断是否在CI环境中运行"""
    return os.environ.get("CI", "").lower() in ("true", "1")


def is_headless() -> bool:
    """判断是否为无头环境"""
    if sys.platform.startswith("linux"):
        if not os.environ.get("DISPLAY"):
            return True
    return False


def skip_if_ci_headless():
    """在CI/无头环境下跳过PyQt6依赖测试"""
    return pytest.mark.skipif(
        is_ci() or is_headless(),
        reason="Skipping PyQt6-dependent test in CI/headless environment"
    )


def skip_on_ci():
    """在CI环境中跳过测试"""
    return pytest.mark.skipif(
        is_ci(),
        reason="Skipping test in CI environment"
    )


def requires_pyqt6_available(func):
    """要求PyQt6可用的装饰器"""
    try:
        import PyQt6  # noqa: F401
        pyqt6_available = True
    except ImportError:
        pyqt6_available = False

    should_skip = is_ci() or is_headless() or not pyqt6_available
    return pytest.mark.skipif(
        should_skip,
        reason="Requires PyQt6 and non-headless environment"
    )(func)
