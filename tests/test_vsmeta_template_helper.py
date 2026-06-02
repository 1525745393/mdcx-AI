"""
测试 VSMETA 模板辅助模块
"""
import pytest

from mdcx.utils.vsmeta_template_helper import (
    TemplatePreset,
    TITLE_PRESETS,
    TITLE2_PRESETS,
    SUMMARY_PRESETS,
    get_all_presets,
    get_preset_by_name,
    validate_template,
    extract_placeholders,
    render_template
)


class TestTemplatePreset:
    """测试模板预设数据类"""

    def test_template_preset_basic(self):
        """测试模板预设基本功能"""
        preset = TemplatePreset(
            name="测试预设",
            template="{number} - {title}",
            description="测试描述"
        )
        
        assert preset.name == "测试预设"
        assert preset.template == "{number} - {title}"
        assert preset.description == "测试描述"


class TestPresets:
    """测试预设模板列表"""

    def test_title_presets_count(self):
        """测试标题预设数量"""
        assert len(TITLE_PRESETS) > 0

    def test_title2_presets_count(self):
        """测试副标题预设数量"""
        assert len(TITLE2_PRESETS) > 0

    def test_summary_presets_count(self):
        """测试简介预设数量"""
        assert len(SUMMARY_PRESETS) > 0

    def test_presets_have_required_fields(self):
        """测试所有预设都有必需字段"""
        for preset in TITLE_PRESETS + TITLE2_PRESETS + SUMMARY_PRESETS:
            assert preset.name is not None
            assert preset.template is not None
            assert preset.description is not None
            assert isinstance(preset.name, str)
            assert isinstance(preset.template, str)
            assert isinstance(preset.description, str)


class TestPresetFunctions:
    """测试预设相关函数"""

    def test_get_all_presets(self):
        """测试获取所有预设"""
        presets = get_all_presets()
        
        assert "title" in presets
        assert "title2" in presets
        assert "summary" in presets
        
        assert presets["title"] == TITLE_PRESETS
        assert presets["title2"] == TITLE2_PRESETS
        assert presets["summary"] == SUMMARY_PRESETS

    def test_get_preset_by_name_found(self):
        """测试按名称查找预设（找到）"""
        preset = get_preset_by_name("title", "番号-标题")
        
        assert preset is not None
        assert preset.name == "番号-标题"

    def test_get_preset_by_name_not_found(self):
        """测试按名称查找预设（找不到）"""
        preset = get_preset_by_name("title", "不存在的预设")
        
        assert preset is None


class TestTemplateValidation:
    """测试模板验证功能"""

    def test_validate_template_valid(self):
        """测试验证有效模板"""
        is_valid, error = validate_template("{number} - {title}")
        assert is_valid is True
        assert error == ""

    def test_validate_template_invalid_syntax(self):
        """测试验证语法错误的模板"""
        is_valid, error = validate_template("{number - {title}")
        assert is_valid is False
        assert len(error) > 0

    def test_validate_template_unclosed_if(self):
        """测试未闭合的条件标签"""
        is_valid, error = validate_template("{if:series}[{series}]")
        assert is_valid is False
        assert "缺少闭合标签" in error


class TestPlaceholderExtraction:
    """测试占位符提取功能"""

    def test_extract_placeholders_basic(self):
        """测试提取基本占位符"""
        placeholders = extract_placeholders("{number} - {title}")
        assert "number" in placeholders
        assert "title" in placeholders

    def test_extract_placeholders_with_conditional(self):
        """测试提取带条件语法的占位符"""
        placeholders = extract_placeholders("{if:series}[{series}] {/if}{number}")
        assert "series" in placeholders
        assert "number" in placeholders

    def test_extract_placeholders_empty(self):
        """测试空模板"""
        placeholders = extract_placeholders("")
        assert len(placeholders) == 0


class TestTemplateRendering:
    """测试模板渲染功能"""

    def test_render_template_basic(self):
        """测试基本模板渲染"""
        template = "{number} - {title}"
        data = {"number": "AB-123", "title": "测试标题"}
        
        result = render_template(template, data)
        assert result == "AB-123 - 测试标题"

    def test_render_template_with_missing_field(self):
        """测试渲染缺少字段的模板"""
        template = "{number} - {title}"
        data = {"number": "AB-123"}  # 缺少 title
        
        result = render_template(template, data)
        assert result == "AB-123 - "

    def test_render_template_with_default(self):
        """测试带默认值的模板渲染"""
        template = "{title|未知标题}"
        data = {}  # 缺少 title
        
        result = render_template(template, data)
        assert result == "未知标题"

    def test_render_template_conditional(self):
        """测试条件渲染"""
        template = "{if:series}[{series}] {/if}{number}"
        
        # 有 series
        result = render_template(template, {"number": "AB-123", "series": "系列A"})
        assert result == "[系列A] AB-123"
        
        # 没有 series
        result = render_template(template, {"number": "AB-123"})
        assert result == "AB-123"
