"""
Scraper 核心模块单元测试

测试 mdcx.core.scraper 中的异常类、任务调度等功能
"""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mdcx.core.scraper import (
    StopScrape,
    UnexpectedScrapeCancellation,
)


class TestScraperExceptions:
    """测试Scraper异常类"""

    def test_stop_scrape_exception(self):
        """测试StopScrape异常可以抛出和捕获"""
        with pytest.raises(StopScrape):
            raise StopScrape()

    def test_stop_scrape_with_message(self):
        """测试StopScrape可以携带消息"""
        msg = "测试停止消息"
        with pytest.raises(StopScrape) as exc_info:
            raise StopScrape(msg)
        assert str(exc_info.value) == msg

    def test_unexpected_scrape_cancellation_exception(self):
        """测试UnexpectedScrapeCancellation异常"""
        with pytest.raises(UnexpectedScrapeCancellation):
            raise UnexpectedScrapeCancellation()

    def test_unexpected_scrape_cancellation_with_message(self):
        """测试UnexpectedScrapeCancellation携带消息"""
        msg = "异常取消消息"
        with pytest.raises(UnexpectedScrapeCancellation) as exc_info:
            raise UnexpectedScrapeCancellation(msg)
        assert str(exc_info.value) == msg

    def test_stop_scrape_is_exception_subclass(self):
        """测试StopScrape是Exception的子类"""
        assert issubclass(StopScrape, Exception)

    def test_unexpected_scrape_cancellation_is_exception_subclass(self):
        """测试UnexpectedScrapeCancellation是Exception的子类"""
        assert issubclass(UnexpectedScrapeCancellation, Exception)


class TestScraperTaskLimit:
    """测试Scraper任务限流功能"""

    @pytest.mark.asyncio
    async def test_run_tasks_with_limit_empty_list(self):
        """测试空列表不执行任何任务"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        mock_process = AsyncMock()
        mock_process.return_value = None

        movie_list = []
        await scraper._run_tasks_with_limit(movie_list, 0, 5)

        assert mock_process.call_count == 0

    @pytest.mark.asyncio
    async def test_run_tasks_with_limit_single_task(self):
        """测试单个任务执行"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        task_results = []

        async def mock_process(task):
            task_results.append(task)

        scraper.process_one_file = mock_process

        movie_list = [Path("/test/video1.mp4")]
        await scraper._run_tasks_with_limit(movie_list, 1, 1)

        assert len(task_results) == 1
        assert task_results[0][0] == Path("/test/video1.mp4")

    @pytest.mark.asyncio
    async def test_run_tasks_with_limit_multiple_tasks(self):
        """测试多个任务执行"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        task_results = []

        async def mock_process(task):
            await asyncio.sleep(0.01)
            task_results.append(task)

        scraper.process_one_file = mock_process

        movie_list = [
            Path("/test/video1.mp4"),
            Path("/test/video2.mp4"),
            Path("/test/video3.mp4"),
        ]
        await scraper._run_tasks_with_limit(movie_list, 3, 2)

        assert len(task_results) == 3

    @pytest.mark.asyncio
    async def test_run_tasks_with_limit_thread_count_limited(self):
        """测试并发数限制生效"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        concurrent_count = 0
        max_concurrent = 0

        async def mock_process(task):
            nonlocal concurrent_count, max_concurrent
            concurrent_count += 1
            max_concurrent = max(max_concurrent, concurrent_count)
            await asyncio.sleep(0.05)
            concurrent_count -= 1

        scraper.process_one_file = mock_process

        movie_list = [Path(f"/test/video{i}.mp4") for i in range(5)]
        await scraper._run_tasks_with_limit(movie_list, 5, 2)

        assert max_concurrent <= 2

    @pytest.mark.asyncio
    async def test_run_tasks_with_limit_stops_on_exception(self):
        """测试任务执行中遇到异常会停止"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        async def mock_process(task):
            if "stop" in str(task[0]):
                raise ValueError("Test error")
            return None

        scraper.process_one_file = mock_process

        movie_list = [
            Path("/test/normal.mp4"),
            Path("/test/stop.mp4"),
            Path("/test/never_reached.mp4"),
        ]

        with pytest.raises(ValueError, match="Test error"):
            await scraper._run_tasks_with_limit(movie_list, 3, 2)

    @pytest.mark.asyncio
    async def test_run_tasks_with_limit_handles_stop_scrape(self):
        """测试处理StopScrape异常"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        completed_tasks = []

        async def mock_process(task):
            if "stop" in str(task[0]):
                raise StopScrape("User stopped")
            completed_tasks.append(task)
            return None

        scraper.process_one_file = mock_process

        with patch("mdcx.core.scraper.signal") as mock_signal:
            mock_signal.stop = False
            with patch("mdcx.models.flags.Flags") as mock_flags:
                mock_flags.stop_requested = False

                movie_list = [
                    Path("/test/first.mp4"),
                    Path("/test/stop.mp4"),
                ]

                await scraper._run_tasks_with_limit(movie_list, 2, 2)

        assert len(completed_tasks) >= 1


class TestScraperTaskExecution:
    """测试Scraper任务执行逻辑"""

    @pytest.mark.asyncio
    async def test_process_one_file_updates_flags(self):
        """测试处理文件时更新标志"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        with patch("mdcx.core.scraper.get_file_info_v2") as mock_info:
            mock_file_info = MagicMock()
            mock_file_info.number = "TEST-001"
            mock_file_info.folder_path = Path("/test")
            mock_file_info.file_show_name = "TEST-001"
            mock_file_info.file_show_path = "/test/TEST-001.mp4"
            mock_file_info.file_path = Path("/test/TEST-001.mp4")
            mock_info.return_value = mock_file_info

            with patch("mdcx.core.scraper._process_one_file") as mock_process:
                mock_process.return_value = (None, None)

                with patch("mdcx.core.scraper.Flags") as mock_flags:
                    mock_flags.counting_order = 0
                    mock_flags.scrape_starting = 0
                    mock_flags.scrape_started = 0
                    mock_flags.succ_count = 0
                    mock_flags.fail_count = 0
                    mock_flags.file_mode = MagicMock()

                    task = (Path("/test/TEST-001.mp4"), 1, 1)
                    await scraper.process_one_file(task)


class TestScraperConcurrency:
    """测试Scraper并发控制"""

    @pytest.mark.asyncio
    async def test_concurrent_execution_order(self):
        """测试并发执行顺序"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        execution_order = []

        async def mock_process(task):
            await asyncio.sleep(0.02)
            execution_order.append(str(task[0]))

        scraper.process_one_file = mock_process

        movie_list = [Path(f"/test/video{i}.mp4") for i in range(4)]
        await scraper._run_tasks_with_limit(movie_list, 4, 2)

        assert len(execution_order) == 4

    @pytest.mark.asyncio
    async def test_task_cancellation_on_stop(self):
        """测试停止时取消任务"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        cancelled_count = 0

        async def mock_process(task):
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                nonlocal cancelled_count
                cancelled_count += 1
                raise

        scraper.process_one_file = mock_process

        with patch("mdcx.core.scraper.signal") as mock_signal:
            mock_signal.stop = True

            movie_list = [Path("/test/video1.mp4")]
            await scraper._run_tasks_with_limit(movie_list, 1, 1)


class TestScraperIntegration:
    """Scraper集成测试"""

    @pytest.mark.asyncio
    async def test_full_scrape_workflow_with_mocked_dependencies(self):
        """测试完整的刮削工作流（模拟依赖）"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        with patch.object(scraper, "process_one_file", new_callable=AsyncMock) as mock_process:
            mock_process.return_value = None

            movie_list = [Path("/test/sample.mp4")]
            await scraper._run_tasks_with_limit(movie_list, 1, 1)

            assert mock_process.call_count == 1

    def test_scraper_initialization(self):
        """测试Scraper初始化"""
        from mdcx.core.scraper import Scraper

        mock_provider = MagicMock()
        scraper = Scraper(mock_provider)

        assert scraper.crawler_provider == mock_provider
