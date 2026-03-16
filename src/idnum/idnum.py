#!/usr/bin/env python3

# ID Number Class

import csv
from pathlib import Path

# 18位str型身份证号码
class IDnum(str):
    """
    中国18位身份证号码处理类
    
    该类继承自str，提供了对中国大陆18位身份证号码的解析、验证和操作功能。
    支持地址码解析、生日提取、性别判断、校验码计算等功能。
    
    Attributes:
        WEIGHT (list): 校验权数列表，用于计算校验码
        MAP (list): 校验码映射表，将余数映射为对应的校验码
    """
    
    WEIGHT  = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]         # 校验权数
    MAP     = ["1","0","X","9","8","7","6","5","4","3","2"] #映射值
    
    def __init__(self, number) -> None:
        """
        初始化身份证号码对象
        
        Args:
            number (str): 身份证号码，支持17位或18位
            
        Raises:
            ValueError: 当身份证号码包含非法字符或长度不正确时抛出
        """
        number = str(number).upper().strip()
        if not self.__check(number):
            raise ValueError("Contains illegal characters")
        
        if len(number) == 18:
            pass
        elif len(number) == 17:
            # 若17位自动视为本体码
            number = number + "-"
        else:
            raise ValueError("The ID Number in Chinese is 18 in length")
        
        self._direction  = number[:6]    # 地址码
        self._birthday   = number[6:14]  # 出生日期码
        self._sequence   = number[14:-1] # 顺序码
        self._check      = number[-1]    # 校验码
        del number
        
        # 数据来自腾讯位置服务(https://lbs.qq.com/service/webService/webServiceGuide/search/webServiceDistrict#9)
        current_dir = Path(__file__).parent
        data_dir = current_dir / "data"
        csv_file_path = data_dir / "dc_20250328.csv"
        
        with csv_file_path.open(newline="", encoding="utf-8") as file:
            codes = csv.reader(file)
            self._code_dict = {line[0]: line[1] for line in codes}
        
        super().__init__() # 初始化父类
    
    def __new__(cls, number):
        """
        创建新的身份证号码对象
        
        Args:
            number (str): 身份证号码
            
        Returns:
            IDnum: 身份证号码对象
        """
        number = str(number).upper().strip()
        return super().__new__(cls, number)
    
    def __check(self, num) -> bool:
        """
        检查身份证号码格式是否合法
        
        Args:
            num (str): 待检查的身份证号码
            
        Returns:
            bool: 如果号码合法返回True，否则返回False
        """
        for position, val in enumerate(num):
            if val.isdigit():
                continue
            elif val == "X" and position == 17:
                continue
            else:
                return False
        return True
    
    @property
    def number(self) -> str:
        """
        获取完整的身份证号码
        
        Returns:
            str: 18位身份证号码
        """
        return (
            self._direction  +
            self._birthday   +
            self._sequence   +
            self._check
        )
    
    @property
    def number_list(self) -> list[str]:
        """
        获取身份证号码的字符列表
        
        Returns:
            list[str]: 身份证号码各字符组成的列表
        """
        return list(self.number)
    
    @property
    def master(self) -> str:
        """
        获取身份证本体码（前17位）
        
        Returns:
            str: 身份证前17位本体码
        """
        return self.number[:-1]
    
    @property
    def master_list(self) -> list[int]:
        """
        获取身份证本体码的数字列表
        
        Returns:
            list[int]: 身份证前17位数字组成的列表
        """
        # 获取str型前17位数列表
        master = self.number_list[:-1]
        return [int(digit) for digit in master]
    
    @property
    def direction(self) -> str:
        """
        获取地址码
        
        Returns:
            str: 6位地址码
        """
        return self._direction
    
    @property
    def address(self) -> str:
        """
        获取地址描述
        
        从腾讯位置服务的行政区划数据中查找对应的地址描述
        
        Returns:
            str: 地址描述信息
            
        Note:
            需要dc_20250328.csv数据文件支持
        """
        return self._code_dict.get(self._direction, "Unknown")
    
    @property
    def birthday(self) -> str:
        """
        获取出生日期码
        
        Returns:
            str: 8位出生日期码，格式为YYYYMMDD
        """
        return self._birthday
    
    @property
    def sequence(self) -> str:
        """
        获取顺序码
        
        Returns:
            str: 3位顺序码
        """
        return self._sequence
    
    @property
    def sex(self) -> str:
        """
        获取性别
        
        Returns:
            str: "Male"表示男性，"Female"表示女性
        """
        return "Male" if int(self._sequence)%2 else "Female"
    
    @property
    def is_male(self) -> bool:
        """
        判断是否为男性
        
        Returns:
            bool: 如果是男性返回True，否则返回False
        """
        return self.sex=="Male"
    
    @property
    def is_female(self) -> bool:
        """
        判断是否为女性
        
        Returns:
            bool: 如果是女性返回True，否则返回False
        """
        return self.sex=="Female"
    
    @property
    def check(self) -> str:
        """
        获取校验码
        
        Returns:
            str: 1位校验码
        """
        return self._check
    
    def change_direction(self, province, city, prefecture, reset_check=True) -> None:
        """
        更改地址码
        
        Args:
            province (str): 省级代码（2位）
            city (str): 市级代码（2位）
            prefecture (str): 县级代码（2位）
            reset_check (bool): 是否重新计算校验码，默认为True
        """
        self._direction = str(province) + str(city) + str(prefecture)
        if reset_check:
            self.set_checknum()
    
    def change_birthday(self, birthday, reset_check=True) -> None:
        """
        更改出生日期码
        
        Args:
            birthday (str): 8位出生日期码，格式为YYYYMMDD
            reset_check (bool): 是否重新计算校验码，默认为True
        """
        self._birthday   = str(birthday)
        if reset_check:
            self.set_checknum()
    
    def change_sequence(self, sequence, reset_check=True) -> None:
        """
        更改顺序码
        
        Args:
            sequence (str): 3位顺序码
            reset_check (bool): 是否重新计算校验码，默认为True
        """
        self._sequence   = str(sequence)
        if reset_check:
            self.set_checknum()
    
    def change_check(self, check) -> None:
        """
        更改校验码
        
        Args:
            check (str): 1位校验码，可以是数字或'X'
            
        Raises:
            ValueError: 当校验码包含非法字符时抛出
        """
        check = str(check)
        if not (
            check.isdigit() or check.upper == "X"
        ):
            raise ValueError("Contains illegal characters")
        else:
            self._check  = str(check)
    
    def set_checknum(self) -> None:
        """
        根据前17位数自动设置校验位
        
        使用国家标准GB 11643-1999规定的校验算法计算校验码
        """
        master_list = self.master_list
        s = 0 # 校验和
        for index, digit in enumerate(master_list):
            s += digit * self.WEIGHT[index]
        self.change_check(
            self.MAP[s % 11]
        )

