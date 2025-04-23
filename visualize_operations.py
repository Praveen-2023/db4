"""
Script to visualize B+ Tree operations.
"""
import os
from database.bplustree import BPlusTree
from database.tree_visualizer import TreeVisualizer
from database.bruteforce import BruteForceDB
from database.db_manager import Database
import pandas as pd
import matplotlib.pyplot as plt

def visualize_insertion_edge_cases():
    """Visualize insertion edge cases in a B+ Tree."""
    print("Visualizing insertion edge cases...")
    
    # Create a B+ Tree with a small order to make it easier to visualize
    tree = BPlusTree(order=3)
    visualizer = TreeVisualizer(output_dir='visualizations/insertion')
    
    # Insert keys to demonstrate node splitting
    keys = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    
    for key in keys:
        print(f"Inserting key {key}...")
        visualizer.visualize_insertion(tree, key, f"value_{key}")
    
    print("Insertion edge cases visualization complete.")
    print("Visualizations saved to 'visualizations/insertion' directory.")

def visualize_deletion_edge_cases():
    """Visualize deletion edge cases in a B+ Tree."""
    print("Visualizing deletion edge cases...")
    
    # Create a B+ Tree with a small order to make it easier to visualize
    tree = BPlusTree(order=3)
    visualizer = TreeVisualizer(output_dir='visualizations/deletion')
    
    # Insert keys to create a tree
    keys = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    
    for key in keys:
        tree.insert(key, f"value_{key}")
    
    # Visualize the tree before deletion
    visualizer.visualize_tree(tree, 'before_deletion')
    
    # Delete keys to demonstrate node merging and redistribution
    delete_keys = [15, 35, 25, 5, 50, 40, 30, 20, 10, 45]
    
    for key in delete_keys:
        print(f"Deleting key {key}...")
        visualizer.visualize_deletion(tree, key)
    
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
    
    # Create the visualizer
    visualizer = TreeVisualizer(output_dir='visualizations/full_table')
    
    # Visualize each table
    for table_name in db.list_tables():
        table = db.get_table(table_name)
        print(f"Visualizing table '{table_name}'...")
        visualizer.visualize_full_table(table, table_name)
    
    print("Full table visualization complete.")
    print("Visualizations saved to 'visualizations/full_table' directory.")

def benchmark_operations():
    """Benchmark B+ Tree operations against a brute force implementation."""
    print("Benchmarking operations...")
    
    # Create the visualizer
    visualizer = TreeVisualizer(output_dir='visualizations/benchmark')
    
    # Define data sizes
    sizes = [10, 15, 20, 100, 500, 1000]
    
    # Benchmark operations
    summary = visualizer.benchmark_operations(BPlusTree, BruteForceDB, sizes, num_runs=3)
    
    # Print the summary
    print("\nOperation Benchmark Summary:")
    print(summary)
    
    print("Operation benchmarking complete.")
    print("Results saved to 'visualizations/benchmark' directory.")

def benchmark_memory():
    """Benchmark memory usage of B+ Tree against a brute force implementation."""
    print("Benchmarking memory usage...")
    
    # Create the visualizer
    visualizer = TreeVisualizer(output_dir='visualizations/benchmark')
    
    # Define data sizes
    sizes = [10, 15, 20, 100, 500, 1000]
    
    # Benchmark memory usage
    summary = visualizer.benchmark_memory(BPlusTree, BruteForceDB, sizes, num_runs=3)
    
    # Print the summary
    print("\nMemory Usage Summary:")
    print(summary)
    
    print("Memory usage benchmarking complete.")
    print("Results saved to 'visualizations/benchmark' directory.")

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
