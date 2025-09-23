import random
import hashlib

class Node:
    """
    A node in the Treap data structure.
    Each node holds a key-value pair, a randomly assigned priority,
    and pointers to its left and right children.
    """
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.priority = random.random()  # Assign a random priority for heap property
        self.left = None
        self.right = None

class OACDT:
    """
    Orthogonal Array Cache Distribution Treap (OACDT).

    This class simulates a distributed caching system that uses a Treap for
    maintaining a balanced search tree of keys and an Orthogonal Array (OA)
    inspired mapping to distribute and replicate data across physical nodes.
    """
    def __init__(self, num_nodes, replica_factor):
        """
        Initializes the OACDT system.

        Args:
            num_nodes (int): The total number of physical cache nodes in the system.
            replica_factor (int): The number of nodes a single piece of data is
                                  replicated across. This corresponds to 'k' in OA notation.
        """
        if not isinstance(num_nodes, int) or num_nodes <= 0:
            raise ValueError("Number of nodes must be a positive integer.")
        if not isinstance(replica_factor, int) or not (0 < replica_factor <= num_nodes):
            raise ValueError("Replica factor must be a positive integer and not exceed the number of nodes.")

        self.root = None
        self.num_nodes = num_nodes
        self.replica_factor = replica_factor
        # A list representing the physical cache nodes, identified by an integer index.
        self.cache_replicas = list(range(num_nodes))
        # Add a verbose flag to control detailed logging like rotations
        self.verbose = False

    def _get_replicas_from_oa(self, key):
        """
        Simulates Orthogonal Array mapping to deterministically select replica nodes.

        This function uses a cryptographic hash to generate a deterministic
        but uniformly distributed starting point. It then selects 'k' nodes
        based on this hash, ensuring any given key always maps to the same set
        of replicas. This simulates the uniform selection property of an OA.

        Args:
            key: The key to be mapped to a set of physical nodes.

        Returns:
            list: A list of node identifiers where the key should be stored.
        """
        hasher = hashlib.sha256(str(key).encode('utf-8'))
        hash_int = int(hasher.hexdigest(), 16)
        start_index = hash_int % self.num_nodes
        
        replicas = []
        for i in range(self.replica_factor):
            node_index = (start_index + i) % self.num_nodes
            replicas.append(self.cache_replicas[node_index])
            
        return sorted(replicas)

    def _rotate_left(self, y):
        """Performs a left rotation in the Treap."""
        if self.verbose:
            print(f"  - Rotating left on node with key: {y.key}")
        x = y.right
        T2 = x.left
        x.left = y
        y.right = T2
        return x

    def _rotate_right(self, x):
        """Performs a right rotation in the Treap."""
        if self.verbose:
            print(f"  - Rotating right on node with key: {x.key}")
        y = x.left
        T2 = y.right
        y.right = x
        x.left = T2
        return y

    def insert(self, key, data):
        """
        Public method to insert a key-value pair into the OACDT.
        """
        self.root = self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, node, key, data):
        """
        Recursively finds the correct position and inserts the new node,
        maintaining both BST and heap properties.
        """
        if node is None:
            return Node(key, data)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, data)
            if node.left and node.left.priority > node.priority:
                node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, data)
            if node.right and node.right.priority > node.priority:
                node = self._rotate_left(node)
        else:
            node.data = data
        return node

    def search(self, key):
        """
        Public method to search for a key in the OACDT.
        """
        node = self._search_recursive(self.root, key)
        if node:
            return node.data
        return None

    def _search_recursive(self, node, key):
        """Recursively searches for a key in the Treap (standard BST search)."""
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def delete(self, key):
        """
        Public method to delete a key from the OACDT.
        """
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        """
        Recursively finds the key and deletes it, maintaining Treap properties.
        """
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            if node.left.priority > node.right.priority:
                node = self._rotate_right(node)
                node.right = self._delete_recursive(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete_recursive(node.left, key)
        return node

    def inorder_traversal(self):
        """
        Returns a list of key-value pairs from an inorder traversal.
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.data))
            self._inorder_recursive(node.right, result)
