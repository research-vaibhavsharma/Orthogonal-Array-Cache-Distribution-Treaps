Orthogonal Array Cache Distribution Treap (OACDT)
This repository contains the Python implementation of the Orthogonal Array Cache Distribution Treap (OACDT), a novel hybrid data structure designed for scalable, fault-tolerant distributed caching. It synergizes the deterministic uniformity of Orthogonal Arrays with the probabilistic efficiency of Treaps.

This work is based on the research paper: "Orthogonal Array Cache Distribution Treaps: A Hybrid Random-Deterministic Approach for Scalable, Fault-Tolerant Distributed Caching" by Vaibhav Sharma, Kamal Pardasani, Mayank Namdev, and Amit Bhagat.

Table of Contents
Core Concepts

Key Features

How It Works

Installation

Usage & API

Running the Demonstration

Citation

License

Core Concepts
The OACDT is built upon two powerful mathematical constructs to address the challenges of large-scale distributed systems:

1. Orthogonal Arrays (for Distribution)
An Orthogonal Array (OA) is a combinatorial structure from statistical design theory. In the context of OACDT, it provides a method to map data keys to a set of physical cache nodes in a way that is both deterministic and uniformly distributed. This means:

The same key will always map to the same set of replica nodes.

Over a large number of keys, the load is spread evenly across all available nodes, preventing "hot spots".

Our implementation simulates this property by using a cryptographic hash function (SHA-256) to deterministically generate a uniformly distributed replica set for any given key.

2. Treaps (for Logical Organization)
A Treap is a randomized binary search tree that maintains its balance with high probability. It cleverly combines two properties in a single node:

Binary Search Tree (BST) Property: Keys are ordered, allowing for efficient O(log n) search operations.

Heap Property: Each node is assigned a random priority, and the tree maintains heap order with respect to these priorities.

This dual-property system ensures that the tree remains balanced on average, leading to efficient insertions, deletions, and lookups without the complex balancing logic of structures like Red-Black Trees.

Key Features
Provable Load Balancing: Guarantees an even distribution of data across physical nodes, leveraging the mathematical properties of Orthogonal Arrays.

Inherent Fault Tolerance: Each piece of data is replicated across a configurable number of nodes (replica_factor), ensuring data availability even if some nodes fail.

High Scalability: With an average time complexity of O(log n) for all core operations (insert, search, delete), the system scales efficiently as the number of keys grows.

Hybrid Random-Deterministic Architecture: Combines the strengths of a deterministic mapping scheme (for predictability and uniformity) with a probabilistic data structure (for simplicity and efficiency).

How It Works
The workflow of an OACDT operation is a two-step process:

Deterministic Mapping (OA): When a key-value pair is to be stored, the OACDT first uses its OA-inspired hashing function (_get_replicas_from_oa) to calculate the specific set of physical nodes where the data and its replicas will reside.

Logical Operation (Treap): The key-value pair is then inserted into the central Treap data structure. This operation maintains the logical organization of all keys in a balanced tree, independent of their physical location.

When a search is performed, the OACDT first determines the responsible replica set and then performs a fast O(log n) lookup in the Treap to retrieve the data.

Installation
The OACDT is implemented in a single Python file (oacdt.py) and requires no external libraries beyond Python's standard hashlib, random, and collections.

Simply save the oacdt.py file in your project directory and import the class:

from oacdt import OACDT

Usage & API
Initialization
Create an instance of the OACDT by specifying the total number of physical nodes and the desired replication factor.

# Initialize a system with 32 cache nodes and a replication factor of 5
oacdt = OACDT(num_nodes=32, replica_factor=5)

Core Methods
insert(key, data)
Inserts or updates a key-value pair.

oacdt.insert("user:101", {"name": "Alice", "tier": "premium"})
oacdt.insert(55, "product_data_for_id_55")

# Updating an existing key
oacdt.insert("user:101", {"name": "Alice", "tier": "gold"})

search(key)
Searches for a key and returns its associated data, or None if not found.

data = oacdt.search("user:101")
if data:
    print(f"Found data: {data}")
# Output: Found data: {'name': 'Alice', 'tier': 'gold'}

delete(key)
Removes a key-value pair from the system.

oacdt.delete("user:101")
print(f"Data after deletion: {oacdt.search('user:101')}")
# Output: Data after deletion: None

Running the Demonstration
The oacdt.py file includes a comprehensive if __name__ == '__main__': block that demonstrates all the core properties of the data structure. To run it, simply execute the script from your terminal:

python oacdt.py

The output will walk you through demonstrations of:

Deterministic Mapping: Showing a key always maps to the same replicas.

Uniform Distribution: Analyzing the load balance across all nodes.

Treap Operations: Showcasing insert, search, update, delete, and the BST sorted-order property.

Fault Tolerance: Explaining how replication helps survive node failures.

Scalability: Proving the system can handle a larger number of keys efficiently.

Citation
This implementation is based on the following research paper. If you use this code in your research, please consider citing the original work:

@article{sharma2025oacdt,
  title={Orthogonal Array Cache Distribution Treaps: A Hybrid Random-Deterministic Approach for Scalable, Fault-Tolerant Distributed Caching},
  author={Sharma, Vaibhav and Pardasani, Kamal and Namdev, Mayank and Bhagat, Amit},
  journal={IEEE Open Journal of the Computer Society (Pending Review)},
  year={2025}
}

License
This project is licensed under the MIT License. See the LICENSE file for details.
