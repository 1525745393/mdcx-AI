import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from mdcx.config.models import Website
from mdcx.utils import perf_monitor


@dataclass
class CrawlerHealthStats:
    """单个爬虫的健康统计"""
    site: Website
    total_requests: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_response_time: float = 0.0
    avg_response_time: float = 0.0
    last_success_time: float = 0.0
    last_failure_time: float = 0.0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    failure_reasons: dict[str, int] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        """获取成功率"""
        if self.total_requests == 0:
            return 1.0
        return self.success_count / self.total_requests

    @property
    def health_score(self) -> float:
        """计算健康评分 (0-100)"""
        # 基础分
        score = 50.0
        
        # 成功率加成
        score += self.success_rate * 40.0
        
        # 响应时间加成 (越快分越高)
        if self.avg_response_time > 0:
            if self.avg_response_time < 0.5:
                score += 10.0
            elif self.avg_response_time < 1.0:
                score += 5.0
            elif self.avg_response_time > 5.0:
                score -= 10.0
        
        # 连续失败扣分
        if self.consecutive_failures > 5:
            score -= min(30, self.consecutive_failures * 3)
        
        return max(0.0, min(100.0, score))

    @property
    def is_healthy(self) -> bool:
        """判断爬虫是否健康"""
        if self.total_requests == 0:
            return True
        # 健康条件: 健康分 > 50, 连续失败 < 10
        return self.health_score > 50 and self.consecutive_failures < 10


class CrawlerHealthMonitor:
    """爬虫健康监控器"""

    _instance: "CrawlerHealthMonitor | None" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._stats: dict[Website, CrawlerHealthStats] = {}
        self._enabled: bool = True

    def enable(self):
        """启用监控"""
        self._enabled = True

    def disable(self):
        """禁用监控"""
        self._enabled = False

    def _get_or_create_stats(self, site: Website) -> CrawlerHealthStats:
        """获取或创建统计对象"""
        if site not in self._stats:
            self._stats[site] = CrawlerHealthStats(site=site)
        return self._stats[site]

    def record_success(self, site: Website, response_time: float):
        """记录成功请求"""
        if not self._enabled:
            return
        
        stats = self._get_or_create_stats(site)
        stats.total_requests += 1
        stats.success_count += 1
        stats.total_response_time += response_time
        stats.avg_response_time = stats.total_response_time / stats.success_count
        stats.last_success_time = time.time()
        stats.consecutive_successes += 1
        stats.consecutive_failures = 0

    def record_failure(self, site: Website, error: str):
        """记录失败请求"""
        if not self._enabled:
            return
        
        stats = self._get_or_create_stats(site)
        stats.total_requests += 1
        stats.failure_count += 1
        stats.last_failure_time = time.time()
        stats.consecutive_failures += 1
        stats.consecutive_successes = 0
        
        # 简化错误类型以便统计
        error_type = self._classify_error(error)
        stats.failure_reasons[error_type] = stats.failure_reasons.get(error_type, 0) + 1

    def _classify_error(self, error: str) -> str:
        """将错误分类"""
        if "timeout" in error.lower():
            return "Timeout"
        elif "connection" in error.lower():
            return "ConnectionError"
        elif "404" in error:
            return "NotFound"
        elif "403" in error or "forbidden" in error.lower():
            return "Forbidden"
        elif "500" in error or "server" in error.lower():
            return "ServerError"
        else:
            return "Other"

    def get_health_status(self, site: Website) -> CrawlerHealthStats | None:
        """获取爬虫健康状态"""
        return self._stats.get(site)

    def get_unhealthy_crawlers(self) -> list[tuple[Website, float]]:
        """获取不健康的爬虫列表，按健康分排序"""
        unhealthy = []
        for site, stats in self._stats.items():
            if not stats.is_healthy:
                unhealthy.append((site, stats.health_score))
        return sorted(unhealthy, key=lambda x: x[1])

    def should_skip_crawler(self, site: Website) -> bool:
        """判断是否应跳过该爬虫"""
        stats = self._get_or_create_stats(site)
        if not stats.is_healthy and stats.total_requests > 5:
            return True
        return False

    def get_all_stats(self) -> list[CrawlerHealthStats]:
        """获取所有爬虫的统计信息"""
        return list(self._stats.values())

    def reset_stats(self, site: Website | None = None):
        """重置统计信息"""
        if site:
            if site in self._stats:
                self._stats[site] = CrawlerHealthStats(site=site)
        else:
            self._stats.clear()

    def generate_report(self) -> str:
        """生成健康报告"""
        lines = []
        lines.append("=" * 80)
        lines.append("刮削源健康报告")
        lines.append("=" * 80)
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # 总体统计
        total_requests = sum(s.total_requests for s in self._stats.values())
        total_success = sum(s.success_count for s in self._stats.values())
        total_failure = sum(s.failure_count for s in self._stats.values())
        
        lines.append(f"总请求数: {total_requests}")
        lines.append(f"成功: {total_success}")
        lines.append(f"失败: {total_failure}")
        if total_requests > 0:
            lines.append(f"总成功率: {total_success/total_requests*100:.1f}%")
        lines.append("")

        # 各爬虫统计
        lines.append("各爬虫状态:")
        lines.append("-" * 80)
        lines.append(f"{'网站':<20} {'状态':<8} {'成功':<6} {'失败':<6} {'成功率':<8} {'响应时间':<10}")
        lines.append("-" * 80)
        
        for site, stats in self._stats.items():
            status = "✅健康" if stats.is_healthy else "⚠️异常"
            success_rate = f"{stats.success_rate*100:.1f}%"
            avg_rt = f"{stats.avg_response_time:.2f}s"
            lines.append(
                f"{site.value:<20} {status:<8} {stats.success_count:<6} {stats.failure_count:<6} {success_rate:<8} {avg_rt:<10}"
            )
        
        lines.append("")
        
        # 不健康的爬虫
        unhealthy = self.get_unhealthy_crawlers()
        if unhealthy:
            lines.append("⚠️ 不健康的爬虫:")
            for site, score in unhealthy:
                stats = self._stats[site]
                lines.append(f"  - {site.value}: 健康分 {score:.0f}, 连续失败 {stats.consecutive_failures}")
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)


# 全局健康监控器实例
health_monitor = CrawlerHealthMonitor()
