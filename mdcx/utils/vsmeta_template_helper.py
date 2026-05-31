"""
VSMETA模板辅助模块
提供预设模板和占位符选择工具
"""
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TemplatePreset:
    """模板预设数据类"""
    name: str
    template: str
    description: str


# 标题预设模板
TITLE_PRESETS: List[TemplatePreset] = [
    TemplatePreset(
        name="番号-标题(原名)",
        template="{number} - {title} ({originaltitle})",
        description="显示番号、中文标题和日文原名"
    ),
    TemplatePreset(
        name="番号-标题",
        template="{number} - {title}",
        description="只显示番号和中文标题"
    ),
    TemplatePreset(
        name="番号 (原名)",
        template="{number} ({originaltitle})",
        description="显示番号和日文原名"
    ),
    TemplatePreset(
        name="仅标题",
        template="{title}",
        description="只显示中文标题"
    ),
    TemplatePreset(
        name="仅原名",
        template="{originaltitle}",
        description="只显示日文原名"
    ),
    TemplatePreset(
        name="完整信息",
        template="{if:series}[{series}] {/if}{number} - {title} {if:actors}[{actors}]{/if}",
        description="包含系列、番号、标题和演员"
    ),
    TemplatePreset(
        name="评分-标题",
        template="{if:score}[{score}] {/if}{number} - {title}",
        description="显示评分、番号和标题"
    ),
]

# 副标题预设模板
TITLE2_PRESETS: List[TemplatePreset] = [
    TemplatePreset(
        name="发行商/片商",
        template="{publisher} / {studio}",
        description="显示发行商和片商"
    ),
    TemplatePreset(
        name="片商/系列",
        template="{studio} / {series}",
        description="显示片商和系列"
    ),
    TemplatePreset(
        name="演员",
        template="{actors}",
        description="显示演员列表"
    ),
    TemplatePreset(
        name="发行日期",
        template="{release}",
        description="显示发行日期"
    ),
    TemplatePreset(
        name="导演",
        template="{if:director}导演: {director}{/if}",
        description="显示导演信息"
    ),
    TemplatePreset(
        name="评分/时长",
        template="{if:score}评分: {score}{/if}{if:runtime} | 时长: {runtime}分钟{/if}",
        description="显示评分和时长"
    ),
    TemplatePreset(
        name="标签/类型",
        template="{genre}",
        description="显示类型标签"
    ),
]

# 简介预设模板
SUMMARY_PRESETS: List[TemplatePreset] = [
    TemplatePreset(
        name="原名+简介+剧情",
        template="{originaltitle}\n\n{outline}\n\n{originalplot}",
        description="完整的三部分简介"
    ),
    TemplatePreset(
        name="原名+简介",
        template="{originaltitle}\n\n{outline}",
        description="日文原名和中文简介"
    ),
    TemplatePreset(
        name="原名+剧情",
        template="{originaltitle}\n\n{originalplot}",
        description="日文原名和日文剧情"
    ),
    TemplatePreset(
        name="仅简介",
        template="{outline}",
        description="只显示中文简介"
    ),
    TemplatePreset(
        name="完整信息",
        template="{if:title}{title}\n\n{/if}"
                 "{if:originaltitle}{originaltitle}\n\n{/if}"
                 "{if:actors}演员: {actors}\n\n{/if}"
                 "{if:release}发行: {release}\n\n{/if}"
                 "{outline}\n\n{originalplot}",
        description="包含所有可用信息的完整简介"
    ),
]

# 所有可用的占位符列表，带描述
PLACEHOLDERS_WITH_DESC = [
    ("number", "视频番号"),
    ("title", "中文标题"),
    ("originaltitle", "日文原始标题"),
    ("publisher", "发行商"),
    ("studio", "片商/工作室"),
    ("series", "系列名"),
    ("actors", "演员列表"),
    ("outline", "中文简介"),
    ("originalplot", "日文剧情"),
    ("year", "年份"),
    ("release", "发行日期"),
    ("score", "评分"),
    ("country", "国家"),
    ("director", "导演"),
    ("genre", "类型/标签"),
    ("mosaic", "马赛克类型"),
    ("runtime", "时长(分钟)"),
    ("label", "标签"),
    ("website", "官网"),
]


def validate_template(template: str) -> tuple[bool, str]:
    """
    验证模板字符串
    
    Returns (is_valid, error_message)
    """
    stack = []
    i = 0
    n = len(template)
    
    while i < n:
        if template.startswith("{if:", i):
            stack.append("if")
            i += 4
        elif template.startswith("{/if}", i):
            if not stack or stack[-1] != "if":
                return False, f"未闭合的标签: {{/if}} 在位置 {i}"
            stack.pop()
            i += 5
        elif template[i] == "{":
            end = template.find("}", i)
            if end == -1:
                return False, f"未闭合的占位符: {{ 在位置 {i}"
            i = end + 1
        else:
            i += 1
    
    if stack:
        return False, f"缺少闭合标签: {{/if}}"
    
    return True, ""


def get_presets_for_type(template_type: str) -> List[TemplatePreset]:
    """
    根据类型获取预设模板列表
    
    Args:
        template_type: "title", "title2", or "summary"
    """
    if template_type == "title":
        return TITLE_PRESETS
    elif template_type == "title2":
        return TITLE2_PRESETS
    elif template_type == "summary":
        return SUMMARY_PRESETS
    return []
