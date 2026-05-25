## 220260536 (2026-05-25)

### 修复
- **VSMETA 翻译后字段识别修复**：修复了打开翻译功能后 VSMETA 文件无法被 Synology Video Station 正确识别的问题
  - 添加了字符清理函数 `normalize_vsmeta_text()` 来处理翻译后的特殊字符
  - 清理了可能破坏 protobuf 编码的控制字符
  - 规范化了换行符和 XML 实体
  - 在 `write_string_field()` 和 `write_indexed_string_field()` 中都使用了字符清理

---

## 220260535 (2026-05-25)

### 修复
- **VSMETA 图片显示修复**：修复图片在 Synology Video Station 中不显示的问题
  - 将 Base64 换行方式从 LF (`\n`) 改为 CRLF (`\r\n`)

---

## 220260534 (2026-05-24)

### 修复
- **VSMETA 格式修复**：移除了多余的索引字节，确保完全符合 Synology Video Station 标准格式
  - 移除 `TAG_GROUP2 (0x9A)` 和 `TAG_GROUP3 (0xAA)` 的 `index=0x01` 字节
  - 修复 `write_poster()` 方法，使用 `write_string_field` 替代 `write_indexed_string_field`
  - 移除海报相关字段的多余索引字节
  - 添加类型安全检查，验证 `md5_hex is None` 时的处理

---

## 220260533 (2026-05-24)

### 重大变更
- **VSMETA 编码器完全重写**：从自定义 TLV 格式迁移到 Synology Video Station 标准 protobuf 格式
  - 魔数头: `b"vsmeta"` → `0x08 0x01` (protobuf field 1, wire 0, value 1 = movie)
  - TAG 方案: 自编 0x01-0x0F → protobuf `(field << 3) | wire_type` 编码
  - 图片编码: 原始 JPEG 二进制 → Base64 (76字符换行) + MD5 校验
  - 评分编码: LEB128 整数 → 单字节 BE 整数 / -1 补码
  - 列表字段: 逗号拼接字符串 → protobuf repeated 字段
  - 嵌套结构: 新增 3 层 GROUP 子消息（GROUP1: cast/crew, GROUP2: series info, GROUP3: backdrop/timestamp）

### 新增
- TAG_YEAR (0x28): 独立年份字段
- TAG_SHOW_TITLE2 (0x1A): 副标题/排序标题 (原始标题 or 制作商)
- TAG_EPISODE_TITLE (0x22): 短标题 (番号)
- TAG_CLASSIFICATION (0x5A): 内容分级 (有码/无码)
- TAG_EPISODE_META_JSON (0x4A): 外部 ID 引用 JSON
- TAG_EPISODE_THUMB_MD5 (0x92): 封面图 MD5 校验
- TAG2_TVSHOW_SUMMARY (0x32): 系列名称
- TAG2_TVSHOW_META_JSON (0x4A): 系列元数据 JSON
- TAG2_POSTER_DATA / TAG2_POSTER_MD5: GROUP2 内嵌封面图
- TAG3_TIMESTAMP (0x18): Unix 时间戳
- VSMetaEncoder: 新增 `write_varint_field` / `write_bytes_field` / `write_string_field` / `write_submessage` 方法
- `leb128.py`: 新增 `encode_varint` 别名

### 移除
- 不存在的字段: TAGLINE (0x04), RUNTIME (0x06), COLLECTION (0x0D), STUDIO (0x0E), VERSION (0x14)
- 内容已迁移到标准 protobuf 字段中

### 兼容性
- `write_vsmeta()` 函数签名完全不变
- `should_update_vsmeta()` 不变
- 所有 config 字段含义不变
- scraper.py 调用方无需修改

---


### 新增
- VSMETA 设置标签页：嵌入封面图/背景图开关、锁定元数据、图片尺寸/质量、数量限制
- VSMETA 保留旧文件勾选框（设置→下载→保留旧文件）
- VSMetaEncoder: 新增 `reset()` 方法支持实例复用
- VSMetaEncoder: 写方法增加 `label` 参数，自动追踪已写入标签

### 优化
- `parse_release_date`: 支持非零填充日期 (2020-5-1, 2020/05/15)
- `parse_score`: 支持中文后缀 (8.5分, ⭐8.5, 评分 8.5)
- `parse_runtime`: 支持中文小时/分钟 (1小时30分钟, 1时30分)
- `write_vsmeta`: 改为 tmp + rename 原子写入，防止写入失败丢失旧文件
- 提取 `get_vsmeta_path()` 消除 scraper.py 中路径构建重复
- `delete_file_async` 内联导入移至模块顶层

### 修复
- 修复 `should_update_vsmeta` 中 `KeepableFile.VSMETA` 通过 UI 无法设置的死代码问题

## 220260531 (2026-05-24)

### 修复
- 修复命名页面 groupBox_vsmeta 与 groupBox_65 布局重叠 131px 的问题
- 同步 MDCx.py 中 10 个组件的 setGeometry 坐标与 MDCx.ui 一致
- 调整命名页面滚动区域高度 3660→3930，确保所有内容可见

## 220260530 (2026-05-24)

### 修复
- 修复命名标签页（tab_3）的布局重叠问题
- 调整 VSMETA 命名规则位置，不再与其他组件重叠
- 更新滚动区域高度，确保所有内容可见

### 改进
- 添加核心模块 API 文档
- 添加架构设计文档
- 更新项目 README，包含完整的特性列表和文档链接
- 添加测试辅助工具和核心模块测试

### 新增
- 添加 CI/CD 工作流配置
- 添加完整的 API 文档
- 添加架构设计文档
- 添加核心模块单元测试
- 添加测试覆盖率报告

## 220260527 (2026-05-23)

### 修复
- 修复 save_config.py 第 375 行 IndentationError 错误
- 确保代码缩进正确，符合 Python 语法规范

## 220260526 (2026-05-23)

### 修复
- 重新编译 UI 文件，修复 AttributeError: 'Ui_MDCx' object has no attribute 'checkBox_download_vsmeta' 错误
- 确保所有 VSMETA 相关 UI 控件正确绑定

## 220260525 (2026-05-22)

### 新增
- 修复 PyInstaller 打包配置，确保所有模块正确包含在安装包中

### 修复
- 修复安装包运行时 ModuleNotFoundError 错误
