from collections import deque
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
    def addChild(self, child):
        self.children.append(child)
    def __str__(self):
        return str(self.data)

def bfs(root):
    if root is None:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.data)
        for child in node.children:
            queue.append(child)

a = TreeNode(1)
b = TreeNode(2)
c = TreeNode(3)
d = TreeNode(4)
e = TreeNode(5)
f = TreeNode(6)
a.addChild(b)
a.addChild(c)
b.addChild(d)
b.addChild(e)
c.addChild(f)
bfs(a)