from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from mdcx.utils.crawler_health import health_monitor
from mdcx.utils.perf import get_performance_report, reset_performance_monitor

from .style import build_scrollbar_style, get_theme_tokens

if TYPE_CHECKING:
    from .main_window import MyMAinWindow


def _get_dialog_colors(dark: bool) -> dict[str, str]:
    tokens = get_theme_tokens(dark)
    if dark:
        return {
            "window": tokens["window"],
            "surface": "#1e2d3c",
            "surface_muted": "#273849",
            "text": tokens["text"],
            "text_muted": tokens["text_muted"],
            "border": tokens["border"],
            "success": "#4ade80",
            "warning": "#fbbf24",
            "danger": "#f87171",
        }
    return {
        "window": tokens["window"],
        "surface": "#f8fafc",
        "surface_muted": "#e2e8f0",
        "text": tokens["text"],
        "text_muted": tokens["text_muted"],
        "border": tokens["border"],
        "success": "#22c55e",
        "warning": "#f59e0b",
        "danger": "#ef4444",
    }


def _style_dialog(dialog: QDialog, dark: bool) -> None:
    colors = _get_dialog_colors(dark)
    dialog.setStyleSheet(
        f"""
        QDialog {{
            color: {colors["text"]};
            background-color: {colors["window"]};
        }}
        QGroupBox {{
            font-weight: bold;
            border: 1px solid {colors["border"]};
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        QLabel {{
            color: {colors["text"]};
        }}
        QPlainTextEdit {{
            color: {colors["text"]};
            background-color: {colors["surface"]};
            border: 1px solid {colors["border"]};
            border-radius: 6px;
            padding: 8px;
            font-family: "Courier New", monospace;
        }}
        {build_scrollbar_style(dark)}
        """
    )


def _style_button(button: QPushButton, dark: bool) -> None:
    colors = _get_dialog_colors(dark)
    button.setStyleSheet(
        f"""
        QPushButton {{
            color: {colors["text"]};
            background-color: {colors["surface_muted"]};
            border: 1px solid {colors["border"]};
            border-radius: 6px;
            padding: 6px 12px;
        }}
        QPushButton:hover {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["border"]};
        }}
        QPushButton:pressed {{
            background-color: {colors["surface"]};
        }}
        """
    )


class PerformanceMonitorDialog(QDialog):
    """性能监控对话框"""

    def __init__(self, parent: "MyMAinWindow | None" = None):
        super().__init__(parent)
        self._dark = bool(getattr(parent, "dark_mode", False))
        self.setWindowTitle("性能监控")
        self.resize(1000, 700)
        _style_dialog(self, self._dark)

        self._setup_ui()
        self._refresh_data()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)

        # 创建选项卡
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 性能监控选项卡
        self._setup_performance_tab()

        # 爬虫健康选项卡
        self._setup_health_tab()

        # 按钮区域
        buttons_layout = QHBoxLayout()
        self.refresh_button = QPushButton("刷新")
        self.reset_perf_button = QPushButton("重置性能监控")
        self.reset_health_button = QPushButton("重置健康监控")

        for button in [self.refresh_button, self.reset_perf_button, self.reset_health_button]:
            _style_button(button, self._dark)
            buttons_layout.addWidget(button)

        buttons_layout.addStretch()

        close_button = QDialogButtonBox.StandardButton.Close
        self.button_box = QDialogButtonBox(close_button)
        self.button_box.rejected.connect(self.reject)
        buttons_layout.addWidget(self.button_box)

        main_layout.addLayout(buttons_layout)

        # 连接信号
        self.refresh_button.clicked.connect(self._refresh_data)
        self.reset_perf_button.clicked.connect(self._reset_performance)
        self.reset_health_button.clicked.connect(self._reset_health)

    def _setup_performance_tab(self) -> None:
        perf_widget = QWidget()
        layout = QVBoxLayout(perf_widget)

        # 性能报告区域
        perf_group = QGroupBox("性能报告")
        perf_layout = QVBoxLayout(perf_group)

        self.perf_text = QPlainTextEdit()
        self.perf_text.setReadOnly(True)
        perf_layout.addWidget(self.perf_text)

        layout.addWidget(perf_group)

        self.tab_widget.addTab(perf_widget, "性能监控")

    def _setup_health_tab(self) -> None:
        health_widget = QWidget()
        layout = QVBoxLayout(health_widget)

        # 总体统计
        overview_group = QGroupBox("总体统计")
        overview_layout = QGridLayout(overview_group)

        self.total_requests_label = QLabel("总请求数: 0")
        self.success_count_label = QLabel("成功: 0")
        self.failure_count_label = QLabel("失败: 0")
        self.success_rate_label = QLabel("成功率: 0%")

        overview_layout.addWidget(self.total_requests_label, 0, 0)
        overview_layout.addWidget(self.success_count_label, 0, 1)
        overview_layout.addWidget(self.failure_count_label, 1, 0)
        overview_layout.addWidget(self.success_rate_label, 1, 1)

        layout.addWidget(overview_group)

        # 健康报告区域
        health_report_group = QGroupBox("详细报告")
        health_report_layout = QVBoxLayout(health_report_group)

        self.health_text = QPlainTextEdit()
        self.health_text.setReadOnly(True)
        health_report_layout.addWidget(self.health_text)

        layout.addWidget(health_report_group)

        self.tab_widget.addTab(health_widget, "爬虫健康")

    def _refresh_data(self) -> None:
        # 更新性能报告
        perf_report = get_performance_report()
        self.perf_text.setPlainText(perf_report)

        # 更新健康报告
        health_report = health_monitor.generate_report()
        self.health_text.setPlainText(health_report)

        # 更新总体统计
        all_stats = health_monitor.get_all_stats()
        total_requests = sum(s.total_requests for s in all_stats)
        total_success = sum(s.success_count for s in all_stats)
        total_failure = sum(s.failure_count for s in all_stats)

        self.total_requests_label.setText(f"总请求数: {total_requests}")
        self.success_count_label.setText(f"成功: {total_success}")
        self.failure_count_label.setText(f"失败: {total_failure}")

        if total_requests > 0:
            success_rate = total_success / total_requests * 100
            self.success_rate_label.setText(f"成功率: {success_rate:.1f}%")
        else:
            self.success_rate_label.setText("成功率: 0%")

    def _reset_performance(self) -> None:
        reset_performance_monitor()
        self._refresh_data()

    def _reset_health(self) -> None:
        health_monitor.reset_stats()
        self._refresh_data()


def open_performance_dialog(parent: "MyMAinWindow") -> None:
    """打开性能监控对话框"""
    dialog = PerformanceMonitorDialog(parent)
    dialog.exec()
