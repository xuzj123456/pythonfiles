# coding=utf-8
import random

secret = random.randint(1, 100)
i = 0
guess = 0

while (guess != secret) or (i == 0):
    i += 1
    temp = input("请输入猜测的数字:")       # 注意input的格式全部为字符串
    guess = int(temp)
    if guess == secret:
        print("猜对了")
    else:
        if guess > secret:
            print("大了")
        else:
            print("小了")

print("猜了%d次" % i)
