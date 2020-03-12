import anytree
from anytree import Node, RenderTree

data = ["abc", "abd", "aec", "add", "adcf"]
from anytree.exporter import DotExporter

nodes = {}
first_node = None

for elem in data:
    parent_node = None
    parent_node_name = ""
    for i, val in enumerate(elem):
        if i not in nodes:
            nodes[i] = {}
        key = parent_node_name + val
        if key not in nodes[i]:
            print("Creating new node for ", key)
            nodes[i][key] = Node(key, parent=parent_node, display_name=val)
            print(nodes[i][key])
        if first_node is None:
            first_node = nodes[i][key]
        parent_node = nodes[i][key]
        parent_node_name = val

# for node in nodes:
#     print(node)
print()
print(nodes[0]["a"])