nums=[]
for i in range(1,21):
    nums.append(i)
new_nums=[2*x for x in nums if x%2==0]#推导式生成新列表
print(f"原列表: {nums}")
print(f"新列表: {new_nums}")