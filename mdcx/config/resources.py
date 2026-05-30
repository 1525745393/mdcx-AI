import os
import sys
import traceback
from pathlib import Path

import zhconv
from lxml import etree
from PyQt6.QtGui import QFontDatabase

from ..consts import IS_PYINSTALLER, MAIN_PATH
from ..manual import ManualConfig
from ..signals import signal
from ..utils import singleton
from ..utils.file import copy_file_sync
from ..utils.perf import perf_monitor
from .manager import manager


@singleton
class Resources:
    def __init__(self):
        # 获取内置资源路径和用户数据路径
        self._resources_base = MAIN_PATH / "resources"
        if IS_PYINSTALLER:
            # 获取 pyinstaller 打包程序运行时解压资源的临时目录
            try:
                self._resources_base = Path(sys._MEIPASS) / "resources"  # type: ignore
            except Exception:
                signal.show_traceback_log(self._resources_base)
                signal.show_traceback_log(traceback.format_exc())
        self._userdata_base = manager.data_folder / "userdata"
        self._userdata_base.mkdir(parents=True, exist_ok=True)  # 确保用户数据目录存在

        # 获取资源路径
        self.actor_map_backup_path = self.r("mapping_table/mapping_actor.xml")  # 内置演员映射表的文件路径
        self.info_map_backup_path = self.r("mapping_table/mapping_info.xml")  # 内置信息映射表的文件路径

        self.icon_ico = self.qtr("Img/MDCx.ico")  # 任务栏图标
        self.right_menu = self.qtr("Img/menu.svg")  # 主界面菜单按钮
        self.play_icon = self.qtr("Img/play.svg")  # 主界面播放按钮
        self.open_folder_icon = self.qtr("Img/folder.svg")  # 主界面打开文件夹按钮
        self.open_nfo_icon = self.qtr("Img/nfo.svg")  # 主界面打开nfo按钮
        self.input_number_icon = self.qtr("Img/number.svg")  # 主界面输入番号按钮
        self.input_website_icon = self.qtr("Img/website.svg")  # 主界面输入网址按钮
        self.del_file_icon = self.qtr("Img/delfile.svg")  # 主界面删除文件按钮
        self.del_folder_icon = self.qtr("Img/delfolder.svg")  # 主界面删除文件夹按钮
        self.start_icon = self.qtr("Img/start.svg")  # 主界面开始按钮
        self.stop_icon = self.qtr("Img/stop.svg")  # 主界面开始按钮
        self.show_logs_icon = self.qtr("Img/show.svg")  # 日志界面显示日志按钮
        self.hide_logs_icon = self.qtr("Img/hide.svg")  # 日志界面隐藏日志按钮
        self.hide_boss_icon = self.qtr("Img/hide_boss.svg")  # 隐藏界面按钮
        self.save_failed_list_icon = self.qtr("Img/save.svg")  # 保存失败列表按钮
        self.clear_tree_icon = self.qtr("Img/clear.svg")  # 主界面清空结果列表按钮
        self.home_icon = self.qtr("Img/home.svg")
        self.log_icon = self.qtr("Img/log.svg")
        self.tool_icon = self.qtr("Img/tool.svg")
        self.setting_icon = self.qtr("Img/setting.svg")
        self.net_icon = self.qtr("Img/net.svg")
        self.help_icon = self.qtr("Img/help.svg")

        self.mark_4k = self.r("Img/4k.png")
        self.mark_8k = self.r("Img/8k.png")
        self.mark_sub = self.r("Img/sub.png")
        self.mark_youma = self.r("Img/youma.png")
        self.mark_umr = self.r("Img/umr.png")
        self.mark_leak = self.r("Img/leak.png")
        self.mark_wuma = self.r("Img/wuma.png")
        self.icon_4k_path = self.u("watermark/4k.png")
        self.icon_8k_path = self.u("watermark/8k.png")
        self.icon_sub_path = self.u("watermark/sub.png")
        self.icon_youma_path = self.u("watermark/youma.png")
        self.icon_umr_path = self.u("watermark/umr.png")
        self.icon_leak_path = self.u("watermark/leak.png")
        self.icon_wuma_path = self.u("watermark/wuma.png")

        self.actor_mapping_data = None  # 演员映射表数据
        self.info_mapping_data = None  # 信息映射表数据

        # 性能优化：索引缓存
        self._actor_index: dict[str, dict] = {}
        self._info_index: dict[str, dict] = {}
        self._actor_cache: dict[str, dict] = {}
        self._info_cache: dict[str, dict] = {}

        self._get_or_generate_local_data()
        self._get_mark_icon()
        zhconv.loaddict(str(self.r("zhconv/zhcdict.json")))  # 加载繁简转换字典

    def _normalize_key(self, key: str) -> str:
        """将字符串规范化为统一的查找键"""
        key = key.upper()
        for each in ManualConfig.FULL_HALF_CHAR:
            key = key.replace(each[0], each[1])
        return key

    def r(self, relative_path: str | Path):
        return self._resources_base / relative_path

    def qtr(self, relative_path: str | Path):
        # Qt 内部所有路径都使用正斜杠
        return self.r(relative_path).as_posix()

    def u(self, relative_path: str | Path):
        return self._userdata_base / relative_path

    def get_actor_data(self, actor):
        with perf_monitor.timeit("get_actor_data", category="mapping"):
            # 快速路径：检查缓存
            cache_key = actor
            if cache_key in self._actor_cache:
                return self._actor_cache[cache_key].copy()

            # 初始化数据
            actor_data = {
                "zh_cn": actor,
                "zh_tw": actor,
                "jp": actor,
                "keyword": [actor],
                "href": "",
                "has_name": False,
            }

            # 优化路径：使用预构建的索引
            normalized_actor = self._normalize_key(actor)
            actor_key = f",{normalized_actor},"

            if actor_key in self._actor_index:
                actor_data = self._actor_index[actor_key].copy()
                actor_data["has_name"] = True

            # 缓存结果
            self._actor_cache[cache_key] = actor_data.copy()
            return actor_data

    def get_info_data(self, info):
        with perf_monitor.timeit("get_info_data", category="mapping"):
            # 快速路径：检查缓存
            cache_key = info
            if cache_key in self._info_cache:
                return self._info_cache[cache_key].copy()

            # 初始化数据
            info_data = {
                "zh_cn": info,
                "zh_tw": info,
                "jp": info,
                "keyword": [info],
                "has_name": False,
            }

            # 优化路径：使用预构建的索引
            normalized_info = self._normalize_key(info)
            info_key = f",{normalized_info},"

            # 检查各种可能的匹配
            match = self._info_index.get(info_key)
            if match is None:
                match = self._info_index.get(normalized_info)

            if match is not None:
                info_data = match.copy()
                info_data["has_name"] = True

            # 缓存结果
            self._info_cache[cache_key] = info_data.copy()
            return info_data

    def get_fonts(self):
        font_folder_path = self.qtr("fonts")
        for f in os.listdir(font_folder_path):
            QFontDatabase.addApplicationFont(os.path.join(font_folder_path, f))  # 字体路径

    def _get_or_generate_local_data(self):
        """如果用户数据目录下已有数据则直接读取, 否则根据内置数据生成"""
        # 载入 mapping_actor.xml mapping_info.xml 数据
        actor_map_local_path = self.u("mapping_actor.xml")
        info_map_local_path = self.u("mapping_info.xml")
        if not os.path.exists(actor_map_local_path):
            if not copy_file_sync(self.actor_map_backup_path, actor_map_local_path):
                actor_map_local_path = self.actor_map_backup_path
        if not os.path.exists(info_map_local_path):
            if not copy_file_sync(self.info_map_backup_path, info_map_local_path):
                info_map_local_path = self.info_map_backup_path
        try:
            parser = etree.HTMLParser(encoding="utf-8")
            with open(actor_map_local_path, encoding="utf-8") as f:
                content = f.read()
            self.actor_mapping_data = etree.HTML(content.encode("utf-8"), parser=parser)
            with open(info_map_local_path, encoding="utf-8") as f:
                content = f.read()
            self.info_mapping_data = etree.HTML(content.encode("utf-8"), parser=parser)

            # 性能优化：预构建索引
            self._build_actor_index()
            self._build_info_index()
        except Exception as e:
            signal.show_log_text(
                f" {actor_map_local_path} 读取失败！请检查该文件是否存在问题！如需重置请删除该文件！错误信息：\n{str(e)}"
            )
            signal.show_traceback_log(traceback.format_exc())
            signal.show_log_text(traceback.format_exc())
            self.actor_mapping_data = None

    def _build_actor_index(self):
        """预构建演员映射表的索引"""
        if self.actor_mapping_data is None:
            return

        with perf_monitor.timeit("build_actor_index", category="mapping"):
            actor_elements = self.actor_mapping_data.xpath("//a")
            for elem in actor_elements:
                keyword = elem.get("keyword", "")
                if keyword:
                    # 构建所有可能的匹配键
                    normalized_keywords = []
                    for kw in keyword.strip(",").split(","):
                        normalized_kw = self._normalize_key(kw)
                        normalized_keywords.append(normalized_kw)

                    actor_data = {
                        "zh_cn": elem.get("zh_cn", ""),
                        "zh_tw": elem.get("zh_tw", ""),
                        "jp": elem.get("jp", ""),
                        "keyword": keyword.strip(",").split(","),
                        "href": elem.get("href", ""),
                        "has_name": False,
                    }

                    # 索引：keyword 列表中的每一项
                    for kw in normalized_keywords:
                        self._actor_index[f",{kw},"] = actor_data

    def _build_info_index(self):
        """预构建信息映射表的索引"""
        if self.info_mapping_data is None:
            return

        with perf_monitor.timeit("build_info_index", category="mapping"):
            info_elements = self.info_mapping_data.xpath("//a")
            for elem in info_elements:
                zh_cn = elem.get("zh_cn", "")
                zh_tw = elem.get("zh_tw", "")
                jp = elem.get("jp", "")
                keyword = elem.get("keyword", "")

                # 移除标记
                zh_cn_clean = zh_cn.replace("删除", "")
                zh_tw_clean = zh_tw.replace("删除", "")
                jp_clean = jp.replace("删除", "")

                info_data = {
                    "zh_cn": zh_cn_clean,
                    "zh_tw": zh_tw_clean,
                    "jp": jp_clean,
                    "keyword": keyword.strip(",").split(",") if keyword else [],
                    "has_name": False,
                }

                # 索引：keyword 列表中的每一项
                if keyword:
                    for kw in keyword.strip(",").split(","):
                        normalized_kw = self._normalize_key(kw)
                        self._info_index[f",{normalized_kw},"] = info_data
                        self._info_index[normalized_kw] = info_data

                # 索引：zh_cn、zh_tw、jp
                for name in [zh_cn_clean, zh_tw_clean, jp_clean]:
                    if name:
                        normalized_name = self._normalize_key(name)
                        self._info_index[normalized_name] = info_data

    def _get_mark_icon(self):
        mark_folder = self.u("watermark")
        if not os.path.isdir(mark_folder):
            os.makedirs(mark_folder)
        if not os.path.isfile(self.icon_4k_path):
            copy_file_sync(self.mark_4k, self.icon_4k_path)
        if not os.path.isfile(self.icon_8k_path):
            copy_file_sync(self.mark_8k, self.icon_8k_path)
        if not os.path.isfile(self.icon_sub_path):
            copy_file_sync(self.mark_sub, self.icon_sub_path)
        if not os.path.isfile(self.icon_youma_path):
            copy_file_sync(self.mark_youma, self.icon_youma_path)
        if not os.path.isfile(self.icon_umr_path):
            copy_file_sync(self.mark_umr, self.icon_umr_path)
        if not os.path.isfile(self.icon_leak_path):
            copy_file_sync(self.mark_leak, self.icon_leak_path)
        if not os.path.isfile(self.icon_wuma_path):
            copy_file_sync(self.mark_wuma, self.icon_wuma_path)


resources = Resources()
