IDnum 类文档

概述

IDnum 是一个继承自 str 的 Python 类，专门用于处理中国大陆 18 位身份证号码。它提供了身份证号码的解析、验证、信息提取和修改等功能。

主要功能

· 身份证号码格式验证
· 地址码解析（省/市/县）
· 出生日期提取
· 性别判断
· 校验码计算与验证
· 身份证信息的修改与更新

安装与依赖

环境要求

· Python 3.6+
· 标准库：csv、pathlib

数据文件

需要 dc_20250328.csv 行政区划数据文件，存放于 data 目录下，格式为：

```
地址码,地址名称
110000,北京市
110101,东城区
...
```

类属性

属性 类型 描述
WEIGHT list[int] 校验权数列表 [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
MAP list[str] 校验码映射表 ["1","0","X","9","8","7","6","5","4","3","2"]

初始化

```python
def __init__(self, number: str) -> None
```

参数

· number (str): 身份证号码，支持 17 位（本体码）或 18 位

异常

· ValueError: 号码包含非法字符或长度不正确时抛出

示例

```python
# 18位身份证
id1 = IDnum("11010119900307663X")

# 17位本体码（自动补全校验码位）
id2 = IDnum("11010119900307663")
```

属性

基本信息

属性 类型 描述
number str 完整的 18 位身份证号码
number_list list[str] 身份证号码字符列表
master str 本体码（前 17 位）
master_list list[int] 本体码数字列表

地址信息

属性 类型 描述
direction str 6 位地址码
address str 地址描述（从数据文件获取）

出生信息

属性 类型 描述
birthday str 8 位出生日期码（YYYYMMDD）

顺序码与性别

属性 类型 描述
sequence str 3 位顺序码
sex str 性别："Male" 或 "Female"
is_male bool 是否为男性
is_female bool 是否为女性

校验信息

属性 类型 描述
check str 1 位校验码

方法

修改方法

change_direction(province, city, prefecture, reset_check=True)

修改地址码。

参数：

· province (str): 省级代码（2 位）
· city (str): 市级代码（2 位）
· prefecture (str): 县级代码（2 位）
· reset_check (bool): 是否重新计算校验码，默认 True

示例：

```python
id_num.change_direction("11", "01", "01")  # 改为北京市东城区
```

change_birthday(birthday, reset_check=True)

修改出生日期码。

参数：

· birthday (str): 8 位出生日期码（YYYYMMDD）
· reset_check (bool): 是否重新计算校验码，默认 True

示例：

```python
id_num.change_birthday("19900101")
```

change_sequence(sequence, reset_check=True)

修改顺序码。

参数：

· sequence (str): 3 位顺序码
· reset_check (bool): 是否重新计算校验码，默认 True

change_check(check)

手动修改校验码。

参数：

· check (str): 1 位校验码（数字或 'X'）

异常：

· ValueError: 校验码包含非法字符时抛出

工具方法

set_checknum()

根据前 17 位自动计算并设置校验码。

算法：

1. 本体码每位数字乘以对应权重后求和
2. 和除以 11 取余数
3. 根据余数从映射表获取校验码

使用示例

基本使用

```python
# 创建身份证对象
id_num = IDnum("11010119900307663X")

# 获取基本信息
print(f"号码: {id_num.number}")
print(f"地址码: {id_num.direction}")
print(f"地址: {id_num.address}")
print(f"出生日期: {id_num.birthday}")
print(f"性别: {id_num.sex}")
print(f"校验码: {id_num.check}")

# 验证校验码是否正确
id_num.set_checknum()
print(f"计算得到的校验码: {id_num.check}")
```

修改身份证信息

```python
id_num = IDnum("11010119900307663X")

# 修改地址为上海市浦东新区
id_num.change_direction("31", "01", "15")

# 修改出生日期
id_num.change_birthday("19951225")

# 修改顺序码（性别由顺序码奇偶决定）
id_num.change_sequence("123")

print(f"修改后的号码: {id_num.number}")
```

批量处理

```python
id_numbers = [
    "11010119900307663X",
    "310101199512250040",
    "440301198507153219"
]

for num in id_numbers:
    id_obj = IDnum(num)
    print(f"{num}: {id_obj.address}, {id_obj.birthday}, {id_obj.sex}")
```

注意事项

1. 数据文件依赖：address 属性需要 dc_20250328.csv 数据文件，确保文件存在于 data 目录下
2. 不可变性：虽然提供了修改方法，但建议谨慎修改身份证信息
3. 校验码自动计算：修改地址码、出生日期或顺序码后，建议保持 reset_check=True 以确保校验码正确
4. 线程安全：该类不是线程安全的，多线程环境下需要外部同步机制

错误处理

```python
try:
    id_num = IDnum("invalid_id")
except ValueError as e:
    print(f"错误: {e}")

try:
    id_num.change_check("Z")  # 非法校验码
except ValueError as e:
    print(f"校验码设置错误: {e}")
```

性能考虑

· 初始化时会读取行政区划数据文件，建议复用对象而不是频繁创建
· 属性访问是 O(1) 操作
· 校验码计算是 O(17) 操作，可忽略不计
