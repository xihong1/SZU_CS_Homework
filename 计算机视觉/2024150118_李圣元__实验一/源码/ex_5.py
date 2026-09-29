test=(1,2)
print("test:",test)
try:
    #尝试修改元组中的元素
    test[0]=3
    print("test:",test)
except Exception as e:
    print("Error:",e)