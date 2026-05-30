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
