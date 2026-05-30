import time
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class PerfRecord:
    """单个性能记录"""
    name: str
    start_time: float
    end_time: float
    duration: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActiveTimer:
    """活跃计时器信息"""
    name: str
    start_time: float
    category: Optional[str] = None


class PerformanceMonitor:
    """性能监控器，用于跟踪和分析代码执行时间"""

    def __init__(self):
        self._records: List[PerfRecord] = []
        self._active_timers: Dict[str, ActiveTimer] = {}
        self._category_records: Dict[str, List[PerfRecord]] = defaultdict(list)
        self._enabled: bool = True
        self._timer_counter: int = 0

    def enable(self):
        """启用监控"""
        self._enabled = True

    def disable(self):
        """禁用监控"""
        self._enabled = False

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self._enabled

    def start(self, name: str, category: Optional[str] = None) -> str:
        """
        开始计时

        Args:
            name: 计时器名称
            category: 可选的分类标签

        Returns:
            计时器标识符（用于结束计时）
        """
        if not self._enabled:
            return name

        self._timer_counter += 1
        timer_id = f"timer_{self._timer_counter}"
        self._active_timers[timer_id] = ActiveTimer(
            name=name,
            start_time=time.time(),
            category=category
        )
        return timer_id

    def end(self, timer_id: str, category: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Optional[float]:
        """
        结束计时并记录结果

        Args:
            timer_id: start() 返回的标识符
            category: 可选的分类标签（会覆盖 start 时的分类）
            metadata: 可选的元数据

        Returns:
            执行时间（秒），如果监控未启用则返回 None
        """
        if not self._enabled:
            return None

        if timer_id not in self._active_timers:
            return None

        active_timer = self._active_timers.pop(timer_id)
        end_time = time.time()
        duration = round(end_time - active_timer.start_time, 4)

        # 使用 end 时提供的分类，否则使用 start 时的分类
        final_category = category or active_timer.category

        record = PerfRecord(
            name=active_timer.name,
            start_time=active_timer.start_time,
            end_time=end_time,
            duration=duration,
            metadata=metadata or {}
        )

        self._records.append(record)
        if final_category:
            self._category_records[final_category].append(record)

        return duration

    def timeit(self, name: str, category: Optional[str] = None):
        """
        上下文管理器，用于监控代码块执行时间

        Usage:
            with perf_monitor.timeit("my_function"):
                my_function()
        """
        return _TimerContext(self, name, category)

    def measure(self, func: Callable, *args, **kwargs) -> Tuple[Any, float]:
        """
        测量函数执行时间

        Args:
            func: 要测量的函数
            *args: 函数参数
            **kwargs: 函数关键字参数

        Returns:
            (函数返回值, 执行时间)
        """
        timer_id = self.start(func.__name__)
        try:
            result = func(*args, **kwargs)
            duration = self.end(timer_id)
            return result, duration or 0.0
        except Exception:
            self.end(timer_id)
            raise

    def get_statistics(self, name: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """
        获取性能统计信息

        Args:
            name: 可选的名称过滤
            category: 可选的分类过滤

        Returns:
            统计信息字典
        """
        records = self._filter_records(name, category)

        if not records:
            return {"count": 0}

        durations = [r.duration for r in records]

        return {
            "count": len(records),
            "total": round(sum(durations), 4),
            "mean": round(statistics.mean(durations), 4),
            "median": round(statistics.median(durations), 4),
            "min": round(min(durations), 4),
            "max": round(max(durations), 4),
            "stdev": round(statistics.stdev(durations) if len(durations) > 1 else 0.0, 4),
        }

    def get_all_statistics(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有统计信息（按名称分组）

        Returns:
            按名称分组的统计信息
        """
        stats = {}
        names = {r.name for r in self._records}
        for name in names:
            stats[name] = self.get_statistics(name=name)
        return stats

    def get_category_statistics(self) -> Dict[str, Dict[str, Any]]:
        """
        获取按分类分组的统计信息

        Returns:
            按分类分组的统计信息
        """
        stats = {}
        for category in self._category_records:
            stats[category] = self.get_statistics(category=category)
        return stats

    def reset(self):
        """重置所有记录"""
        self._records.clear()
        self._active_timers.clear()
        self._category_records.clear()

    def _filter_records(self, name: Optional[str] = None, category: Optional[str] = None) -> List[PerfRecord]:
        """内部方法：过滤记录"""
        records = self._records

        if name:
            records = [r for r in records if r.name == name]

        if category:
            records = self._category_records.get(category, [])

        return records

    def report(self) -> str:
        """
        生成性能报告字符串

        Returns:
            格式化的性能报告
        """
        all_stats = self.get_all_statistics()
        category_stats = self.get_category_statistics()

        lines = []
        lines.append("=" * 80)
        lines.append("PERFORMANCE REPORT")
        lines.append("=" * 80)

        if all_stats:
            lines.append("\nBy Name:")
            lines.append("-" * 80)
            lines.append(f"{'Name':<30} {'Count':<6} {'Total':<10} {'Mean':<10} {'Median':<10} {'Min':<10} {'Max':<10}")
            lines.append("-" * 80)
            for name, stats in sorted(all_stats.items(), key=lambda x: -x[1]["total"]):
                lines.append(
                    f"{name:<30} {stats['count']:<6} {stats['total']:<10} {stats['mean']:<10} "
                    f"{stats['median']:<10} {stats['min']:<10} {stats['max']:<10}"
                )

        if category_stats:
            lines.append("\nBy Category:")
            lines.append("-" * 80)
            lines.append(f"{'Category':<30} {'Count':<6} {'Total':<10} {'Mean':<10} {'Median':<10} {'Min':<10} {'Max':<10}")
            lines.append("-" * 80)
            for category, stats in sorted(category_stats.items(), key=lambda x: -x[1]["total"]):
                lines.append(
                    f"{category:<30} {stats['count']:<6} {stats['total']:<10} {stats['mean']:<10} "
                    f"{stats['median']:<10} {stats['min']:<10} {stats['max']:<10}"
                )

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)


class _TimerContext:
    """性能计时器的上下文管理器"""

    def __init__(self, monitor: PerformanceMonitor, name: str, category: Optional[str] = None):
        self.monitor = monitor
        self.name = name
        self.category = category
        self.timer_id: Optional[str] = None

    def __enter__(self):
        self.timer_id = self.monitor.start(self.name, self.category)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.timer_id:
            self.monitor.end(self.timer_id, self.category)


# 全局性能监控器实例
perf_monitor = PerformanceMonitor()


def get_performance_report() -> str:
    """获取全局性能监控器的报告"""
    return perf_monitor.report()


def reset_performance_monitor():
    """重置全局性能监控器"""
    perf_monitor.reset()
