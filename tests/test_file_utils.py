"""
测试文件工具函数
"""
import os
import atexit
import tempfile
from pathlib import Path

import pytest
from unittest.mock import MagicMock, patch


# 在导入前立即 mock signal 模块
signal_mock = MagicMock()
signal_mock.add_log = MagicMock()
_patcher = patch.dict('sys.modules', {'mdcx.signals': MagicMock(signal=signal_mock)})
_patcher.start()


def _cleanup_patcher():
    """清理 mock 补丁"""
    try:
        _patcher.stop()
    except:
        pass


atexit.register(_cleanup_patcher)


from mdcx.utils.file import (
    build_file_name_index,
    find_file_from_index,
    find_file_in_folder,
    delete_file_sync,
    move_file_sync
)


class TestFileUtils:
    """测试文件工具函数"""

    @pytest.fixture
    def temp_folder(self):
        """创建临时测试目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试文件结构
            folder = Path(tmpdir)
            (folder / "subfolder1").mkdir()
            (folder / "subfolder2").mkdir()
            
            # 创建测试文件
            (folder / "file1.txt").write_text("content1")
            (folder / "file2.txt").write_text("content2")
            (folder / "subfolder1" / "file3.txt").write_text("content3")
            (folder / "subfolder1" / "file4.txt").write_text("content4")
            (folder / "subfolder2" / "FILE5.txt").write_text("content5")  # 大写文件名
            
            yield folder

    @pytest.mark.asyncio
    async def test_build_file_name_index(self, temp_folder):
        """测试构建文件名索引"""
        index = await build_file_name_index(temp_folder)
        
        # 验证索引包含所有文件
        assert "file1.txt" in index
        assert "file2.txt" in index
        assert "file3.txt" in index
        assert "file4.txt" in index
        assert "file5.txt" in index  # 应该是小写的
        
        # 验证路径正确
        assert index["file1.txt"] == temp_folder / "file1.txt"
        assert index["file3.txt"] == temp_folder / "subfolder1" / "file3.txt"
        assert index["file5.txt"] == temp_folder / "subfolder2" / "FILE5.txt"

    @pytest.mark.asyncio
    async def test_build_file_name_index_empty_folder(self):
        """测试空目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            index = await build_file_name_index(tmpdir)
            assert index == {}

    @pytest.mark.asyncio
    async def test_build_file_name_index_nonexistent(self):
        """测试不存在的目录"""
        index = await build_file_name_index("/nonexistent/path/xyz123")
        assert index == {}

    def test_find_file_from_index(self, temp_folder):
        """测试从索引查找文件"""
        index = {
            "file1.txt": temp_folder / "file1.txt",
            "file2.txt": temp_folder / "file2.txt"
        }
        
        # 找到存在的文件
        result = find_file_from_index(index, ["file1.txt"])
        assert result == temp_folder / "file1.txt"
        
        # 按顺序查找，返回第一个匹配
        result = find_file_from_index(index, ["nonexistent.txt", "file2.txt", "file1.txt"])
        assert result == temp_folder / "file2.txt"
        
        # 找不到文件
        result = find_file_from_index(index, ["nonexistent.txt", "missing.txt"])
        assert result is None

    @pytest.mark.asyncio
    async def test_find_file_in_folder(self, temp_folder):
        """测试在文件夹中查找文件"""
        # 找到存在的文件
        result = await find_file_in_folder(temp_folder, ["file1.txt"])
        assert result == temp_folder / "file1.txt"
        
        # 大小写不敏感
        result = await find_file_in_folder(temp_folder, ["FILE1.TXT"])
        assert result == temp_folder / "file1.txt"
        
        # 找不到文件
        result = await find_file_in_folder(temp_folder, ["nonexistent.txt"])
        assert result is None

    def test_delete_file_sync(self):
        """测试同步删除文件"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = Path(f.name)
        
        # 删除存在的文件
        success, message = delete_file_sync(temp_file)
        assert success is True
        assert message == ""
        assert not temp_file.exists()
        
        # 删除不存在的文件（应该不报错）
        success, message = delete_file_sync(temp_file)
        assert success is True  # missing_ok=True，所以成功
        
        # 删除空路径
        success, message = delete_file_sync("")
        assert success is False
        assert "路径不能为空" in message

    def test_move_file_sync(self):
        """测试同步移动文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "source.txt"
            dst = Path(tmpdir) / "dest.txt"
            subdir = Path(tmpdir) / "sub"
            
            src.write_text("test content")
            
            # 正常移动
            success, message = move_file_sync(src, dst)
            assert success is True
            assert not src.exists()
            assert dst.exists()
            assert dst.read_text() == "test content"
            
            # 移动到不存在的目录（应该自动创建）
            subdir.mkdir()
            dst2 = subdir / "dest2.txt"
            success, message = move_file_sync(dst, dst2)
            assert success is True
            assert not dst.exists()
            assert dst2.exists()
