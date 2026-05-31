# MDCx 常见问题解答（FAQ）

> 📖 **更多文档**: [文档中心](docs/README.md) | [主 README](README.md) | [用户手册](USER_GUIDE.md) | [配置说明](docs/CONFIGURATION.md)

欢迎使用 MDCx！本文档收集了用户最常遇到的问题及其解决方案，帮助您快速上手和解决使用过程中的问题。

---

## 目录

1. [安装和启动](#安装和启动)
2. [配置问题](#配置问题)
3. [使用问题](#使用问题)
4. [刮削问题](#刮削问题)
5. [VSMETA 问题](#vsmeta-问题)
6. [翻译问题](#翻译问题)
7. [Emby/Jellyfin 集成问题](#embyjellyfin-集成问题)
8. [网络问题](#网络问题)
9. [故障排除](#故障排除)
10. [其他常见问题](#其他常见问题)

---

## 安装和启动

### Q: MDCx 支持哪些操作系统？
A: MDCx 支持 Windows 10+、macOS 10.15+ 和 Linux。Windows 7 用户需要使用 Python 3.8 进行本地构建。

### Q: 如何安装 MDCx？
A: 有两种安装方式：
1. **推荐方式**：从 [GitHub Release](https://github.com/1525745393/mdcx-AI/releases/latest) 页面下载预编译版本，解压后直接运行。
2. **从源码运行**：
   ```bash
   git clone https://github.com/1525745393/mdcx-AI.git
   cd mdcx-AI
   uv sync --locked --all-extras --dev
   uv run python main.py
   ```

### Q: 首次启动需要注意什么？
A: 首次启动时，程序会自动：
- 在用户目录下创建配置文件夹
- 生成默认配置文件
- 显示主界面

您只需要在首次使用时配置好媒体路径即可。

### Q: Python 版本有要求吗？
A: 如果从源码运行，需要 Python 3.13+。预编译版本不需要单独安装 Python。

---

## 配置问题

### Q: 配置文件保存在哪里？
A: 配置文件位置取决于您的操作系统：
- Windows: `%APPDATA%\MDCx\`
- macOS: `~/Library/Application Support/MDCx/`
- Linux: `~/.config/MDCx/`

### Q: 如何重置配置？
A: 重置配置的步骤：
1. 关闭 MDCx
2. 删除配置文件夹中的配置文件
3. 重新启动 MDCx，程序会自动生成默认配置

### Q: 媒体路径如何设置？
A: 在「设置」→「通用」中设置：
- `media_path`：存放待刮削视频文件的目录
- `success_output_folder`（可选）：刮削成功后文件移动的位置
- `failed_output_folder`（可选）：刮削失败后文件移动的位置

### Q: 线程数设置多少合适？
A: 建议 `thread_number` 设置为 20-50。过高可能导致网站反爬虫限制，过低则影响刮削效率。

### Q: 如何为不同类型的视频配置不同的刮削源？
A: 在「设置」→「网站设置」中，您可以分别为有码、无码、FC2、欧美、国产等类型配置不同的刮削源列表。

---

## 使用问题

### Q: 基本使用流程是什么？
A: 基本刮削流程：
1. 配置媒体路径
2. 选择刮削源网站
3. 配置下载选项（海报、缩略图、NFO、VSMETA 等）
4. 点击「扫描」按钮扫描媒体目录
5. 选择要刮削的文件
6. 点击「开始」按钮开始刮削

### Q: 支持哪些视频文件格式？
A: MDCx 支持以下媒体文件格式：
`.mp4`, `.avi`, `.rmvb`, `.wmv`, `.mov`, `.mkv`, `.flv`, `.ts`, `.webm`, `.iso`, `.mpg`, `.m4v`, `.hevc`

### Q: 字幕文件会被处理吗？
A: 是的，MDCx 会自动识别并处理以下字幕格式：
`.smi`, `.srt`, `.idx`, `.sub`, `.sup`, `.psb`, `.ssa`, `.ass`, `.usf`, `.xss`, `.ssf`, `.rt`, `.lrc`, `.sbv`, `.vtt`, `.ttml`

### Q: 如何自定义文件命名规则？
A: 在「设置」→「命名和格式化」中配置：
- `folder_name`：目录名称模板
- `naming_file`：文件命名模板
- 使用 Jinja2 语法，支持 `{{ number }}`、`{{ title }}`、`{{ actor }}` 等变量

### Q: 什么是 VSMETA 自定义模板？如何使用？
A: VSMETA 自定义模板允许您灵活控制 Synology Video Station 中显示的内容：
1. 进入「设置」→「命名和格式化」
2. 找到 VSMETA 设置区域
3. 将 `vsmeta_show_title`、`vsmeta_show_title2`、`vsmeta_summary` 设置为 `custom`
4. 在对应的自定义模板字段中输入您的模板

支持的占位符：`{number}`, `{title}`, `{originaltitle}`, `{publisher}`, `{studio}`, `{series}`, `{actors}`, `{outline}`, `{originalplot}`, `{year}`, `{release}`, `{score}`, `{country}`, `{director}`, `{genre}`, `{mosaic}`, `{runtime}`, `{label}`, `{website}`

支持条件语法：`{if:field}内容{/if}`

支持默认值：`{field|默认值}`

---

## 刮削问题

### Q: 哪些网站可以作为刮削源？
A: MDCx 支持 40+ 个网站，包括：
- 有码：DMM, MGStage, Prestige, Official, JavBus, Jav321, JavDB, MissAV 等
- 无码：Kin8, Love6 等
- FC2：FC2, FC2Club, FC2Hub, FC2PPVDB
- 国产：HDOUBAN, CNMDB, GUOCHAN, MADOUQU
- 欧美：THEPORNDB

### Q: 某些视频无法识别番号怎么办？
A: 可能的原因和解决方案：
1. 检查文件名是否包含完整的番号
2. 尝试手动修改文件名，使其包含正确的番号
3. 在设置中检查番号识别规则
4. 确认视频类型是否被正确识别（有码/无码/FC2 等）

### Q: 刮削结果不正确怎么办？
A: 解决方案：
1. 检查刮削源配置，尝试更换其他刮削源
2. 调整字段优先级配置
3. 查看日志了解详细信息
4. 可以尝试手动编辑生成的 NFO 文件

### Q: 如何提高刮削成功率？
A: 建议：
1. 配置多个刮削源作为备选
2. 根据您的网络条件调整网站优先级
3. 适当增加超时时间和重试次数
4. 对于欧美片，建议获取 THEPORNDB API Token

### Q: 刮削时可以跳过已处理的文件吗？
A: 可以，在「设置」→「刮削设置」中配置 `read_mode`：
- `has_nfo_update`：有 NFO 时更新
- `no_nfo_scrape`：无 NFO 时刮削
- `read_download_again`：重新下载
- `read_update_nfo`：更新 NFO

---

## VSMETA 问题

### Q: 什么是 VSMETA？
A: VSMETA 是 Synology Video Station 使用的元数据格式。MDCx 完整支持 VSMETA 格式生成，包括嵌入海报和背景图。

### Q: Synology Video Station 不显示 VSMETA 元数据怎么办？
A: 检查以下几点：
1. 确认在「下载选项」中勾选了「下载 VSMETA」
2. 检查 VSMETA 配置是否正确
3. 在 Synology Video Station 中刷新媒体库
4. 确认 VSMETA 文件与视频文件在同一目录

### Q: VSMETA 中的图片不显示怎么办？
A: 解决方案：
1. 检查 `vsmeta_include_poster` 和 `vsmeta_include_backdrop` 是否勾选
2. 尝试减小 `vsmeta_image_max_dimension` 和 `vsmeta_jpeg_quality`
3. 确认图片文件本身没有损坏

### Q: VSMETA 文件太大怎么办？
A: 可以调整以下设置来减小 VSMETA 文件大小：
- 降低 `vsmeta_image_max_dimension`（默认 1920）
- 降低 `vsmeta_jpeg_quality`（默认 90）
- 减少 `vsmeta_actor_limit`（默认 20）
- 减少 `vsmeta_tag_limit`（默认 10）

---

## 翻译问题

### Q: 支持哪些翻译服务？
A: MDCx 支持多种翻译服务：
- Google 翻译（免费，无需配置）
- 百度翻译（需要 APP ID 和密钥）
- DeepL 翻译（需要 API Key）
- DeepLX（需要配置 URL）
- LLM 翻译（支持自定义 API）

### Q: 翻译失败怎么办？
A: 排查步骤：
1. 检查翻译服务配置是否正确
2. 确认 API 密钥有效
3. 检查网络连接
4. 查看日志了解详细错误信息
5. 尝试更换其他翻译服务

### Q: 翻译质量不理想怎么办？
A: 建议：
1. 尝试更换其他翻译服务（DeepL 或 LLM 通常质量较高）
2. 对于 LLM 翻译，可以自定义提示词
3. 手动编辑 NFO 文件进行修正

### Q: 可以只翻译部分字段吗？
A: 可以，在「设置」→「字段配置」中，您可以为每个字段单独设置是否翻译。

---

## Emby/Jellyfin 集成问题

### Q: 如何配置 Emby/Jellyfin 集成？
A: 在「设置」→「服务器设置」中配置：
1. 选择服务器类型（Emby 或 Jellyfin）
2. 输入服务器地址（如 `http://192.168.1.100:8096`）
3. 输入 API 密钥
4. 勾选需要的功能（如演员信息同步、演员照片同步等）

### Q: 如何获取 Emby API 密钥？
A: 在 Emby 中：
1. 进入「设置」→「高级」→「API 密钥」
2. 点击「新建 API 密钥」
3. 输入应用名称（如 MDCx）并保存
4. 复制生成的 API 密钥到 MDCx 配置中

### Q: 演员照片无法同步怎么办？
A: 检查以下几点：
1. 确认 API 密钥和用户 ID 配置正确
2. 确认勾选了 `actor_photo_net` 或 `actor_photo_local`
3. 检查网络连接
4. 查看日志了解详细信息

---

## 网络问题

### Q: 刮削时提示网络连接失败怎么办？
A: 解决方案：
1. 检查您的网络连接
2. 在「设置」→「网络」中配置代理
3. 检查防火墙设置
4. 尝试增加超时时间和重试次数

### Q: 如何配置代理？
A: 在「设置」→「网络」中：
1. 勾选 `use_proxy`
2. 在 `proxy` 中输入代理地址（如 `http://127.0.0.1:7890`）
3. 根据需要调整 `timeout` 和 `retry`

### Q: 某些网站无法访问怎么办？
A: 可能的原因和解决方案：
1. 尝试使用代理
2. 更换其他刮削源
3. 检查该网站是否正常运行
4. 对于被 Cloudflare 保护的网站，尝试配置 `cf_bypass_url`

### Q: 遇到 Cloudflare 保护怎么办？
A: 在「设置」→「网络」中配置 `cf_bypass_url` 来绕过 Cloudflare 保护。

---

## 故障排除

### Q: 如何查看日志？
A: 有两种方式：
1. 在主界面点击「日志」按钮
2. 在配置文件夹中查找日志文件

### Q: 程序崩溃怎么办？
A: 排查步骤：
1. 查看日志文件了解错误详情
2. 尝试重置配置
3. 确认使用的是最新版本
4. 如果问题持续，在 GitHub 提交 Issue 并附上日志

### Q: 图片下载失败怎么办？
A: 解决方案：
1. 检查网络连接
2. 尝试配置代理
3. 更换其他刮削源
4. 可以勾选 `ignore_pic_fail` 忽略图片下载失败继续刮削

### Q: 文件移动失败怎么办？
A: 检查以下几点：
1. 确认目标目录存在且有写入权限
2. 检查磁盘空间是否充足
3. 确认文件没有被其他程序占用
4. 可以暂时禁用文件移动功能（`success_file_move`/`failed_file_move`）

---

## 其他常见问题

### Q: MDCx 会自动更新吗？
A: 默认情况下，MDCx 会检查更新（`update_check` 默认开启）。当有新版本时，会提示您。您也可以手动访问 GitHub Release 页面查看最新版本。

### Q: 如何获取帮助？
A: 获取帮助的途径：
1. 查看本文档和其他文档（README.md、USER_GUIDE.md、CONFIGURATION.md）
2. 加入 [Telegram 交流群](https://t.me/mdcx_chat) 与群友交流
3. 在 [GitHub Issues](https://github.com/1525745393/mdcx-AI/issues) 提交问题（请附上相关日志和问题番号）

### Q: 可以贡献代码吗？
A: 欢迎贡献代码！请参考 CONTRIBUTING.md 了解详细的贡献流程。

### Q: MDCx 可以用于商业用途吗？
A: 不可以。MDCx 使用 GPLv3 许可证，并且项目明确禁止用于商业用途。仅供学习和技术交流使用。

### Q: 使用 MDCx 需要注意什么法律问题？
A: 使用 MDCx 时请遵守当地法律法规，不要使用 MDCx 处理非法内容。法律及使用后果由使用者自己承担。

---

## 附录

### A. 快速参考：配置文件默认值
- `thread_number`：50
- `timeout`：10 秒
- `retry`：3 次
- `vsmeta_image_max_dimension`：1920
- `vsmeta_jpeg_quality`：90

### B. 快速参考：常用模板变量
- `{{ number }}`：番号
- `{{ title }}`：标题（翻译后）
- `{{ originaltitle }}`：原始标题
- `{{ actor }}`：演员名
- `{{ release }}`：发布日期
- `{{ year }}`：年份
- `{{ studio }}`：工作室
- `{{ publisher }}`：发行商

---

*本文档最后更新：2026-05-31*
*如有其他问题，欢迎加入 Telegram 交流群讨论！*