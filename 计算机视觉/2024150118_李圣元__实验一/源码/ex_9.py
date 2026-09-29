class Student:
    #初始化
    def __init__(self, name, score):
        self.name = name
        self.score = score
    #展示信息
    def display_info(self):
        return f"姓名: {self.name}, 成绩: {self.score}"
#主函数
def main():
    name = input("请输入学生姓名：")
    score = float(input("请输入学生成绩："))
    student = Student(name, score)
    print(student.display_info())

if __name__ == "__main__":
    main()