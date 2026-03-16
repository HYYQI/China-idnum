"""测试 __init__.py 模块"""

from idnum import (
    IDnum,
    get_address_map,
    get_full_version,
    __version__,
    __author__,
    __all__
)


class TestInitModule:
    """测试 __init__ 模块的导出内容"""
    
    def test_version(self):
        """测试版本号"""
        assert __version__ == "1.1.4"
    
    def test_author(self):
        """测试作者信息"""
        assert __author__ == "HYYQI"
    
    def test_all_exports(self):
        """测试 __all__ 列表"""
        expected = [
            "IDnum",
            "get_address_map", 
            "get_full_version"
        ]
        assert __all__ == expected
        assert all(hasattr(__import__('idnum'), attr) for attr in expected)
    
    def test_get_full_version(self):
        """测试get_full_version函数"""
        version_info = get_full_version()
        assert isinstance(version_info, str)
        assert "idnum 1.1.4" in version_info
        assert "20251005" in version_info
        assert "20250328" in version_info
    
    def test_get_address_map_type(self):
        """测试get_address_map返回类型"""
        address_map = get_address_map()
        assert isinstance(address_map, dict)