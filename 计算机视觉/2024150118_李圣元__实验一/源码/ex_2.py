for i in range(1,21):
    #如果i是3的倍数，则跳过本次循环
    if i%3==0:
        continue
    else:
        #如果i大于15，则退出循环
        if i>15:
            break
        print(i)