class Stack:
    def __init__(self):
        #使用列表实现栈
        self.items=[]
        #记录在B进队列之前，未匹对括号数
        self.length=0
        #B进栈时需要拆除的包裹数
        self.blength=0
    def push(self,item):
        if item=='(':
            self.length+=1
            self.items.append(item)
        elif item==')'and self.items[-1]=='(':
            self.length-=1
            self.items.pop()
        elif item==')'and self.items[-1]=='B':
            self.length+=1
            self.items.append(item)
        elif item=='B':
            self.blength=self.length
    def pop(self):
        return self.items.pop()
inStr=input()
s=Stack()
for e in inStr:
    s.push(e)
print(s.blength)

