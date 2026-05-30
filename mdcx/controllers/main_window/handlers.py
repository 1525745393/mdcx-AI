import time
import webbrowser

from mdcx.config.enums import VsmetaShowTitle, VsmetaShowTitle2, VsmetaSummary
from mdcx.config.manager import manager
from mdcx.signals import signal_qt


def show_netstatus() -> None:
    signal_qt.show_net_info(time.strftime("%Y-%m-%d %H:%M:%S").center(80, "="))

    use_proxy, proxy, cf_bypass_url, cf_bypass_proxy, timeout, retry_count = (
        manager.config.use_proxy,
        manager.config.proxy,
        manager.config.cf_bypass_url,
        manager.config.cf_bypass_proxy,
        manager.config.timeout,
        manager.config.retry,
    )
    bypass_status = "已配置" if cf_bypass_url else "未配置"
    bypass_proxy_status = "已配置" if cf_bypass_proxy else "未配置"

    if not use_proxy or not proxy:
        signal_qt.show_net_info(
            f" 当前网络状态：❌ 未启用代理\n"
            f"   CF Bypass：{bypass_status}    Bypass代理：{bypass_proxy_status}    超时：{str(timeout)}    重试：{str(retry_count)}"
        )
    else:
        signal_qt.show_net_info(
            f" 当前网络状态：✅ 已启用代理\n"
            f"   地址：{proxy}\n"
            f"   CF Bypass：{bypass_status}    Bypass代理：{bypass_proxy_status}    超时：{str(timeout)}    重试：{str(retry_count)}"
        )
    signal_qt.show_net_info("=" * 80)


def apply_vsmeta_preset_recommended(self):
    """推荐配置：平衡图片质量和文件大小"""
    self.Ui.checkBox_vsmeta_include_poster.setChecked(True)
    self.Ui.checkBox_vsmeta_include_backdrop.setChecked(True)
    self.Ui.checkBox_vsmeta_locked.setChecked(True)
    self.Ui.spinBox_vsmeta_image_dimension.setValue(1920)
    self.Ui.slider_vsmeta_jpeg_quality.setValue(90)
    self.Ui.label_vsmeta_jpeg_value.setText("90")
    self.Ui.spinBox_vsmeta_actor_limit.setValue(20)
    self.Ui.spinBox_vsmeta_tag_limit.setValue(10)
    self.Ui.comboBox_vsmeta_show_title.setCurrentIndex(list(VsmetaShowTitle).index(VsmetaShowTitle.TITLE))
    self.Ui.comboBox_vsmeta_show_title2.setCurrentIndex(list(VsmetaShowTitle2).index(VsmetaShowTitle2.ORIGINALTITLE))
    self.Ui.comboBox_vsmeta_summary.setCurrentIndex(list(VsmetaSummary).index(VsmetaSummary.JP_ZH_JP))
    signal_qt.show_log_text("✅ 已应用 VSMETA 推荐配置")


def apply_vsmeta_preset_high_quality(self):
    """高画质配置：高质量图片设置"""
    self.Ui.checkBox_vsmeta_include_poster.setChecked(True)
    self.Ui.checkBox_vsmeta_include_backdrop.setChecked(True)
    self.Ui.checkBox_vsmeta_locked.setChecked(True)
    self.Ui.spinBox_vsmeta_image_dimension.setValue(2160)
    self.Ui.slider_vsmeta_jpeg_quality.setValue(100)
    self.Ui.label_vsmeta_jpeg_value.setText("100")
    self.Ui.spinBox_vsmeta_actor_limit.setValue(50)
    self.Ui.spinBox_vsmeta_tag_limit.setValue(30)
    self.Ui.comboBox_vsmeta_show_title.setCurrentIndex(list(VsmetaShowTitle).index(VsmetaShowTitle.NUMBER_TITLE))
    self.Ui.comboBox_vsmeta_show_title2.setCurrentIndex(list(VsmetaShowTitle2).index(VsmetaShowTitle2.ORIGINALTITLE))
    self.Ui.comboBox_vsmeta_summary.setCurrentIndex(list(VsmetaSummary).index(VsmetaSummary.JP_ZH_JP))
    signal_qt.show_log_text("✅ 已应用 VSMETA 高画质配置")


def apply_vsmeta_preset_small_file(self):
    """最小文件配置：节省空间的配置"""
    self.Ui.checkBox_vsmeta_include_poster.setChecked(False)
    self.Ui.checkBox_vsmeta_include_backdrop.setChecked(False)
    self.Ui.checkBox_vsmeta_locked.setChecked(True)
    self.Ui.spinBox_vsmeta_image_dimension.setValue(1080)
    self.Ui.slider_vsmeta_jpeg_quality.setValue(70)
    self.Ui.label_vsmeta_jpeg_value.setText("70")
    self.Ui.spinBox_vsmeta_actor_limit.setValue(5)
    self.Ui.spinBox_vsmeta_tag_limit.setValue(5)
    self.Ui.comboBox_vsmeta_show_title.setCurrentIndex(list(VsmetaShowTitle).index(VsmetaShowTitle.TITLE))
    self.Ui.comboBox_vsmeta_show_title2.setCurrentIndex(list(VsmetaShowTitle2).index(VsmetaShowTitle2.NONE))
    self.Ui.comboBox_vsmeta_summary.setCurrentIndex(list(VsmetaSummary).index(VsmetaSummary.OUTLINE))
    signal_qt.show_log_text("✅ 已应用 VSMETA 最小文件配置")


def reset_vsmeta_to_default(self):
    """重置为默认值"""
    # 使用配置模型中的默认值
    self.Ui.checkBox_vsmeta_include_poster.setChecked(True)
    self.Ui.checkBox_vsmeta_include_backdrop.setChecked(True)
    self.Ui.checkBox_vsmeta_locked.setChecked(True)
    self.Ui.spinBox_vsmeta_image_dimension.setValue(1920)
    self.Ui.slider_vsmeta_jpeg_quality.setValue(90)
    self.Ui.label_vsmeta_jpeg_value.setText("90")
    self.Ui.spinBox_vsmeta_actor_limit.setValue(20)
    self.Ui.spinBox_vsmeta_tag_limit.setValue(10)
    self.Ui.comboBox_vsmeta_show_title.setCurrentIndex(list(VsmetaShowTitle).index(VsmetaShowTitle.TITLE))
    self.Ui.comboBox_vsmeta_show_title2.setCurrentIndex(list(VsmetaShowTitle2).index(VsmetaShowTitle2.ORIGINALTITLE))
    self.Ui.comboBox_vsmeta_summary.setCurrentIndex(list(VsmetaSummary).index(VsmetaSummary.JP_ZH_JP))
    signal_qt.show_log_text("✅ 已重置 VSMETA 配置为默认值")


def show_vsmeta_help(self):
    """显示 VSMETA 帮助"""
    webbrowser.open("https://www.synology.com/zh-cn/knowledgebase/DSM/help/VideoStation/VideoStation_desc")


def update_vsmeta_preview(self):
    """更新 VSMETA 预览"""
    try:
        from mdcx.config.enums import VsmetaShowTitle, VsmetaShowTitle2, VsmetaSummary
        
        # 模拟数据
        sample_data = {
            "number": "ABP-123",
            "title": "超人气演员的精彩演出",
            "originaltitle": "大人気女優の素敵な演技",
            "publisher": "Premium",
            "studio": "Premium",
            "series": "Premium EX",
            "actors": ["演员A", "演员B", "演员C"],
            "outline": "这是一部精彩的影片，讲述了精彩的故事内容，非常值得观看。",
            "originalplot": "これは素敵な映画で、素敵なストーリーを描いています。是非ご覧ください。"
        }
        
        # 生成标题预览
        title_mode = VsmetaShowTitle(list(VsmetaShowTitle)[self.Ui.comboBox_vsmeta_show_title.currentIndex()])
        if title_mode == VsmetaShowTitle.TITLE:
            preview_title = sample_data["title"]
        elif title_mode == VsmetaShowTitle.NUMBER_TITLE and sample_data["title"] and sample_data["number"]:
            preview_title = f"[{sample_data['number']}] {sample_data['title']}"
        elif title_mode == VsmetaShowTitle.NUMBER_ONLY and sample_data["number"]:
            preview_title = sample_data["number"]
        elif title_mode == VsmetaShowTitle.NUMBER_ORIGINALTITLE and sample_data["number"] and sample_data["originaltitle"]:
            preview_title = f"[{sample_data['number']}] {sample_data['originaltitle']}"
        elif title_mode == VsmetaShowTitle.TITLE_ORIGINALTITLE and sample_data["title"] and sample_data["originaltitle"]:
            preview_title = f"{sample_data['title']} | {sample_data['originaltitle']}"
        elif title_mode == VsmetaShowTitle.ORIGINALTITLE_TITLE and sample_data["originaltitle"] and sample_data["title"]:
            preview_title = f"{sample_data['originaltitle']} | {sample_data['title']}"
        else:
            preview_title = sample_data["title"] or sample_data["number"]
        
        # 生成副标题预览
        title2_mode = VsmetaShowTitle2(list(VsmetaShowTitle2)[self.Ui.comboBox_vsmeta_show_title2.currentIndex()])
        if title2_mode == VsmetaShowTitle2.ORIGINALTITLE:
            preview_title2 = sample_data["originaltitle"]
        elif title2_mode == VsmetaShowTitle2.PUBLISHER:
            preview_title2 = sample_data["publisher"]
        elif title2_mode == VsmetaShowTitle2.STUDIO:
            preview_title2 = sample_data["studio"]
        elif title2_mode == VsmetaShowTitle2.PUBLISHER_STUDIO:
            parts = []
            if sample_data["publisher"]:
                parts.append(sample_data["publisher"])
            if sample_data["studio"] and sample_data["studio"] != sample_data["publisher"]:
                parts.append(sample_data["studio"])
            preview_title2 = " | ".join(parts) if parts else ""
        elif title2_mode == VsmetaShowTitle2.SERIES:
            preview_title2 = sample_data["series"]
        elif title2_mode == VsmetaShowTitle2.ACTOR:
            preview_title2 = ", ".join(sample_data["actors"][:3]) if sample_data["actors"] else ""
        else:
            preview_title2 = ""
        
        # 生成简介预览
        summary_mode = VsmetaSummary(list(VsmetaSummary)[self.Ui.comboBox_vsmeta_summary.currentIndex()])
        summary_parts = []
        if summary_mode == VsmetaSummary.JP_ZH_JP:
            if sample_data["originaltitle"]:
                summary_parts.append(sample_data["originaltitle"])
            if sample_data["outline"]:
                summary_parts.append(sample_data["outline"])
            if sample_data["originalplot"] and sample_data["originalplot"] != sample_data["outline"]:
                summary_parts.append(sample_data["originalplot"])
        elif summary_mode == VsmetaSummary.OUTLINE:
            if sample_data["outline"]:
                summary_parts.append(sample_data["outline"])
        elif summary_mode == VsmetaSummary.ORIGINALPLOT:
            if sample_data["originalplot"]:
                summary_parts.append(sample_data["originalplot"])
        elif summary_mode == VsmetaSummary.ZH_JP:
            if sample_data["outline"]:
                summary_parts.append(sample_data["outline"])
            if sample_data["originalplot"] and sample_data["originalplot"] != sample_data["outline"]:
                summary_parts.append(sample_data["originalplot"])
        elif summary_mode == VsmetaSummary.JP_ZH:
            if sample_data["originaltitle"]:
                summary_parts.append(sample_data["originaltitle"])
            if sample_data["outline"]:
                summary_parts.append(sample_data["outline"])
        elif summary_mode == VsmetaSummary.TITLE_ONLY:
            if sample_data["originaltitle"]:
                summary_parts.append(sample_data["originaltitle"])
        elif summary_mode == VsmetaSummary.OUTLINE_PUBLISHER:
            if sample_data["outline"]:
                summary_parts.append(sample_data["outline"])
            info_parts = []
            if sample_data["publisher"]:
                info_parts.append(f"制作商: {sample_data['publisher']}")
            if sample_data["studio"] and sample_data["studio"] != sample_data["publisher"]:
                info_parts.append(f"工作室: {sample_data['studio']}")
            if info_parts:
                summary_parts.append("---")
                summary_parts.append("\n".join(info_parts))
        elif summary_mode == VsmetaSummary.NUMBER_TITLE:
            if sample_data["number"]:
                summary_parts.append(f"番号: {sample_data['number']}")
            if sample_data["title"]:
                summary_parts.append(sample_data["title"])
        
        preview_summary = "\n\n".join(summary_parts) if summary_parts else ""
        
        # 更新 UI
        self.Ui.label_preview_title.setText(preview_title or "（标题为空）")
        self.Ui.label_preview_title2.setText(preview_title2 or "（副标题为空）")
        self.Ui.label_preview_summary.setText(preview_summary or "（简介为空）")
    except Exception as e:
        import traceback
        from mdcx.signals import signal_qt
        signal_qt.show_traceback_log(traceback.format_exc())
