"""测试 IDnum 类的单元测试"""

import pytest
import tempfile
import csv
from pathlib import Path
from idnum import IDnum, get_address_map, get_full_version


class TestIDnumBasic:
    """测试 IDnum 类的基本功能"""
    
    def test_init_valid_18digit(self):
        """测试初始化有效的18位身份证号"""
        id_num = IDnum("11010119900307663X")
        assert id_num.number == "11010119900307663X"
        assert isinstance(id_num, str)
        assert str(id_num) == "11010119900307663X"
    
    def test_init_valid_17digit(self):
        """测试初始化17位本体码"""
        id_num = IDnum("11010119900307663")
        assert id_num.number == "11010119900307663-"
        assert id_num.master == "11010119900307663"
    
    def test_init_with_spaces(self):
        """测试带空格的身份证号"""
        id_num = IDnum(" 11010119900307663X ")
        assert id_num.number == "11010119900307663X"
    
    def test_init_lowercase_x(self):
        """测试小写x的身份证号"""
        id_num = IDnum("11010119900307663x")
        assert id_num.number == "11010119900307663X"
    
    def test_init_invalid_length(self):
        """测试无效长度的身份证号"""
        with pytest.raises(ValueError, match="The ID Number in Chinese is 18 in length"):
            IDnum("1101011990030766")  # 16位
        
        with pytest.raises(ValueError, match="The ID Number in Chinese is 18 in length"):
            IDnum("1101011990030766312")  # 19位
    
    def test_init_illegal_characters(self):
        """测试包含非法字符的身份证号"""
        with pytest.raises(ValueError, match="Contains illegal characters"):
            IDnum("11010119900307663A")  # 非法字符A
        
        with pytest.raises(ValueError, match="Contains illegal characters"):
            IDnum("1101011990030766#X")  # 非法字符#


class TestIDnumProperties:
    """测试 IDnum 类的属性"""
    
    @pytest.fixture
    def id_male(self):
        """男性身份证号（顺序码奇数）"""
        return IDnum("11010119900307663X")
    
    @pytest.fixture
    def id_female(self):
        """女性身份证号（顺序码偶数）"""
        return IDnum("110101199003076640")
    
    def test_number_property(self, id_male):
        """测试number属性"""
        assert id_male.number == "11010119900307663X"
    
    def test_number_list_property(self, id_male):
        """测试number_list属性"""
        expected = ['1','1','0','1','0','1','1','9','9','0','0','3','0','7','6','6','3','X']
        assert id_male.number_list == expected
    
    def test_master_property(self, id_male):
        """测试master属性（本体码）"""
        assert id_male.master == "11010119900307663"
        assert len(id_male.master) == 17
    
    def test_master_list_property(self, id_male):
        """测试master_list属性"""
        expected = [1,1,0,1,0,1,1,9,9,0,0,3,0,7,6,6,3]
        assert id_male.master_list == expected
    
    def test_direction_property(self, id_male):
        """测试direction属性（地址码）"""
        assert id_male.direction == "110101"
        assert len(id_male.direction) == 6
    
    def test_birthday_property(self, id_male):
        """测试birthday属性（出生日期码）"""
        assert id_male.birthday == "19900307"
        assert len(id_male.birthday) == 8
    
    def test_sequence_property(self, id_male):
        """测试sequence属性（顺序码）"""
        assert id_male.sequence == "663"
        assert len(id_male.sequence) == 3
    
    def test_sex_property(self, id_male, id_female):
        """测试sex属性（性别）"""
        assert id_male.sex == "Male"
        assert id_female.sex == "Female"
    
    def test_is_male_property(self, id_male, id_female):
        """测试is_male属性"""
        assert id_male.is_male is True
        assert id_female.is_male is False
    
    def test_is_female_property(self, id_male, id_female):
        """测试is_female属性"""
        assert id_male.is_female is False
        assert id_female.is_female is True
    
    def test_check_property(self, id_male):
        """测试check属性（校验码）"""
        assert id_male.check == "X"


class TestIDnumAddress:
    """测试地址码相关功能"""
    
    @pytest.fixture
    def temp_csv_file(self):
        """创建临时CSV文件用于测试"""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(["110101", "北京市东城区"])
            writer.writerow(["310101", "上海市黄浦区"])
            writer.writerow(["440301", "深圳市福田区"])
            temp_path = Path(f.name)
        
        yield temp_path
        
        # 清理临时文件
        temp_path.unlink()
    
    def test_address_property_with_mock_data(self, monkeypatch, temp_csv_file):
        """使用模拟数据测试address属性"""
        # 模拟get_address_map函数返回测试数据
        def mock_get_map():
            with temp_csv_file.open(newline="", encoding="utf-8") as file:
                codes = csv.reader(file)
                return {line[0]: line[1] for line in codes}
        
        monkeypatch.setattr("idnum.get_address_map", mock_get_map)
        
        id_num = IDnum("11010119900307663X")
        assert id_num.address == "北京市东城区"
        
        id_num2 = IDnum("310101199003076640")
        assert id_num2.address == "上海市黄浦区"
    
    def test_address_unknown(self, monkeypatch, temp_csv_file):
        """测试未知地址码"""
        def mock_get_map():
            with temp_csv_file.open(newline="", encoding="utf-8") as file:
                codes = csv.reader(file)
                return {line[0]: line[1] for line in codes}
        
        monkeypatch.setattr("idnum.get_address_map", mock_get_map)
        
        id_num = IDnum("99999919900307663X")
        assert id_num.address == "Unknown"


class TestIDnumModification:
    """测试IDnum类的修改方法"""
    
    @pytest.fixture
    def id_num(self):
        return IDnum("11010119900307663X")
    
    def test_change_direction(self, id_num):
        """测试修改地址码"""
        id_num.change_direction("31", "01", "01", reset_check=False)
        assert id_num.direction == "310101"
        assert id_num.number.startswith("310101")
    
    def test_change_direction_with_reset_check(self, id_num):
        """测试修改地址码并自动重算校验码"""
        original_check = id_num.check
        id_num.change_direction("31", "01", "01", reset_check=True)
        assert id_num.direction == "310101"
        assert id_num.check != original_check  # 校验码应该改变
    
    def test_change_birthday(self, id_num):
        """测试修改出生日期"""
        id_num.change_birthday("19951225", reset_check=False)
        assert id_num.birthday == "19951225"
        assert "19951225" in id_num.number
    
    def test_change_birthday_with_reset_check(self, id_num):
        """测试修改出生日期并自动重算校验码"""
        original_check = id_num.check
        id_num.change_birthday("19951225", reset_check=True)
        assert id_num.birthday == "19951225"
        assert id_num.check != original_check
    
    def test_change_sequence(self, id_num):
        """测试修改顺序码"""
        id_num.change_sequence("888", reset_check=False)
        assert id_num.sequence == "888"
        assert id_num.number[14:17] == "888"
    
    def test_change_sequence_with_reset_check(self, id_num):
        """测试修改顺序码并自动重算校验码"""
        original_check = id_num.check
        id_num.change_sequence("888", reset_check=True)
        assert id_num.sequence == "888"
        assert id_num.check != original_check
    
    def test_change_sequence_affects_sex(self, id_num):
        """测试修改顺序码影响性别"""
        assert id_num.sex == "Male"  # 原顺序码663为奇数
        
        id_num.change_sequence("888", reset_check=False)
        assert id_num.sex == "Female"  # 888为偶数
    
    def test_change_check_valid(self, id_num):
        """测试手动修改有效的校验码"""
        id_num.change_check("8")
        assert id_num.check == "8"
        
        id_num.change_check("X")
        assert id_num.check == "X"
    
    def test_change_check_invalid(self, id_num):
        """测试手动修改无效的校验码"""
        with pytest.raises(ValueError, match="Contains illegal characters"):
            id_num.change_check("A")
        
        with pytest.raises(ValueError, match="Contains illegal characters"):
            id_num.change_check("12")  # 长度不对但会被str()转换，这里测试逻辑


class TestIDnumCheckDigit:
    """测试校验码计算功能"""
    
    def test_set_checknum_for_male(self):
        """测试为男性身份证号设置校验码"""
        id_num = IDnum("11010119900307663-")  # 17位本体码加占位符
        id_num.set_checknum()
        assert id_num.check == "X"
        assert id_num.number == "11010119900307663X"
    
    def test_set_checknum_for_female(self):
        """测试为女性身份证号设置校验码"""
        # 使用已知的正确身份证号
        id_num = IDnum("11010119900307664-")
        id_num.set_checknum()
        assert id_num.number[-1] in ["0","1","2","3","4","5","6","7","8","9","X"]
    
    def test_set_checknum_edge_cases(self):
        """测试边界情况的校验码计算"""
        test_cases = [
            ("11010119900307123", "3"),  # 假设的测试用例
            ("11010119900307456", "7"),
            ("11010119900307789", "2"),
        ]
        
        for master, expected_check in test_cases:
            id_num = IDnum(master + "-")
            id_num.set_checknum()
            assert id_num.check == expected_check, f"Failed for {master}"
    
    def test_verify_checkdigit_algorithm(self):
        """验证校验码算法的正确性"""
        # 测试几个已知的正确身份证号
        valid_ids = [
            "11010119900307663X",  # 示例号码
            "310101199003076640",
            "440301199003153219",
        ]
        
        for valid_id in valid_ids:
            id_num = IDnum(valid_id)
            original_check = id_num.check
            id_num.set_checknum()  # 重新计算
            assert id_num.check == original_check, f"Check digit mismatch for {valid_id}"


class TestIDnumIntegration:
    """集成测试"""
    
    def test_complete_workflow(self):
        """测试完整的工作流程"""
        # 1. 创建身份证对象
        id_num = IDnum("11010119900307663X")
        
        # 2. 验证初始状态
        assert id_num.direction == "110101"
        assert id_num.birthday == "19900307"
        assert id_num.sequence == "663"
        assert id_num.sex == "Male"
        
        # 3. 修改信息
        id_num.change_direction("44", "03", "01", reset_check=False)
        id_num.change_birthday("19951225", reset_check=False)
        id_num.change_sequence("246", reset_check=False)  # 改为女性
        
        # 4. 验证修改
        assert id_num.direction == "440301"
        assert id_num.birthday == "19951225"
        assert id_num.sequence == "246"
        assert id_num.sex == "Female"
        
        # 5. 重新计算校验码
        id_num.set_checknum()
        assert id_num.check != "X"  # 应该改变了
        
        # 6. 最终验证
        assert len(id_num.number) == 18
        assert id_num.number.startswith("44030119951225246")
    
    def test_from_17digit_to_18digit(self):
        """测试从17位到18位的转换"""
        master_17 = "11010119900307663"
        id_num = IDnum(master_17)
        
        assert id_num.master == master_17
        assert id_num.check == "-"  # 初始占位符
        
        id_num.set_checknum()
        assert id_num.check != "-"
        assert len(id_num.number) == 18
        assert id_num.number[:-1] == master_17


class TestModuleFunctions:
    """测试模块级函数"""
    
    def test_get_full_version(self):
        """测试get_full_version函数"""
        version = get_full_version()
        assert isinstance(version, str)
        assert "idnum 1.1.4" in version
        assert "20250328" in version
    
    def test_get_address_map(self, monkeypatch, temp_csv_file):
        """测试get_address_map函数"""
        def mock_get_map():
            with temp_csv_file.open(newline="", encoding="utf-8") as file:
                codes = csv.reader(file)
                return {line[0]: line[1] for line in codes}
        
        monkeypatch.setattr("idnum.get_address_map", mock_get_map)
        
        address_map = get_address_map()
        assert isinstance(address_map, dict)
        assert "110101" in address_map
        assert address_map["110101"] == "北京市东城区"
        assert address_map["310101"] == "上海市黄浦区"
        assert address_map["440301"] == "深圳市福田区"


@pytest.mark.parametrize("id_number,expected_direction,expected_birthday,expected_sex", [
    ("11010119900307663X", "110101", "19900307", "Male"),
    ("310101199512250040", "310101", "19951225", "Female"),
    ("440301198507153219", "440301", "19850715", "Male"),
    ("510107200112310024", "510107", "20011231", "Female"),
])
def test_parametrized_id_numbers(id_number, expected_direction, expected_birthday, expected_sex):
    """参数化测试多个身份证号"""
    id_num = IDnum(id_number)
    assert id_num.direction == expected_direction
    assert id_num.birthday == expected_birthday
    assert id_num.sex == expected_sex
