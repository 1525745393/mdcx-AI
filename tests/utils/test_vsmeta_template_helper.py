import pytest
from mdcx.utils.vsmeta_template_helper import validate_template_syntax, render_template, PREVIEW_SAMPLE_DATA


class TestValidateTemplateSyntax:
    def test_valid_template_no_conditionals(self):
        result, error = validate_template_syntax("{number} - {title}")
        assert result is True
        assert error == ""

    def test_valid_template_balanced_conditionals(self):
        result, error = validate_template_syntax("{if:series}[{series}] {/if}{number}")
        assert result is True
        assert error == ""

    def test_valid_template_nested_conditionals(self):
        result, error = validate_template_syntax("{if:a}{if:b}x{/if}y{/if}")
        assert result is True
        assert error == ""

    def test_invalid_unclosed_if(self):
        result, error = validate_template_syntax("{if:series}[{series}]")
        assert result is False
        assert error == "{if:} 没有对应的 {/if}"

    def test_invalid_extra_endif(self):
        result, error = validate_template_syntax("{/if}{number}")
        assert result is False
        assert error == "{/if} 没有对应的 {if:}"


class TestRenderTemplateWithSampleData:
    def test_basic_placeholder(self):
        result = render_template("{number}", PREVIEW_SAMPLE_DATA)
        assert result == "ABC-123"

    def test_conditional_with_value(self):
        result = render_template("{if:series}[{series}]{/if}", PREVIEW_SAMPLE_DATA)
        assert result == "[测试系列]"

    def test_conditional_without_value(self):
        result = render_template("{if:nonexistent}[存在]{/if}", PREVIEW_SAMPLE_DATA)
        assert result == ""

    def test_default_value(self):
        result = render_template("{nonexistent|默认值}", PREVIEW_SAMPLE_DATA)
        assert result == "默认值"
