class TreeNode:
    def __init__(self) -> None:
        self.children = []
        self.metadata = []

    def value(self):
        value = 0
        if not self.children:
            value = sum(self.metadata)
        else:
            for metadata_entry in self.metadata:
                if 0 < metadata_entry <= len(self.children):
                    value += self.children[metadata_entry - 1].value()

        return value

    def __repr__(self) -> str:
        return "TreeNode({}, {})".format(self.children, self.metadata)


def parse_child(numbers: list[int], index: int = 0) -> (TreeNode, int):
    node = TreeNode()
    num_children = numbers[index]
    index += 1
    num_metadata = numbers[index]
    index += 1

    for i in range(num_children):
        child, index = parse_child(numbers, index)
        node.children.append(child)

    for i in range(num_metadata):
        node.metadata.append(numbers[index])
        index += 1

    return node, index


def parse_input(filename) -> list[int]:
    with open(filename, "r") as f:
        return list(map(int, f.read().strip().split(" ")))


def sum_metadata(node: TreeNode) -> int:
    cumulative = 0
    for child in node.children:
        cumulative += sum_metadata(child)
    cumulative += sum(node.metadata)
    return cumulative


numbers = parse_input("input.txt")
root, index = parse_child(numbers)
print(root)

print(sum_metadata(root))
print("value = ", root.value())
