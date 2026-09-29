import copy
from collections import deque
#定义棋盘
class grid:
    target = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    #初始化
    def __init__(self, state,parent=None):
        self.state = state
        self.parent = parent
        if parent:
            self.step_num = parent.step_num + 1
        else:
            self.step_num = 0
    #找数字0的位置
    def find_0(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return [i, j]
    #up,down,left,right
    def move(self, i, j):
        x,y=self.find_0()
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
        i = self.find_0()[0]
        j = self.find_0()[1]
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
#BFS算法
def BFS(start_grid):
    queue = deque([start_grid])
    visited = set()
    visited.add(tuple(tuple(row) for row in start_grid.state))
    while queue:
        current = queue.popleft()
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
                    visited.add(state_tuple)
                    new_grid = grid(move, current)
                    queue.append(new_grid)
    return None
start_state=[[1, 2, 3], [0, 8, 4], [7, 6, 5]]
g=grid(start_state)
if not judge(start_state,grid.target):
    print("无解")
else :
    path=BFS(g)
    if path:
        for i, state in enumerate(path):
            print(f"第{i}步:")
            for row in state:
                print(row)
            print()
    else:
        print("未找到解")
