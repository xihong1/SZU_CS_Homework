phone_book={}
#添加联系人
def add_contact(name, phone):
    if name in phone_book:
        print("联系人已存在！")
        return
    phone_book[name] = phone
    print("联系人已添加！")

def add():
    name=input("请输入联系人姓名：")
    phone=input("请输入联系人电话：")
    add_contact(name, phone)
#查找联系人
def find():
    name=input("请输入联系人姓名：")
    if name in phone_book:
        print("联系人电话为："+phone_book[name])
    else:
        print("联系人不存在！")
#删除联系人
def delete():
    name=input("请输入联系人姓名：")
    if name in phone_book:
        del phone_book[name]
        print("联系人已删除！")
    else:
        print("联系人不存在！")
#主菜单
def main():
    while True:
        print("欢迎使用通讯录系统")
        print("1. 添加联系人")
        print("2. 查找联系人")
        print("3. 删除联系人")
        print("4. 退出")
        choice=input("请输入操作编号：")
        if choice=="1":
            add()
        elif choice=="2":
            find()
        elif choice=="3":
            delete()
        elif choice=="4":
            break
        else:
            print("输入有误，请重新输入！")
        print()
        

if __name__=="__main__":
    main()