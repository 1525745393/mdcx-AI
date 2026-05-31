# MDCx 配置项说明文档

> 📖 **更多文档**: [文档中心](README.md) | [主 README](../README.md) | [用户手册](../USER_GUIDE.md) | [FAQ](../FAQ.md)

本文档详细介绍 MDCx 的所有配置项，包括配置项含义、可选值、默认值，以及最佳配置建议。

## 目录

1. [通用设置](#通用设置)
2. [清理设置](#清理设置)
3. [刮削设置](#刮削设置)
4. [网站设置](#网站设置)
5. [字段配置](#字段配置)
6. [翻译配置](#翻译配置)
7. [命名和格式化](#命名和格式化)
8. [服务器设置](#服务器设置)
9. [水印设置](#水印设置)
10. [网络设置](#网络设置)
11. [日志设置](#日志设置)
12. [杂项设置](#杂项设置)
13. [配置示例](#配置示例)
14. [最佳配置建议](#最佳配置建议)
15. [VSMETA 配置详解](#vsmeta-配置详解)

---

## 通用设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `config_version` | int | 2 | 配置文件版本号，系统自动管理 |
| `media_path` | string | `"./media"` | 媒体文件所在路径 |
| `softlink_path` | string | `"softlink"` | 软链接存储路径 |
| `success_output_folder` | string | `"JAV_output"` | 刮削成功后的输出目录 |
| `failed_output_folder` | string | `"failed"` | 刮削失败后的输出目录 |
| `extrafanart_folder` | string | `"extrafanart_copy"` | 额外剧照目录 |
| `media_type` | list | `[".mp4", ".avi", ".rmvb", ".wmv", ".mov", ".mkv", ".flv", ".ts", ".webm", ".iso", ".mpg"]` | 要处理的媒体文件扩展名列表 |
| `sub_type` | list | `[".smi", ".srt", ".idx", ".sub", ".sup", ".psb", ".ssa", ".ass", ".usf", ".xss", ".ssf", ".rt", ".lrc", ".sbv", ".vtt", ".ttml"]` | 要处理的字幕文件扩展名列表 |
| `scrape_softlink_path` | bool | `false` | 是否刮削软链接路径下的文件 |
| `auto_link` | bool | `false` | 是否自动创建软链接 |

---

## 清理设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `folders` | list | `["JAV_output", "examples"]` | 要排除的目录列表 |
| `string` | list | 见下文 | 要从文件名中删除的字符串列表 |
| `file_size` | float | `100.0` | 要处理的最小文件大小（MB），小于此值的文件会被忽略 |
| `no_escape` | list | `["record_success_file"]` | 不进行转义的选项列表 |
| `clean_ext` | list | `[".html", ".url"]` | 要清理的文件扩展名列表 |
| `clean_name` | list | `["uur76.mp4", "uur93.com.mp4"]` | 要清理的文件名（完全匹配）列表 |
| `clean_contains` | list | 见下文 | 文件名包含这些字符串时需要清理 |
| `clean_size` | float | `0.0` | 清理小于此大小的文件（KB） |
| `clean_ignore_ext` | list | `[]` | 清理时忽略的文件扩展名列表 |
| `clean_ignore_contains` | list | `["skip", "ignore"]` | 文件名包含这些字符串时忽略清理 |
| `clean_enable` | list | 见下文 | 启用的清理规则列表 |

### 默认 `string` 值
```
[
  "h_720",
  "2048论坛@fun2048.com",
  "1080p",
  "720p",
  "22-sht.me",
  "-HD",
  "bbs2048.org@",
  "hhd800.com@",
  "icao.me@",
  "hhb_000",
  "[456k.me]",
  "[ThZu.Cc]"
]
```

### 默认 `clean_contains` 值
```
[
  "直播盒子",
  "最新情报",
  "最新位址",
  "注册免费送",
  "房间火爆",
  "美女荷官",
  "妹妹直播",
  "精彩直播"
]
```

### 默认 `clean_enable` 值
```
[
  "clean_ext",
  "clean_name",
  "clean_contains",
  "clean_size",
  "clean_ignore_ext",
  "clean_ignore_contains"
]
```

### `no_escape` 可选值
- `no_skip_small_file` - 不跳过小文件
- `folder` - 目录
- `skip_success_file` - 跳过成功文件
- `record_success_file` - 记录成功文件（默认）
- `check_symlink` - 检查符号链接
- `symlink_definition` - 符号链接定义

### `clean_enable` 可选值
- `clean_ext` - 清理指定后缀文件
- `clean_name` - 清理指定文件名
- `clean_contains` - 清理包含特定字符串的文件
- `clean_size` - 清理小于指定大小的文件
- `clean_ignore_ext` - 忽略指定后缀
- `clean_ignore_contains` - 忽略包含特定字符串的文件
- `i_know` - 我知道
- `i_agree` - 我同意
- `auto_clean` - 自动清理

---

## 刮削设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `thread_number` | int | `50` | 并发线程数 |
| `thread_time` | int | `0` | 线程时间 |
| `javdb_time` | int | `10` | Javdb 时间 |
| `main_mode` | int | `1` | 主模式 |
| `read_mode` | list | `[]` | 读取模式列表 |
| `update_mode` | string | `"c"` | 更新模式 |
| `update_a_folder` | string | `"{{ actor }}"` | 更新 A 目录模板 |
| `update_b_folder` | string | `"{{ number }} {{ actor }}"` | 更新 B 目录模板 |
| `update_c_filetemplate` | string | `"{{ number }}"` | 更新 C 文件模板 |
| `update_d_folder` | string | `"{{ number }} {{ actor }}"` | 更新 D 目录模板 |
| `update_titletemplate` | string | 见下文 | 更新标题模板 |
| `soft_link` | int | `0` | 软链接选项 |
| `success_file_move` | bool | `true` | 成功后是否移动文件 |
| `failed_file_move` | bool | `true` | 失败后是否移动文件 |
| `success_file_rename` | bool | `true` | 成功后是否重命名文件 |
| `del_empty_folder` | bool | `true` | 是否删除空目录 |
| `show_poster` | bool | `true` | 是否显示海报 |
| `download_files` | list | 见下文 | 要下载的文件类型列表 |
| `keep_files` | list | 见下文 | 要保留的文件类型列表 |
| `download_hd_pics` | list | `["amazon"]` | 下载高清图片的来源 |
| `amazon_skip_poster_size_precheck` | bool | `false` | 是否跳过前置 Poster 大小校验 |
| `amazon_strict_pic_verify` | bool | `false` | 是否严格校验 Amazon 图片 |
| `scrape_like` | string | `"info"` | 刮削模式：`info`、`speed` 或 `single` |
| `field_priority_try_all_images` | bool | `false` | 字段优先时是否尝试所有图片 |

### 默认 `update_titletemplate` 值
```
"[{% if number %}{{ number }}{% endif %}]{% if title and title != number %}{{ title }}{% endif %}"
```

### 默认 `download_files` 值
```
[
  "poster",
  "thumb",
  "fanart",
  "extrafanart",
  "trailer",
  "nfo",
  "vsmeta",
  "extrafanart_extras",
  "extrafanart_copy",
  "theme_videos",
  "ignore_pic_fail",
  "ignore_youma",
  "ignore_wuma",
  "ignore_fc2",
  "ignore_guochan",
  "ignore_size"
]
```

### 默认 `keep_files` 值
```
[
  "trailer",
  "theme_videos"
]
```

### `read_mode` 可选值
- `has_nfo_update` - 有 NFO 时更新
- `no_nfo_scrape` - 无 NFO 时刮削
- `read_download_again` - 重新下载
- `read_update_nfo` - 更新 NFO

### `download_files` 可选值
- `poster` - 海报
- `thumb` - 缩略图
- `fanart` - 剧照
- `extrafanart` - 额外剧照
- `trailer` - 预告片
- `nfo` - Nfo 文件
- `vsmeta` - VSMETA 文件
- `extrafanart_extras` - 额外剧照扩展
- `extrafanart_copy` - 额外剧照复制
- `theme_videos` - 主题视频
- `ignore_pic_fail` - 忽略图片失败
- `ignore_youma` - 忽略有码
- `poster_auto_best` - 有码 Poster 竖图自动选优
- `ignore_wuma` - 忽略无码
- `ignore_oumei` - 忽略欧美
- `ignore_fc2` - 忽略 FC2
- `ignore_guochan` - 忽略国产
- `ignore_size` - 忽略大小

### `keep_files` 可选值
- `poster` - 海报
- `thumb` - 缩略图
- `fanart` - 剧照
- `extrafanart` - 额外剧照
- `trailer` - 预告片
- `nfo` - nfo 文件
- `vsmeta` - VSMETA 文件
- `extrafanart_copy` - 复制额外剧照
- `theme_videos` - 主题视频

### `download_hd_pics` 可选值
- `amazon` - Amazon 高清图片（默认）

---

## 网站设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `website_single` | string | `"airav_cc"` | 单个网站（待移除） |
| `website_youma` | list | 见下文 | 有码网站源列表 |
| `website_wuma` | list | 见下文 | 无码网站源列表 |
| `website_suren` | list | 见下文 | 素人网站源列表 |
| `website_fc2` | list | 见下文 | FC2 网站源列表 |
| `website_oumei` | list | 见下文 | 欧美网站源列表 |
| `website_guochan` | list | 见下文 | 国产网站源列表 |
| `fixed_scraping_type` | string | `"auto"` | 锁定刮削类型，跳过自动判断 |
| `actor_realname` | bool | `true` | 是否使用演员真名 |
| `outline_format` | list | `[]` | 简介格式 |

### 默认 `website_youma` 值
```
[
  "mgstage",
  "official",
  "missav",
  "javbus",
  "javdbapi",
  "jav321",
  "dmm",
  "avbase"
]
```

### 默认 `website_wuma` 值
```
[
  "missav",
  "7mmtv",
  "avsox"
]
```

### 默认 `website_suren` 值
```
[
  "mgstage",
  "javbus",
  "jav321",
  "dmm",
  "avbase",
  "7mmtv"
]
```

### 默认 `website_fc2` 值
```
[
  "fc2",
  "7mmtv",
  "fc2hub",
  "fc2club"
]
```

### 默认 `website_oumei` 值
```
[
  "theporndb"
]
```

### 默认 `website_guochan` 值
```
[
  "cnmdb",
  "hdouban",
  "madouqu",
  "javday",
  "mdtv"
]
```

### `fixed_scraping_type` 可选值
- `auto` - 自动判断（默认）
- `youma` - 有码
- `wuma` - 无码
- `suren` - 素人
- `fc2` - FC2
- `oumei` - 欧美
- `guochan` - 国产

### `outline_format` 可选值
- `show_from` - 显示来源
- `show_zh_jp` - 显示中日
- `show_jp_zh` - 显示日中

### 可用网站列表
- `avbase`
- `airav`
- `airav_cc`
- `avsex`
- `avsox`
- `cableav`
- `cnmdb`
- `dmm`
- `faleno`
- `fantastica`
- `fc2`
- `fc2club`
- `fc2hub`
- `fc2ppvdb`
- `freejavbt`
- `getchu`
- `giga`
- `hdouban`
- `hscangku`
- `iqqtv`
- `jav321`
- `javbus`
- `javday`
- `javdb`
- `javdbapi`
- `javlibrary`
- `kin8`
- `love6`
- `lulubar`
- `madouqu`
- `mdtv`
- `missav`
- `mgstage`
- `7mmtv`
- `mywife`
- `prestige`
- `theporndb`
- `xcity`
- `dahlia`
- `getchu_dmm`
- `official`

---

## 字段配置

`field_configs` 是一个字典，用于配置各个字段的刮削行为。每个字段可以配置：

| 配置项 | 说明 |
|--------|------|
| `site_prority` | 来源网站优先级列表 |
| `language` | 语言偏好 |
| `translate` | 是否翻译此字段 |

### 可配置字段

| 字段名 | 默认网站优先级 | 默认语言 | 是否翻译 |
|--------|----------------|----------|----------|
| `title` | 默认列表 | `zh_cn` | `true` |
| `originaltitle` | 默认列表 | `undefined` | `true` |
| `outline` | 默认列表 | `zh_cn` | `true` |
| `originalplot` | 默认列表 | `undefined` | `true` |
| `actors` | 默认列表 | `zh_cn` | `true` |
| `all_actors` | 默认列表 | `zh_cn` | `true` |
| `tags` | 默认列表 | `zh_cn` | `true` |
| `directors` | 默认列表 | `zh_cn` | `true` |
| `series` | 默认列表 | `zh_cn` | `true` |
| `studio` | 默认列表 | `zh_cn` | `true` |
| `publisher` | 默认列表 | `zh_cn` | `true` |
| `thumb` | 默认列表 | `undefined` | `true` |
| `poster` | 默认列表 | `undefined` | `true` |
| `extrafanart` | 默认列表 | `undefined` | `true` |
| `trailer` | 默认列表 | `undefined` | `true` |
| `release` | 默认列表 | `undefined` | `true` |
| `runtime` | 默认列表 | `undefined` | `true` |
| `score` | 默认列表 | `undefined` | `true` |
| `wanted` | 默认列表 | `undefined` | `true` |

### 默认网站优先级列表
```
[
  "theporndb",
  "dmm",
  "official",
  "mgstage",
  "prestige",
  "avbase",
  "jav321",
  "7mmtv",
  "javdb",
  "javbus",
  "iqqtv",
  "freejavbt",
  "missav",
  "avsox",
  "fc2hub",
  "fc2",
  "fc2ppvdb"
]
```

### 语言选项
- `undefined` - 未定义（默认）
- `unknown` - 未知
- `zh_cn` - 简体中文
- `zh_tw` - 繁体中文
- `jp` - 日语
- `en` - 英语

---

## 翻译配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `translate_by` | list | 见下文 | 翻译服务列表，按优先级排序 |
| `baidu_appid` | string | `""` | 百度翻译 APP ID |
| `baidu_key` | string | `""` | 百度翻译密钥 |
| `deepl_key` | string | `""` | DeepL API Key |
| `deeplx_url` | string | `""` | DeepLX URL |
| `llm_url` | HttpUrl | `"https://api.llm.com/v1"` | LLM API 地址 |
| `llm_model` | string | `"gpt-3.5-turbo"` | LLM 模型 ID |
| `llm_key` | string | `""` | LLM API Key |
| `llm_prompt_title` | string | 见下文 | LLM 标题翻译提示词 |
| `llm_prompt_outline` | string | 见下文 | LLM 简介翻译提示词 |
| `llm_read_timeout` | int | `60` | LLM 读取超时（秒） |
| `llm_max_req_sec` | float | `1.0` | LLM 每秒最大请求数 |
| `llm_max_try` | int | `5` | LLM 最大尝试次数 |
| `llm_temperature` | float | `0.2` | LLM 温度参数 |

### 默认 `translate_by` 值
```
[
  "google",
  "baidu",
  "deepl",
  "deeplx",
  "llm"
]
```

### 默认 `llm_prompt_title` 值
```
"Please translate the following text to {lang}. Output only the translation without any explanation.\n{content}"
```

### 默认 `llm_prompt_outline` 值
```
"Please translate the following text to {lang}. Output only the translation without any explanation.\n{content}"
```

### 翻译服务选项
- `google` - 谷歌翻译
- `baidu` - 百度翻译
- `deepl` - DeepL 翻译
- `deeplx` - DeepLX 翻译
- `llm` - LLM 翻译

---

## 命名和格式化

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `nfo_include_new` | list | 见下文 | NFO 包含内容列表 |
| `nfo_tagline` | string | `"发行日期 release"` | NFO 标语 |
| `nfo_tag_include` | list | 见下文 | 包含的标签列表 |
| `nfo_tag_series` | string | `"系列: series"` | NFO 系列标签 |
| `nfo_tag_studio` | string | `"片商: studio"` | NFO 工作室标签 |
| `nfo_tag_publisher` | string | `"发行: publisher"` | NFO 发行商标签 |
| `nfo_tag_actor` | string | `"actor"` | NFO 演员标签 |
| `nfo_tag_actor_contains` | list | `[]` | NFO 演员名白名单 |
| `folder_name` | string | `"{{ actor }}/{{ number }} {{ actor }}"` | 目录名称模板 |
| `naming_file` | string | `"{{ number }}"` | 文件命名模板 |
| `naming_media` | string | 见下文 | 媒体命名模板 |
| `prevent_char` | string | `""` | 禁止字符 |
| `fields_rule` | list | 见下文 | 字段规则列表 |
| `suffix_sort` | list | 见下文 | 后缀排序列表 |
| `actor_no_name` | string | `"未知演员"` | 未知演员名称 |
| `release_rule` | string | `"YYYY-MM-DD"` | 发布日期格式规则 |
| `folder_name_max` | int | `60` | 目录名称最大长度 |
| `file_name_max` | int | `60` | 文件名称最大长度 |
| `actor_name_max` | int | `3` | 演员名称最大数量 |
| `actor_name_more` | string | `"等演员"` | 更多演员名称 |
| `umr_style` | string | `"-破解"` | 破解样式 |
| `leak_style` | string | `"-流出"` | 流出样式 |
| `wuma_style` | string | `""` | 无码样式 |
| `youma_style` | string | `""` | 有码样式 |
| `cd_name` | int | `0` | CD 名称 |
| `cd_char` | list | 见下文 | 分集规则列表 |
| `pic_simple_name` | bool | `false` | 图片简化命名 |
| `trailer_simple_name` | bool | `true` | 预告片简化命名 |
| `vsmeta_keep_ext` | bool | `false` | VSMETA 是否保留视频扩展名 |
| `vsmeta_include_poster` | bool | `true` | VSMETA 是否嵌入封面图 |
| `vsmeta_include_backdrop` | bool | `true` | VSMETA 是否嵌入背景图 |
| `vsmeta_locked` | bool | `true` | VSMETA 是否锁定元数据 |
| `vsmeta_image_max_dimension` | int | `1920` | VSMETA 图片最大尺寸 |
| `vsmeta_jpeg_quality` | int | `90` | VSMETA 图片 JPEG 质量 |
| `vsmeta_actor_limit` | int | `20` | VSMETA 演员数量上限 |
| `vsmeta_tag_limit` | int | `10` | VSMETA 标签数量上限 |
| `vsmeta_show_title` | string | `"title"` | VSMETA 标题内容 |
| `vsmeta_show_title2` | string | `"originaltitle"` | VSMETA 副标题内容 |
| `vsmeta_summary` | string | `"jp_zh_jp"` | VSMETA 简介内容 |
| `vsmeta_custom_title` | string | 见下文 | VSMETA 标题自定义模板 |
| `vsmeta_custom_title2` | string | 见下文 | VSMETA 副标题自定义模板 |
| `vsmeta_custom_summary` | string | 见下文 | VSMETA 简介自定义模板 |
| `hd_name` | string | `"height"` | 高清名称选项：`height` 或 `hd` |
| `hd_get` | string | `"video"` | 获取高清方式：`video`、`path` 或 `none` |
| `folder_moword` | bool | `true` | 目录是否包含马赛克字符 |
| `file_moword` | bool | `true` | 文件是否包含马赛克字符 |
| `folder_hd` | bool | `true` | 目录是否包含画质字符 |
| `file_hd` | bool | `true` | 文件是否包含画质字符 |
| `cnword_char` | list | 见下文 | 中文字符列表 |
| `cnword_style` | string | `"-C"` | 中文样式 |
| `folder_cnword` | bool | `true` | 目录是否包含中文标识 |
| `file_cnword` | bool | `true` | 文件是否包含中文标识 |
| `subtitle_folder` | string | `""` | 字幕目录 |
| `subtitle_add` | bool | `false` | 是否添加字幕 |
| `subtitle_add_chs` | bool | `true` | 是否添加中文字幕 |
| `subtitle_add_rescrape` | bool | `true` | 重新刮削时是否添加字幕 |

### 默认 `nfo_include_new` 值
```
[
  "sorttitle",
  "originaltitle",
  "title_cd",
  "outline",
  "plot_",
  "originalplot",
  "outline_no_cdata",
  "release_",
  "releasedate",
  "premiered",
  "country",
  "mpaa",
  "customrating",
  "year",
  "runtime",
  "wanted",
  "score",
  "criticrating",
  "actor",
  "actor_all",
  "director",
  "series",
  "tag",
  "genre",
  "actor_set",
  "series_set",
  "studio",
  "maker",
  "publisher",
  "label",
  "poster",
  "cover",
  "trailer",
  "website"
]
```

### 默认 `naming_media` 值
```
"[{% if number %}{{ number }}{% endif %}]{% if title and title != number %}{{ title }}{% endif %}"
```

### 默认 `fields_rule` 值
```
[
  "del_actor",
  "del_char",
  "fc2_seller",
  "del_num"
]
```

### 默认 `suffix_sort` 值
```
[
  "moword",
  "cnword",
  "definition"
]
```

### 默认 `cd_char` 值
```
[
  "letter",
  "endc",
  "digital",
  "middle_number",
  "underline",
  "space",
  "point"
]
```

### 默认 `vsmeta_custom_title` 值
```
"{number} - {title} ({originaltitle})"
```

### 默认 `vsmeta_custom_title2` 值
```
"{publisher} / {studio}"
```

### 默认 `vsmeta_custom_summary` 值
```
"{originaltitle}\n\n{outline}\n\n{originalplot}"
```

### 默认 `cnword_char` 值
```
[
  "-C.",
  "-C-",
  "ch.",
  "字幕"
]
```

### `nfo_include_new` 可选值
- `sorttitle` - 排序标题
- `originaltitle` - 原始标题
- `title_cd` - 标题 CD
- `outline` - 简介
- `plot_` - 剧情
- `originalplot` - 原始剧情
- `outline_no_cdata` - 无 CDATA 简介
- `release_` - 发布
- `releasedate` - 发布日期
- `premiered` - 首映
- `country` - 国家
- `mpaa` - MPAA
- `customrating` - 自定义评分
- `year` - 年份
- `runtime` - 时长
- `wanted` - 想看
- `score` - 评分
- `criticrating` - 评论家评分
- `actor` - 演员
- `actor_all` - 所有演员
- `director` - 导演
- `series` - 系列
- `tag` - 标签
- `genre` - 类型
- `actor_set` - 演员集
- `series_set` - 系列集
- `studio` - 工作室
- `maker` - 制造商
- `publisher` - 发行商
- `label` - 标签
- `poster` - 海报
- `cover` - 封面
- `trailer` - 预告片
- `website` - 网站

### `nfo_tag_include` 可选值
- `actor` - 演员
- `letters` - 字母
- `series` - Series
- `studio` - Studio
- `publisher` - Publisher
- `cnword` - Cnword
- `mosaic` - Mosaic
- `definition` - Definition

### `fields_rule` 可选值
- `del_actor` - 移除标题后的演员名
- `del_char` - 移除演员名中的括号
- `fc2_seller` - 使用 FC2 卖家作为演员名
- `del_num` - 移除番号前缀数字

### `suffix_sort` 可选值
- `moword` - 马赛克
- `cnword` - 中文字幕
- `definition` - 清晰度

### `cd_char` 可选值
- `letter` - 除 C 以外的字母
- `endc` - C 结尾也视为分集而非字幕
- `digital` - 末尾两位数字
- `middle_number` - 不在结尾的数字
- `underline` - 分集分隔符: 下划线
- `space` - 分集分隔符: 空格
- `point` - 分集分隔符: 英文句号

### `vsmeta_show_title` 可选值
- `title` - 中文翻译标题（默认）
- `number_title` - 番号 + 中文翻译标题
- `number_only` - 仅番号
- `number_originaltitle` - 番号 + 日文原始标题
- `title_originaltitle` - 中文标题 + 日文标题
- `originaltitle_title` - 日文标题 + 中文标题
- `custom` - 自定义模板

### `vsmeta_show_title2` 可选值
- `originaltitle` - 日文原始标题（默认）
- `publisher` - 制作商
- `studio` - 工作室
- `none` - 不写入
- `custom` - 自定义模板

### `vsmeta_summary` 可选值
- `jp_zh_jp` - 日文标题 + 中文简介 + 日文简介（默认）
- `outline` - 中文简介
- `originalplot` - 日文简介
- `zh_jp` - 中文简介 + 日文简介
- `jp_zh` - 日文标题 + 中文简介
- `title_only` - 仅日文标题
- `none` - 不写入
- `custom` - 自定义模板

---

## 服务器设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `server_type` | string | `"emby"` | 服务器类型：`emby` 或 `jellyfin` |
| `emby_url` | HttpUrl | `"http://127.0.0.1:8096"` | Emby 服务器地址 |
| `api_key` | string | `""` | API 密钥 |
| `user_id` | string | `""` | 用户 ID |
| `emby_on` | list | 见下文 | Emby 功能开关列表 |
| `use_database` | bool | `false` | 是否使用数据库 |
| `info_database_path` | string | `""` | 信息数据库路径 |
| `gfriends_github` | HttpUrl | `"https://github.com/gfriends/gfriends"` | Gfriends GitHub 地址 |
| `actor_photo_folder` | string | `""` | 演员照片目录 |
| `actor_photo_kodi_auto` | bool | `false` | 演员照片 Kodi 自动 |

### 默认 `emby_on` 值
```
[
  "actor_info_zh_cn",
  "actor_info_miss",
  "actor_photo_net",
  "actor_photo_miss",
  "actor_info_translate",
  "actor_info_photo",
  "graphis_backdrop",
  "graphis_face",
  "graphis_new",
  "actor_photo_auto",
  "actor_replace"
]
```

### `emby_on` 可选值
- `actor_info_zh_cn` - 获取简体中文演员信息
- `actor_info_zh_tw` - 获取繁体中文演员信息
- `actor_info_ja` - Actor Info Ja
- `actor_info_all` - Actor Info All
- `actor_info_miss` - Actor Info Miss
- `actor_photo_net` - Actor Photo Net
- `actor_photo_local` - Actor Photo Local
- `actor_photo_all` - Actor Photo All
- `actor_photo_miss` - Actor Photo Miss
- `actor_info_translate` - Actor Info Translate
- `actor_info_photo` - Actor Info Photo
- `graphis_backdrop` - Graphis Backdrop
- `graphis_face` - Graphis Face
- `graphis_new` - Graphis New
- `actor_photo_auto` - Actor Photo Auto
- `actor_replace` - Actor Replace

---

## 水印设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `poster_mark` | int | `1` | 海报水印 |
| `thumb_mark` | int | `1` | 缩略图水印 |
| `fanart_mark` | int | `0` | Fanart 水印 |
| `mark_size` | int | `5` | 水印大小 |
| `mark_type` | list | 见下文 | 水印类型列表 |
| `mark_fixed` | string | `"not_fixed"` | 水印添加规则 |
| `mark_pos` | string | `"top_left"` | 水印规则为不固定时首个水印的位置 |
| `mark_pos_corner` | string | `"top_left"` | 水印规则为固定时的位置 |
| `mark_pos_sub` | string | `"top_left"` | 中文字幕水印位置 |
| `mark_pos_mosaic` | string | `"top_right"` | 马赛克类型水印位置 |
| `mark_pos_hd` | string | `"bottom_right"` | 清晰度水印位置 |

### 默认 `mark_type` 值
```
[
  "sub",
  "youma",
  "umr",
  "leak",
  "uncensored",
  "hd"
]
```

### `mark_type` 可选值
- `sub` - 字幕
- `youma` - 有码
- `umr` - 破解
- `leak` - 流出
- `uncensored` - 无码
- `hd` - 高清

### `mark_fixed` 可选值
- `not_fixed` - 不固定位置，从首个位置开始顺时针方向依次添加
- `fixed` - 固定一个位置，水印在此依次横向添加
- `corner` - 分别设置不同种类水印的位置

---

## 网络设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `use_proxy` | bool | `false` | 是否使用代理 |
| `proxy` | string | `"http://127.0.0.1:7890"` | 代理地址 |
| `cf_bypass_url` | string | `""` | Cloudflare Bypass 地址 |
| `cf_bypass_proxy` | string | `""` | Cloudflare Bypass 代理地址 |
| `timeout` | int | `10` | 请求超时时间（秒） |
| `retry` | int | `3` | 重试次数 |
| `theporndb_api_token` | string | `""` | Theporndb API 令牌 |
| `javdb` | string | `""` | Javdb |
| `fc2ppvdb` | string | `""` | FC2PPVDB |
| `javbus` | string | `""` | Javbus |

---

## 日志设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `show_web_log` | bool | `false` | 是否显示网页日志 |
| `show_from_log` | bool | `true` | 是否显示来源日志 |
| `show_data_log` | bool | `true` | 是否显示数据日志 |
| `save_log` | bool | `true` | 是否保存日志 |

---

## 杂项设置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `update_check` | bool | `true` | 是否检查更新 |
| `local_library` | list | `[]` | 本地库列表 |
| `actors_name` | string | `""` | 演员名称 |
| `netdisk_path` | string | `""` | 网盘路径 |
| `localdisk_path` | string | `""` | 本地磁盘路径 |
| `window_title` | string | `"hide"` | 窗口标题 |
| `switch_on` | list | 见下文 | 功能开关列表 |
| `timed_interval` | timedelta | `0:30:00` | 定时器间隔 |
| `rest_count` | int | `20` | 休息计数 |
| `rest_time` | timedelta | `0:00:00` | 休息时间 |

### 默认 `switch_on` 值
```
[
  "auto_exit",
  "rest_scrape",
  "timed_scrape",
  "remain_task",
  "show_dialog_stop_scrape",
  "sort_del",
  "theporndb_no_hash",
  "hide_dock",
  "passthrough",
  "hide_menu",
  "dark_mode",
  "copy_netdisk_nfo",
  "show_logs",
  "hide_none"
]
```

### `switch_on` 可选值
- `auto_start` - 自动开始
- `auto_exit` - 自动退出
- `rest_scrape` - Rest Scrape
- `timed_scrape` - Timed Scrape
- `remain_task` - Remain Task
- `show_dialog_exit` - Show Dialog Exit
- `show_dialog_stop_scrape` - Show Dialog Stop Scrape
- `sort_del` - Sort Del
- `qt_dialog` - Qt Dialog
- `theporndb_no_hash` - Theporndb No Hash
- `hide_dock` - Hide Dock
- `passthrough` - Passthrough
- `hide_menu` - Hide Menu
- `dark_mode` - 深色模式
- `copy_netdisk_nfo` - Copy Netdisk Nfo
- `show_logs` - 显示日志
- `hide_close` - Hide Close
- `hide_mini` - Hide Mini
- `hide_none` - Hide None
- `ipv4_only` - 仅 IPv4（已废弃）

---

## 配置示例

### 基础配置示例

```json
{
  "config_version": 2,
  "media_path": "./media",
  "softlink_path": "softlink",
  "success_output_folder": "JAV_output",
  "failed_output_folder": "failed",
  "thread_number": 50,
  "success_file_move": true,
  "failed_file_move": true,
  "success_file_rename": true,
  "download_files": [
    "poster",
    "thumb",
    "fanart",
    "nfo",
    "vsmeta"
  ],
  "website_youma": [
    "mgstage",
    "official",
    "javbus",
    "dmm"
  ]
}
```

### Emby 服务器配置示例

```json
{
  "server_type": "emby",
  "emby_url": "http://192.168.1.100:8096",
  "api_key": "your_emby_api_key_here",
  "user_id": "your_user_id_here",
  "emby_on": [
    "actor_info_zh_cn",
    "actor_photo_net",
    "actor_info_translate"
  ]
}
```

### 翻译配置示例

```json
{
  "translate_config": {
    "translate_by": ["google", "deepl"],
    "baidu_appid": "",
    "baidu_key": "",
    "deepl_key": "your_deepl_key_here",
    "deeplx_url": "",
    "llm_url": "https://api.openai.com/v1",
    "llm_model": "gpt-3.5-turbo",
    "llm_key": "your_llm_key_here"
  }
}
```

### 代理配置示例

```json
{
  "use_proxy": true,
  "proxy": "http://127.0.0.1:7890",
  "timeout": 30,
  "retry": 5
}
```

### 命名模板示例

```json
{
  "folder_name": "{{ actor }}/{{ number }} {{ title }}",
  "naming_file": "{{ number }}",
  "naming_media": "[{{ number }}] {{ title }}",
  "folder_name_max": 80,
  "file_name_max": 80,
  "actor_name_max": 5
}
```

---

## 最佳配置建议

### 1. 性能优化

- **线程数**：`thread_number` 建议设置为 20-50，过高可能导致网站反爬虫
- **超时时间**：网络条件差时可适当增加 `timeout` 到 20-30 秒
- **重试次数**：`retry` 建议保持 3-5 次

### 2. 刮削质量

- **网站优先级**：根据你的网络条件调整网站优先级，优先选择速度快的网站
- **高清图片**：启用 `download_hd_pics` 中的 Amazon 源以获取更高质量的封面
- **字段配置**：为不同字段设置合理的网站优先级，提高刮削准确性

### 3. 文件组织

- **目录结构**：建议使用 `{{ actor }}/{{ number }} {{ actor }}` 这样的结构便于管理
- **命名长度**：根据操作系统限制调整 `folder_name_max` 和 `file_name_max`
- **中文字幕**：启用 `folder_cnword` 和 `file_cnword` 快速识别中文字幕文件

### 4. 翻译设置

- **翻译服务**：优先使用 Google 或 DeepL，质量更高
- **LLM 配置**：使用 LLM 翻译时，建议设置较长的 `llm_read_timeout`（60秒以上）
- **翻译范围**：根据需要选择是否翻译所有字段

### 5. Emby 集成

- **API 密钥**：务必配置正确的 `api_key` 和 `user_id`
- **演员信息**：启用 `actor_info_zh_cn` 获取中文演员信息
- **演员照片**：启用 `actor_photo_net` 自动下载演员照片

### 6. 水印设置

- **水印位置**：建议使用 `mark_fixed: "corner"` 分别设置不同水印的位置
- **水印大小**：`mark_size` 建议设置为 3-5，避免遮挡重要内容

### 7. 网络设置

- **代理配置**：中国大陆用户建议配置代理以访问国外网站
- **Cloudflare**：遇到 Cloudflare 保护时配置 `cf_bypass_url`
- **API Token**：获取 Theporndb API Token 以提高欧美片刮削成功率

---

## VSMETA 配置详解

VSMETA 是 Emby/Jellyfin 用于识别和管理元数据的文件格式。本章节详细介绍 VSMETA 相关的配置选项，帮助用户自定义 VSMETA 文件中标题、副标题和简介内容的显示方式。

### VSMETA 配置概述

VSMETA 文件包含以下主要配置维度：

- **标题内容配置**（`vsmeta_show_title`）：定义 VSMETA 中的主标题显示内容
- **副标题内容配置**（`vsmeta_show_title2`）：定义 VSMETA 中的副标题显示内容
- **简介内容配置**（`vsmeta_summary`）：定义 VSMETA 中的简介显示内容
- **嵌入选项配置**：控制是否在 VSMETA 中嵌入封面图、背景图等媒体资源
- **质量参数配置**：控制图片尺寸、JPEG 质量等质量参数
- **数量限制配置**：控制演员、标签等元素的数量上限

### 配置项总览表

#### 标题内容配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `vsmeta_show_title` | string | `"title"` | VSMETA 标题内容显示模式 |
| `vsmeta_custom_title` | string | 见下文 | 自定义标题模板（当模式为 `custom` 时使用） |

#### 副标题内容配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `vsmeta_show_title2` | string | `"originaltitle"` | VSMETA 副标题内容显示模式 |
| `vsmeta_custom_title2` | string | 见下文 | 自定义副标题模板（当模式为 `custom` 时使用） |

#### 简介内容配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `vsmeta_summary` | string | `"jp_zh_jp"` | VSMETA 简介内容显示模式 |
| `vsmeta_custom_summary` | string | 见下文 | 自定义简介模板（当模式为 `custom` 时使用） |

#### 其他 VSMETA 配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `vsmeta_keep_ext` | bool | `false` | VSMETA 是否保留视频文件扩展名 |
| `vsmeta_include_poster` | bool | `true` | 是否在 VSMETA 中嵌入封面图 |
| `vsmeta_include_backdrop` | bool | `true` | 是否在 VSMETA 中嵌入背景图 |
| `vsmeta_locked` | bool | `true` | VSMETA 元数据是否锁定 |
| `vsmeta_image_max_dimension` | int | `1920` | VSMETA 图片最大尺寸（像素） |
| `vsmeta_jpeg_quality` | int | `90` | VSMETA 图片 JPEG 质量（1-100） |
| `vsmeta_actor_limit` | int | `20` | VSMETA 演员数量上限 |
| `vsmeta_tag_limit` | int | `10` | VSMETA 标签数量上限 |

### VsmetaShowTitle 配置项详解

#### 功能说明

`vsmeta_show_title` 配置项用于定义 VSMETA 文件中主标题（Show Title）的显示内容。这个配置项决定了在 Emby/Jellyfin 等媒体服务器中显示的视频标题格式。

#### 可选值说明

| 可选值 | 功能描述 | 使用场景 |
|--------|----------|----------|
| `TITLE` | 中文翻译标题 | 默认选项，简洁明了，适合大多数用户 |
| `NUMBER_TITLE` | 番号 + 中文翻译标题 | 需要同时显示番号和标题，便于识别 |
| `NUMBER_ONLY` | 仅显示番号 | 番好型用户，只关注番号 |
| `NUMBER_ORIGINALTITLE` | 番号 + 日文原始标题 | 日文用户，需要原始标题信息 |
| `TITLE_ORIGINALTITLE` | 中文标题 + 日文标题 | 双语环境，显示两种语言 |
| `ORIGINALTITLE_TITLE` | 日文标题 + 中文标题 | 日文优先，中文作为参考 |
| `CUSTOM` | 自定义模板 | 需要完全自定义标题格式 |

#### 配置效果示例

假设有一部影片信息如下：

- 番号：`ABC-123`
- 中文标题：`经典剧情`
- 日文原始标题：`クラシックドラマ`

**示例 1：使用 `TITLE` 模式**

```json
{
  "vsmeta_show_title": "title"
}
```

显示效果：`经典剧情`

**示例 2：使用 `NUMBER_TITLE` 模式**

```json
{
  "vsmeta_show_title": "number_title"
}
```

显示效果：`ABC-123 经典剧情`

**示例 3：使用 `NUMBER_ONLY` 模式**

```json
{
  "vsmeta_show_title": "number_only"
}
```

显示效果：`ABC-123`

**示例 4：使用 `NUMBER_ORIGINALTITLE` 模式**

```json
{
  "vsmeta_show_title": "number_originaltitle"
}
```

显示效果：`ABC-123 クラシックドラマ`

**示例 5：使用 `TITLE_ORIGINALTITLE` 模式**

```json
{
  "vsmeta_show_title": "title_originaltitle"
}
```

显示效果：`经典剧情 クラシックドラマ`

**示例 6：使用 `ORIGINALTITLE_TITLE` 模式**

```json
{
  "vsmeta_show_title": "originaltitle_title"
}
```

显示效果：`クラシックドラマ 经典剧情`

**示例 7：使用 `CUSTOM` 自定义模式**

```json
{
  "vsmeta_show_title": "custom",
  "vsmeta_custom_title": "{number} - {title}"
}
```

显示效果：`ABC-123 - 经典剧情`

### VsmetaShowTitle2 配置项详解

#### 功能说明

`vsmeta_show_title2` 配置项用于定义 VSMETA 文件中副标题（Second Title/Subtitle）的显示内容。这个配置项在 Emby/Jellyfin 中通常显示在主标题下方，提供额外的影片信息。

#### 可选值说明

| 可选值 | 功能描述 | 使用场景 |
|--------|----------|----------|
| `ORIGINALTITLE` | 日文原始标题 | 显示原始日文标题 |
| `PUBLISHER` | 制作商/发行商 | 显示发行公司信息 |
| `STUDIO` | 工作室/制作公司 | 显示制作工作室信息 |
| `PUBLISHER_STUDIO` | 制作商 + 工作室 | 同时显示发行和制作信息 |
| `SERIES` | 系列名称 | 显示所属系列 |
| `ACTOR` | 主要演员 | 显示影片主要演员 |
| `NONE` | 不写入 | 不显示副标题 |
| `CUSTOM` | 自定义模板 | 完全自定义副标题格式 |

#### 配置效果示例

假设有一部影片信息如下：

- 日文原始标题：`クラシックドラマ`
- 制作商：`ABC 出版社`
- 工作室：`XYZ 工作室`
- 系列：`经典系列`
- 演员：`演员A`、`演员B`

**示例 1：使用 `ORIGINALTITLE` 模式**

```json
{
  "vsmeta_show_title2": "originaltitle"
}
```

显示效果：`クラシックドラマ`

**示例 2：使用 `PUBLISHER` 模式**

```json
{
  "vsmeta_show_title2": "publisher"
}
```

显示效果：`ABC 出版社`

**示例 3：使用 `STUDIO` 模式**

```json
{
  "vsmeta_show_title2": "studio"
}
```

显示效果：`XYZ 工作室`

**示例 4：使用 `PUBLISHER_STUDIO` 模式**

```json
{
  "vsmeta_show_title2": "publisher_studio"
}
```

显示效果：`ABC 出版社 / XYZ 工作室`

**示例 5：使用 `SERIES` 模式**

```json
{
  "vsmeta_show_title2": "series"
}
```

显示效果：`经典系列`

**示例 6：使用 `ACTOR` 模式**

```json
{
  "vsmeta_show_title2": "actor"
}
```

显示效果：`演员A、演员B`

**示例 7：使用 `NONE` 模式**

```json
{
  "vsmeta_show_title2": "none"
}
```

不显示副标题内容

**示例 8：使用 `CUSTOM` 自定义模式**

```json
{
  "vsmeta_show_title2": "custom",
  "vsmeta_custom_title2": "{publisher} / {studio}"
}
```

显示效果：`ABC 出版社 / XYZ 工作室`

### VsmetaSummary 配置项详解

#### 功能说明

`vsmeta_summary` 配置项用于定义 VSMETA 文件中简介（Summary/Plot）的显示内容。这个配置项决定了在 Emby/Jellyfin 中显示的影片剧情介绍格式。

#### 可选值说明

| 可选值 | 功能描述 | 使用场景 |
|--------|----------|----------|
| `JP_ZH_JP` | 日文标题 + 中文简介 + 日文简介 | 完整的三语言版本（默认） |
| `OUTLINE` | 中文简介 | 仅显示中文剧情介绍 |
| `ORIGINALPLOT` | 日文简介 | 仅显示日文剧情介绍 |
| `ZH_JP` | 中文简介 + 日文简介 | 双语剧情介绍 |
| `JP_ZH` | 日文标题 + 中文简介 | 日文标题 + 中文剧情 |
| `TITLE_ONLY` | 仅日文标题 | 仅显示日文标题 |
| `OUTLINE_PUBLISHER` | 中文简介 + 制作信息 | 剧情介绍 + 发行信息 |
| `NUMBER_TITLE` | 番号 + 标题 | 显示番号和标题 |
| `NONE` | 不写入 | 不显示简介内容 |
| `CUSTOM` | 自定义模板 | 完全自定义简介格式 |

#### 配置效果示例

假设有一部影片信息如下：

- 番号：`ABC-123`
- 日文原始标题：`クラシックドラマ`
- 中文标题：`经典剧情`
- 中文简介：`这是一部精彩的剧情片，讲述了感人至深的故事。`
- 日文简介：`心を打つ感動的な物語を語った素晴らしいドラマです。`
- 制作商：`ABC 出版社`

**示例 1：使用 `JP_ZH_JP` 模式（默认）**

```json
{
  "vsmeta_summary": "jp_zh_jp"
}
```

显示效果：
```
クラシックドラマ

这是一部精彩的剧情片，讲述了感人至深的故事。

心を打つ感動的な物語を語った素晴らしいドラマです。
```

**示例 2：使用 `OUTLINE` 模式**

```json
{
  "vsmeta_summary": "outline"
}
```

显示效果：
```
这是一部精彩的剧情片，讲述了感人至深的故事。
```

**示例 3：使用 `ORIGINALPLOT` 模式**

```json
{
  "vsmeta_summary": "originalplot"
}
```

显示效果：
```
心を打つ感動的な物語を語った素晴らしいドラマです。
```

**示例 4：使用 `ZH_JP` 模式**

```json
{
  "vsmeta_summary": "zh_jp"
}
```

显示效果：
```
这是一部精彩的剧情片，讲述了感人至深的故事。

心を打つ感動的な物語を語った素晴らしいドラマです。
```

**示例 5：使用 `JP_ZH` 模式**

```json
{
  "vsmeta_summary": "jp_zh"
}
```

显示效果：
```
クラシックドラマ

这是一部精彩的剧情片，讲述了感人至深的故事。
```

**示例 6：使用 `TITLE_ONLY` 模式**

```json
{
  "vsmeta_summary": "title_only"
}
```

显示效果：
```
クラシックドラマ
```

**示例 7：使用 `OUTLINE_PUBLISHER` 模式**

```json
{
  "vsmeta_summary": "outline_publisher"
}
```

显示效果：
```
这是一部精彩的剧情片，讲述了感人至深的故事。

发行: ABC 出版社
```

**示例 8：使用 `NUMBER_TITLE` 模式**

```json
{
  "vsmeta_summary": "number_title"
}
```

显示效果：
```
ABC-123 经典剧情
```

**示例 9：使用 `NONE` 模式**

```json
{
  "vsmeta_summary": "none"
}
```

不显示简介内容

**示例 10：使用 `CUSTOM` 自定义模式**

```json
{
  "vsmeta_summary": "custom",
  "vsmeta_custom_summary": "{originaltitle}\n\n{outline}\n\n{originalplot}"
}
```

显示效果：
```
クラシックドラマ

这是一部精彩的剧情片，讲述了感人至深的故事。

心を打つ感動的な物語を語った素晴らしいドラマです。
```

### 其他 VSMETA 配置详解

#### vsmeta_keep_ext

**功能说明**：控制 VSMETA 文件名是否保留视频文件扩展名。

**配置示例**：

```json
{
  "vsmeta_keep_ext": true
}
```

- `true`：VSMETA 文件保留扩展名，如 `ABC-123.mp4.vsmeta`
- `false`：VSMETA 文件不保留扩展名，如 `ABC-123.vsmeta`（默认）

#### vsmeta_include_poster

**功能说明**：控制是否在 VSMETA 文件中嵌入封面图（Poster）。

**配置示例**：

```json
{
  "vsmeta_include_poster": true
}
```

- `true`：嵌入封面图到 VSMETA 文件中（默认）
- `false`：不嵌入封面图

#### vsmeta_include_backdrop

**功能说明**：控制是否在 VSMETA 文件中嵌入背景图（Backdrop/Fanart）。

**配置示例**：

```json
{
  "vsmeta_include_backdrop": true
}
```

- `true`：嵌入背景图到 VSMETA 文件中（默认）
- `false`：不嵌入背景图

#### vsmeta_locked

**功能说明**：控制 VSMETA 元数据是否锁定，防止在媒体服务器中被意外修改。

**配置示例**：

```json
{
  "vsmeta_locked": true
}
```

- `true`：锁定元数据（默认）
- `false`：不锁定元数据

#### vsmeta_image_max_dimension

**功能说明**：控制 VSMETA 中嵌入图片的最大尺寸（宽度或高度）。

**配置示例**：

```json
{
  "vsmeta_image_max_dimension": 1920
}
```

- 默认值：`1920`（像素）
- 推荐值：1920-4096，根据实际需求调整

#### vsmeta_jpeg_quality

**功能说明**：控制 VSMETA 中嵌入图片的 JPEG 压缩质量。

**配置示例**：

```json
{
  "vsmeta_jpeg_quality": 90
}
```

- 默认值：`90`（1-100）
- 推荐值：80-95，质量与文件大小的平衡

#### vsmeta_actor_limit

**功能说明**：限制 VSMETA 中显示的演员数量。

**配置示例**：

```json
{
  "vsmeta_actor_limit": 20
}
```

- 默认值：`20`
- 推荐值：10-30，根据实际演员数量调整

#### vsmeta_tag_limit

**功能说明**：限制 VSMETA 中显示的标签数量。

**配置示例**：

```json
{
  "vsmeta_tag_limit": 10
}
```

- 默认值：`10`
- 推荐值：5-20，根据实际标签数量调整

### 自定义模板语法

当选择 `CUSTOM` 模式时，可以使用以下变量构建自定义模板：

#### 标题模板变量

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `{number}` | 影片番号 | `ABC-123` |
| `{title}` | 中文翻译标题 | `经典剧情` |
| `{originaltitle}` | 日文原始标题 | `クラシックドラマ` |
| `{publisher}` | 制作商 | `ABC 出版社` |
| `{studio}` | 工作室 | `XYZ 工作室` |
| `{series}` | 系列名称 | `经典系列` |
| `{actor}` | 主要演员 | `演员A、演员B` |
| `{release}` | 发布日期 | `2024-01-15` |
| `{year}` | 发布年份 | `2024` |
| `{runtime}` | 时长（分钟） | `120` |

#### 模板语法示例

**示例 1：简单标题格式**

```json
{
  "vsmeta_custom_title": "{number} - {title}"
}
```

效果：`ABC-123 - 经典剧情`

**示例 2：带括号的番号**

```json
{
  "vsmeta_custom_title": "[{number}] {title}"
}
```

效果：`[ABC-123] 经典剧情`

**示例 3：完整标题格式**

```json
{
  "vsmeta_custom_title": "{number} - {title} ({originaltitle})"
}
```

效果：`ABC-123 - 经典剧情 (クラシックドラマ)`

**示例 4：副标题自定义**

```json
{
  "vsmeta_custom_title2": "{publisher} / {studio}"
}
```

效果：`ABC 出版社 / XYZ 工作室`

**示例 5：简介自定义**

```json
{
  "vsmeta_custom_summary": "{originaltitle}\n\n{outline}\n\n发行: {publisher}\n片商: {studio}"
}
```

效果：
```
クラシックドラマ

这是一部精彩的剧情片，讲述了感人至深的故事。

發行: ABC 出版社
片商: XYZ 工作室
```

### 自定义模板完整指南

当你选择 `CUSTOM` 模式时，可以使用功能强大的自定义模板来精确控制 VSMETA 文件中标题、副标题和简介的显示内容。本指南将详细介绍模板语法的各个方面。

#### 模板语法基础

自定义模板采用简单的文本替换机制。你可以在模板中使用**占位符**，系统会自动将其替换为对应的影片信息。

**基本语法格式**：

```
{占位符名称}
```

**示例**：

```
{title}                    → 经典剧情
{number}                   → ABC-123
{publisher} / {studio}     → ABC 出版社 / XYZ 工作室
```

#### 所有可用占位符

以下是 VSMETA 自定义模板中所有可用的占位符及其说明：

##### 基础信息类

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{number}` | 影片番号 | `ABC-123` |
| `{title}` | 中文翻译标题 | `经典剧情` |
| `{originaltitle}` | 日文原始标题 | `クラシックドラマ` |
| `{publisher}` | 发行商/制作商 | `ABC 出版社` |
| `{studio}` | 工作室/制作公司 | `XYZ 工作室` |
| `{series}` | 系列名称 | `经典系列` |

##### 演职人员类

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{actors}` | 演员列表（逗号分隔，最多显示3个） | `演员A、演员B、演员C` |
| `{director}` | 导演 | `张三` |

##### 内容描述类

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{outline}` | 中文简介/剧情介绍 | `这是一部精彩的剧情片...` |
| `{originalplot}` | 日文剧情简介 | `心を打つ感動的な...` |
| `{genre}` | 类型/Genre 标签 | `剧情、爱情` |
| `{label}` | 标签/Label 信息 | `高清`、`独家` |

##### 时间数值类

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{year}` | 发布年份 | `2024` |
| `{release}` | 发布日期（完整） | `2024-01-15` |
| `{runtime}` | 时长（分钟） | `120` |
| `{score}` | 评分 | `8.5` |

##### 其他信息类

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{country}` | 国家/地区 | `日本` |
| `{mosaic}` | 马赛克类型 | `有码`、`无码` |
| `{website}` | 官方网站 | `https://example.com` |

#### 增强语法：条件渲染

条件渲染允许你根据字段是否存在来动态决定是否显示某些内容。这对于处理可选字段非常有用。

**语法格式**：

```
{if:字段名}内容{/if}
```

**工作原理**：

- 当指定字段存在且不为空时，`{if:字段名}` 和 `{/if}` 标签之间的内容会被显示
- 当字段不存在或为空时，这部分内容会被完全省略

**嵌套条件**：

条件标签可以嵌套使用，以实现更复杂的逻辑：

```
{if:field1}内容1{if:field2}内容2{/if}内容3{/if}
```

**示例 1：显示系列信息（如果存在）**

```
模板：{if:series}[{series}] {/if}{number} - {title}
```

- 当有系列时：`[经典系列] ABC-123 - 经典剧情`
- 当无系列时：`ABC-123 - 经典剧情`

**示例 2：演员信息条件显示**

```
模板：{if:actors}演员: {actors}{/if}
```

- 当有演员时：`演员: 演员A、演员B、演员C`
- 当无演员时：（完全省略，不显示任何内容）

**示例 3：多字段条件组合**

```
模板：{if:score}评分: {score} | {/if}{if:runtime}时长: {runtime}分钟{/if}
```

- 当有评分和时长时：`评分: 8.5 | 时长: 120分钟`
- 当只有评分时：`评分: 8.5`
- 当只有时长时：`时长: 120分钟`

**示例 4：带前缀的条件显示**

```
模板：{if:director}导演: {director}\n\n{/if}{outline}
```

- 当有导演时：
  ```
  导演: 张三
  
  这是一部精彩的剧情片...
  ```
- 当无导演时：
  ```
  这是一部精彩的剧情片...
  ```

**示例 5：复杂嵌套条件**

```
模板：{if:series}[{series}] {/if}{number} {if:actors}- [{actors}]{/if}
```

- 当有系列和演员时：`[经典系列] ABC-123 - [演员A、演员B]`
- 当只有演员时：`ABC-123 - [演员A、演员B]`
- 当只有系列时：`[经典系列] ABC-123`

#### 增强语法：默认值

默认值语法允许你为可能为空的字段提供备选显示内容。

**语法格式**：

```
{字段名|默认值}
```

**工作原理**：

- 当字段存在且不为空时，显示字段的实际值
- 当字段不存在或为空时，显示 `|` 后面的默认值

**示例 1：标题默认值**

```
模板：{title|无标题}
```

- 当有标题时：`经典剧情`
- 当无标题时：`无标题`

**示例 2：发行商默认值**

```
模板：发行: {publisher|未知发行商}
```

- 当有发行商时：`发行: ABC 出版社`
- 当无发行商时：`发行: 未知发行商`

**示例 3：评分默认值**

```
模板：{score|暂无评分}
```

- 当有评分时：`8.5`
- 当无评分时：`暂无评分`

**示例 4：系列默认值**

```
模板：{series|单集作品}
```

- 当有系列时：`经典系列`
- 当无系列时：`单集作品`

#### 高级用法：组合使用

##### 条件渲染 + 默认值组合

可以将条件渲染与默认值结合使用：

```
{if:publisher|未知发行商}发行: {publisher}\n{/if}
```

解析逻辑：
1. 首先检查 `publisher` 字段是否存在
2. 如果存在，显示 `发行: {publisher}`
3. 如果不存在，显示 `发行: 未知发行商`

##### 多条件组合模板

以下是一个完整信息的简介模板示例：

```
{if:title}{title}\n\n{/if}\
{if:originaltitle}{originaltitle}\n\n{/if}\
{if:actors}演员: {actors}\n\n{/if}\
{if:release}发行日期: {release}\n\n{/if}\
{if:publisher}发行: {publisher}\n{/if}\
{if:studio}片商: {studio}{/if}\
\n\n\
{if:outline}【中文简介】\n{outline}\n\n{/if}\
{if:originalplot}【日文剧情】\n{originalplot}{/if}
```

这个模板会生成一个包含所有可用信息的完整简介：

```
经典剧情

クラシックドラマ

演员: 演员A、演员B、演员C

发行日期: 2024-01-15

发行: ABC 出版社
片商: XYZ 工作室

【中文简介】
这是一部精彩的剧情片，讲述了感人至深的故事。

【日文剧情】
心を打つ感動的な物語を語った素晴らしいドラマです。
```

#### 丰富的模板示例

##### 简单标题模板

**示例 1：仅番号**

```json
{
  "vsmeta_custom_title": "{number}"
}
```

效果：`ABC-123`

**示例 2：番号 + 中文标题**

```json
{
  "vsmeta_custom_title": "{number} - {title}"
}
```

效果：`ABC-123 - 经典剧情`

**示例 3：番号 + 中文标题 + 日文原名**

```json
{
  "vsmeta_custom_title": "{number} - {title} ({originaltitle})"
}
```

效果：`ABC-123 - 经典剧情 (クラシックドラマ)`

**示例 4：带括号格式**

```json
{
  "vsmeta_custom_title": "[{number}] {title}"
}
```

效果：`[ABC-123] 经典剧情`

##### 复杂标题模板

**示例 5：包含系列信息**

```json
{
  "vsmeta_custom_title": "{if:series}[{series}] {/if}{number} - {title}"
}
```

- 有系列时：`[经典系列] ABC-123 - 经典剧情`
- 无系列时：`ABC-123 - 经典剧情`

**示例 6：包含评分**

```json
{
  "vsmeta_custom_title": "{if:score}[{score}] {/if}{number} - {title}"
}
```

- 有评分时：`[8.5] ABC-123 - 经典剧情`
- 无评分时：`ABC-123 - 经典剧情`

**示例 7：完整信息标题**

```json
{
  "vsmeta_custom_title": "{if:series}[{series}] {/if}{number} - {title} {if:actors}[{actors}]{/if}"
}
```

效果示例：`[经典系列] ABC-123 - 经典剧情 [演员A、演员B、演员C]`

##### 副标题模板示例

**示例 8：发行商/片商**

```json
{
  "vsmeta_custom_title2": "{publisher} / {studio}"
}
```

效果：`ABC 出版社 / XYZ 工作室`

**示例 9：仅演员列表**

```json
{
  "vsmeta_custom_title2": "{actors}"
}
```

效果：`演员A、演员B、演员C`

**示例 10：发行日期**

```json
{
  "vsmeta_custom_title2": "{release}"
}
```

效果：`2024-01-15`

**示例 11：带条件的评分和时长**

```json
{
  "vsmeta_custom_title2": "{if:score}评分: {score}{/if}{if:runtime} | 时长: {runtime}分钟{/if}"
}
```

- 有评分和时长时：`评分: 8.5 | 时长: 120分钟`
- 只有评分时：`评分: 8.5`

**示例 12：导演信息**

```json
{
  "vsmeta_custom_title2": "{if:director}导演: {director}{/if}"
}
```

- 有导演时：`导演: 张三`
- 无导演时：（不显示）

##### 简介模板示例

**示例 13：原名 + 中文简介**

```json
{
  "vsmeta_custom_summary": "{originaltitle}\n\n{outline}"
}
```

效果：
```
クラシックドラマ

这是一部精彩的剧情片，讲述了感人至深的故事。
```

**示例 14：三段式完整简介**

```json
{
  "vsmeta_custom_summary": "{originaltitle}\n\n{outline}\n\n{originalplot}"
}
```

效果：
```
クラシックドラマ

这是一部精彩的剧情片，讲述了感人至深的故事。

心を打つ感動的な物語を語った素晴らしいドラマです。
```

**示例 15：带元数据的简介**

```json
{
  "vsmeta_custom_summary": "{if:title}{title}\n\n{/if}{outline}\n\n发行: {publisher|未知发行商}\n片商: {studio|未知片商}"
}
```

效果示例：
```
经典剧情

这是一部精彩的剧情片，讲述了感人至深的故事。

发行: ABC 出版社
片商: XYZ 工作室
```

**示例 16：演员信息简介**

```json
{
  "vsmeta_custom_summary": "演员: {actors}\n\n{outline}"
}
```

效果：
```
演员: 演员A、演员B、演员C

这是一部精彩的剧情片，讲述了感人至深的故事。
```

**示例 17：详细元数据简介**

```json
{
  "vsmeta_custom_summary": "发行日期: {release}\n类型: {genre}\n评分: {score|暂无}\n\n{outline}"
}
```

效果：
```
发行日期: 2024-01-15
类型: 剧情、爱情
评分: 8.5

这是一部精彩的剧情片，讲述了感人至深的故事。
```

##### 预设模板快速参考

系统内置了多个预设模板，可以直接使用：

**标题预设**：

| 预设名称 | 模板内容 |
|----------|----------|
| 番号-标题(原名) | `{number} - {title} ({originaltitle})` |
| 番号-标题 | `{number} - {title}` |
| 番号 (原名) | `{number} ({originaltitle})` |
| 仅标题 | `{title}` |
| 仅原名 | `{originaltitle}` |
| 完整信息 | `{if:series}[{series}] {/if}{number} - {title} {if:actors}[{actors}]{/if}` |
| 评分-标题 | `{if:score}[{score}] {/if}{number} - {title}` |

**副标题预设**：

| 预设名称 | 模板内容 |
|----------|----------|
| 发行商/片商 | `{publisher} / {studio}` |
| 片商/系列 | `{studio} / {series}` |
| 演员 | `{actors}` |
| 发行日期 | `{release}` |
| 导演 | `{if:director}导演: {director}{/if}` |
| 评分/时长 | `{if:score}评分: {score}{/if}{if:runtime} \| 时长: {runtime}分钟{/if}` |
| 标签/类型 | `{genre}` |

**简介预设**：

| 预设名称 | 模板内容 |
|----------|----------|
| 原名+简介+剧情 | `{originaltitle}\n\n{outline}\n\n{originalplot}` |
| 原名+简介 | `{originaltitle}\n\n{outline}` |
| 原名+剧情 | `{originaltitle}\n\n{originalplot}` |
| 仅简介 | `{outline}` |
| 完整信息 | 包含所有可用信息的完整简介 |

#### 常见问题解答

**Q1：为什么我的条件渲染不生效？**

请确保 `{if:}` 和 `{/if}` 标签正确配对使用。每个 `{if:字段}` 必须有对应的 `{/if}`。检查方法：
- 打开模板，确认每个 `{if:` 都有对应的 `{/if}`
- 条件标签不能嵌套错误，例如：`{if:a}{if:b}...{/if}...{/if}` 是正确的，但 `{if:a}{if:b}...{/if}` 缺少一个 `{/if}`

**Q2：字段为空时会显示什么？**

- 如果没有使用默认值语法，空字段会显示为空字符串（即什么都不显示）
- 如果使用了默认值语法，例如 `{title|无标题}`，空字段会显示默认值 "无标题"

**Q3：可以使用多个条件标签吗？**

是的，可以在一个模板中使用多个条件标签。例如：
```
{if:series}[{series}] {/if}{number} {if:actors}[{actors}]{/if} {if:score}[{score}]{/if}
```

**Q4：条件标签可以嵌套吗？**

可以，但建议保持嵌套结构清晰。例如：
```
{if:series}[{series}] {if:score}({score}){/if}{/if}{number}
```

**Q5：如何处理换行？**

在 JSON 字符串中，换行使用 `\n` 表示。例如：
```
{originaltitle}\n\n{outline}
```
两个 `\n` 会产生一个空行。

**Q6：占位符名称大小写敏感吗？**

是的，占位符名称必须完全匹配，例如使用 `{title}` 而不是 `{Title}` 或 `{TITLE}`。

**Q7：如何避免字段为空时出现多余的分隔符？**

使用条件渲染来处理分隔符。例如：
```
错误写法：{title} | {publisher} | {studio}
正确写法：{title}{if:publisher} | {publisher}{/if}{if:studio} | {studio}{/if}
```

**Q8：演员列表最多显示几个？**

演员列表默认最多显示3个演员（可通过 `actor_name_max` 配置），多个演员之间用顿号（`、`）分隔。

#### 最佳实践建议

##### 1. 标题模板建议

- **简洁优先**：对于大多数用户，`{number} - {title}` 格式足够清晰
- **信息丰富**：需要更多信息时，使用 `{if:series}[{series}] {/if}{number} - {title}`
- **避免过长**：标题过长可能影响显示效果，建议控制在合理长度内

##### 2. 副标题模板建议

- **相关性强**：副标题应与主标题内容相关，如 `{publisher} / {studio}`
- **条件使用**：对于可选字段（如导演），使用条件渲染避免空白
- **信息分层**：副标题用于补充主标题未包含的重要信息

##### 3. 简介模板建议

- **结构清晰**：使用空行分隔不同部分，如 `{originaltitle}\n\n{outline}\n\n{originalplot}`
- **包含元数据**：在简介开头包含关键元数据（演员、发行日期等）
- **使用默认值**：对可选字段使用默认值，避免完全空白

##### 4. 性能考虑

- **避免过度嵌套**：过多嵌套的条件标签可能影响解析性能
- **简洁模板**：模板越简洁，解析速度越快
- **合理使用默认值**：默认值会增加模板复杂度，按需使用

##### 5. 兼容性考虑

- **测试不同场景**：确保模板在各种数据完整度下都能正确显示
- **处理空字段**：测试字段为空时的显示效果
- **跨服务器测试**：如果使用多个媒体服务器，建议在各服务器上测试显示效果

##### 6. 维护建议

- **注释模板**：复杂的自定义模板建议添加注释说明用途
- **版本记录**：记录不同配置版本，方便回溯
- **预设模板**：可以从预设模板开始，逐步修改以适应需求

### 完整配置示例

以下是 VSMETA 配置的完整示例，展示了各种配置的组合使用：

```json
{
  "vsmeta_show_title": "NUMBER_TITLE",
  "vsmeta_show_title2": "PUBLISHER_STUDIO",
  "vsmeta_summary": "JP_ZH_JP",
  "vsmeta_keep_ext": false,
  "vsmeta_include_poster": true,
  "vsmeta_include_backdrop": true,
  "vsmeta_locked": true,
  "vsmeta_image_max_dimension": 1920,
  "vsmeta_jpeg_quality": 90,
  "vsmeta_actor_limit": 20,
  "vsmeta_tag_limit": 10,
  "vsmeta_custom_title": "{number} - {title}",
  "vsmeta_custom_title2": "{publisher} / {studio}",
  "vsmeta_custom_summary": "{originaltitle}\n\n{outline}\n\n{originalplot}"
}
```

#### 简化配置示例

如果只需要基本配置，可以使用以下简化版本：

```json
{
  "vsmeta_show_title": "title",
  "vsmeta_show_title2": "originaltitle",
  "vsmeta_summary": "jp_zh_jp"
}
```

#### 隐私保护配置示例

如果需要减少 VSMETA 中嵌入的信息量：

```json
{
  "vsmeta_show_title": "NUMBER_ONLY",
  "vsmeta_show_title2": "NONE",
  "vsmeta_summary": "NONE",
  "vsmeta_include_poster": true,
  "vsmeta_include_backdrop": false,
  "vsmeta_actor_limit": 5,
  "vsmeta_tag_limit": 5
}
```

### 最佳配置建议

#### 1. 标题配置建议

- **日常使用**：推荐使用 `NUMBER_TITLE` 或 `TITLE` 模式，兼顾识别度和美观度
- **番好型用户**：推荐使用 `NUMBER_ONLY` 模式，简洁明了
- **日语学习者**：推荐使用 `NUMBER_ORIGINALTITLE` 或 `TITLE_ORIGINALTITLE` 模式

#### 2. 副标题配置建议

- **一般用户**：推荐使用 `ORIGINALTITLE` 或 `PUBLISHER` 模式
- **系列收藏者**：推荐使用 `SERIES` 模式
- **演员粉丝**：推荐使用 `ACTOR` 模式

#### 3. 简介配置建议

- **完整信息**：推荐使用 `JP_ZH_JP` 或 `ZH_JP` 模式
- **简洁信息**：推荐使用 `OUTLINE` 或 `ORIGINALPLOT` 模式
- **隐私保护**：推荐使用 `NONE` 模式

#### 4. 性能与质量建议

- **图片质量**：建议 `vsmeta_jpeg_quality` 设置在 85-95 之间
- **图片尺寸**：建议 `vsmeta_image_max_dimension` 设置在 1920-2048 之间
- **信息限制**：建议 `vsmeta_actor_limit` 和 `vsmeta_tag_limit` 根据实际需要设置

#### 5. 媒体服务器兼容性

- **Emby**：推荐使用默认配置，所有功能完全支持
- **Jellyfin**：推荐使用默认配置，大多数功能支持
- **其他服务器**：建议测试后再决定具体配置

---

## 附录

### 模板变量说明

在命名模板中可以使用以下变量：

- `{{ number }}` - 番号
- `{{ title }}` - 标题（翻译后）
- `{{ originaltitle }}` - 原始标题
- `{{ actor }}` - 演员名
- `{{ actors }}` - 所有演员
- `{{ release }}` - 发布日期
- `{{ year }}` - 年份
- `{{ studio }}` - 工作室
- `{{ publisher }}` - 发行商
- `{{ series }}` - 系列
- `{{ runtime }}` - 时长
- `{{ score }}` - 评分

### 版本兼容性

- Config V2 是当前最新版本
- 旧版本配置会自动迁移到新版本
- 如遇到兼容性问题，请参考 `migrations.py`

### 更多资源

- [开发文档](./DEVELOPMENT.md)
- [用户指南](./USER_GUIDE.md)
- [GitHub 仓库](https://github.com)

---

*本文档最后更新时间：2024年*
