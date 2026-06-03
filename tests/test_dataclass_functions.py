"""
测试修复的函数
"""
import pytest

from mdcx.utils.dataclass import update_existing, update_existing_valid


class TestUpdateExisting:
    """测试 update_existing 函数"""

    def test_update_existing_basic(self):
        """测试基本更新功能"""
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"b": 20, "c": 30, "d": 40}
        
        result = update_existing(d1, d2)
        
        # 验证结果正确
        assert result == {"a": 1, "b": 20, "c": 30}
        # 验证原始字典 d1 未被修改
        assert d1 == {"a": 1, "b": 2, "c": 3}
        # 验证原始字典 d2 未被修改
        assert d2 == {"b": 20, "c": 30, "d": 40}

    def test_update_existing_empty_d1(self):
        """测试空字典 d1"""
        d1 = {}
        d2 = {"a": 1, "b": 2}
        
        result = update_existing(d1, d2)
        
        assert result == {}
        assert d1 == {}
        assert d2 == {"a": 1, "b": 2}

    def test_update_existing_empty_d2(self):
        """测试空字典 d2"""
        d1 = {"a": 1, "b": 2}
        d2 = {}
        
        result = update_existing(d1, d2)
        
        assert result == {"a": 1, "b": 2}
        assert d1 == {"a": 1, "b": 2}
        assert d2 == {}

    def test_update_existing_no_common_keys(self):
        """测试无共同 key 的情况"""
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        
        result = update_existing(d1, d2)
        
        assert result == {"a": 1, "b": 2}
        assert d1 == {"a": 1, "b": 2}

    def test_update_existing_with_nested_dict(self):
        """测试嵌套字典"""
        d1 = {"a": 1, "nested": {"x": 10, "y": 20}}
        d2 = {"nested": {"x": 100}, "b": 2}
        
        result = update_existing(d1, d2)
        
        # 验证嵌套字典整体替换（非深度合并）
        assert result == {"a": 1, "nested": {"x": 100}}
        # 验证原始字典未被修改
        assert d1 == {"a": 1, "nested": {"x": 10, "y": 20}}

    def test_update_existing_preserves_original(self):
        """验证不修改原始字典（修复后的关键行为）"""
        original = {"key1": "value1", "key2": "value2"}
        update_source = {"key1": "updated", "key3": "new"}
        
        _ = update_existing(original, update_source)
        
        # 原始字典应该完全不变
        assert original == {"key1": "value1", "key2": "value2"}, \
            "update_existing 不应该修改原始字典"


class TestUpdateExistingValid:
    """测试 update_existing_valid 函数"""

    def test_update_existing_valid_basic(self):
        """测试基本验证更新功能"""
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"a": 0, "b": 20, "c": "", "d": 40}
        
        result = update_existing_valid(d1, d2)
        
        # 0 和空字符串被 bool() 视为无效，不会更新
        assert result == {"a": 1, "b": 20, "c": 3}
        # 验证原始字典未被修改
        assert d1 == {"a": 1, "b": 2, "c": 3}

    def test_update_existing_valid_custom_validator(self):
        """测试自定义验证函数"""
        d1 = {"name": "old", "count": 0, "score": -1}
        d2 = {"name": "", "count": 5, "score": 100}
        
        # 自定义验证器：非空字符串或正数
        def positive_or_non_empty(value):
            if isinstance(value, str):
                return len(value) > 0
            elif isinstance(value, (int, float)):
                return value > 0
            return bool(value)
        
        result = update_existing_valid(d1, d2, positive_or_non_empty)
        
        assert result == {"name": "old", "count": 5, "score": 100}
        assert d1 == {"name": "old", "count": 0, "score": -1}

    def test_update_existing_valid_none_values(self):
        """测试 None 值处理"""
        d1 = {"a": 1, "b": 2}
        d2 = {"a": None, "b": 20}
        
        result = update_existing_valid(d1, d2)
        
        assert result == {"a": 1, "b": 20}
        assert d1 == {"a": 1, "b": 2}

    def test_update_existing_valid_preserves_original(self):
        """验证不修改原始字典（修复后的关键行为）"""
        original = {"x": 10, "y": 20}
        update_source = {"x": 100, "z": 30}
        
        _ = update_existing_valid(original, update_source)
        
        assert original == {"x": 10, "y": 20}, \
            "update_existing_valid 不应该修改原始字典"
