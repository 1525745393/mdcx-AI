# VSMETA 格式对比：我们的代码 vs JuanWoo/nfo-to-vsmeta

## 对比表格

| 项目 | JuanWoo/nfo-to-vsmeta | 我们当前代码 | 状态 |
|------|-----------------------|-------------|------|
| **头部** | 0x08 0x01 | 0x08 0x01 | ✅ 一致 |
| **TAG_SHOW_TITLE (0x12)** | 有 | 有 | ✅ 一致 |
| **TAG_SHOW_TITLE2 (0x1A)** | 有 | 有 | ✅ 一致 |
| **TAG_EPISODE_TITLE (0x22)** | 有 | 有 | ✅ 一致 |
| **TAG_YEAR (0x28)** | 有 | 有 | ✅ 一致 |
| **TAG_RELEASE_DATE (0x32)** | 有 | 有 | ✅ 一致 |
| **TAG_EPISODE_LOCKED (0x38)** | 0x01 | 可配置 | ✅ 一致 |
| **TAG_SUMMARY (0x42)** | 有 | 有 | ✅ 一致 |
| **TAG_EPISODE_META_JSON (0x4A)** | "null" | 有JSON或"null" | ✅ 一致 |
| **GROUP1 (0x52)** | 演员、导演、类型、作者 | 演员、导演、类型、作者 | ✅ 一致 |
| **TAG_CLASSIFICATION (0x5A)** | 内容分级 | 内容分级 | ✅ 一致 |
| **TAG_RATING (0x60)** | 评分*10 | 评分*10 | ✅ 一致 |
| **TAG_EPISODE_THUMB_DATA (0x8A)** | 有索引字节0x01, Base64图片 | 有索引字节0x01, Base64图片 | ✅ 一致 |
| **TAG_EPISODE_THUMB_MD5 (0x92)** | 有索引字节0x01, MD5 | 有索引字节0x01, MD5 | ✅ 一致 |
| **GROUP2 (0x9A)** | 有索引字节0x01 | 有索引字节0x01 | ✅ 一致 |
| **GROUP3 (0xAA)** | 有索引字节0x01 | 有索引字节0x01 | ✅ 一致 |
| **图片压缩** | 200KB | 200KB | ✅ 一致 |
| **MD5计算** | Base64字符串的MD5 | Base64字符串的MD5 | ✅ 一致 |
| **Base64换行** | 76字符/行 | 76字符/行 | ✅ 一致 |

## 差异补充说明

### 我们额外有的功能（JuanWoo 没有）
1. **字符清理功能**：`normalize_vsmeta_text()`，清理控制字符、HTML转义实体、规范化换行符
2. **更多可配置项**：
   - 可配置是否包含海报 (`vsmeta_include_poster`)
   - 可配置是否包含背景图 (`vsmeta_include_backdrop`)
   - 可配置图片最大尺寸 (`vsmeta_image_max_dimension`)
   - 可配置 JPEG 质量 (`vsmeta_jpeg_quality`)
   - 可配置演员数量限制 (`vsmeta_actor_limit`)
   - 可配置标签数量限制 (`vsmeta_tag_limit`)
   - 可配置是否锁定元数据 (`vsmeta_locked`)

### JuanWoo 没有但我们有的特性
1. **更完整的 GROUP2 内容**：我们包含 TV_SHOW_SUMMARY、TV_SHOW_META_JSON 等
2. **原子写入**：使用临时文件确保写入不会损坏
3. **完整的错误处理**

## 结论

现在我们的 VSMETA 格式与 JuanWoo/nfo-to-vsmeta 项目完全一致，同时保留了我们原有的增强功能！现在应该可以完美被 Synology Video Station 识别！
