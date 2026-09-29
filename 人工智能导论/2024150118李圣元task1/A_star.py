import copy
from collections import deque
#定义棋盘
class grid:
    target = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    #初始化
    def __init__(self, state,parent=None):
        self.state = state
        self.parent = parent
        self.h = self.get_h()
        if parent:
            self.step_num = parent.step_num + 1
        else:
            self.step_num = 0
        self.f=self.h+self.step_num
    #计算h值,使用曼哈顿距离
    def get_h(self):
        h=0
        for i in range(3):
            for j in range(3):
                target_num=self.target[i][j]
                index=self.find_num(target_num)
                h+=abs(index[0]-i)+abs(index[1]-j)
        return h
    #找数字0的位置
    def find_num(self,target_num):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == target_num:
                    return [i, j]
    #up,down,left,right
    def move(self, i, j):
        x,y=self.find_num(0)
        new_i,new_j=x+i, y+j
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = copy.deepcopy(self.state)
            new_state[x][y] = new_state[new_i][new_j]
            new_state[new_i][new_j] = 0
            return new_state
        return None
    def up(self):
        return self.move(-1, 0)
    def down(self):
        return self.move(1, 0)
    def left(self):
        return self.move(0, -1)
    def right(self):
        return self.move(0, 1)
    #主要move操作
    def move_0(self):
        new_grid = []
        i = self.find_num(0)[0]
        j = self.find_num(0)[1]
        if i>0:
            new_grid.append(self.up())
        if i<2:
            new_grid.append(self.down())
        if j>0:
            new_grid.append(self.left())
        if j<2:
            new_grid.append(self.right())
        return new_grid
#计算逆序数
def get_t(nums):
    sum_num = 0
    flat = []
    for i in range(3):
        for j in range(3):
            if nums[i][j] == 0:
                continue
            else:
                flat.append(nums[i][j])
    for i in range(len(flat)):
        for j in range(i):
            if flat[j] > flat[i]:
                sum_num+=1
    return sum_num

#判断当前八数码问题是否可解
def judge(now, target):
    num1 = get_t(now)
    num2 = get_t(target)
    if num1 % 2 == num2 % 2:
        return True
    return False
#A_star算法
def A_star(start_grid):
    A_list= [start_grid]
    visited = set()
    while A_list:
        # 从A_list中选择f值最小的网格
        A_list.sort(key=lambda x: x.f)
        current = A_list.pop(0)
        state_tuple = tuple(tuple(row) for row in current.state)
        # 如果当前状态已访问过，跳过
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        # 检查是否达到目标状态
        if current.state == grid.target:
            path = []
            while current:
                path.append(current.state)
                current = current.parent
            return path[::-1]
        # 尝试所有可能的移动
        move_states = current.move_0()
        for move in move_states:
            if move is not None:
                state_tuple = tuple(tuple(row) for row in move)
                if state_tuple not in visited:
                    new_grid = grid(move, current)
                    new_state_tuple = tuple(tuple(row) for row in new_grid.state)
                    if new_state_tuple not in visited:
                        state=False
                        for A_list_grid in A_list:
                            if tuple(tuple(row) for row in A_list_grid.state) == new_state_tuple and A_list_grid.f <= new_grid.f:
                                state=True
                                break
                        if not state:
                            A_list.append(new_grid)
    return None
start_state=[[1, 2, 3], [0, 8, 4], [7, 6, 5]]
g=grid(start_state)
if not judge(start_state,grid.target):
    print("无解")
else :
    path=A_star(g)
    if path:
        for i, state in enumerate(path):
            print(f"第{i}步:")
            for row in state:
                print(row)
            print()
    else:
        print("未找到解")
