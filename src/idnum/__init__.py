"""
中国身份证号码处理模块

提供对中国大陆18位身份证号码的解析和操作。
"""

import csv
from pathlib import Path

from .idnum import IDnum

__version__ = "1.1.4"
__author__ = "HYYQI"
__all__ = [
    "IDnum",
    "get_address_map",
    "get_full_version"
]

def get_full_version() -> str:
    return """
idnum 1.1.4(20251005)
adcode csv file: 20250328
"""

def get_address_map() -> dict:
    # 数据来自腾讯位置服务(https://lbs.qq.com/service/webService/webServiceGuide/search/webServiceDistrict#9)
    data_dir = Path(__file__).parent / 'idnum.data'
    file_path = data_dir / "dc_20250328.csv"
    with file_path.open(newline="", encoding="utf-8") as file:
        codes = csv.reader(file)
        return {line[0]: line[1] for line in codes}
