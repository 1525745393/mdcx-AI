import tempfile
import time

from mdcx.utils.report_system import (
    ReportGenerator,
    ReportType,
    ScrapeRecord,
    ScrapeSession,
    ScrapeTracker,
    scrape_tracker,
)


class TestScrapeRecord:
    """测试单个刮削记录"""

    def test_create_record(self):
        """测试创建记录"""
        record = ScrapeRecord(
            number="ABC-123",
            title="测试视频",
            success=True,
            start_time=time.time(),
            end_time=time.time() + 1.0,
            source="javbus",
            actors=["演员A", "演员B"],
        )
        assert record.number == "ABC-123"
        assert record.title == "测试视频"
        assert record.success is True
        assert record.source == "javbus"
        assert len(record.actors) == 2


class TestScrapeSession:
    """测试刮削会话"""

    def test_create_session(self):
        """测试创建会话"""
        start_time = time.time()
        session = ScrapeSession(
            session_id="test_session_1",
            start_time=start_time,
            total_files=10,
        )
        assert session.session_id == "test_session_1"
        assert session.total_files == 10
        assert session.duration > 0

    def test_session_success_rate(self):
        """测试成功率计算"""
        session = ScrapeSession(
            session_id="test_session",
            start_time=time.time(),
            total_files=10,
            success_count=7,
            failure_count=3,
        )
        assert session.success_rate == 0.7


class TestScrapeTracker:
    """测试刮削跟踪器"""

    def test_singleton(self):
        """测试单例模式"""
        tracker1 = ScrapeTracker()
        tracker2 = ScrapeTracker()
        assert tracker1 is tracker2

    def test_start_session(self):
        """测试开始会话"""
        tracker = ScrapeTracker()
        tracker.clear_sessions()  # 确保清空之前的会话

        session_id = tracker.start_session(total_files=5)
        assert session_id.startswith("session_")
        assert tracker.get_current_session() is not None
        assert tracker.get_current_session().total_files == 5

    def test_record_scrape(self):
        """测试记录刮削"""
        tracker = ScrapeTracker()
        tracker.clear_sessions()

        tracker.start_session(total_files=3)

        start_time = time.time()
        tracker.record_scrape(
            number="ABC-001",
            title="视频1",
            success=True,
            start_time=start_time,
            end_time=start_time + 0.5,
            source="javbus",
            actors=["演员1"],
        )

        tracker.record_scrape(
            number="ABC-002",
            title="视频2",
            success=False,
            start_time=start_time,
            end_time=start_time + 0.3,
            source="javdb",
            error_message="找不到资源",
        )

        session = tracker.get_current_session()
        assert len(session.records) == 2
        assert session.records[0].number == "ABC-001"
        assert session.records[1].error_message == "找不到资源"

    def test_end_session(self):
        """测试结束会话"""
        tracker = ScrapeTracker()
        tracker.clear_sessions()

        tracker.start_session(total_files=3)

        start_time = time.time()
        tracker.record_scrape(
            number="ABC-001",
            title="视频1",
            success=True,
            start_time=start_time,
            end_time=start_time + 0.5,
        )
        tracker.record_scrape(
            number="ABC-002",
            title="视频2",
            success=False,
            start_time=start_time,
            end_time=start_time + 0.5,
        )

        tracker.end_session()
        session = tracker.get_current_session()

        assert session.success_count == 1
        assert session.failure_count == 1
        assert session.success_rate == 1.0 / 3.0  # 基于 total_files=3 计算

    def test_get_sessions(self):
        """测试获取会话列表"""
        tracker = ScrapeTracker()
        tracker.clear_sessions()

        # 创建两个会话
        tracker.start_session(total_files=5)
        tracker.end_session()

        tracker.start_session(total_files=10)
        tracker.end_session()

        sessions = tracker.get_sessions(limit=5)
        assert len(sessions) == 2


class TestReportGenerator:
    """测试报告生成器"""

    def setup_method(self):
        """每个测试前的准备"""
        scrape_tracker.clear_sessions()

        # 创建测试会话和记录
        scrape_tracker.start_session(total_files=5)

        start_time = time.time()
        scrape_tracker.record_scrape(
            number="ABC-001",
            title="测试视频1",
            success=True,
            start_time=start_time,
            end_time=start_time + 0.5,
            source="javbus",
            actors=["演员A", "演员B"],
        )
        scrape_tracker.record_scrape(
            number="ABC-002",
            title="测试视频2",
            success=True,
            start_time=start_time,
            end_time=start_time + 0.8,
            source="javdb",
            actors=["演员A", "演员C"],
        )
        scrape_tracker.record_scrape(
            number="ABC-003",
            title="测试视频3",
            success=False,
            start_time=start_time,
            end_time=start_time + 0.3,
            source="javlibrary",
            error_message="页面加载失败",
        )

        scrape_tracker.end_session()

    def test_generate_scrape_result_report(self):
        """测试生成刮削结果报告"""
        report_gen = ReportGenerator()
        report = report_gen.generate_scrape_result_report()

        assert "刮削结果报告" in report
        assert "ABC-001" in report
        assert "ABC-002" in report
        assert "ABC-003" in report
        assert "成功率" in report

    def test_generate_scrape_history_report(self):
        """测试生成刮削历史报告"""
        report_gen = ReportGenerator()
        report = report_gen.generate_scrape_history_report()

        assert "刮削历史报告" in report
        assert "会话ID" in report

    def test_generate_resource_statistics_report(self):
        """测试生成资源统计报告"""
        report_gen = ReportGenerator()
        report = report_gen.generate_resource_statistics_report()

        assert "资源统计报告" in report
        assert "演员统计" in report
        assert "演员A" in report

    def test_generate_actor_statistics_report(self):
        """测试生成演员统计报告"""
        report_gen = ReportGenerator()
        report = report_gen.generate_actor_statistics_report()

        assert "演员统计报告" in report
        assert "演员A" in report
        assert "ABC-001" in report

    def test_export_report_to_file(self):
        """测试导出报告到文件"""
        report_gen = ReportGenerator()
        report = report_gen.generate_scrape_result_report()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = report_gen.export_report_to_file(report, ReportType.SCRAPE_RESULT, temp_dir)

            assert output_path.exists()
            assert output_path.name.startswith("scrape_result_")

            with open(output_path, encoding="utf-8") as f:
                content = f.read()
                assert content == report

    def test_no_data_report(self):
        """测试没有数据时的报告"""
        scrape_tracker.clear_sessions()
        report_gen = ReportGenerator()

        result_report = report_gen.generate_scrape_result_report()
        history_report = report_gen.generate_scrape_history_report()

        assert "暂无" in result_report
        assert "暂无" in history_report
