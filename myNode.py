from anytree import Node, RenderTree


class MyNode():
    def __init__(self, parent, child, name, finished = False, node = None):
        self.parent = parent
        self.child = child
        self.name = name
        self.finished = finished
        self.node = Node(name, parent = parent)

    def setChildren(self, children):
        self.node.children = children
    
    def setFinished(self):
        self.finished = True