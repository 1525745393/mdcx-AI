import time

from mdcx.utils.perf import (
    PerformanceMonitor,
    PerfRecord,
    get_performance_report,
    perf_monitor,
    reset_performance_monitor,
)


def test_performance_monitor_basic():
    """测试基本的计时功能"""
    monitor = PerformanceMonitor()

    timer_id = monitor.start("test_function")
    time.sleep(0.01)
    duration = monitor.end(timer_id)

    assert duration is not None
    assert duration >= 0.01
    assert len(monitor._records) == 1


def test_performance_monitor_context_manager():
    """测试上下文管理器"""
    monitor = PerformanceMonitor()

    with monitor.timeit("context_test"):
        time.sleep(0.01)

    assert len(monitor._records) == 1
    assert monitor._records[0].name == "context_test"


def test_performance_monitor_measure():
    """测试函数测量功能"""
    monitor = PerformanceMonitor()

    def sample_func():
        time.sleep(0.01)
        return "result"

    result, duration = monitor.measure(sample_func)

    assert result == "result"
    assert duration >= 0.01
    assert len(monitor._records) == 1


def test_performance_monitor_statistics():
    """测试统计功能"""
    monitor = PerformanceMonitor()

    for i in range(5):
        timer_id = monitor.start("stat_test")
        time.sleep(0.01)
        monitor.end(timer_id)

    stats = monitor.get_statistics(name="stat_test")

    assert stats["count"] == 5
    assert stats["total"] >= 0.05
    assert stats["mean"] >= 0.01
    assert stats["min"] >= 0.01
    assert stats["max"] >= 0.01


def test_performance_monitor_category():
    """测试分类功能"""
    monitor = PerformanceMonitor()

    with monitor.timeit("test1", category="cat1"):
        time.sleep(0.01)

    with monitor.timeit("test2", category="cat1"):
        time.sleep(0.01)

    with monitor.timeit("test3", category="cat2"):
        time.sleep(0.01)

    cat1_stats = monitor.get_statistics(category="cat1")
    cat2_stats = monitor.get_statistics(category="cat2")

    assert cat1_stats["count"] == 2
    assert cat2_stats["count"] == 1


def test_performance_monitor_reset():
    """测试重置功能"""
    monitor = PerformanceMonitor()

    timer_id = monitor.start("test")
    monitor.end(timer_id)

    assert len(monitor._records) == 1

    monitor.reset()

    assert len(monitor._records) == 0
    assert len(monitor._active_timers) == 0


def test_performance_monitor_enable_disable():
    """测试启用/禁用功能"""
    monitor = PerformanceMonitor()

    monitor.disable()

    timer_id = monitor.start("disabled_test")
    time.sleep(0.01)
    duration = monitor.end(timer_id)

    assert duration is None
    assert len(monitor._records) == 0

    monitor.enable()

    timer_id = monitor.start("enabled_test")
    time.sleep(0.01)
    duration = monitor.end(timer_id)

    assert duration is not None
    assert len(monitor._records) == 1


def test_performance_monitor_report():
    """测试报告生成功能"""
    monitor = PerformanceMonitor()

    with monitor.timeit("report_test1", category="report_cat"):
        time.sleep(0.01)

    with monitor.timeit("report_test2", category="report_cat"):
        time.sleep(0.01)

    report = monitor.report()

    assert "PERFORMANCE REPORT" in report
    assert "report_test1" in report
    assert "report_test2" in report
    assert "report_cat" in report


def test_global_perf_monitor():
    """测试全局性能监控器"""
    reset_performance_monitor()

    with perf_monitor.timeit("global_test"):
        time.sleep(0.01)

    report = get_performance_report()

    assert "global_test" in report
    assert len(perf_monitor._records) == 1


def test_performance_monitor_multiple_timers():
    """测试多个同时运行的计时器"""
    monitor = PerformanceMonitor()

    timer1 = monitor.start("timer1")
    time.sleep(0.005)
    timer2 = monitor.start("timer2")
    time.sleep(0.005)

    duration2 = monitor.end(timer2)
    time.sleep(0.005)
    duration1 = monitor.end(timer1)

    assert duration1 >= 0.01
    assert duration2 >= 0.005
    assert duration1 > duration2
    assert len(monitor._records) == 2


def test_performance_monitor_metadata():
    """测试元数据功能"""
    monitor = PerformanceMonitor()

    timer_id = monitor.start("metadata_test")
    time.sleep(0.01)
    duration = monitor.end(timer_id, metadata={"key": "value", "number": 42})

    assert duration is not None
    assert len(monitor._records) == 1
    assert monitor._records[0].metadata["key"] == "value"
    assert monitor._records[0].metadata["number"] == 42


def test_perf_record_dataclass():
    """测试 PerfRecord 数据类"""
    record = PerfRecord(
        name="test_record",
        start_time=1000.0,
        end_time=1001.5,
        duration=1.5,
        metadata={"foo": "bar"}
    )

    assert record.name == "test_record"
    assert record.start_time == 1000.0
    assert record.end_time == 1001.5
    assert record.duration == 1.5
    assert record.metadata["foo"] == "bar"
