"""
Script to visualize B+ Tree operations using text-based visualization.
"""
import os
from database.bplustree import BPlusTree
from database.bruteforce import BruteForceDB
from database.db_manager import Database
import pandas as pd
import matplotlib.pyplot as plt
import time
import tracemalloc
import random

def visualize_tree_text(tree, indent=0):
    """
    Generate a text representation of a B+ Tree.
    
    Args:
        tree: The B+ Tree to visualize
        indent: The indentation level
        
    Returns:
        A string representation of the tree
    """
    if not tree.root.keys:
        return "Empty Tree"
    
    return _visualize_node_text(tree.root, indent)

def _visualize_node_text(node, indent=0):
    """
    Generate a text representation of a B+ Tree node.
    
    Args:
        node: The node to visualize
        indent: The indentation level
        
    Returns:
        A string representation of the node
    """
    result = ""
    
    # Add indentation
    prefix = "  " * indent
    
    # Add node type
    if node.is_leaf:
        result += f"{prefix}Leaf: "
    else:
        result += f"{prefix}Node: "
    
    # Add keys
    result += f"{node.keys}\n"
    
    # Add children
    if not node.is_leaf:
        for i, child in enumerate(node.children):
            result += _visualize_node_text(child, indent + 1)
    else:
        # For leaf nodes, show values
        result += f"{prefix}  Values: {node.children}\n"
    
    return result

def visualize_insertion_edge_cases():
    """Visualize insertion edge cases in a B+ Tree."""
    print("Visualizing insertion edge cases...")
    
    # Create a B+ Tree with a small order to make it easier to visualize
    tree = BPlusTree(order=3)
    
    # Create the output directory
    os.makedirs('visualizations/insertion', exist_ok=True)
    
    # Insert keys to demonstrate node splitting
    keys = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    
    # Visualize the tree before insertion
    with open('visualizations/insertion/before_insertion.txt', 'w') as f:
        f.write(visualize_tree_text(tree))
    
    for key in keys:
        print(f"Inserting key {key}...")
        
        # Visualize the tree before insertion
        with open(f'visualizations/insertion/before_insert_{key}.txt', 'w') as f:
            f.write(visualize_tree_text(tree))
        
        # Insert the key
        tree.insert(key, f"value_{key}")
        
        # Visualize the tree after insertion
        with open(f'visualizations/insertion/after_insert_{key}.txt', 'w') as f:
            f.write(visualize_tree_text(tree))
    
    print("Insertion edge cases visualization complete.")
    print("Visualizations saved to 'visualizations/insertion' directory.")

def visualize_deletion_edge_cases():
    """Visualize deletion edge cases in a B+ Tree."""
    print("Visualizing deletion edge cases...")
    
    # Create a B+ Tree with a small order to make it easier to visualize
    tree = BPlusTree(order=3)
    
    # Create the output directory
    os.makedirs('visualizations/deletion', exist_ok=True)
    
    # Insert keys to create a tree
    keys = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    
    for key in keys:
        tree.insert(key, f"value_{key}")
    
    # Visualize the tree before deletion
    with open('visualizations/deletion/before_deletion.txt', 'w') as f:
        f.write(visualize_tree_text(tree))
    
    # Delete keys to demonstrate node merging and redistribution
    delete_keys = [15, 35, 25, 5, 50, 40, 30, 20, 10, 45]
    
    for key in delete_keys:
        print(f"Deleting key {key}...")
        
        # Visualize the tree before deletion
        with open(f'visualizations/deletion/before_delete_{key}.txt', 'w') as f:
            f.write(visualize_tree_text(tree))
        
        # Delete the key
        tree.delete(key)
        
        # Visualize the tree after deletion
        with open(f'visualizations/deletion/after_delete_{key}.txt', 'w') as f:
            f.write(visualize_tree_text(tree))
    
    print("Deletion edge cases visualization complete.")
    print("Visualizations saved to 'visualizations/deletion' directory.")

def visualize_full_table():
    """Visualize a full table in a B+ Tree."""
    print("Visualizing full table...")
    
    # Load the database
    db = Database.load('retail_db')
    
    if db is None:
        print("Database not found. Please run create_tables.py first.")
        return
    
    # Create the output directory
    os.makedirs('visualizations/full_table', exist_ok=True)
    
    # Visualize each table
    for table_name in db.list_tables():
        table = db.get_table(table_name)
        print(f"Visualizing table '{table_name}'...")
        
        # Visualize the B+ Tree index
        with open(f'visualizations/full_table/{table_name}_index.txt', 'w') as f:
            f.write(visualize_tree_text(table.index))
        
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
        with open(f'visualizations/full_table/{table_name}.txt', 'w') as f:
            f.write(text)
    
    print("Full table visualization complete.")
    print("Visualizations saved to 'visualizations/full_table' directory.")

def benchmark_operations():
    """Benchmark B+ Tree operations against a brute force implementation."""
    print("Benchmarking operations...")
    
    # Create the output directory
    os.makedirs('visualizations/benchmark', exist_ok=True)
    
    # Define data sizes
    sizes = [10, 15, 20, 100, 500, 1000]
    num_runs = 3
    
    results = []
    
    for size in sizes:
        for run in range(num_runs):
            print(f"Benchmarking size {size}, run {run+1}...")
            
            # Generate random data
            data = [(i, f"value_{i}") for i in range(size)]
            
            # Benchmark B+ Tree insertion (sorted)
            tree = BPlusTree()
            start_time = time.time()
            for key, value in data:
                tree.insert(key, value)
            end_time = time.time()
            tree_insert_time_sorted = end_time - start_time
            
            # Benchmark B+ Tree insertion (unsorted)
            tree = BPlusTree()
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
            tree = BPlusTree()
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
            brute_force = BruteForceDB()
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
            brute_force = BruteForceDB()
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
    df.to_csv('visualizations/benchmark/benchmark_results.csv', index=False)
    
    # Create a summary DataFrame
    summary = df.groupby(['Size', 'Structure', 'Operation'])['Time (s)'].mean().reset_index()
    summary.to_csv('visualizations/benchmark/benchmark_summary.csv', index=False)
    
    # Plot the results
    _plot_benchmark_results(summary)
    
    print("Operation benchmarking complete.")
    print("Results saved to 'visualizations/benchmark' directory.")
    
    return summary

def _plot_benchmark_results(df):
    """
    Plot benchmark results.
    
    Args:
        df: A pandas DataFrame with benchmark results
    """
    # Plot insertion time
    _plot_operation(df, 'Insert', 'insertion_time.png')
    
    # Plot search time
    _plot_operation(df, 'Search', 'search_time.png')
    
    # Plot range query time
    _plot_operation(df, 'Range Query', 'range_query_time.png')
    
    # Plot deletion time
    _plot_operation(df, 'Delete', 'deletion_time.png')
    
    # Plot mixed workload time
    _plot_operation(df, 'Mixed', 'mixed_time.png')

def _plot_operation(df, operation, filename):
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
    plt.savefig(f'visualizations/benchmark/{filename}')
    plt.close()

def benchmark_memory():
    """Benchmark memory usage of B+ Tree against a brute force implementation."""
    print("Benchmarking memory usage...")
    
    # Create the output directory
    os.makedirs('visualizations/benchmark', exist_ok=True)
    
    # Define data sizes
    sizes = [10, 15, 20, 100, 500, 1000]
    num_runs = 3
    
    results = []
    
    for size in sizes:
        for run in range(num_runs):
            print(f"Benchmarking memory usage for size {size}, run {run+1}...")
            
            # Generate random data
            data = [(i, f"value_{i}") for i in range(size)]
            
            # Benchmark B+ Tree memory usage (sorted)
            tracemalloc.start()
            tree = BPlusTree()
            for key, value in data:
                tree.insert(key, value)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            tree_memory_sorted = peak / (1024 * 1024)  # Convert to MB
            
            # Benchmark B+ Tree memory usage (unsorted)
            tracemalloc.start()
            tree = BPlusTree()
            random_data = data.copy()
            random.shuffle(random_data)
            for key, value in random_data:
                tree.insert(key, value)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            tree_memory_unsorted = peak / (1024 * 1024)  # Convert to MB
            
            # Benchmark brute force memory usage
            tracemalloc.start()
            brute_force = BruteForceDB()
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
    df.to_csv('visualizations/benchmark/memory_results.csv', index=False)
    
    # Create a summary DataFrame
    summary = df.groupby(['Size', 'Structure'])['Memory (MB)'].mean().reset_index()
    summary.to_csv('visualizations/benchmark/memory_summary.csv', index=False)
    
    # Plot the results
    _plot_memory_results(summary)
    
    print("Memory usage benchmarking complete.")
    print("Results saved to 'visualizations/benchmark' directory.")
    
    return summary

def _plot_memory_results(df):
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
    plt.savefig('visualizations/benchmark/memory_usage.png')
    plt.close()

def main():
    """Run all visualizations and benchmarks."""
    # Create the output directories
    os.makedirs('visualizations/insertion', exist_ok=True)
    os.makedirs('visualizations/deletion', exist_ok=True)
    os.makedirs('visualizations/full_table', exist_ok=True)
    os.makedirs('visualizations/benchmark', exist_ok=True)
    
    # Visualize insertion edge cases
    visualize_insertion_edge_cases()
    
    # Visualize deletion edge cases
    visualize_deletion_edge_cases()
    
    # Visualize full table
    visualize_full_table()
    
    # Benchmark operations
    benchmark_operations()
    
    # Benchmark memory usage
    benchmark_memory()

if __name__ == '__main__':
    main()
