#!/usr/bin/env python3
"""
性能优化演示脚本
演示我们添加的性能监控和优化功能
"""

import sys
import time
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from mdcx.utils.perf import perf_monitor, get_performance_report, reset_performance_monitor
    from mdcx.config.resources import resources
except Exception as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)


def demo_resources_query():
    """演示优化后的资源查询性能"""
    print("=" * 80)
    print("资源查询性能演示")
    print("=" * 80)

    # 重置监控器
    reset_performance_monitor()

    # 模拟一些查询
    test_actors = ["波多野结衣", "天海翼", "深田咏美", "三上悠亚", "葵司"]
    test_info = ["S1", "MOODYZ", "IDEAPOCKET", "PRESTIGE", "MAXING"]

    print("\n1. 第一轮查询（未缓存）:")
    start = time.perf_counter()
    for actor in test_actors:
        resources.get_actor_data(actor)
    for info in test_info:
        resources.get_info_data(info)
    first_round_time = time.perf_counter() - start
    print(f"   耗时: {first_round_time * 1000:.2f} ms")

    print("\n2. 第二轮查询（已缓存）:")
    start = time.perf_counter()
    for actor in test_actors:
        resources.get_actor_data(actor)
    for info in test_info:
        resources.get_info_data(info)
    second_round_time = time.perf_counter() - start
    print(f"   耗时: {second_round_time * 1000:.2f} ms")

    print(f"\n3. 性能提升: {(first_round_time / second_round_time) if second_round_time > 0 else 0:.1f}x")

    print("\n" + "=" * 80)
    print("性能统计报告:")
    print("=" * 80)
    print(get_performance_report())


def main():
    print("MDCx 性能优化演示")
    print("=" * 80)

    demo_resources_query()

    print("\n✅ 演示完成！")


if __name__ == "__main__":
    main()
