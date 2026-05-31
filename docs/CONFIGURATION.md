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
