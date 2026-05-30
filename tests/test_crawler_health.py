import pytest
import time

from mdcx.utils.crawler_health import (
    CrawlerHealthStats,
    CrawlerHealthMonitor,
    health_monitor,
)
from mdcx.config.models import Website


class TestCrawlerHealthStats:
    """测试健康统计类"""

    def test_initial_stats(self):
        """测试初始状态"""
        stats = CrawlerHealthStats(site=Website.JAVBUS)
        assert stats.total_requests == 0
        assert stats.success_count == 0
        assert stats.failure_count == 0
        assert stats.success_rate == 1.0
        assert stats.health_score > 50  # 初始状态评分较高
        assert stats.is_healthy is True

    def test_record_success(self):
        """测试记录成功"""
        stats = CrawlerHealthStats(site=Website.JAVBUS)
        stats.total_requests = 1
        stats.success_count = 1
        stats.total_response_time = 0.5
        stats.avg_response_time = 0.5
        stats.last_success_time = time.time()
        stats.consecutive_successes = 1
        
        assert stats.success_rate == 1.0
        assert stats.health_score > 50
        assert stats.is_healthy is True

    def test_record_failure(self):
        """测试记录失败"""
        stats = CrawlerHealthStats(site=Website.JAVBUS)
        stats.total_requests = 10
        stats.success_count = 5
        stats.failure_count = 5
        stats.consecutive_failures = 10
        
        assert stats.success_rate == 0.5
        assert stats.is_healthy is False  # 连续失败太多


class TestCrawlerHealthMonitor:
    """测试健康监控类"""

    def test_singleton(self):
        """测试单例模式"""
        monitor1 = CrawlerHealthMonitor()
        monitor2 = CrawlerHealthMonitor()
        assert monitor1 is monitor2

    def test_record_success(self):
        """测试记录成功"""
        monitor = CrawlerHealthMonitor()
        monitor.reset_stats()
        
        monitor.record_success(Website.JAVBUS, 0.5)
        stats = monitor.get_health_status(Website.JAVBUS)
        
        assert stats is not None
        assert stats.total_requests == 1
        assert stats.success_count == 1

    def test_record_failure(self):
        """测试记录失败"""
        monitor = CrawlerHealthMonitor()
        monitor.reset_stats()
        
        monitor.record_failure(Website.JAVBUS, "timeout error")
        stats = monitor.get_health_status(Website.JAVBUS)
        
        assert stats is not None
        assert stats.failure_count == 1
        assert "Timeout" in stats.failure_reasons

    def test_should_skip_crawler(self):
        """测试是否应该跳过爬虫"""
        monitor = CrawlerHealthMonitor()
        monitor.reset_stats()
        
        # 初始状态不应该跳过
        assert monitor.should_skip_crawler(Website.JAVBUS) is False
        
        # 多次失败后应该跳过
        for _ in range(20):
            monitor.record_failure(Website.JAVBUS, "error")
        
        assert monitor.should_skip_crawler(Website.JAVBUS) is True

    def test_generate_report(self):
        """测试生成报告"""
        monitor = CrawlerHealthMonitor()
        monitor.reset_stats()
        
        # 记录一些数据
        monitor.record_success(Website.JAVBUS, 0.3)
        monitor.record_success(Website.JAVBUS, 0.4)
        monitor.record_failure(Website.JAVDB, "connection error")
        
        report = monitor.generate_report()
        
        assert "刮削源健康报告" in report
        assert Website.JAVBUS.value in report
        assert Website.JAVDB.value in report
        assert "总请求数: 3" in report

    def test_enable_disable(self):
        """测试启用/禁用"""
        monitor = CrawlerHealthMonitor()
        monitor.reset_stats()
        
        monitor.disable()
        monitor.record_success(Website.JAVBUS, 0.5)
        stats = monitor.get_health_status(Website.JAVBUS)
        assert stats is None  # 禁用状态下不会记录
        
        monitor.enable()
        monitor.record_success(Website.JAVBUS, 0.5)
        stats = monitor.get_health_status(Website.JAVBUS)
        assert stats is not None


class TestGlobalHealthMonitor:
    """测试全局健康监控器"""

    def test_health_monitor_exists(self):
        """测试全局实例是否存在"""
        assert health_monitor is not None
        assert isinstance(health_monitor, CrawlerHealthMonitor)
