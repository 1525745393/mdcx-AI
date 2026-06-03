# VSMeta UI 优化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现 VSMeta 界面配置的优化功能，包括模板预览、预设管理、语法验证、批量操作等

**Architecture:** 在现有代码基础上添加新功能，保持代码向后兼容。UI 修改集中在 MDCx.py，逻辑功能添加到 vsmeta_template_helper.py，配置模型扩展放在 config/models.py

**Tech Stack:** Python, PyQt6, Pydantic

---

## 文件结构

### 需要创建的文件
- `tests/utils/test_vsmeta_template_helper.py` - 模板辅助函数测试

### 需要修改的文件
- `mdcx/utils/vsmeta_template_helper.py` - 添加语法验证函数和示例数据
- `mdcx/views/MDCx.py` - 添加预览区域、自定义预设管理 UI、重置/导出按钮
- `mdcx/config/models.py` - 添加自定义预设数据结构和配置
- `mdcx/controllers/main_window/load_config.py` - 加载自定义预设
- `mdcx/controllers/main_window/save_config.py` - 保存自定义预设

---

## 任务 1: 添加模板语法验证函数

**Files:**
- Modify: `mdcx/utils/vsmeta_template_helper.py:1-10` (imports)
- Modify: `mdcx/utils/vsmeta_template_helper.py` (添加函数在文件末尾)
- Create: `tests/utils/test_vsmeta_template_helper.py`

- [ ] **Step 1: 添加语法验证函数到 vsmeta_template_helper.py**

在文件末尾添加:

```python
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
    "actors": "演员A、演员B",
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
}
```

- [ ] **Step 2: 创建测试文件**

```python
# tests/utils/test_vsmeta_template_helper.py
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
```

- [ ] **Step 3: 运行测试验证**

Run: `pytest tests/utils/test_vsmeta_template_helper.py -v`
Expected: PASS (所有测试)

- [ ] **Step 4: 提交**

```bash
git add mdcx/utils/vsmeta_template_helper.py tests/utils/test_vsmeta_template_helper.py
git commit -m "feat(vsmeta): add template syntax validation and preview sample data"
```

---

## 任务 2: 添加自定义预设数据结构

**Files:**
- Modify: `mdcx/config/models.py` - 添加 VsmetaCustomPreset dataclass 和 custom_presets 字段

- [ ] **Step 1: 在 models.py 添加预设数据类**

在 imports 区域后添加:

```python
@dataclass
class VsmetaCustomPreset:
    """VSMeta 自定义预设"""
    name: str
    show_title_type: int      # 对应 VsmetaShowTitle 枚举值
    show_title2_type: int     # 对应 VsmetaShowTitle2 枚举值
    summary_type: int         # 对应 VsmetaSummary 枚举值
    custom_title: str
    custom_title2: str
    custom_summary: str
```

- [ ] **Step 2: 在 Config 类中添加 custom_presets 字段**

在 `vsmeta_summary` 字段后添加:

```python
    custom_presets: list[VsmetaCustomPreset] = Field(default_factory=list, title="VSMeta 自定义预设")
```

- [ ] **Step 3: 提交**

```bash
git add mdcx/config/models.py
git commit -m "feat(config): add VsmetaCustomPreset dataclass and custom_presets field"
```

---

## 任务 3: 更新界面字符串

**Files:**
- Modify: `mdcx/views/MDCx.py` - retranslateUi 函数中的字符串定义

- [ ] **Step 1: 更新翻译字符串**

找到 retranslateUi 函数中 `label_vsmeta_template_help` 的设置，更新为:

```python
self.label_vsmeta_template_help.setText(_translate(
    "MDCx",
    "【模板语法完整指南】\n\n"
    "【基础占位符】\n"
    "• 番号相关：{number}\n"
    "• 标题相关：{title}（中文）、{originaltitle}（日文）\n"
    "• 制作信息：{publisher}（发行商）、{studio}（工作室）、{series}（系列）\n"
    "• 演职人员：{actors}（演员列表）、{director}（导演）\n"
    "• 剧情描述：{outline}（中文简介）、{originalplot}（日文简介）\n"
    "• 时间信息：{year}（年份）、{release}（发布日期）、{runtime}（时长）\n"
    "• 其他信息：{score}（评分）、{country}（国家）、{genre}（类型）、{mosaic}（马赛克类型）、{label}（标签）、{website}（官网）\n\n"
    "【增强语法】\n"
    "• 条件显示：{if:field}内容{/if} - 字段存在时显示内容\n"
    "• 默认值：{field|默认值} - 字段为空时使用默认值\n\n"
    "【默认值语法示例】\n"
    "• {title|无标题} - 标题为空时显示\"无标题\"\n"
    "• {actors|未知演员} - 演员为空时显示\"未知演员\"\n"
    "• {score|暂无评分} - 评分为空时显示\"暂无评分\"\n"
))
```

- [ ] **Step 2: 提交**

```bash
git add mdcx/views/MDCx.py
git commit -m "docs(ui): update VSMeta template help text with default value syntax examples"
```

---

## 任务 4: 添加预览区域 UI

**Files:**
- Modify: `mdcx/views/MDCx.py` - setupUi 函数中 gridLayout_vsmeta_config 的布局

- [ ] **Step 1: 在自定义简介模板输入后添加预览区域**

在 `plainTextEdit_vsmeta_custom_summary` 添加后，找到帮助标签的位置，在其后添加预览标签:

在 `self.label_vsmeta_template_help` 后添加:

```python
        # 标题预览
        self.label_vsmeta_title_preview = QtWidgets.QLabel(parent=self.gridLayoutWidget_vsmeta_config)
        self.label_vsmeta_title_preview.setStyleSheet("background-color: #f5f5f5; padding: 5px;")
        self.label_vsmeta_title_preview.setWordWrap(True)
        self.label_vsmeta_title_preview.setObjectName("label_vsmeta_title_preview")
        self.gridLayout_vsmeta_config.addWidget(self.label_vsmeta_title_preview, 14, 0, 1, 2)

        # 副标题预览
        self.label_vsmeta_title2_preview = QtWidgets.QLabel(parent=self.gridLayoutWidget_vsmeta_config)
        self.label_vsmeta_title2_preview.setStyleSheet("background-color: #f5f5f5; padding: 5px;")
        self.label_vsmeta_title2_preview.setWordWrap(True)
        self.label_vsmeta_title2_preview.setObjectName("label_vsmeta_title2_preview")
        self.gridLayout_vsmeta_config.addWidget(self.label_vsmeta_title2_preview, 15, 0, 1, 2)

        # 简介预览
        self.label_vsmeta_summary_preview = QtWidgets.QLabel(parent=self.gridLayoutWidget_vsmeta_config)
        self.label_vsmeta_summary_preview.setStyleSheet("background-color: #f5f5f5; padding: 5px;")
        self.label_vsmeta_summary_preview.setWordWrap(True)
        self.label_vsmeta_summary_preview.setObjectName("label_vsmeta_summary_preview")
        self.gridLayout_vsmeta_config.addWidget(self.label_vsmeta_summary_preview, 16, 0, 1, 2)
```

- [ ] **Step 2: 更新 retranslateUi 添加预览标签翻译**

在 `label_vsmeta_template_help` 翻译后添加:

```python
        self.label_vsmeta_title_preview.setText(_translate("MDCx", "标题预览："))
        self.label_vsmeta_title2_preview.setText(_translate("MDCx", "副标题预览："))
        self.label_vsmeta_summary_preview.setText(_translate("MDCx", "简介预览："))
```

- [ ] **Step 3: 调整 geometry 使预览区域可见**

需要增加 `scrollAreaWidgetContents_vsmeta` 的高度:
```python
# 将
self.scrollAreaWidgetContents_vsmeta.setGeometry(QtCore.QRect(0, 0, 796, 950))
# 改为
self.scrollAreaWidgetContents_vsmeta.setGeometry(QtCore.QRect(0, 0, 796, 1200))
```

同样调整 groupBox_vsmeta_config 的高度:
```python
# 将
self.groupBox_vsmeta_config.setGeometry(QtCore.QRect(30, 20, 701, 880))
# 改为
self.groupBox_vsmeta_config.setGeometry(QtCore.QRect(30, 20, 701, 1100))
```

- [ ] **Step 4: 提交**

```bash
git add mdcx/views/MDCx.py
git commit -m "feat(ui): add VSMeta preview labels for title, title2, and summary"
```

---

## 任务 5: 连接预览更新逻辑

**Files:**
- Modify: `mdcx/controllers/main_window/load_config.py` - 绑定预览更新信号
- Modify: `mdcx/controllers/main_window/save_config.py` - 实现预览更新方法

- [ ] **Step 1: 在 load_config.py 中添加预览更新绑定**

找到 Vsmeta 配置加载部分，在 `lineEdit_vsmeta_custom_summary` 初始化后添加:

```python
# 绑定自定义模板输入的 textChanged 信号以更新预览
self.Ui.lineEdit_vsmeta_custom_title.textChanged.connect(
    lambda: self._update_vsmeta_preview("title")
)
self.Ui.lineEdit_vsmeta_custom_title2.textChanged.connect(
    lambda: self._update_vsmeta_preview("title2")
)
self.Ui.plainTextEdit_vsmeta_custom_summary.textChanged.connect(
    lambda: self._update_vsmeta_preview("summary")
)
```

- [ ] **Step 2: 在 save_config.py 或 load_config.py 中添加预览更新方法**

在 MyMAinWindow 类中添加:

```python
def _update_vsmeta_preview(self, template_type: str) -> None:
    """更新 VSMeta 模板预览

    Args:
        template_type: 模板类型 ("title", "title2", "summary")
    """
    from mdcx.utils.vsmeta_template_helper import (
        PREVIEW_SAMPLE_DATA,
        render_template,
        validate_template_syntax,
    )

    if template_type == "title":
        template = self.Ui.lineEdit_vsmeta_custom_title.text()
        preview_label = self.Ui.label_vsmeta_title_preview
    elif template_type == "title2":
        template = self.Ui.lineEdit_vsmeta_custom_title2.text()
        preview_label = self.Ui.label_vsmeta_title2_preview
    else:
        template = self.Ui.plainTextEdit_vsmeta_custom_summary.toPlainText()
        preview_label = self.Ui.label_vsmeta_summary_preview

    # 验证语法
    is_valid, error_msg = validate_template_syntax(template)

    if not is_valid:
        preview_label.setStyleSheet("background-color: #ffcccc; padding: 5px;")
        preview_label.setText(f"语法错误: {error_msg}")
        return

    # 渲染预览
    preview_label.setStyleSheet("background-color: #f5f5f5; padding: 5px;")
    prefix_map = {
        "title": "标题预览：",
        "title2": "副标题预览：",
        "summary": "简介预览：",
    }
    preview_text = render_template(template, PREVIEW_SAMPLE_DATA)
    preview_label.setText(f"{prefix_map[template_type]}{preview_text}")
```

- [ ] **Step 3: 提交**

```bash
git add mdcx/controllers/main_window/load_config.py mdcx/controllers/main_window/save_config.py
git commit -m "feat(ui): connect VSMeta template preview update signals"
```

---

## 任务 6: 添加预设管理 UI

**Files:**
- Modify: `mdcx/views/MDCx.py` - setupUi 函数
- Modify: `mdcx/controllers/main_window/load_config.py` - 加载预设到下拉框
- Modify: `mdcx/controllers/main_window/save_config.py` - 保存预设逻辑

- [ ] **Step 1: 在 comboBox_vsmeta_show_title 添加后添加预设管理按钮**

在 `self.comboBox_vsmeta_show_title.addItems(...)` 后添加:

```python
        # 自定义预设管理
        self.pushButton_vsmeta_save_preset = QtWidgets.QPushButton(parent=self.gridLayoutWidget_vsmeta_config)
        self.pushButton_vsmeta_save_preset.setObjectName("pushButton_vsmeta_save_preset")
        self.gridLayout_vsmeta_config.addWidget(self.pushButton_vsmeta_save_preset, 7, 2, 1, 1)

        self.pushButton_vsmeta_delete_preset = QtWidgets.QPushButton(parent=self.gridLayoutWidget_vsmeta_config)
        self.pushButton_vsmeta_delete_preset.setObjectName("pushButton_vsmeta_delete_preset")
        self.gridLayout_vsmeta_config.addWidget(self.pushButton_vsmeta_delete_preset, 7, 3, 1, 1)
```

同样为 title2 和 summary 添加:

```python
        # 副标题预设管理
        self.pushButton_vsmeta_save_preset2 = QtWidgets.QPushButton(parent=self.gridLayoutWidget_vsmeta_config)
        self.pushButton_vsmeta_save_preset2.setObjectName("pushButton_vsmeta_save_preset2")
        self.gridLayout_vsmeta_config.addWidget(self.pushButton_vsmeta_save_preset2, 9, 2, 1, 1)

        self.pushButton_vsmeta_delete_preset2 = QtWidgets.QPushButton(parent=self.gridLayoutWidget_vsmeta_config)
        self.pushButton_vsmeta_delete_preset2.setObjectName("pushButton_vsmeta_delete_preset2")
        self.gridLayout_vsmeta_config.addWidget(self.pushButton_vsmeta_delete_preset2, 9, 3, 1, 1)

        # 简介预设管理
        self.pushButton_vsmeta_save_preset3 = QtWidgets.QPushButton(parent=self.gridLayoutWidget_vsmeta_config)
        self.pushButton_vsmeta_save_preset3.setObjectName("pushButton_vsmeta_save_preset3")
        self.gridLayout_vsmeta_config.addWidget(self.pushButton_vsmeta_save_preset3, 11, 2, 1, 1)

        self.pushButton_vsmeta_delete_preset3 = QtWidgets.QPushButton(parent=self.gridLayoutWidget_vsmeta_config)
        self.pushButton_vsmeta_delete_preset3.setObjectName("pushButton_vsmeta_delete_preset3")
        self.gridLayout_vsmeta_config.addWidget(self.pushButton_vsmeta_delete_preset3, 11, 3, 1, 1)
```

- [ ] **Step 2: 添加翻译字符串**

在 retranslateUi 中添加:

```python
        self.pushButton_vsmeta_save_preset.setText(_translate("MDCx", "保存预设"))
        self.pushButton_vsmeta_delete_preset.setText(_translate("MDCx", "删除预设"))
        self.pushButton_vsmeta_save_preset2.setText(_translate("MDCx", "保存预设"))
        self.pushButton_vsmeta_delete_preset2.setText(_translate("MDCx", "删除预设"))
        self.pushButton_vsmeta_save_preset3.setText(_translate("MDCx", "保存预设"))
        self.pushButton_vsmeta_delete_preset3.setText(_translate("MDCx", "删除预设"))
```

- [ ] **Step 3: 在 load_config.py 中添加预设加载逻辑**

在 Vsmeta 配置加载部分添加:

```python
        # 加载自定义预设到下拉框
        self._load_vsmeta_custom_presets()
```

添加方法:

```python
def _load_vsmeta_custom_presets(self) -> None:
    """加载自定义 VSMeta 预设到下拉框"""
    custom_presets = manager.config.custom_presets

    # 标题预设
    for preset in custom_presets:
        preset_name = f"[自定义] {preset.name}"
        if preset_name not in [self.Ui.comboBox_vsmeta_show_title.itemText(i)
                               for i in range(self.Ui.comboBox_vsmeta_show_title.count())]:
            self.Ui.comboBox_vsmeta_show_title.addItem(preset_name)
```

- [ ] **Step 4: 在 save_config.py 中添加预设保存和删除方法**

```python
def _save_vsmeta_preset(self, preset_type: str) -> None:
    """保存当前 VSMeta 配置为预设

    Args:
        preset_type: 预设类型 ("title", "title2", "summary")
    """
    from PyQt6.QtWidgets import QInputDialog
    from mdcx.config.models import VsmetaCustomPreset

    name, ok = QInputDialog.getText(self, "保存预设", "请输入预设名称:")
    if not ok or not name:
        return

    preset = VsmetaCustomPreset(
        name=name,
        show_title_type=self.Ui.comboBox_vsmeta_show_title.currentIndex(),
        show_title2_type=self.Ui.comboBox_vsmeta_show_title2.currentIndex(),
        summary_type=self.Ui.comboBox_vsmeta_summary.currentIndex(),
        custom_title=self.Ui.lineEdit_vsmeta_custom_title.text(),
        custom_title2=self.Ui.lineEdit_vsmeta_custom_title2.text(),
        custom_summary=self.Ui.plainTextEdit_vsmeta_custom_summary.toPlainText(),
    )

    # 检查是否已存在同名预设
    existing_names = [p.name for p in manager.config.custom_presets]
    if name in existing_names:
        # 更新现有预设
        idx = existing_names.index(name)
        manager.config.custom_presets[idx] = preset
    else:
        # 添加新预设
        manager.config.custom_presets.append(preset)

    manager.save()
    self._load_vsmeta_custom_presets()


def _delete_vsmeta_preset(self, preset_type: str) -> None:
    """删除选中的 VSMeta 自定义预设"""
    from PyQt6.QtWidgets import QMessageBox
    from mdcx.config.models import VsmetaCustomPreset

    current_text = self.Ui.comboBox_vsmeta_show_title.currentText()
    if not current_text.startswith("[自定义]"):
        QMessageBox.information(self, "提示", "请选择一个自定义预设")
        return

    preset_name = current_text[5:]  # 去掉 "[自定义] " 前缀

    reply = QMessageBox.question(
        self, "确认删除", f"确定要删除预设 \"{preset_name}\" 吗?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if reply != QMessageBox.StandardButton.Yes:
        return

    manager.config.custom_presets = [
        p for p in manager.config.custom_presets if p.name != preset_name
    ]
    manager.save()
    self._load_vsmeta_custom_presets()
```

- [ ] **Step 5: 绑定按钮信号**

在 load_config.py 中绑定:

```python
        self.Ui.pushButton_vsmeta_save_preset.clicked.connect(
            lambda: self._save_vsmeta_preset("title")
        )
        self.Ui.pushButton_vsmeta_delete_preset.clicked.connect(
            lambda: self._delete_vsmeta_preset("title")
        )
        self.Ui.pushButton_vsmeta_save_preset2.clicked.connect(
            lambda: self._save_vsmeta_preset("title2")
        )
        self.Ui.pushButton_vsmeta_delete_preset2.clicked.connect(
            lambda: self._delete_vsmeta_preset("title2")
        )
        self.Ui.pushButton_vsmeta_save_preset3.clicked.connect(
            lambda: self._save_vsmeta_preset("summary")
        )
        self.Ui.pushButton_vsmeta_delete_preset3.clicked.connect(
            lambda: self._delete_vsmeta_preset("summary")
        )
```

- [ ] **Step 6: 提交**

```bash
git add mdcx/views/MDCx.py mdcx/controllers/main_window/load_config.py mdcx/controllers/main_window/save_config.py
git commit -m "feat(ui): add VSMeta custom preset management buttons"
```

---

## 任务 7: 添加重置和导出功能

**Files:**
- Modify: `mdcx/views/MDCx.py` - setupUi 添加按钮
- Modify: `mdcx/controllers/main_window/save_config.py` - 实现重置和导出逻辑

- [ ] **Step 1: 在 VSMeta 配置页面底部添加重置和导出按钮**

在 `label_vsmeta_tips` 之后添加:

```python
        # 重置和导出按钮
        self.pushButton_vsmeta_reset = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents_vsmeta)
        self.pushButton_vsmeta_reset.setGeometry(QtCore.QRect(30, 940, 100, 30))
        self.pushButton_vsmeta_reset.setObjectName("pushButton_vsmeta_reset")

        self.pushButton_vsmeta_export = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents_vsmeta)
        self.pushButton_vsmeta_export.setGeometry(QtCore.QRect(140, 940, 100, 30))
        self.pushButton_vsmeta_export.setObjectName("pushButton_vsmeta_export")
```

- [ ] **Step 2: 添加翻译字符串**

```python
        self.pushButton_vsmeta_reset.setText(_translate("MDCx", "重置为默认"))
        self.pushButton_vsmeta_export.setText(_translate("MDCx", "导出配置"))
```

- [ ] **Step 3: 实现重置功能**

```python
def _reset_vsmeta_config(self) -> None:
    """重置所有 VSMeta 配置为默认值"""
    from PyQt6.QtWidgets import QMessageBox
    from mdcx.config.enums import VsmetaShowTitle, VsmetaShowTitle2, VsmetaSummary

    reply = QMessageBox.question(
        self, "确认重置", "确定要重置所有 VSMeta 配置为默认值吗?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if reply != QMessageBox.StandardButton.Yes:
        return

    # 重置为默认值
    self.Ui.checkBox_vsmeta_include_poster.setChecked(True)
    self.Ui.checkBox_vsmeta_include_backdrop.setChecked(True)
    self.Ui.checkBox_vsmeta_locked.setChecked(True)
    self.Ui.spinBox_vsmeta_image_dimension.setValue(1920)
    self.Ui.spinBox_vsmeta_jpeg_quality.setValue(90)
    self.Ui.spinBox_vsmeta_actor_limit.setValue(20)
    self.Ui.spinBox_vsmeta_tag_limit.setValue(10)
    self.Ui.comboBox_vsmeta_show_title.setCurrentIndex(0)
    self.Ui.comboBox_vsmeta_show_title2.setCurrentIndex(0)
    self.Ui.comboBox_vsmeta_summary.setCurrentIndex(0)
    self.Ui.lineEdit_vsmeta_custom_title.setText("{number} - {title} ({originaltitle})")
    self.Ui.lineEdit_vsmeta_custom_title2.setText("{publisher} / {studio}")
    self.Ui.plainTextEdit_vsmeta_custom_summary.setPlainText("{originaltitle}\n\n{outline}\n\n{originalplot}")

    QMessageBox.information(self, "完成", "VSMeta 配置已重置为默认值")
```

- [ ] **Step 4: 实现导出功能**

```python
def _export_vsmeta_config(self) -> None:
    """导出 VSMeta 配置到 JSON 文件"""
    import json
    from datetime import datetime
    from PyQt6.QtWidgets import QFileDialog

    file_path, _ = QFileDialog.getSaveFileName(
        self, "导出 VSMeta 配置", "vsmeta_config.json",
        "JSON Files (*.json)"
    )
    if not file_path:
        return

    config_data = {
        "version": 1,
        "exported_at": datetime.now().isoformat(),
        "vsmeta_include_poster": self.Ui.checkBox_vsmeta_include_poster.isChecked(),
        "vsmeta_include_backdrop": self.Ui.checkBox_vsmeta_include_backdrop.isChecked(),
        "vsmeta_locked": self.Ui.checkBox_vsmeta_locked.isChecked(),
        "vsmeta_image_max_dimension": self.Ui.spinBox_vsmeta_image_dimension.value(),
        "vsmeta_jpeg_quality": self.Ui.spinBox_vsmeta_jpeg_quality.value(),
        "vsmeta_actor_limit": self.Ui.spinBox_vsmeta_actor_limit.value(),
        "vsmeta_tag_limit": self.Ui.spinBox_vsmeta_tag_limit.value(),
        "vsmeta_show_title_type": self.Ui.comboBox_vsmeta_show_title.currentIndex(),
        "vsmeta_show_title2_type": self.Ui.comboBox_vsmeta_show_title2.currentIndex(),
        "vsmeta_summary_type": self.Ui.comboBox_vsmeta_summary.currentIndex(),
        "vsmeta_custom_title": self.Ui.lineEdit_vsmeta_custom_title.text(),
        "vsmeta_custom_title2": self.Ui.lineEdit_vsmeta_custom_title2.text(),
        "vsmeta_custom_summary": self.Ui.plainTextEdit_vsmeta_custom_summary.toPlainText(),
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    from PyQt6.QtWidgets import QMessageBox
    QMessageBox.information(self, "完成", f"VSMeta 配置已导出到:\n{file_path}")
```

- [ ] **Step 5: 绑定按钮信号**

```python
        self.Ui.pushButton_vsmeta_reset.clicked.connect(self._reset_vsmeta_config)
        self.Ui.pushButton_vsmeta_export.clicked.connect(self._export_vsmeta_config)
```

- [ ] **Step 6: 提交**

```bash
git add mdcx/views/MDCx.py mdcx/controllers/main_window/save_config.py
git commit -m "feat(ui): add VSMeta reset and export functionality"
```

---

## 任务 8: 添加预设选择功能

**Files:**
- Modify: `mdcx/controllers/main_window/load_config.py` - 添加预设选择处理

- [ ] **Step 1: 在 comboBox_vsmeta_show_title 的 currentIndexChanged 信号中处理自定义预设选择**

首先需要移除之前的简单 lambda，改为使用方法:

```python
def _on_vsmeta_show_title_changed(self, index: int) -> None:
    """处理标题预设选择变化"""
    from mdcx.config.models import VsmetaCustomPreset

    current_text = self.Ui.comboBox_vsmeta_show_title.currentText()
    if current_text.startswith("[自定义]"):
        preset_name = current_text[5:]
        for preset in manager.config.custom_presets:
            if preset.name == preset_name:
                self.Ui.comboBox_vsmeta_show_title.blockSignals(True)
                self.Ui.comboBox_vsmeta_show_title.setCurrentIndex(6)  # 自定义模板
                self.Ui.comboBox_vsmeta_show_title.blockSignals(False)
                self.Ui.lineEdit_vsmeta_custom_title.setText(preset.custom_title)
                break

# 绑定信号
self.Ui.comboBox_vsmeta_show_title.currentIndexChanged.connect(self._on_vsmeta_show_title_changed)
```

同样为 title2 和 summary 添加处理方法并绑定信号。

- [ ] **Step 2: 提交**

```bash
git add mdcx/controllers/main_window/load_config.py
git commit -m "feat(ui): handle custom preset selection in VSMeta combo boxes"
```

---

## 任务 9: 最终测试和调整

**Files:**
- Modify: 相关文件根据测试结果调整

- [ ] **Step 1: 运行所有测试**

Run: `pytest tests/ -v -k vsmeta --tb=short`

- [ ] **Step 2: 检查 UI 布局是否正确**

手动测试:
1. 打开设置页面 VSMeta tab
2. 切换不同预设查看预览是否更新
3. 输入错误的 {if:} 语法检查是否显示红色边框
4. 测试保存/删除预设功能
5. 测试重置功能
6. 测试导出功能

- [ ] **Step 3: 根据测试结果修复问题**

- [ ] **Step 4: 最终提交**

```bash
git add -A
git commit -m "feat: complete VSMeta UI optimization features"
```

---

## 实施检查清单

- [ ] 任务1: 语法验证函数和测试
- [ ] 任务2: 自定义预设数据结构
- [ ] 任务3: 帮助文档更新（默认值语法）
- [ ] 任务4: 预览区域 UI
- [ ] 任务5: 预览更新逻辑
- [ ] 任务6: 预设管理 UI 和逻辑
- [ ] 任务7: 重置和导出功能
- [ ] 任务8: 预设选择功能
- [ ] 任务9: 测试和调整
