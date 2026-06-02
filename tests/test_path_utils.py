"""
测试路径工具函数
"""
import os
import tempfile
from pathlib import Path

import pytest

from mdcx.utils.path import (
    showFilePath,
    is_descendant,
    is_any_descendant
)


class TestShowFilePath:
    """测试文件路径显示功能"""

    def test_showFilePath_short(self):
        """测试短路径显示"""
        path = "/short/path/to/file.txt"
        assert showFilePath(path) == path

    def test_showFilePath_long(self):
        """测试长路径显示"""
        path = "/very/long/path/that/exceeds/the/limit/by/a/lot/file.txt"
        result = showFilePath(path)
        assert result.startswith("..")
        assert len(result) <= 55

    def test_showFilePath_empty(self):
        """测试空路径"""
        assert showFilePath("") == ""


class TestIsDescendant:
    """测试后代路径判断功能"""

    def test_is_descendant_true(self):
        """测试确实是后代"""
        parent = "/home/user"
        child = "/home/user/documents/file.txt"
        assert is_descendant(child, parent) is True

    def test_is_descendant_same(self):
        """测试相同路径"""
        path = "/home/user/documents"
        assert is_descendant(path, path) is True

    def test_is_descendant_false(self):
        """测试不是后代"""
        parent = "/home/user"
        child = "/home/other/file.txt"
        assert is_descendant(child, parent) is False

    def test_is_descendant_prefix_issue(self):
        """测试前缀问题（/foo/bar vs /foo/barbar）"""
        parent = "/foo/bar"
        child = "/foo/barbar"
        assert is_descendant(child, parent) is False

    def test_is_descendant_nonexistent(self):
        """测试不存在的路径的字符串比较"""
        parent = "/nonexistent/path/a"
        child = "/nonexistent/path/b"
        assert is_descendant(child, parent) is False


class TestIsAnyDescendant:
    """测试多父路径后代判断功能"""

    def test_is_any_descendant_true(self):
        """测试是其中一个父路径的后代"""
        parents = ["/home/user1", "/home/user2"]
        child = "/home/user2/documents/file.txt"
        assert is_any_descendant(child, *parents) is True

    def test_is_any_descendant_false(self):
        """测试不是任何父路径的后代"""
        parents = ["/home/user1", "/home/user2"]
        child = "/home/other/file.txt"
        assert is_any_descendant(child, *parents) is False

    def test_is_any_descendant_empty_parents(self):
        """测试空父路径列表"""
        child = "/home/user/file.txt"
        assert is_any_descendant(child) is False
