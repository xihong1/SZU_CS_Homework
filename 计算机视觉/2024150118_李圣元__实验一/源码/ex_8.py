import random
#产生随机数
def generate_a_num():
    return random.randint(1, 100)
#猜数字游戏实现逻辑
def guess_num(num):
    while True:
        guess = int(input("请输入你猜的数字（1-100）："))
        if guess < num:
            print("太小了，请再试一次。")
        elif guess > num:
            print("太大了，请再试一次。")
        else:
            #如果猜对了，打印恭喜信息并退出循环
            print("恭喜你，猜对了！")
            break

def main():
    num = generate_a_num()
    guess_num(num)

if __name__ == "__main__":
    main()