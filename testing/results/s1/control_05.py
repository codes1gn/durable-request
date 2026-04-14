"""Binary search tree: insert, delete, search."""


class TreeNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key: int) -> None:
        self.key = key
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


class BST:
    def __init__(self) -> None:
        self._root: TreeNode | None = None

    def search(self, key: int) -> bool:
        return self._find(self._root, key) is not None

    def _find(self, node: TreeNode | None, key: int) -> TreeNode | None:
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._find(node.left, key)
        return self._find(node.right, key)

    def insert(self, key: int) -> None:
        self._root = self._insert(self._root, key)

    def _insert(self, node: TreeNode | None, key: int) -> TreeNode:
        if node is None:
            return TreeNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def delete(self, key: int) -> None:
        self._root = self._delete(self._root, key)

    def _delete(self, node: TreeNode | None, key: int) -> TreeNode | None:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = self._min_node(node.right)
            node.key = succ.key
            node.right = self._delete_min(node.right)
        return node

    def _min_node(self, node: TreeNode) -> TreeNode:
        while node.left is not None:
            node = node.left
        return node

    def _delete_min(self, node: TreeNode) -> TreeNode | None:
        if node.left is None:
            return node.right
        node.left = self._delete_min(node.left)
        return node
