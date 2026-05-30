## 220260555 (2026-05-30)

### 新功能和优化
- **VSMETA 设置界面优化**：
  - 添加功能分组：图片配置、元数据内容、其他选项
  - 为所有控件添加详细的工具提示
  - 添加预设按钮：推荐配置、高画质、最小文件
  - 添加重置默认值按钮
  - 调整布局高度，确保所有控件正常显示

- **UI 文件修复**：修复 gridLayoutWidget_vsmeta_config 高度不一致问题

---

## 220260554 (2026-05-30)

### 修复和新增
- **恢复 VSMETA 配置选项**：完整恢复了 VSMETA 配置界面
  - 重新添加 `comboBox_vsmeta_show_title` 控件，配置标题内容格式
  - 重新添加 `comboBox_vsmeta_show_title2` 控件，配置副标题内容格式
  - 重新添加 `comboBox_vsmeta_summary` 控件，配置简介内容格式
  - 恢复配置的加载和保存功能
  - 调整界面布局，确保所有控件正常显示

---

## 220260553 (2026-05-30)

### 修复
- **AttributeError 错误**：修复程序启动时出现的属性错误
  - 移除了对已删除 UI 控件 `comboBox_vsmeta_show_title` 的引用
  - 移除了对已删除 UI 控件 `comboBox_vsmeta_show_title2` 的引用
  - 移除了对已删除 UI 控件 `comboBox_vsmeta_summary` 的引用
  - 配置字段保留默认值功能，确保 VSMETA 功能正常工作

---

## 220260552 (2026-05-30)

### 修复
- **UI widget 生命周期问题**：修复导致 RuntimeError 的对象被删除问题
  - 修复了 scrollArea widget 被错误替换导致对象删除的问题
  - 修正了 groupBox_22 的 parent 关系，确保对象生命周期正确

---

## 220260551 (2026-05-30)

### 新功能
- **报告系统**：实现完整的刮削结果报告系统
  - 新增 `report_system.py` 模块，提供刮削跟踪和报告生成功能
  - 新增 `ScrapeTracker` 单例，用于跟踪刮削会话和记录
  - 新增 `ReportGenerator`，支持生成多种类型的报告
  - 支持的报告类型：刮削结果报告、刮削历史报告、资源统计报告、演员统计报告
  - 支持将报告导出到文件

- **性能监控UI扩展**：扩展性能监控对话框
  - 新增4个标签页：刮削结果、刮削历史、资源统计、演员统计
  - 添加「导出报告」功能，支持将当前标签页的报告保存到本地
  - 添加「重置刮削跟踪」功能，用于清空历史记录

- **性能监控系统**：实现完整的性能监控功能
  - 新增 `perf.py` 模块，提供性能监控功能
  - 新增 `PerformanceMonitor` 类，用于跟踪函数执行时间
  - 新增 `PerfRecord` 数据类，存储性能记录
  - 提供性能报告生成功能

- **爬虫健康监控**：实现爬虫健康监控功能
  - 新增 `crawler_health.py` 模块
  - 新增 `CrawlerHealthStats` 和 `CrawlerHealthMonitor` 类
  - 跟踪爬虫成功率、响应时间、失败原因等指标

### 改进
- **代码质量优化**：修复所有代码质量检查问题
  - 修复未使用的变量和导入
  - 统一导入排序格式
  - 移除不必要的文件打开模式参数

### 测试
- **完整测试覆盖**：为新功能添加全面的测试
  - 新增 `test_report_system.py`：14个测试用例
  - 新增 `test_perf.py`：15个测试用例
  - 新增 `test_crawler_health.py`：10个测试用例
  - 新增 `test_vsmeta.py`：VSMETA相关测试

---

## 220260550 (2026-05-28)

### 修复
- **VSMETA 标签字段修正**：严格遵循语义分离 TAG_SHOW_TITLE 和 TAG_SHOW_TITLE2
  - TAG_SHOW_TITLE：仅写入中文翻译标题（去除番号前缀和日文标题后缀）
  - TAG_SHOW_TITLE2：仅写入日文原始标题（去除 studio/publisher 回退逻辑）
  - TAG_CHAPTER_SUMMARY：组合为「日文原始标题 + 中文简介 + 日文简介」三段式

---

## 220260549 (2026-05-28)

### 文档更新
- 更新 README.md，添加对 nfo-vsmeta 项目的感谢
- 完善 VSMETA 文档，添加详细的标签说明和内容格式

### 改进
- 优化 VSMETA 简介格式：日文标题放在简介开头，支持中日/日中双语显示

---

## 220260546 (2026-05-26)

### 修复
- **VSMETA 图片处理完全修复**：参考 JuanWoo/nfo-to-vsmeta 项目实现正确的 VSMETA 格式
  - 图片添加索引字节（0x01）在 TAG_EPISODE_THUMB_DATA、TAG_EPISODE_THUMB_MD5 后
  - GROUP2（0x9A）和 GROUP3（0xAA）也添加索引字节（0x01）
  - 新增图片压缩功能，限制在 200KB 以内
  - 修正 MD5 计算方式：现在计算的是 Base64 字符串的 MD5，而非原始图片的
  - 完整解决 VSMETA 无法被 Synology Video Station 识别的问题

---

## 220260545 (2026-05-26)

### 修复
- **VSMETA 格式完整修复**：完全恢复 VSMETA 正确格式，确保与 Synology Video Station 100% 兼容
  - 完全恢复原始格式为 Base64 编码图片（76字符换行）
  - 移除之前错误添加的索引字节
  - 保留字符清理功能 `normalize_vsmeta_text`，清理控制字符和 HTML 转义实体
  - 解决翻译后内容包含特殊字符导致的 VSMETA 无法识别的问题

---

## 220260544 (2026-05-26)

### 修复
- **VSMETA 索引字节修复**：重新添加了被错误移除的索引字节，确保与 Synology Video Station 完全兼容
  - 重新添加 `TAG_EPISODE_THUMB_DATA` 和 `TAG_EPISODE_THUMB_MD5` 的索引字节 (0x01)
  - 重新添加 `TAG_GROUP2` 和 `TAG_GROUP3` 的索引字节 (0x01)
  - 保持字符清理功能和原始二进制图片编码功能
  - 完整修复翻译后 VSMETA 文件无法被识别的问题

---

## 220260543 (2026-05-26)

### 修复
- **VSMETA 字符清理和图片编码修复**：修复翻译后 VSMETA 文件无法被 Synology Video Station 识别的问题
  - 添加 `normalize_vsmeta_text()` 函数，清理字符串中的控制字符和 HTML 转义实体
  - 移除图片的 Base64 编码，改用原始二进制 JPEG 数据直接写入
  - 解决翻译内容包含特殊字符导致的解析错误

---

## 220260542 (2026-05-26)

### 改进
- **增强 OpenSSL 错误识别**：添加了特定 OpenSSL 底层错误的详细描述
  - "OPENSSL_internal:invalid library" → OpenSSL 库配置错误
  - "TLS 版本不匹配" → 请更新 curl_cffi 或更换代理
  - "证书验证失败" → 请检查系统时间或更新根证书
  - "连接被重置/拒绝" → 请检查网络或更换代理
  - 帮助用户快速定位 SSL/TLS 连接问题

---

## 220260541 (2026-05-26)

### 改进
- **添加详细的 curl 错误处理**：为网络请求添加了完整的 curl 错误码映射和友好的错误提示
  - 包含 100+ 个 curl 错误码的中文详细说明
  - 常见错误自动归类：SSL证书错误、DNS解析错误、连接错误等
  - 错误消息格式：`curl错误 [错误名称]: 简短描述 - 详细说明`
  - 帮助用户快速定位和解决网络问题

---

## 220260540 (2026-05-25)

### 改进
- **参考 NFO 优化 VSMETA**：完全参考 NFO 的处理方式来优化 VSMETA
  - 分级字段：根据国家决定是 "JP-18+" 还是 "NC-17"
  - 简介字段：保持同时显示翻译和原文，用分隔线标注
  - 与 NFO 的处理逻辑保持一致

---

## 220260535 (2026-05-25)

### 修复
- **VSMETA 图片显示修复**：将 Base64 换行从 LF 改为 CRLF
  - 将 `base64.encodebytes()` 替换为自定义的 `base64_with_crlf()` 函数
  - 符合 Synology Video Station 的图片格式要求

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
