#查表法
left=['(','[','{']
right=[')',']','}']

def lIndex(item):
    if item == left[0]:
        return 0
    elif item == left[1]:
        return 1
    else:
        return 2
class Stack:
    def __init__(self):
        #使用列表实现栈
        self.items=[]
        #记录未匹对括号数
        self.length=0
        #左括号数
        self.leftL=0
        # 右括号数
        self.rightL=0
    def push(self,item):
        #左括号不做判断直接进栈
        if item in left:
            self.items.append(item)
            self.length+=1
            self.leftL+=1
        #右括号分两个情况，右括号进栈前栈内有元素
        elif item in right and self.length>0 and self.items[-1] in left:
            #如果进栈前栈顶元素和进栈的元素不匹配，则直接进栈
            if item !=right[lIndex(self.items[-1])]:
                self.items.append(item)
                self.rightL+=1
                self.length+=1
            #如果匹配则栈顶元素出栈
            elif item ==right[lIndex(self.items[-1])]:
                self.items.pop(-1)
                self.leftL-=1
                self.length-=1
            #栈内没有元素则直接进栈
        else:
            self.items.append(item)
            self.rightL+=1
            self.length+=1
    #弹出操作
    def pop(self):
        return self.items.pop()
    #对应题目要求返回输出
    def out(self):
        #完全匹配
        if self.length==0:
            return 0
        #左侧多
        elif self.leftL>self.rightL:
            return -3
        #左和右数量一样但是不匹配
        elif self.leftL==self.rightL:
            return -1
        #右侧多
        else:
            return -2
i=4#这里遍历四次方便展示样例
while i:
    inStr = input()
    s = Stack()
    for e in inStr:
        if e in left or e in right:
            s.push(e)
    print(s.out())
    i-=1
