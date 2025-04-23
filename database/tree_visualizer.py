"""
Visualization module for B+ Tree operations.
"""
import os
import graphviz
from typing import List, Dict, Any, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import tracemalloc
import pandas as pd
import time
import gc
import psutil

class TreeVisualizer:
    """
    A class for visualizing B+ Tree operations.
    """

    def __init__(self, output_dir: str = 'visualizations'):
        """
        Initialize the tree visualizer.

        Args:
            output_dir: The directory to save visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.step_counter = 0
        self.operation_counter = 0

    def visualize_tree(self, tree, filename: str = None, show_values: bool = True) -> graphviz.Digraph:
        """
        Visualize a B+ Tree.

        Args:
            tree: The B+ Tree to visualize
            filename: The filename to save the visualization
            show_values: Whether to show values in leaf nodes

        Returns:
            A graphviz.Digraph object
        """
        dot = graphviz.Digraph(comment='B+ Tree')

        # Add nodes
        self._add_nodes(dot, tree.root, 0, show_values)

        # Save the visualization
        if filename:
            dot.render(os.path.join(self.output_dir, filename), format='png', cleanup=True)

        return dot

    def _add_nodes(self, dot, node, node_id: int, show_values: bool) -> int:
        """
        Add nodes to the graphviz.Digraph object.

        Args:
            dot: The graphviz.Digraph object
            node: The node to add
            node_id: The ID of the node
            show_values: Whether to show values in leaf nodes

        Returns:
            The next available node ID
        """
        if node is None:
            return node_id

        # Create node label
        if node.is_leaf:
            if show_values:
                # Show keys and values
                label = "Leaf | "
                for i, (key, value) in enumerate(zip(node.keys, node.children)):
                    if i > 0:
                        label += " | "
                    label += f"{key}: {value}"
            else:
                # Show only keys
                label = "Leaf | " + " | ".join(map(str, node.keys))
        else:
            # Internal node, show only keys
            label = "Node | " + " | ".join(map(str, node.keys))

        # Add node to graph
        dot.node(str(node_id), label)

        # Add edges to children
        next_id = node_id + 1
        if not node.is_leaf:
            for i, child in enumerate(node.children):
                child_id = next_id
                next_id = self._add_nodes(dot, child, next_id, show_values)
                dot.edge(str(node_id), str(child_id), label=f"{i}")

        # Add edge to next leaf node
        if node.is_leaf and hasattr(node, 'next') and node.next:
            # Find the ID of the next leaf node
            next_leaf_id = self._find_node_id(dot, node.next)
            if next_leaf_id is not None:
                dot.edge(str(node_id), str(next_leaf_id), style='dashed', color='blue')

        return next_id

    def _find_node_id(self, dot, node) -> Optional[int]:
        """
        Find the ID of a node in the graphviz.Digraph object.

        Args:
            dot: The graphviz.Digraph object
            node: The node to find

        Returns:
            The ID of the node, or None if not found
        """
        # This is a placeholder. In a real implementation, we would need to
        # keep track of node IDs during the _add_nodes process.
        return None

    def visualize_insertion(self, tree, key, value, filename_prefix: str = 'insert'):
        """
        Visualize the insertion of a key-value pair into a B+ Tree.

        Args:
            tree: The B+ Tree
            key: The key to insert
            value: The value to insert
            filename_prefix: The prefix for the filename
        """
        self.operation_counter += 1
        self.step_counter = 0

        # Visualize the tree before insertion
        self._visualize_step(tree, f"{filename_prefix}_{self.operation_counter}_before")

        # Create a copy of the tree for step-by-step visualization
        tree_copy = tree.copy()

        # Set up the visualization callback
        def visualization_callback(node, action, details=None):
            self.step_counter += 1
            self._visualize_step(tree_copy, f"{filename_prefix}_{self.operation_counter}_step_{self.step_counter}",
                                highlight_node=node, highlight_action=action, highlight_details=details)

        # Insert the key-value pair with visualization
        tree_copy.insert(key, value, visualization_callback)

        # Visualize the tree after insertion
        self._visualize_step(tree_copy, f"{filename_prefix}_{self.operation_counter}_after")

    def visualize_deletion(self, tree, key, filename_prefix: str = 'delete'):
        """
        Visualize the deletion of a key from a B+ Tree.

        Args:
            tree: The B+ Tree
            key: The key to delete
            filename_prefix: The prefix for the filename
        """
        self.operation_counter += 1
        self.step_counter = 0

        # Visualize the tree before deletion
        self._visualize_step(tree, f"{filename_prefix}_{self.operation_counter}_before")

        # Create a copy of the tree for step-by-step visualization
        tree_copy = tree.copy()

        # Set up the visualization callback
        def visualization_callback(node, action, details=None):
            self.step_counter += 1
            self._visualize_step(tree_copy, f"{filename_prefix}_{self.operation_counter}_step_{self.step_counter}",
                                highlight_node=node, highlight_action=action, highlight_details=details)

        # Delete the key with visualization
        tree_copy.delete(key, visualization_callback)

        # Visualize the tree after deletion
        self._visualize_step(tree_copy, f"{filename_prefix}_{self.operation_counter}_after")

    def _visualize_step(self, tree, filename: str, highlight_node=None, highlight_action=None, highlight_details=None):
        """
        Visualize a step in a B+ Tree operation.

        Args:
            tree: The B+ Tree
            filename: The filename to save the visualization
            highlight_node: The node to highlight
            highlight_action: The action being performed
            highlight_details: Additional details about the action
        """
        dot = graphviz.Digraph(comment='B+ Tree')

        # Add nodes
        self._add_nodes_with_highlight(dot, tree.root, 0, highlight_node, highlight_action, highlight_details)

        # Save the visualization
        dot.render(os.path.join(self.output_dir, filename), format='png', cleanup=True)

    def _add_nodes_with_highlight(self, dot, node, node_id: int, highlight_node, highlight_action, highlight_details) -> int:
        """
        Add nodes to the graphviz.Digraph object with highlighting.

        Args:
            dot: The graphviz.Digraph object
            node: The node to add
            node_id: The ID of the node
            highlight_node: The node to highlight
            highlight_action: The action being performed
            highlight_details: Additional details about the action

        Returns:
            The next available node ID
        """
        if node is None:
            return node_id

        # Create node label
        if node.is_leaf:
            # Show keys and values
            label = "Leaf | "
            for i, (key, value) in enumerate(zip(node.keys, node.children)):
                if i > 0:
                    label += " | "
                label += f"{key}: {value}"
        else:
            # Internal node, show only keys
            label = "Node | " + " | ".join(map(str, node.keys))

        # Add node to graph with highlighting
        if node == highlight_node:
            if highlight_action == 'split':
                dot.node(str(node_id), label, style='filled', fillcolor='lightblue',
                        xlabel=f"Splitting node: {highlight_details}")
            elif highlight_action == 'merge':
                dot.node(str(node_id), label, style='filled', fillcolor='lightgreen',
                        xlabel=f"Merging node: {highlight_details}")
            elif highlight_action == 'redistribute':
                dot.node(str(node_id), label, style='filled', fillcolor='lightyellow',
                        xlabel=f"Redistributing keys: {highlight_details}")
            elif highlight_action == 'insert':
                dot.node(str(node_id), label, style='filled', fillcolor='lightpink',
                        xlabel=f"Inserting key: {highlight_details}")
            elif highlight_action == 'delete':
                dot.node(str(node_id), label, style='filled', fillcolor='lightcoral',
                        xlabel=f"Deleting key: {highlight_details}")
            else:
                dot.node(str(node_id), label, style='filled', fillcolor='lightgray')
        else:
            dot.node(str(node_id), label)

        # Add edges to children
        next_id = node_id + 1
        if not node.is_leaf:
            for i, child in enumerate(node.children):
                child_id = next_id
                next_id = self._add_nodes_with_highlight(dot, child, next_id, highlight_node, highlight_action, highlight_details)
                dot.edge(str(node_id), str(child_id), label=f"{i}")

        # Add edge to next leaf node
        if node.is_leaf and hasattr(node, 'next') and node.next:
            # Find the ID of the next leaf node
            next_leaf_id = self._find_node_id(dot, node.next)
            if next_leaf_id is not None:
                dot.edge(str(node_id), str(next_leaf_id), style='dashed', color='blue')

        return next_id

    def visualize_full_table(self, table, filename: str = 'full_table'):
        """
        Visualize a full table in a B+ Tree.

        Args:
            table: The table to visualize
            filename: The filename to save the visualization
        """
        # Visualize the B+ Tree index
        dot = self.visualize_tree(table.index, filename, show_values=True)

        # Create a text representation of the table
        text = f"Table: {table.name}\n"
        text += f"Primary Key: {table.primary_key}\n"
        text += f"Schema: {table.schema}\n"
        text += f"Number of rows: {len(table.select_all())}\n\n"

        # Add the first 10 rows
        rows = table.select_all()[:10]
        for row in rows:
            text += f"{row}\n"

        # Save the text representation
        with open(os.path.join(self.output_dir, f"{filename}.txt"), 'w') as f:
            f.write(text)

    def benchmark_operations(self, tree_class, brute_force_class, sizes: List[int], num_runs: int = 3) -> pd.DataFrame:
        """
        Benchmark B+ Tree operations against a brute force implementation.

        Args:
            tree_class: The B+ Tree class
            brute_force_class: The brute force class
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over

        Returns:
            A pandas DataFrame with the benchmark results
        """
        results = []

        for size in sizes:
            for run in range(num_runs):
                # Generate random data
                data = [(i, f"value_{i}") for i in range(size)]

                # Benchmark B+ Tree insertion (sorted)
                tree = tree_class()
                start_time = time.time()
                for key, value in data:
                    tree.insert(key, value)
                end_time = time.time()
                tree_insert_time_sorted = end_time - start_time

                # Benchmark B+ Tree insertion (unsorted)
                tree = tree_class()
                import random
                random_data = data.copy()
                random.shuffle(random_data)
                start_time = time.time()
                for key, value in random_data:
                    tree.insert(key, value)
                end_time = time.time()
                tree_insert_time_unsorted = end_time - start_time

                # Benchmark B+ Tree search
                search_keys = [i for i in range(0, size, max(1, size // 100))]
                start_time = time.time()
                for key in search_keys:
                    tree.search(key)
                end_time = time.time()
                tree_search_time = end_time - start_time

                # Benchmark B+ Tree range query
                range_queries = [(i, i + size // 10) for i in range(0, size, max(1, size // 10))]
                start_time = time.time()
                for start, end in range_queries:
                    tree.range_query(start, end)
                end_time = time.time()
                tree_range_time = end_time - start_time

                # Benchmark B+ Tree deletion
                delete_keys = [i for i in range(0, size, max(1, size // 10))]
                start_time = time.time()
                for key in delete_keys:
                    tree.delete(key)
                end_time = time.time()
                tree_delete_time = end_time - start_time

                # Benchmark B+ Tree mixed workload
                tree = tree_class()
                for key, value in data:
                    tree.insert(key, value)

                operations = []
                for i in range(size):
                    op_type = random.choice(['insert', 'search', 'delete', 'range'])
                    if op_type == 'insert':
                        key = random.randint(size, size * 2)
                        value = f"value_{key}"
                        operations.append(('insert', key, value))
                    elif op_type == 'search':
                        key = random.randint(0, size - 1)
                        operations.append(('search', key))
                    elif op_type == 'delete':
                        key = random.randint(0, size - 1)
                        operations.append(('delete', key))
                    else:  # range
                        start = random.randint(0, size - 1)
                        end = random.randint(start, size - 1)
                        operations.append(('range', start, end))

                start_time = time.time()
                for op in operations:
                    if op[0] == 'insert':
                        tree.insert(op[1], op[2])
                    elif op[0] == 'search':
                        tree.search(op[1])
                    elif op[0] == 'delete':
                        tree.delete(op[1])
                    else:  # range
                        tree.range_query(op[1], op[2])
                end_time = time.time()
                tree_mixed_time = end_time - start_time

                # Benchmark brute force insertion
                brute_force = brute_force_class()
                start_time = time.time()
                for key, value in data:
                    brute_force.insert(key, value)
                end_time = time.time()
                bf_insert_time = end_time - start_time

                # Benchmark brute force search
                start_time = time.time()
                for key in search_keys:
                    brute_force.search(key)
                end_time = time.time()
                bf_search_time = end_time - start_time

                # Benchmark brute force range query
                start_time = time.time()
                for start, end in range_queries:
                    brute_force.range_query(start, end)
                end_time = time.time()
                bf_range_time = end_time - start_time

                # Benchmark brute force deletion
                start_time = time.time()
                for key in delete_keys:
                    brute_force.delete(key)
                end_time = time.time()
                bf_delete_time = end_time - start_time

                # Benchmark brute force mixed workload
                brute_force = brute_force_class()
                for key, value in data:
                    brute_force.insert(key, value)

                start_time = time.time()
                for op in operations:
                    if op[0] == 'insert':
                        brute_force.insert(op[1], op[2])
                    elif op[0] == 'search':
                        brute_force.search(op[1])
                    elif op[0] == 'delete':
                        brute_force.delete(op[1])
                    else:  # range
                        brute_force.range_query(op[1], op[2])
                end_time = time.time()
                bf_mixed_time = end_time - start_time

                # Add results to the list
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree (Sorted)',
                    'Operation': 'Insert',
                    'Time (s)': tree_insert_time_sorted
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree (Unsorted)',
                    'Operation': 'Insert',
                    'Time (s)': tree_insert_time_unsorted
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree',
                    'Operation': 'Search',
                    'Time (s)': tree_search_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree',
                    'Operation': 'Range Query',
                    'Time (s)': tree_range_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree',
                    'Operation': 'Delete',
                    'Time (s)': tree_delete_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree',
                    'Operation': 'Mixed',
                    'Time (s)': tree_mixed_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'Brute Force',
                    'Operation': 'Insert',
                    'Time (s)': bf_insert_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'Brute Force',
                    'Operation': 'Search',
                    'Time (s)': bf_search_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'Brute Force',
                    'Operation': 'Range Query',
                    'Time (s)': bf_range_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'Brute Force',
                    'Operation': 'Delete',
                    'Time (s)': bf_delete_time
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'Brute Force',
                    'Operation': 'Mixed',
                    'Time (s)': bf_mixed_time
                })

        # Create a DataFrame
        df = pd.DataFrame(results)

        # Save the results
        df.to_csv(os.path.join(self.output_dir, 'benchmark_results.csv'), index=False)

        # Create a summary DataFrame
        summary = df.groupby(['Size', 'Structure', 'Operation'])['Time (s)'].mean().reset_index()
        summary.to_csv(os.path.join(self.output_dir, 'benchmark_summary.csv'), index=False)

        # Plot the results
        self._plot_benchmark_results(summary)

        return summary

    def _plot_benchmark_results(self, df: pd.DataFrame):
        """
        Plot benchmark results.

        Args:
            df: A pandas DataFrame with benchmark results
        """
        # Plot insertion time
        self._plot_operation(df, 'Insert', 'insertion_time.png')

        # Plot search time
        self._plot_operation(df, 'Search', 'search_time.png')

        # Plot range query time
        self._plot_operation(df, 'Range Query', 'range_query_time.png')

        # Plot deletion time
        self._plot_operation(df, 'Delete', 'deletion_time.png')

        # Plot mixed workload time
        self._plot_operation(df, 'Mixed', 'mixed_time.png')

    def _plot_operation(self, df: pd.DataFrame, operation: str, filename: str):
        """
        Plot benchmark results for a specific operation.

        Args:
            df: A pandas DataFrame with benchmark results
            operation: The operation to plot
            filename: The filename to save the plot
        """
        plt.figure(figsize=(10, 6))

        # Filter the DataFrame for the operation
        op_df = df[df['Operation'] == operation]

        # Plot the results
        for structure in op_df['Structure'].unique():
            struct_df = op_df[op_df['Structure'] == structure]
            plt.plot(struct_df['Size'], struct_df['Time (s)'], marker='o', label=structure)

        plt.title(f"{operation} Time vs. Data Size")
        plt.xlabel("Data Size")
        plt.ylabel("Time (seconds)")
        plt.grid(True)
        plt.legend()

        # Save the plot
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()

    def benchmark_memory(self, tree_class, brute_force_class, sizes: List[int], num_runs: int = 3) -> pd.DataFrame:
        """
        Benchmark memory usage of B+ Tree against a brute force implementation.

        Args:
            tree_class: The B+ Tree class
            brute_force_class: The brute force class
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over

        Returns:
            A pandas DataFrame with the benchmark results
        """
        results = []

        for size in sizes:
            for run in range(num_runs):
                # Generate random data
                data = [(i, f"value_{i}") for i in range(size)]

                # Benchmark B+ Tree memory usage (sorted)
                tracemalloc.start()
                tree = tree_class()
                for key, value in data:
                    tree.insert(key, value)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tree_memory_sorted = peak / (1024 * 1024)  # Convert to MB

                # Benchmark B+ Tree memory usage (unsorted)
                tracemalloc.start()
                tree = tree_class()
                import random
                random_data = data.copy()
                random.shuffle(random_data)
                for key, value in random_data:
                    tree.insert(key, value)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tree_memory_unsorted = peak / (1024 * 1024)  # Convert to MB

                # Benchmark brute force memory usage
                tracemalloc.start()
                brute_force = brute_force_class()
                for key, value in data:
                    brute_force.insert(key, value)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                bf_memory = peak / (1024 * 1024)  # Convert to MB

                # Add results to the list
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree (Sorted)',
                    'Memory (MB)': tree_memory_sorted
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'B+ Tree (Unsorted)',
                    'Memory (MB)': tree_memory_unsorted
                })
                results.append({
                    'Size': size,
                    'Run': run + 1,
                    'Structure': 'Brute Force',
                    'Memory (MB)': bf_memory
                })

        # Create a DataFrame
        df = pd.DataFrame(results)

        # Save the results
        df.to_csv(os.path.join(self.output_dir, 'memory_results.csv'), index=False)

        # Create a summary DataFrame
        summary = df.groupby(['Size', 'Structure'])['Memory (MB)'].mean().reset_index()
        summary.to_csv(os.path.join(self.output_dir, 'memory_summary.csv'), index=False)

        # Plot the results
        self._plot_memory_results(summary)

        return summary

    def _plot_memory_results(self, df: pd.DataFrame):
        """
        Plot memory usage results.

        Args:
            df: A pandas DataFrame with memory usage results
        """
        plt.figure(figsize=(10, 6))

        # Plot the results
        for structure in df['Structure'].unique():
            struct_df = df[df['Structure'] == structure]
            plt.plot(struct_df['Size'], struct_df['Memory (MB)'], marker='o', label=structure)

        plt.title("Memory Usage vs. Data Size")
        plt.xlabel("Data Size")
        plt.ylabel("Memory (MB)")
        plt.grid(True)
        plt.legend()

        # Save the plot
        plt.savefig(os.path.join(self.output_dir, 'memory_usage.png'))
        plt.close()
