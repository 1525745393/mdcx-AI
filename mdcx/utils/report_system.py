import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ReportType(Enum):
    """报告类型枚举"""

    SCRAPE_RESULT = "scrape_result"
    SCRAPE_HISTORY = "scrape_history"
    RESOURCE_STATISTICS = "resource_statistics"
    ACTOR_STATISTICS = "actor_statistics"


@dataclass
class ScrapeRecord:
    """单个刮削记录"""

    number: str
    title: str
    success: bool
    start_time: float
    end_time: float
    source: str = ""
    error_message: str = ""
    file_path: str = ""
    actors: list[str] = field(default_factory=list)


@dataclass
class ScrapeSession:
    """刮削会话记录"""

    session_id: str
    start_time: float
    end_time: float = 0.0
    records: list[ScrapeRecord] = field(default_factory=list)
    total_files: int = 0
    success_count: int = 0
    failure_count: int = 0

    @property
    def duration(self) -> float:
        """获取会话持续时间"""
        if self.end_time > 0:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    @property
    def success_rate(self) -> float:
        """获取成功率"""
        if self.total_files == 0:
            return 0.0
        return self.success_count / self.total_files


class ScrapeTracker:
    """刮削跟踪器 - 跟踪刮削会话和结果"""

    _instance: "ScrapeTracker | None" = None
    _sessions: list[ScrapeSession] = []
    _current_session: ScrapeSession | None = None
    _enabled: bool = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._sessions = []
        self._current_session = None

    def enable(self):
        """启用跟踪"""
        self._enabled = True

    def disable(self):
        """禁用跟踪"""
        self._enabled = False

    def start_session(self, total_files: int = 0) -> str:
        """
        开始新的刮削会话

        Args:
            total_files: 本次会话要处理的文件总数

        Returns:
            会话ID
        """
        if not self._enabled:
            return ""

        session_id = f"session_{int(time.time())}"
        self._current_session = ScrapeSession(
            session_id=session_id,
            start_time=time.time(),
            total_files=total_files,
        )
        self._sessions.append(self._current_session)
        return session_id

    def end_session(self):
        """结束当前刮削会话"""
        if self._current_session and self._enabled:
            self._current_session.end_time = time.time()
            # 统计成功和失败
            self._current_session.success_count = sum(1 for r in self._current_session.records if r.success)
            self._current_session.failure_count = sum(1 for r in self._current_session.records if not r.success)

    def record_scrape(
        self,
        number: str,
        title: str,
        success: bool,
        start_time: float,
        end_time: float,
        source: str = "",
        error_message: str = "",
        file_path: str = "",
        actors: list[str] | None = None,
    ):
        """
        记录单个刮削结果

        Args:
            number: 番号
            title: 标题
            success: 是否成功
            start_time: 开始时间
            end_time: 结束时间
            source: 数据来源
            error_message: 错误信息（如果失败）
            file_path: 文件路径
            actors: 演员列表
        """
        if not self._enabled or self._current_session is None:
            return

        record = ScrapeRecord(
            number=number,
            title=title,
            success=success,
            start_time=start_time,
            end_time=end_time,
            source=source,
            error_message=error_message,
            file_path=file_path,
            actors=actors or [],
        )
        self._current_session.records.append(record)

    def get_sessions(self, limit: int = 10) -> list[ScrapeSession]:
        """
        获取刮削会话历史

        Args:
            limit: 最大返回数量

        Returns:
            会话列表
        """
        return list(reversed(self._sessions[-limit:]))

    def get_current_session(self) -> ScrapeSession | None:
        """获取当前会话"""
        return self._current_session

    def clear_sessions(self):
        """清除所有会话记录"""
        self._sessions.clear()
        self._current_session = None


# 全局跟踪器实例
scrape_tracker = ScrapeTracker()


class ReportGenerator:
    """报告生成器"""

    @staticmethod
    def generate_scrape_result_report(session: ScrapeSession | None = None) -> str:
        """
        生成刮削结果报告

        Args:
            session: 要报告的会话，如果为None则使用最新会话

        Returns:
            格式化的报告字符串
        """
        if session is None:
            sessions = scrape_tracker.get_sessions(1)
            if not sessions:
                return "暂无刮削记录"
            session = sessions[0]

        lines = []
        lines.append("=" * 80)
        lines.append("刮削结果报告")
        lines.append("=" * 80)
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"会话ID: {session.session_id}")
        lines.append(f"会话时间: {datetime.fromtimestamp(session.start_time).strftime('%Y-%m-%d %H:%M:%S')} ~ ")
        if session.end_time > 0:
            lines[-1] += datetime.fromtimestamp(session.end_time).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"持续时间: {session.duration:.2f} 秒")
        lines.append("")

        # 总体统计
        lines.append("--- 总体统计 ---")
        lines.append(f"总文件数: {session.total_files}")
        lines.append(f"成功: {session.success_count}")
        lines.append(f"失败: {session.failure_count}")
        lines.append(f"成功率: {session.success_rate * 100:.1f}%")
        lines.append("")

        # 成功记录
        success_records = [r for r in session.records if r.success]
        if success_records:
            lines.append("--- 成功记录 ---")
            lines.append(f"{'番号':<15} {'标题':<30} {'来源':<12} {'耗时(s)':<8}")
            lines.append("-" * 80)
            for record in success_records:
                duration = record.end_time - record.start_time
                title = (record.title[:27] + "...") if len(record.title) > 30 else record.title
                lines.append(f"{record.number:<15} {title:<30} {record.source:<12} {duration:.2f}")
            lines.append("")

        # 失败记录
        failure_records = [r for r in session.records if not r.success]
        if failure_records:
            lines.append("--- 失败记录 ---")
            lines.append(f"{'番号':<15} {'错误信息':<45}")
            lines.append("-" * 80)
            for record in failure_records:
                error_msg = (
                    (record.error_message[:42] + "...") if len(record.error_message) > 45 else record.error_message
                )
                lines.append(f"{record.number:<15} {error_msg:<45}")
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    @staticmethod
    def generate_scrape_history_report(limit: int = 10) -> str:
        """
        生成刮削历史报告

        Args:
            limit: 要包含的会话数量

        Returns:
            格式化的报告字符串
        """
        sessions = scrape_tracker.get_sessions(limit)

        lines = []
        lines.append("=" * 80)
        lines.append("刮削历史报告")
        lines.append("=" * 80)
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"总会话数: {len(sessions)}")
        lines.append("")

        if not sessions:
            lines.append("暂无刮削历史记录")
            lines.append("=" * 80)
            return "\n".join(lines)

        lines.append("--- 会话列表 ---")
        lines.append(
            f"{'会话ID':<20} {'时间':<20} {'总文件':<8} {'成功':<8} {'失败':<8} {'成功率':<10} {'耗时(s)':<10}"
        )
        lines.append("-" * 80)

        for session in sessions:
            success_rate = session.success_rate * 100
            duration = session.duration
            time_str = datetime.fromtimestamp(session.start_time).strftime("%Y-%m-%d %H:%M")
            lines.append(
                f"{session.session_id:<20} {time_str:<20} {session.total_files:<8} "
                f"{session.success_count:<8} {session.failure_count:<8} {success_rate:<10.1f} {duration:<10.2f}"
            )

        lines.append("")
        lines.append("=" * 80)
        return "\n".join(lines)

    @staticmethod
    def generate_resource_statistics_report(session: ScrapeSession | None = None) -> str:
        """
        生成资源统计报告

        Args:
            session: 要报告的会话，如果为None则使用最新会话

        Returns:
            格式化的报告字符串
        """
        if session is None:
            sessions = scrape_tracker.get_sessions(1)
            if not sessions:
                return "暂无刮削记录"
            session = sessions[0]

        lines = []
        lines.append("=" * 80)
        lines.append("资源统计报告")
        lines.append("=" * 80)
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # 演员统计
        actor_counts: dict[str, int] = {}
        for record in session.records:
            for actor in record.actors:
                actor_counts[actor] = actor_counts.get(actor, 0) + 1

        if actor_counts:
            lines.append("--- 演员统计 ---")
            lines.append(f"{'演员':<20} {'出现次数':<10}")
            lines.append("-" * 80)
            for actor, count in sorted(actor_counts.items(), key=lambda x: -x[1]):
                lines.append(f"{actor:<20} {count:<10}")
            lines.append("")

        # 来源统计
        source_counts: dict[str, int] = {}
        for record in session.records:
            if record.source:
                source_counts[record.source] = source_counts.get(record.source, 0) + 1

        if source_counts:
            lines.append("--- 来源统计 ---")
            lines.append(f"{'来源':<20} {'数量':<10}")
            lines.append("-" * 80)
            for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
                lines.append(f"{source:<20} {count:<10}")
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    @staticmethod
    def generate_actor_statistics_report(session: ScrapeSession | None = None) -> str:
        """
        生成演员统计报告

        Args:
            session: 要报告的会话，如果为None则使用最新会话

        Returns:
            格式化的报告字符串
        """
        if session is None:
            sessions = scrape_tracker.get_sessions(1)
            if not sessions:
                return "暂无刮削记录"
            session = sessions[0]

        lines = []
        lines.append("=" * 80)
        lines.append("演员统计报告")
        lines.append("=" * 80)
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        actor_counts: dict[str, list[str]] = {}
        for record in session.records:
            if record.success:
                for actor in record.actors:
                    if actor not in actor_counts:
                        actor_counts[actor] = []
                    actor_counts[actor].append(record.number)

        if not actor_counts:
            lines.append("暂无演员数据")
            lines.append("=" * 80)
            return "\n".join(lines)

        lines.append(f"总演员数: {len(actor_counts)}")
        lines.append("")

        lines.append("--- 演员详情 ---")
        lines.append(f"{'演员':<20} {'作品数':<8} {'作品列表':<40}")
        lines.append("-" * 80)

        for actor, numbers in sorted(actor_counts.items(), key=lambda x: -len(x[1])):
            number_str = ", ".join(numbers[:3])
            if len(numbers) > 3:
                number_str += "..."
            lines.append(f"{actor:<20} {len(numbers):<8} {number_str:<40}")

        lines.append("")
        lines.append("=" * 80)
        return "\n".join(lines)

    @staticmethod
    def export_report_to_file(report: str, report_type: ReportType, output_dir: Path | str) -> Path:
        """
        导出报告到文件

        Args:
            report: 报告内容
            report_type: 报告类型
            output_dir: 输出目录

        Returns:
            输出文件路径
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_type.value}_{timestamp}.txt"
        output_path = output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

        return output_path


# 便捷函数
def get_report_generator() -> ReportGenerator:
    """获取报告生成器实例"""
    return ReportGenerator()
