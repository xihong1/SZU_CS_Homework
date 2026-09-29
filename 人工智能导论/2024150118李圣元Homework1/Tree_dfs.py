class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
    def addChild(self, child):
        self.children.append(child)
    def __str__(self):
        return str(self.data)


def dfs(root):
    if root is None:
        return
    for child in root.children:
        dfs(child)
    print(root.data)
a=TreeNode(1)
b=TreeNode(2)
c=TreeNode(3)
d=TreeNode(4)
e=TreeNode(5)
f=TreeNode(6)
a.addChild(b)
a.addChild(c)
b.addChild(d)
b.addChild(e)
c.addChild(f)
dfs(a)