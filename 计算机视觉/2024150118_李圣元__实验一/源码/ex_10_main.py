#导入对应模块
from ex_10_add import add
#获取用户输入的两个数字
num1 = int(input("请输入第一个数字："))
num2 = int(input("请输入第二个数字："))
#调用add函数进行相加
result = add(num1, num2)
print("两个数字的和为：" + str(result))