"""
B+ Tree implementation for the lightweight DBMS.
"""
import graphviz
from typing import Any, List, Dict, Tuple, Optional, Union


class BPlusTreeNode:
    """Base class for B+ Tree nodes."""

    def __init__(self, order: int, is_leaf: bool = False):
        """
        Initialize a B+ Tree node.

        Args:
            order: The maximum number of keys in a node
            is_leaf: Whether this node is a leaf node
        """
        self.order = order
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.next = None  # For leaf nodes to form a linked list

    def is_full(self) -> bool:
        """Check if the node is full."""
        return len(self.keys) >= self.order - 1


class BPlusTree:
    """B+ Tree implementation for indexing."""

    def __init__(self, order: int = 5):
        """
        Initialize an empty B+ Tree.

        Args:
            order: The maximum number of keys in a node
        """
        self.root = BPlusTreeNode(order, True)
        self.order = order

    def copy(self):
        """Create a copy of the B+ Tree."""
        new_tree = BPlusTree(self.order)

        # Copy all key-value pairs
        for key, value in self.get_all():
            new_tree.insert(key, value)

        return new_tree

    def search(self, key: Any) -> Any:
        """
        Search for a key in the B+ tree. Return associated value if found, else None.

        Args:
            key: The key to search for

        Returns:
            The value associated with the key, or None if not found
        """
        node = self.root

        # Traverse from root to appropriate leaf node
        while not node.is_leaf:
            # Find the appropriate child to follow
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        # Search in the leaf node
        for i, k in enumerate(node.keys):
            if k == key:
                return node.children[i]  # In leaf nodes, children array stores values

        return None  # Key not found

    def insert(self, key: Any, value: Any, callback=None) -> None:
        """
        Insert key-value pair into the B+ tree.
        Handle root splitting if necessary.
        Maintain sorted order and balance properties.

        Args:
            key: The key to insert
            value: The value associated with the key
            callback: Optional callback function for visualization
        """
        # If root is full, create a new root
        if self.root.is_full():
            # Create a new root
            new_root = BPlusTreeNode(self.order, False)
            new_root.children.append(self.root)
            old_root = self.root
            self.root = new_root
            self._split_child(new_root, 0, callback)

            if callback:
                callback(old_root, 'split', f'Root node split, new key: {key}')

        self._insert_non_full(self.root, key, value, callback)

    def _insert_non_full(self, node: BPlusTreeNode, key: Any, value: Any, callback=None) -> None:
        """
        Recursive helper to insert into a non-full node.
        Split child nodes if they become full during insertion.

        Args:
            node: The current node
            key: The key to insert
            value: The value associated with the key
            callback: Optional callback function for visualization
        """
        # Find position to insert
        i = len(node.keys) - 1

        # If this is a leaf node
        if node.is_leaf:
            # Find the position to insert the key
            while i >= 0 and key < node.keys[i]:
                i -= 1

            # Insert the key and value
            node.keys.insert(i + 1, key)
            node.children.insert(i + 1, value)  # In leaf nodes, children array stores values

            if callback:
                callback(node, 'insert', f'Inserted key {key} at position {i + 1}')
        else:
            # Find the child which is going to have the new key
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            # If the child is full, split it
            if node.children[i].is_full():
                self._split_child(node, i, callback)
                # After split, the middle key is pushed up and the node now has one more key
                if key > node.keys[i]:
                    i += 1

            # Recursively insert into the appropriate child
            self._insert_non_full(node.children[i], key, value, callback)

    def _split_child(self, parent: BPlusTreeNode, index: int, callback=None) -> None:
        """
        Split parent's child at given index.
        For leaves: preserve linked list structure and copy middle key to parent.
        For internal nodes: promote middle key and split children.

        Args:
            parent: The parent node
            index: The index of the child to split
            callback: Optional callback function for visualization
        """
        child = parent.children[index]
        new_node = BPlusTreeNode(self.order, child.is_leaf)

        # Split the child
        mid = self.order // 2

        # For leaf nodes
        if child.is_leaf:
            # Copy keys and values to the new node
            new_node.keys = child.keys[mid:]
            new_node.children = child.children[mid:]  # Values in leaf nodes

            # Update the original child
            child.keys = child.keys[:mid]
            child.children = child.children[:mid]

            # Update the linked list
            new_node.next = child.next
            child.next = new_node

            # Insert the middle key into the parent
            parent.keys.insert(index, new_node.keys[0])
            parent.children.insert(index + 1, new_node)

            if callback:
                callback(child, 'split', f'Leaf node split at key {new_node.keys[0]}')
        else:
            # For internal nodes
            # Copy keys and children to the new node
            new_node.keys = child.keys[mid+1:]
            new_node.children = child.children[mid+1:]

            # Move the middle key to the parent
            middle_key = child.keys[mid]
            parent.keys.insert(index, middle_key)

            # Update the original child
            child.keys = child.keys[:mid]
            child.children = child.children[:mid+1]

            # Insert the new node into the parent
            parent.children.insert(index + 1, new_node)

            if callback:
                callback(child, 'split', f'Internal node split at key {middle_key}')

    def delete(self, key: Any, callback=None) -> bool:
        """
        Delete key from the B+ tree.
        Handle underflow by borrowing from siblings or merging nodes.
        Update root if it becomes empty.
        Return True if deletion succeeded, False otherwise.

        Args:
            key: The key to delete
            callback: Optional callback function for visualization

        Returns:
            True if the key was deleted, False otherwise
        """
        if not self.root.keys:
            return False  # Empty tree

        result = self._delete(self.root, key, callback)

        # If the root is an internal node with no keys, make its first child the new root
        if not self.root.is_leaf and not self.root.keys:
            old_root = self.root
            self.root = self.root.children[0]

            if callback:
                callback(old_root, 'delete', f'Root node became empty, promoting child')

        return result

    def _delete(self, node: BPlusTreeNode, key: Any, callback=None) -> bool:
        """
        Recursive helper for deletion. Handle leaf and internal nodes.
        Ensure all nodes maintain minimum keys after deletion.

        Args:
            node: The current node
            key: The key to delete
            callback: Optional callback function for visualization

        Returns:
            True if the key was deleted, False otherwise
        """
        min_keys = (self.order - 1) // 2

        # Case 1: Key is in this node and it's a leaf
        if node.is_leaf:
            if key in node.keys:
                idx = node.keys.index(key)
                node.keys.pop(idx)
                node.children.pop(idx)  # Remove the associated value

                if callback:
                    callback(node, 'delete', f'Deleted key {key} from leaf node')

                return True
            return False  # Key not found

        # Case 2: Key might be in a child node
        # Find the child that would contain the key
        idx = 0
        while idx < len(node.keys) and key >= node.keys[idx]:
            idx += 1

        child = node.children[idx]

        # Ensure the child has enough keys before recursing
        if len(child.keys) <= min_keys:
            self._fill_child(node, idx, callback)

        # If the last child has been merged, recurse into the previous child
        if idx > len(node.children) - 1:
            return self._delete(node.children[idx-1], key, callback)
        else:
            return self._delete(node.children[idx], key, callback)

    def _fill_child(self, node: BPlusTreeNode, idx: int, callback=None) -> None:
        """
        Ensure child at given index has enough keys by borrowing from siblings or merging.

        Args:
            node: The parent node
            idx: The index of the child to fill
            callback: Optional callback function for visualization
        """
        min_keys = (self.order - 1) // 2
        child = node.children[idx]

        # Try to borrow from left sibling
        if idx > 0 and len(node.children[idx-1].keys) > min_keys:
            self._borrow_from_prev(node, idx, callback)
        # Try to borrow from right sibling
        elif idx < len(node.children) - 1 and len(node.children[idx+1].keys) > min_keys:
            self._borrow_from_next(node, idx, callback)
        # Merge with a sibling
        else:
            if idx < len(node.children) - 1:
                self._merge(node, idx, callback)
            else:
                self._merge(node, idx-1, callback)

    def _borrow_from_prev(self, node: BPlusTreeNode, idx: int, callback=None) -> None:
        """
        Borrow a key from the left sibling to prevent underflow.

        Args:
            node: The parent node
            idx: The index of the child that needs a key
            callback: Optional callback function for visualization
        """
        child = node.children[idx]
        sibling = node.children[idx-1]

        # For leaf nodes
        if child.is_leaf:
            # Move the last key and value from sibling to child
            child.keys.insert(0, sibling.keys.pop())
            child.children.insert(0, sibling.children.pop())

            # Update the parent key
            node.keys[idx-1] = child.keys[0]

            if callback:
                callback(child, 'redistribute', f'Borrowed key {child.keys[0]} from left sibling')
        else:
            # For internal nodes
            # Move a key from parent to child
            child.keys.insert(0, node.keys[idx-1])

            # Move the last key from sibling to parent
            node.keys[idx-1] = sibling.keys.pop()

            # Move the last child from sibling to child
            if sibling.children:
                child.children.insert(0, sibling.children.pop())

            if callback:
                callback(child, 'redistribute', f'Borrowed key {node.keys[idx-1]} from parent')

    def _borrow_from_next(self, node: BPlusTreeNode, idx: int, callback=None) -> None:
        """
        Borrow a key from the right sibling to prevent underflow.

        Args:
            node: The parent node
            idx: The index of the child that needs a key
            callback: Optional callback function for visualization
        """
        child = node.children[idx]
        sibling = node.children[idx+1]

        # For leaf nodes
        if child.is_leaf:
            # Move the first key and value from sibling to child
            child.keys.append(sibling.keys.pop(0))
            child.children.append(sibling.children.pop(0))

            # Update the parent key
            node.keys[idx] = sibling.keys[0]

            if callback:
                callback(child, 'redistribute', f'Borrowed key {child.keys[-1]} from right sibling')
        else:
            # For internal nodes
            # Move a key from parent to child
            child.keys.append(node.keys[idx])

            # Move the first key from sibling to parent
            node.keys[idx] = sibling.keys.pop(0)

            # Move the first child from sibling to child
            if sibling.children:
                child.children.append(sibling.children.pop(0))

            if callback:
                callback(child, 'redistribute', f'Borrowed key {node.keys[idx]} from parent')

    def _merge(self, node: BPlusTreeNode, idx: int, callback=None) -> None:
        """
        Merge child at index with its right sibling. Update parent keys.

        Args:
            node: The parent node
            idx: The index of the left child to merge
            callback: Optional callback function for visualization
        """
        left = node.children[idx]
        right = node.children[idx+1]

        # For leaf nodes
        if left.is_leaf:
            # Append all keys and values from right to left
            left.keys.extend(right.keys)
            left.children.extend(right.children)

            # Update the linked list
            left.next = right.next

            if callback:
                callback(left, 'merge', f'Merged leaf nodes')
        else:
            # For internal nodes
            # Move the key from parent to left
            left.keys.append(node.keys[idx])

            # Append all keys and children from right to left
            left.keys.extend(right.keys)
            left.children.extend(right.children)

            if callback:
                callback(left, 'merge', f'Merged internal nodes with key {node.keys[idx]}')

        # Remove the key and right child from parent
        node.keys.pop(idx)
        node.children.pop(idx+1)

    def update(self, key: Any, new_value: Any) -> bool:
        """
        Update value associated with an existing key. Return True if successful.

        Args:
            key: The key to update
            new_value: The new value to associate with the key

        Returns:
            True if the key was updated, False otherwise
        """
        node = self.root

        # Traverse to the leaf node
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        # Find the key in the leaf node
        for i, k in enumerate(node.keys):
            if k == key:
                node.children[i] = new_value  # Update the value
                return True

        return False  # Key not found

    def range_query(self, start_key: Any, end_key: Any) -> List[Tuple[Any, Any]]:
        """
        Return all key-value pairs where start_key <= key <= end_key.
        Traverse leaf nodes using next pointers for efficient range scans.

        Args:
            start_key: The lower bound of the range (inclusive)
            end_key: The upper bound of the range (inclusive)

        Returns:
            A list of (key, value) tuples in the range
        """
        result = []

        if not self.root.keys:
            return result  # Empty tree

        # Find the leaf node containing the start key
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and start_key >= node.keys[i]:
                i += 1
            node = node.children[i]

        # Traverse the leaf nodes and collect keys in the range
        while node:
            for i, key in enumerate(node.keys):
                if start_key <= key <= end_key:
                    result.append((key, node.children[i]))

            # If we've passed the end key, break
            if node.keys and node.keys[-1] > end_key:
                break

            node = node.next

        return result

    def get_all(self) -> List[Tuple[Any, Any]]:
        """
        Return all key-value pairs in the tree using in-order traversal.

        Returns:
            A list of (key, value) tuples
        """
        result = []

        if not self.root.keys:
            return result  # Empty tree

        # Find the leftmost leaf
        node = self.root
        while not node.is_leaf:
            node = node.children[0]

        # Traverse all leaf nodes
        while node:
            for i, key in enumerate(node.keys):
                result.append((key, node.children[i]))
            node = node.next

        return result

    def visualize_tree(self) -> graphviz.Digraph:
        """
        Generate Graphviz representation of the B+ tree structure.

        Returns:
            A Graphviz Digraph object
        """
        dot = graphviz.Digraph()
        dot.attr('node', shape='record')

        if not self.root.keys:
            dot.node('root', 'Empty Tree')
            return dot

        # Add nodes and edges
        self._add_nodes(dot, self.root)
        self._add_edges(dot, self.root)

        return dot

    def _add_nodes(self, dot: graphviz.Digraph, node: BPlusTreeNode, prefix: str = '') -> None:
        """
        Recursively add nodes to Graphviz object (for visualization).

        Args:
            dot: The Graphviz Digraph object
            node: The current node
            prefix: A prefix for the node ID
        """
        # Create a unique ID for the node
        node_id = f"{prefix}_{id(node)}"

        # Create the node label
        if node.is_leaf:
            # For leaf nodes, show keys and values
            label = "{ "
            for i, key in enumerate(node.keys):
                if i > 0:
                    label += " | "
                label += f"{key}: {node.children[i]}"
            label += " }"
        else:
            # For internal nodes, show only keys
            label = "{ " + " | ".join(str(key) for key in node.keys) + " }"

        # Add the node to the graph
        dot.node(node_id, label)

        # Recursively add child nodes
        if not node.is_leaf:
            for i, child in enumerate(node.children):
                self._add_nodes(dot, child, f"{prefix}_{i}")

    def _add_edges(self, dot: graphviz.Digraph, node: BPlusTreeNode, prefix: str = '') -> None:
        """
        Add edges between nodes and dashed lines for leaf connections (for visualization).

        Args:
            dot: The Graphviz Digraph object
            node: The current node
            prefix: A prefix for the node ID
        """
        node_id = f"{prefix}_{id(node)}"

        # Add edges to children
        if not node.is_leaf:
            for i, child in enumerate(node.children):
                child_id = f"{prefix}_{i}_{id(child)}"
                dot.edge(node_id, child_id)
                self._add_edges(dot, child, f"{prefix}_{i}")

        # Add dashed edges between leaf nodes
        if node.is_leaf and node.next:
            next_id = f"{prefix}_next_{id(node.next)}"
            dot.edge(node_id, next_id, style='dashed', color='blue')
