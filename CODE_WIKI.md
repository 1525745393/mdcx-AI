# MDCx Code Wiki

## 目录

1. [项目概述](#项目概述)
2. [项目架构](#项目架构)
3. [核心模块](#核心模块)
4. [数据模型](#数据模型)
5. [配置系统](#配置系统)
6. [爬虫系统](#爬虫系统)
7. [VSMETA 生成](#vsmeta-生成)
8. [工具类与辅助函数](#工具类与辅助函数)
9. [项目运行方式](#项目运行方式)
10. [依赖关系](#依赖关系)

---

## 项目概述

### 项目简介

MDCx 是一个影视元数据抓取和整理工具，主要用于从多个成人视频网站获取元数据信息，包括标题、简介、演员、标签、封面图等，并支持与 Emby 等媒体服务器集成。

### 历史沿革

- 上游项目：yoshiko2/Movie_Data_Capture（已闭源）
- 后续分支：moyy996/AVDC（已停止维护）
- 基于：sqzw-x/mdcx
- 当前：Hazard804/mdcx

### 核心功能

1. 支持多个数据源网站抓取
2. 多线程并发处理
3. 元数据翻译（支持多种翻译服务）
4. 文件整理和重命名
5. 图片下载和水印添加
6. NFO 生成
7. Emby/Jellyfin 集成
8. 软链接创建
9. 多语言支持

---

## 项目架构

### 目录结构

```
/workspace/
├── main.py                 # 程序入口
├── mdcx/                   # 主源码目录
│   ├── base/               # 基础功能模块
│   ├── cmd/                # 命令行工具
│   ├── config/             # 配置管理
│   ├── controllers/        # 控制器（业务逻辑）
│   ├── core/               # 核心功能
│   ├── crawlers/           # 爬虫实现
│   ├── gen/                # 自动生成的枚举
│   ├── models/             # 数据模型
│   ├── tools/              # 工具模块
│   ├── utils/              # 工具函数
│   ├── views/              # UI 视图
│   ├── consts.py           # 常量定义
│   ├── crawler.py          # 爬虫提供者
│   ├── number.py           # 番号识别
│   ├── signals.py          # 信号系统
│   └── web_async.py        # 异步 web 请求
├── resources/              # 资源文件
│   ├── Img/                # 图片资源
│   ├── config/             # 默认配置
│   ├── fonts/              # 字体文件
│   └── mapping_table/      # 映射表
├── tests/                  # 测试代码
├── scripts/                # 脚本工具
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

### 架构分层

1. **表现层（Views）**：PyQt6 图形界面
2. **控制层（Controllers）**：业务逻辑和事件处理
3. **核心层（Core）**：刮削、文件处理、NFO 生成等
4. **数据层（Models）**：数据模型定义
5. **基础设施层**：爬虫、配置、网络请求等

### 主要模块依赖关系

```
main.py
  └─> controllers/main_window/
        └─> core/scraper.py
              └─> crawler.py
                    └─> crawlers/
              ├─> core/file_crawler.py
              ├─> core/nfo.py
              ├─> core/media_resource.py
              └─> config/manager.py
```

---

## 核心模块

### 1. 入口模块 ([main.py](file:///workspace/main.py))

**功能**：程序启动入口，初始化 GUI 应用

**主要类/函数**：
- `show_constants()`：显示运行时常量
- 主程序入口：初始化 PyQt6 应用，加载配置，显示主窗口

### 2. 常量定义 ([mdcx/consts.py](file:///workspace/mdcx/consts.py))

**功能**：定义项目常量

**主要常量**：
- `LOCAL_VERSION`：本地版本号
- `GITHUB_REPO`：GitHub 仓库地址
- `GITHUB_RELEASES_URL`：发布页地址
- `IS_WINDOWS`、`IS_MAC`、`IS_DOCKER`：平台判断
- `MAIN_PATH`：主路径
- `MARK_FILE`：配置标记文件

### 3. 信号系统 ([mdcx/signals.py](file:///workspace/mdcx/signals.py))

**功能**：PyQt6 信号定义，用于组件间通信

### 4. 爬虫提供者 ([mdcx/crawler.py](file:///workspace/mdcx/crawler.py))

**功能**：管理和提供爬虫实例

**主要类**：
- `CrawlerProvider`：爬虫提供者，管理爬虫实例生命周期

---

## 数据模型

### 文件信息模型 ([mdcx/models/types.py](file:///workspace/mdcx/models/types.py))

#### `FileInfo`
媒体文件基础信息

**主要字段**：
- `number`：番号
- `mosaic`：马赛克类型
- `file_path`：文件路径
- `has_sub`：是否有字幕
- `definition`：分辨率
- `codec`：编码格式

**主要方法**：
- `crawler_input()`：转换为爬虫输入
- `crawl_task()`：转换为刮削任务

#### `CrawlerInput`
单个爬虫调用输入

#### `CrawlTask`
单个文件刮削任务

#### `BaseCrawlerResult`
爬虫结果基础类型

**主要字段**：
- `number`、`title`、`outline`、`actors`、`tags` 等元数据
- `poster`、`thumb`、`trailer` 等资源 URL

#### `CrawlerResult`
单一网站爬虫结果

#### `CrawlersResult`
整合所有网站的结果

#### `OtherInfo`
其他处理信息（文件移动、水印等）

---

## 配置系统

### 配置模型 ([mdcx/config/models.py](file:///workspace/mdcx/config/models.py))

#### `Config`
主配置类，基于 Pydantic

**主要配置区域**：

1. **General Settings（通用设置）**
   - `media_path`：媒体路径
   - `success_output_folder`：成功输出目录
   - `media_type`：媒体文件类型
   - `sub_type`：字幕文件类型

2. **Cleaning Settings（清理设置）**
   - `folders`：排除目录
   - `string`：需要从文件名删除的字符串
   - `clean_enable`：启用的清理规则

3. **Scraping Settings（刮削设置）**
   - `thread_number`：并发数
   - `download_files`：下载文件类型
   - `website_youma`：有码网站源
   - `website_wuma`：无码网站源
   - `website_fc2`：FC2 网站源
   - 等等...

4. **字段配置**
   - `field_configs`：各字段的网站优先级、语言、翻译开关

5. **Naming and Formatting（命名和格式化）**
   - `folder_name`：目录名模板
   - `naming_file`：文件名模板
   - `nfo_include_new`：NFO 包含内容

6. **Server Settings（服务器设置）**
   - `server_type`：服务器类型（emby/jellyfin）
   - `emby_url`：Emby 地址
   - `api_key`：API 密钥

7. **Watermark Settings（水印设置）**
   - `poster_mark`、`thumb_mark`、`fanart_mark`：水印开关
   - `mark_type`：水印类型
   - `mark_size`：水印大小

8. **Network Settings（网络设置）**
   - `use_proxy`：代理开关
   - `proxy`：代理地址
   - `timeout`：超时时间
   - `retry`：重试次数

9. **Translation Settings（翻译设置）**
   - `translate_config`：翻译配置（TranslateConfig）

#### `TranslateConfig`
翻译服务配置

**主要字段**：
- `translate_by`：翻译服务列表
- `baidu_appid`、`baidu_key`：百度翻译配置
- `deepl_key`：DeepL 配置
- `llm_url`、`llm_model`、`llm_key`：LLM 翻译配置

### 配置枚举 ([mdcx/config/enums.py](file:///workspace/mdcx/config/enums.py))

#### `Website`
支持的网站枚举

**主要网站**：
- DMM、MGSTAGE、PRESTIGE、OFFICIAL（官方）
- JAVBUS、JAV321、JAVDB、JAVDBAPI
- MISSAV、AVSOX、MMTV、MYWIFE
- FC2、FC2HUB、FC2CLUB、FC2PPVDB
- THEPORNDB（欧美）
- HDOUBAN、CNMDB、GUOCHAN、MADOUQU（国产）
- 等等...

#### `FixedScrapingType`
刮削类型枚举

**类型**：
- `AUTO`：自动
- `YOUMA`：有码
- `WUMA`：无码
- `SUREN`：素人
- `FC2`：FC2
- `OUMEI`：欧美
- `GUOCHAN`：国产

#### 其他枚举
- `DownloadableFile`：可下载文件类型
- `Language`：语言
- `Translator`：翻译服务
- 等等...

### 配置管理器 ([mdcx/config/manager.py](file:///workspace/mdcx/config/manager.py))

管理配置的加载、保存、迁移等

---

## 爬虫系统

### 爬虫基类 ([mdcx/crawlers/base/base.py](file:///workspace/mdcx/crawlers/base/base.py))

#### `GenericBaseCrawler[T]`
爬虫抽象基类

**主要方法**：
- `run(input)`：执行爬虫
- `_generate_search_url(ctx)`：生成搜索 URL（抽象）
- `_parse_search_page(ctx, html, search_url)`：解析搜索页（抽象）
- `_parse_detail_page(ctx, html, detail_url)`：解析详情页（抽象）
- `post_process(ctx, res)`：后处理

**生命周期**：
1. 生成搜索 URL
2. 请求搜索页
3. 解析搜索页，获取详情页 URL
4. 请求详情页
5. 解析详情页，获取数据
6. 后处理

#### `BaseCrawler`
基础爬虫实现（使用默认 Context）

### 爬虫注册与获取

**主要函数**：
- `register_crawler(crawler_cls)`：注册爬虫
- `get_crawler(site)`：获取网站爬虫

### 爬虫实现目录 ([mdcx/crawlers/](file:///workspace/mdcx/crawlers/))

每个网站一个爬虫文件，例如：
- `dmm_new/`：DMM 爬虫
- `javbus.py`：JavBus 爬虫
- `missav.py`：MissAV 爬虫
- 等等...

### 爬虫提供者 ([mdcx/crawler.py](file:///workspace/mdcx/crawler.py))

#### `CrawlerProvider`
管理爬虫实例，提供获取和关闭功能

**主要方法**：
- `get(site)`：获取爬虫实例（懒加载）
- `close()`：关闭所有爬虫

### 核心刮削器 ([mdcx/core/scraper.py](file:///workspace/mdcx/core/scraper.py))

#### `Scraper`
主刮削器类

**主要方法**：
- `run(file_mode, movie_list)`：执行刮削
- `process_one_file(task)`：处理单个文件
- `_process_one_file(file_info, file_mode)`：内部处理

**刮削流程**：
1. 获取文件信息
2. 调用爬虫获取数据
3. 翻译元数据
4. 下载图片和预告片
5. 添加水印
6. 生成 NFO
7. 移动和重命名文件
8. 创建软链接（可选）

### 文件刮削器 ([mdcx/core/file_crawler.py](file:///workspace/mdcx/core/file_crawler.py))

#### `FileScraper`
处理单个文件的刮削逻辑

**主要功能**：
- 识别番号和刮削类型
- 调用多个网站爬虫
- 整合各网站结果
- 字段优先级处理

---

## VSMETA 生成

### 概述

VSMETA 是 **Synology Video Station** 使用的二进制元数据格式，用于在群晖 NAS 上为视频文件提供元数据（如标题、演员、海报、评分等）。MDCx 完整实现了该格式，确保与 Synology Video Station 完全兼容。

### 核心文件

- **[mdcx/core/vsmeta.py](file:///workspace/mdcx/core/vsmeta.py)**：VSMETA 编码器核心实现

### 格式规范

VSMETA 采用 **Protobuf 风格**的二进制编码：

| 特性 | 说明 |
|------|------|
| **头部标识** | `0x08 0x01`（field 1, wire 0, value 1 = movie） |
| **标签编码** | `(field_number << 3) | wire_type` |
| **Wire Type 0** | Varint 整数 |
| **Wire Type 2** | Length-delimited（字符串、字节数组、子消息） |
| **图片格式** | Base64 编码的 JPEG，最大 200KB |
| **Base64 换行** | 每 76 字符换行 |
| **MD5 校验** | 基于 Base64 字符串计算 |

### 主要标签详解

#### 顶层标签

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 | 示例内容 |
|--------|----------|-------|------|----------|------|----------|
| `TAG_SHOW_TITLE` | 0x12 | 2 | 2 | string | 显示标题 | `[ABP-123] 作品标题` |
| `TAG_SHOW_TITLE2` | 0x1A | 3 | 2 | string | 排序/备用标题 | `Original Title` |
| `TAG_EPISODE_TITLE` | 0x22 | 4 | 2 | string | 简短标题（番号） | `ABP-123` |
| `TAG_YEAR` | 0x28 | 5 | 0 | varint | 年份 | `2024` |
| `TAG_EPISODE_RELEASE_DATE` | 0x32 | 6 | 2 | string | 发布日期 | `2024-01-15` |
| `TAG_EPISODE_LOCKED` | 0x38 | 7 | 0 | varint | 锁定元数据 | `1`（锁定） |
| `TAG_CHAPTER_SUMMARY` | 0x42 | 8 | 2 | string | 简介/剧情 | 日文标题+中日简介 |
| `TAG_EPISODE_META_JSON` | 0x4A | 9 | 2 | string | 外部 ID JSON | `{"external_ids": {...}}` |
| `TAG_GROUP1` | 0x52 | 10 | 2 | submessage | 演员、导演、类型 | 嵌套结构 |
| `TAG_CLASSIFICATION` | 0x5A | 11 | 2 | string | 内容分级 | `有码` / `无码` |
| `TAG_RATING` | 0x60 | 12 | 0 | special | 评分（×10） | `85`（表示 8.5 分） |
| `TAG_EPISODE_THUMB_DATA` | 0x8A | 17 | 2 | string | 海报数据（含索引） | Base64 图片 |
| `TAG_EPISODE_THUMB_MD5` | 0x92 | 18 | 2 | string | 海报 MD5（含索引） | MD5 十六进制 |
| `TAG_GROUP2` | 0x9A | 19 | 2 | submessage | 剧集信息+海报 | 嵌套结构 |
| `TAG_GROUP3` | 0xAA | 21 | 2 | submessage | 背景图+时间戳 | 嵌套结构 |

#### GROUP1 内部标签（演员/导演/类型）

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 |
|--------|----------|-------|------|----------|------|
| `TAG1_CAST` | 0x0A | 1 | 2 | string (repeated) | 演员列表 |
| `TAG1_DIRECTOR` | 0x12 | 2 | 2 | string (repeated) | 导演列表 |
| `TAG1_GENRE` | 0x1A | 3 | 2 | string (repeated) | 类型/标签列表 |
| `TAG1_WRITER` | 0x22 | 4 | 2 | string (repeated) | 编剧列表（保留） |

#### GROUP2 内部标签（剧集信息）

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 |
|--------|----------|-------|------|----------|------|
| `TAG2_SEASON` | 0x08 | 1 | 0 | varint | 季数（电影为 0） |
| `TAG2_EPISODE` | 0x10 | 2 | 0 | varint | 集数（电影为 0） |
| `TAG2_TV_SHOW_YEAR` | 0x18 | 3 | 0 | varint | 电视剧年份 |
| `TAG2_RELEASE_DATE_TV_SHOW` | 0x22 | 4 | 2 | string | 电视剧发布日期 |
| `TAG2_LOCKED` | 0x28 | 5 | 0 | varint | 锁定电视剧元数据 |
| `TAG2_TVSHOW_SUMMARY` | 0x32 | 6 | 2 | string | 系列名称 |
| `TAG2_POSTER_DATA` | 0x3A | 7 | 2 | string | 海报 Base64 数据 |
| `TAG2_POSTER_MD5` | 0x42 | 8 | 2 | string | 海报 MD5 |
| `TAG2_TVSHOW_META_JSON` | 0x4A | 9 | 2 | string | 电视剧元数据 JSON |

#### GROUP3 内部标签（背景图）

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 |
|--------|----------|-------|------|----------|------|
| `TAG3_BACKDROP_DATA` | 0x0A | 1 | 2 | string | 背景图 Base64 数据 |
| `TAG3_BACKDROP_MD5` | 0x12 | 2 | 2 | string | 背景图 MD5 |
| `TAG3_TIMESTAMP` | 0x18 | 3 | 0 | varint | Unix 时间戳 |

### 核心类：VSMetaEncoder

**主要方法**：

| 方法 | 功能 | 示例 |
|------|------|------|
| `write_header()` | 写入文件头部 `0x08 0x01` | - |
| `write_string_field(tag, value)` | 写入字符串字段 | `write_string_field(0x12, "标题")` |
| `write_varint_field(tag, value)` | 写入 Varint 整数字段 | `write_varint_field(0x28, 2024)` |
| `write_bytes_field(tag, data)` | 写入字节字段 | `write_bytes_field(0x8A, b"...")` |
| `write_indexed_string_field(tag, index, value)` | 写入带索引的字符串（用于海报等） | `write_indexed_string_field(0x8A, 0x01, base64_data)` |
| `write_poster(image_path)` | 写入海报图片（自动处理 Base64 和 MD5） | `write_poster(Path("poster.jpg"))` |
| `write_submessage(tag, build_func, index)` | 写入嵌套子消息 | `write_submessage(0x52, build_group1)` |
| `normalize_vsmeta_text(text)` | 清理文本中的控制字符和 HTML 实体 | - |
| `get_bytes()` | 获取最终的 VSMETA 字节数据 | - |

### 简介格式详解

VSMETA 的简介字段（`TAG_CHAPTER_SUMMARY`）格式如下：

```
日文标题（originaltitle）

简介内容（根据 outline_show 配置显示）
  - SHOW_ZH_JP：中文简介 + 日文简介
  - SHOW_JP_ZH：日文简介 + 中文简介
```

**实际示例**（SHOW_ZH_JP 模式）：
```
美しい花

この作品は美しい花に関する物語です。

This is a story about beautiful flowers.
```

### 配置选项

在 `Config` 类中提供了丰富的 VSMETA 配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `vsmeta_include_poster` | bool | `True` | 是否在 VSMETA 中嵌入封面图 |
| `vsmeta_include_backdrop` | bool | `True` | 是否在 VSMETA 中嵌入背景图 |
| `vsmeta_locked` | bool | `True` | 是否锁定元数据（禁止 Video Station 自动更新） |
| `vsmeta_image_max_dimension` | int | `1920` | 图片最大尺寸（像素） |
| `vsmeta_jpeg_quality` | int | `90` | JPEG 质量（1-100） |
| `vsmeta_actor_limit` | int | `20` | 演员数量上限 |
| `vsmeta_tag_limit` | int | `10` | 标签数量上限 |
| `vsmeta_keep_ext` | bool | `False` | 生成的 VSMETA 文件是否保留视频扩展名 |

### 关键特性

1. **格式兼容性**：与 JuanWoo/nfo-to-vsmeta 项目完全一致，确保被 Synology Video Station 识别
2. **字符清理**：自动清理控制字符和 HTML 转义实体（`normalize_vsmeta_text`）
3. **图片压缩**：自动将图片压缩至 200KB 以内
4. **原子写入**：使用临时文件 → 重命名的方式确保写入不会损坏
5. **完整错误处理**：完善的异常处理和日志记录
6. **高度可配置**：多项配置选项满足不同需求

### 格式对比

参考文档：[VSMETA_COMPARISON.md](file:///workspace/VSMETA_COMPARISON.md)

### 实际生成的 VSMETA 结构示例

```
0x08 0x01                              # HEADER_MOVIE (field 1, value 1)
0x12 len(title) [title bytes]           # TAG_SHOW_TITLE
0x1A len(title2) [title2 bytes]         # TAG_SHOW_TITLE2  
0x22 len(number) [number bytes]         # TAG_EPISODE_TITLE
0x28 [year varint]                      # TAG_YEAR
0x32 len(date) [date bytes]             # TAG_EPISODE_RELEASE_DATE
0x38 0x01                              # TAG_EPISODE_LOCKED (locked)
0x42 len(summary) [summary bytes]       # TAG_CHAPTER_SUMMARY
0x4A len(json) [json bytes]             # TAG_EPISODE_META_JSON
0x52 len(group1) [group1 bytes]         # TAG_GROUP1 (cast/director/genre)
0x5A len(classification) [...]          # TAG_CLASSIFICATION
0x60 [rating byte]                      # TAG_RATING
0x8A 0x01 len(data) [base64 data]       # TAG_EPISODE_THUMB_DATA (with index)
0x92 0x01 len(md5) [md5 bytes]          # TAG_EPISODE_THUMB_MD5 (with index)
0x9A 0x01 len(group2) [group2 bytes]   # TAG_GROUP2 (with index)
0xAA 0x01 len(group3) [group3 bytes]   # TAG_GROUP3 (with index)
```

---

## 工具类与辅助函数

### 工具函数 ([mdcx/utils/__init__.py](file:///workspace/mdcx/utils/__init__.py))

#### `AsyncBackgroundExecutor`
异步后台任务执行器

**主要方法**：
- `submit(coro)`：提交协程
- `run(coro)`：阻塞运行协程
- `wait_all(timeout)`：等待所有任务完成
- `cancel()`：取消所有任务

**其他工具函数**：
- `get_current_time()`：获取当前时间
- `get_used_time(start_time)`：计算耗时
- `add_html(text)`：添加 HTML 链接
- `get_random_headers()`：生成随机 HTTP 头
- `singleton(cls)`：单例装饰器
- 等等...

### 文件工具 ([mdcx/utils/file.py](file:///workspace/mdcx/utils/file.py))

文件相关工具函数

### 路径工具 ([mdcx/utils/path.py](file:///workspace/mdcx/utils/path.py))

路径相关工具函数

### 视频工具 ([mdcx/utils/video.py](file:///workspace/mdcx/utils/video.py))

视频相关工具函数

---

## 控制器层

### 主窗口控制器 ([mdcx/controllers/main_window/](file:///workspace/mdcx/controllers/main_window/))

#### `MyMAinWindow`
主窗口控制器（[main_window.py](file:///workspace/mdcx/controllers/main_window/main_window.py)）

**主要功能**：
- 初始化 UI
- 绑定事件处理
- 管理配置加载和保存
- 处理刮削任务

---

## 核心功能模块

### NFO 生成 ([mdcx/core/nfo.py](file:///workspace/mdcx/core/nfo.py))

生成符合 Kodi/Emby 规范的 NFO 文件

### 媒体资源处理 ([mdcx/core/media_resource.py](file:///workspace/mdcx/core/media_resource.py))

处理图片、预告片等媒体资源下载

### 翻译功能 ([mdcx/core/translate.py](file:///workspace/mdcx/core/translate.py))

支持多种翻译服务：
- Google
- Baidu
- DeepL
- DeepLX
- LLM（大语言模型）

### 图片处理 ([mdcx/core/image.py](file:///workspace/mdcx/core/image.py))

图片下载、水印添加等

### 命名模板 ([mdcx/core/naming/](file:///workspace/mdcx/core/naming/))

文件和目录命名模板系统

---

## 项目运行方式

### 开发模式

1. **安装依赖**
   ```bash
   pip install -e .
   # 或使用 uv
   uv sync
   ```

2. **运行程序**
   ```bash
   python main.py
   ```

### 打包发布

使用 `scripts/build.py` 进行打包

### 命令行工具

项目提供了命令行工具：

1. **crawl**：命令行刮削
   ```bash
   python -m mdcx.cmd.crawl
   ```

2. **gen_enums**：生成枚举
   ```bash
   python -m mdcx.cmd.gen_enums
   ```

### 测试

运行测试：
```bash
pytest tests/
```

---

## 依赖关系

### 主要依赖 ([pyproject.toml](file:///workspace/pyproject.toml))

| 依赖 | 用途 |
|------|------|
| Python | >= 3.13.4 |
| PyQt6 | GUI 框架 |
| httpx | 异步 HTTP 请求 |
| curl-cffi | HTTP 请求（支持 Cloudflare） |
| beautifulsoup4 | HTML 解析 |
| parsel | 选择器解析 |
| lxml | XML/HTML 解析 |
| pillow | 图片处理 |
| opencv-contrib-python-headless | 图片处理 |
| av | 视频处理 |
| pydantic-settings | 配置管理 |
| openai | LLM 翻译 |
| zhconv | 中文简繁转换 |
| aiofiles | 异步文件操作 |
| aiolimiter | 异步限流 |
| oshash | OpenSubtitles 哈希 |
| jinja2 | 模板引擎 |
| ping3 | 网络检查 |

### 开发依赖

- pytest
- pytest-asyncio
- pytest-cov
- pyinstaller
- ruff
- rich
- typer

---

## 关键类关系图

```
Scraper (core/scraper.py)
  │
  ├─> CrawlerProvider (crawler.py)
  │     │
  │     └─> GenericBaseCrawler (crawlers/base/base.py)
  │           ├─> DMMNewCrawler
  │           ├─> JavBusCrawler
  │           ├─> MissAVCrawler
  │           └─> ...
  │
  ├─> FileScraper (core/file_crawler.py)
  │
  ├─> MediaResourceContext (core/media_resource.py)
  │
  └─> write_nfo (core/nfo.py)


Config (config/models.py)
  │
  ├─> TranslateConfig
  ├─> SiteConfig
  └─> FieldConfig


数据流程：
FileInfo ──> CrawlTask ──> [Crawlers] ──> CrawlersResult ──> (translation) ──> NFO / Files
```

---

## 开发注意事项

1. **异步编程**：项目大量使用 asyncio，注意协程安全
2. **配置迁移**：配置版本管理，支持旧配置迁移
3. **平台兼容性**：注意 Windows/macOS/Linux 的差异
4. **爬虫更新**：网站结构变化时需要更新对应爬虫
5. **测试**：新增功能需添加对应测试

---

## 扩展开发

### 添加新的爬虫

1. 在 `mdcx/crawlers/` 下创建新文件
2. 继承 `BaseCrawler`
3. 实现抽象方法
4. 使用 `@register_crawler` 装饰器注册
5. 在 `Website` 枚举中添加对应网站

### 添加新的翻译服务

1. 在 `Translator` 枚举中添加
2. 在 `core/translate.py` 中实现对应翻译函数
3. 在 `TranslateConfig` 中添加配置（如需要）

---

*文档生成时间：2026-05-22*
