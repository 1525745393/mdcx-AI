"""
VSMETA模板辅助模块
提供预设模板和占位符选择工具
"""
from dataclasses import dataclass


@dataclass
class TemplatePreset:
    """模板预设数据类"""
    name: str
    template: str
    description: str


# 标题预设模板
TITLE_PRESETS: list[TemplatePreset] = [
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
TITLE2_PRESETS: list[TemplatePreset] = [
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
SUMMARY_PRESETS: list[TemplatePreset] = [
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
    ("actors", "演员列表(最多3个)"),
    ("actors_full", "完整演员列表"),
    ("all_actors", "全部演员列表(最多3个)"),
    ("all_actors_full", "完整全部演员列表"),
    ("outline", "中文简介"),
    ("originalplot", "日文剧情"),
    ("year", "年份"),
    ("release", "发行日期"),
    ("score", "评分"),
    ("country", "国家"),
    ("director", "导演"),
    ("director_list", "导演列表"),
    ("genre", "类型/标签(最多5个)"),
    ("mosaic", "马赛克类型"),
    ("runtime", "时长(分钟)"),
    ("label", "标签"),
    ("website", "官网"),
    ("letters", "番号字母部分"),
    ("wanted", "想看人数"),
    ("tag", "标签(逗号分隔)"),
    ("thumb", "缩略图URL"),
    ("poster", "海报URL"),
    ("trailer", "预告片URL"),
    ("extrafanart", "额外剧照列表"),
    ("actor", "单个演员"),
    ("tags_list", "标签列表"),
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

            inner_content = template[i+1:end]
            if "{" in inner_content:
                return False, f"占位符内不允许嵌套 {{ 在位置 {i}"

            i = end + 1
        else:
            i += 1

    if stack:
        return False, "缺少闭合标签: {/if}"

    return True, ""


def get_presets_for_type(template_type: str) -> list[TemplatePreset]:
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


def get_all_presets() -> dict[str, list[TemplatePreset]]:
    """
    获取所有预设模板
    
    Returns:
        包含 title, title2, summary 预设的字典
    """
    return {
        "title": TITLE_PRESETS,
        "title2": TITLE2_PRESETS,
        "summary": SUMMARY_PRESETS
    }


def get_preset_by_name(template_type: str, name: str) -> TemplatePreset | None:
    """
    根据名称查找预设模板
    
    Args:
        template_type: 预设类型
        name: 预设名称
    
    Returns:
        找到的预设，未找到返回 None
    """
    presets = get_presets_for_type(template_type)
    for preset in presets:
        if preset.name == name:
            return preset
    return None


def extract_placeholders(template: str) -> set[str]:
    """
    从模板中提取所有占位符名称
    
    Args:
        template: 模板字符串
    
    Returns:
        占位符名称集合
    """
    placeholders = set()
    i = 0
    n = len(template)

    while i < n:
        if template.startswith("{if:", i):
            # 条件标签 {if:field}
            end = template.find("}", i)
            if end != -1:
                field = template[i + 4:end]
                placeholders.add(field.strip())
            i = end + 1 if end != -1 else i + 1
        elif template.startswith("{/if}", i):
            i += 5
        elif template[i] == "{":
            end = template.find("}", i)
            if end != -1:
                content = template[i + 1:end]
                # 处理默认值语法 {field|default}
                if "|" in content:
                    field = content.split("|")[0]
                else:
                    field = content
                placeholders.add(field.strip())
            i = end + 1 if end != -1 else i + 1
        else:
            i += 1

    return placeholders


def render_template(template: str, data: dict) -> str:
    """
    使用数据渲染模板
    
    Args:
        template: 模板字符串
        data: 数据字典
    
    Returns:
        渲染后的字符串
    """
    result = []
    i = 0
    n = len(template)

    while i < n:
        if template.startswith("{if:", i):
            # 条件渲染 {if:field}...{/if}
            field_end = template.find("}", i)
            if field_end == -1:
                result.append(template[i])
                i += 1
                continue

            field = template[i + 4:field_end].strip()
            content_start = field_end + 1

            # 查找对应的 {/if}
            depth = 1
            j = content_start
            while j < n and depth > 0:
                if template.startswith("{if:", j):
                    depth += 1
                    j += 4
                elif template.startswith("{/if}", j):
                    depth -= 1
                    if depth == 0:
                        break
                    j += 5
                else:
                    j += 1

            if depth == 0:
                # 找到了闭合标签
                if field in data and data[field]:
                    # 递归渲染条件内容
                    inner_content = template[content_start:j]
                    result.append(render_template(inner_content, data))
                i = j + 5
            else:
                # 未找到闭合标签，原样输出
                result.append(template[i])
                i += 1

        elif template[i] == "{":
            # 普通占位符 {field} 或 {field|default}
            end = template.find("}", i)
            if end == -1:
                result.append(template[i])
                i += 1
                continue

            content = template[i + 1:end]
            if "|" in content:
                field, default = content.split("|", 1)
                value = data.get(field.strip(), default)
            else:
                value = data.get(content, "")

            result.append(str(value) if value is not None else "")
            i = end + 1

        else:
            result.append(template[i])
            i += 1

    return "".join(result)


def validate_template_syntax(template: str) -> tuple[bool, str]:
    """验证模板语法，检查 {if:} 和 {/if} 是否配对

    Args:
        template: 模板字符串

    Returns:
        tuple[bool, str]: (是否有效, 错误信息)
    """
    depth = 0
    for i in range(len(template)):
        if template.startswith("{if:", i):
            depth += 1
        elif template.startswith("{/if}", i):
            depth -= 1
            if depth < 0:
                return False, "{/if} 没有对应的 {if:}"
    if depth > 0:
        return False, "{if:} 没有对应的 {/if}"
    return True, ""


# 预览用的示例数据
PREVIEW_SAMPLE_DATA: dict = {
    "number": "ABC-123",
    "title": "测试标题",
    "originaltitle": "テストタイトル",
    "publisher": "测试发行商",
    "studio": "测试片商",
    "series": "测试系列",
    "actors": "演员A、演员B、演员C",
    "actors_full": "演员A、演员B、演员C、演员D、演员E",
    "all_actors": "演员A、演员B、演员C",
    "all_actors_full": "演员A、演员B、演员C、演员D、演员E",
    "director": "测试导演",
    "outline": "这是中文简介",
    "originalplot": "これは日本語の梗概です",
    "year": "2024",
    "release": "2024-01-15",
    "runtime": "120",
    "score": "8.5",
    "genre": "剧情",
    "country": "日本",
    "mosaic": "有码",
    "label": "测试标签",
    "website": "https://example.com",
    "letters": "ABC",
    "wanted": "1234",
    "tag": "标签1,标签2,标签3",
    "thumb": "https://example.com/thumb.jpg",
    "poster": "https://example.com/poster.jpg",
    "trailer": "https://example.com/trailer.mp4",
    "extrafanart": "https://example.com/fan1.jpg,https://example.com/fan2.jpg",
    "actor": "演员A",
    "director_list": "导演A,导演B",
    "tags_list": "标签1,标签2,标签3",
}
