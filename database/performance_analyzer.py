"""
Performance analyzer for comparing B+ Tree with BruteForceDB.
"""
import time
import random
import gc
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict, Any, Callable
import psutil
import os

from .bplustree import BPlusTree
from .bruteforce import BruteForceDB


class PerformanceAnalyzer:
    """
    A class for analyzing the performance of B+ Tree and BruteForceDB.
    """
    
    def __init__(self):
        """Initialize the performance analyzer."""
        self.results = {}
    
    def measure_memory_usage(self, func: Callable) -> float:
        """
        Measure the memory usage of a function.
        
        Args:
            func: The function to measure
            
        Returns:
            The memory usage in MB
        """
        # Force garbage collection
        gc.collect()
        
        # Get the current process
        process = psutil.Process(os.getpid())
        
        # Measure memory before
        memory_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        
        # Run the function
        func()
        
        # Measure memory after
        memory_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        
        # Return the difference
        return memory_after - memory_before
    
    def measure_time(self, func: Callable) -> float:
        """
        Measure the execution time of a function.
        
        Args:
            func: The function to measure
            
        Returns:
            The execution time in seconds
        """
        # Force garbage collection
        gc.collect()
        
        # Measure time
        start_time = time.time()
        func()
        end_time = time.time()
        
        # Return the difference
        return end_time - start_time
    
    def benchmark_insertion(self, sizes: List[int], num_runs: int = 3) -> Dict[str, Dict[int, float]]:
        """
        Benchmark insertion performance for different data sizes.
        
        Args:
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over
            
        Returns:
            A dictionary mapping structure names to dictionaries mapping data sizes to average times
        """
        results = {
            'bplustree': {'time': {}, 'memory': {}},
            'bruteforce': {'time': {}, 'memory': {}}
        }
        
        for size in sizes:
            bplustree_time = 0
            bplustree_memory = 0
            bruteforce_time = 0
            bruteforce_memory = 0
            
            for _ in range(num_runs):
                # Generate random data
                data = [(random.randint(1, size * 10), f"value_{i}") for i in range(size)]
                
                # Benchmark B+ Tree
                bplus_tree = BPlusTree()
                bplustree_time += self.measure_time(
                    lambda: [bplus_tree.insert(key, value) for key, value in data]
                )
                
                # Reset and benchmark memory
                bplus_tree = BPlusTree()
                bplustree_memory += self.measure_memory_usage(
                    lambda: [bplus_tree.insert(key, value) for key, value in data]
                )
                
                # Benchmark BruteForceDB
                bruteforce_db = BruteForceDB()
                bruteforce_time += self.measure_time(
                    lambda: [bruteforce_db.insert(key, value) for key, value in data]
                )
                
                # Reset and benchmark memory
                bruteforce_db = BruteForceDB()
                bruteforce_memory += self.measure_memory_usage(
                    lambda: [bruteforce_db.insert(key, value) for key, value in data]
                )
            
            # Average the results
            results['bplustree']['time'][size] = bplustree_time / num_runs
            results['bplustree']['memory'][size] = bplustree_memory / num_runs
            results['bruteforce']['time'][size] = bruteforce_time / num_runs
            results['bruteforce']['memory'][size] = bruteforce_memory / num_runs
        
        self.results['insertion'] = results
        return results
    
    def benchmark_search(self, sizes: List[int], num_runs: int = 3) -> Dict[str, Dict[int, float]]:
        """
        Benchmark search performance for different data sizes.
        
        Args:
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over
            
        Returns:
            A dictionary mapping structure names to dictionaries mapping data sizes to average times
        """
        results = {
            'bplustree': {'time': {}},
            'bruteforce': {'time': {}}
        }
        
        for size in sizes:
            bplustree_time = 0
            bruteforce_time = 0
            
            for _ in range(num_runs):
                # Generate random data
                data = [(random.randint(1, size * 10), f"value_{i}") for i in range(size)]
                
                # Create and populate the structures
                bplus_tree = BPlusTree()
                bruteforce_db = BruteForceDB()
                
                for key, value in data:
                    bplus_tree.insert(key, value)
                    bruteforce_db.insert(key, value)
                
                # Generate random search keys
                search_keys = [random.randint(1, size * 10) for _ in range(size // 10)]
                
                # Benchmark B+ Tree
                bplustree_time += self.measure_time(
                    lambda: [bplus_tree.search(key) for key in search_keys]
                )
                
                # Benchmark BruteForceDB
                bruteforce_time += self.measure_time(
                    lambda: [bruteforce_db.search(key) for key in search_keys]
                )
            
            # Average the results
            results['bplustree']['time'][size] = bplustree_time / num_runs
            results['bruteforce']['time'][size] = bruteforce_time / num_runs
        
        self.results['search'] = results
        return results
    
    def benchmark_range_query(self, sizes: List[int], num_runs: int = 3) -> Dict[str, Dict[int, float]]:
        """
        Benchmark range query performance for different data sizes.
        
        Args:
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over
            
        Returns:
            A dictionary mapping structure names to dictionaries mapping data sizes to average times
        """
        results = {
            'bplustree': {'time': {}},
            'bruteforce': {'time': {}}
        }
        
        for size in sizes:
            bplustree_time = 0
            bruteforce_time = 0
            
            for _ in range(num_runs):
                # Generate random data
                data = [(random.randint(1, size * 10), f"value_{i}") for i in range(size)]
                
                # Create and populate the structures
                bplus_tree = BPlusTree()
                bruteforce_db = BruteForceDB()
                
                for key, value in data:
                    bplus_tree.insert(key, value)
                    bruteforce_db.insert(key, value)
                
                # Generate random range queries
                range_queries = []
                for _ in range(size // 10):
                    start = random.randint(1, size * 10)
                    end = random.randint(start, size * 10)
                    range_queries.append((start, end))
                
                # Benchmark B+ Tree
                bplustree_time += self.measure_time(
                    lambda: [bplus_tree.range_query(start, end) for start, end in range_queries]
                )
                
                # Benchmark BruteForceDB
                bruteforce_time += self.measure_time(
                    lambda: [bruteforce_db.range_query(start, end) for start, end in range_queries]
                )
            
            # Average the results
            results['bplustree']['time'][size] = bplustree_time / num_runs
            results['bruteforce']['time'][size] = bruteforce_time / num_runs
        
        self.results['range_query'] = results
        return results
    
    def benchmark_deletion(self, sizes: List[int], num_runs: int = 3) -> Dict[str, Dict[int, float]]:
        """
        Benchmark deletion performance for different data sizes.
        
        Args:
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over
            
        Returns:
            A dictionary mapping structure names to dictionaries mapping data sizes to average times
        """
        results = {
            'bplustree': {'time': {}},
            'bruteforce': {'time': {}}
        }
        
        for size in sizes:
            bplustree_time = 0
            bruteforce_time = 0
            
            for _ in range(num_runs):
                # Generate random data
                data = [(random.randint(1, size * 10), f"value_{i}") for i in range(size)]
                
                # Create and populate the structures
                bplus_tree = BPlusTree()
                bruteforce_db = BruteForceDB()
                
                for key, value in data:
                    bplus_tree.insert(key, value)
                    bruteforce_db.insert(key, value)
                
                # Generate random deletion keys
                delete_keys = [key for key, _ in random.sample(data, size // 10)]
                
                # Benchmark B+ Tree
                bplustree_time += self.measure_time(
                    lambda: [bplus_tree.delete(key) for key in delete_keys]
                )
                
                # Benchmark BruteForceDB
                bruteforce_time += self.measure_time(
                    lambda: [bruteforce_db.delete(key) for key in delete_keys]
                )
            
            # Average the results
            results['bplustree']['time'][size] = bplustree_time / num_runs
            results['bruteforce']['time'][size] = bruteforce_time / num_runs
        
        self.results['deletion'] = results
        return results
    
    def benchmark_random_operations(self, sizes: List[int], num_runs: int = 3) -> Dict[str, Dict[int, float]]:
        """
        Benchmark random operations (insert, search, delete) for different data sizes.
        
        Args:
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over
            
        Returns:
            A dictionary mapping structure names to dictionaries mapping data sizes to average times
        """
        results = {
            'bplustree': {'time': {}},
            'bruteforce': {'time': {}}
        }
        
        for size in sizes:
            bplustree_time = 0
            bruteforce_time = 0
            
            for _ in range(num_runs):
                # Generate random data
                data = [(random.randint(1, size * 10), f"value_{i}") for i in range(size)]
                
                # Create the structures
                bplus_tree = BPlusTree()
                bruteforce_db = BruteForceDB()
                
                # Generate random operations
                operations = []
                for _ in range(size):
                    op_type = random.choice(['insert', 'search', 'delete'])
                    if op_type == 'insert':
                        key = random.randint(1, size * 10)
                        value = f"value_{key}"
                        operations.append(('insert', key, value))
                    else:
                        key = random.choice([k for k, _ in data])
                        operations.append((op_type, key))
                
                # Benchmark B+ Tree
                bplustree_time += self.measure_time(
                    lambda: [
                        bplus_tree.insert(key, value) if op == 'insert' else
                        bplus_tree.search(key) if op == 'search' else
                        bplus_tree.delete(key)
                        for op, key, *args in operations
                    ]
                )
                
                # Benchmark BruteForceDB
                bruteforce_time += self.measure_time(
                    lambda: [
                        bruteforce_db.insert(key, value) if op == 'insert' else
                        bruteforce_db.search(key) if op == 'search' else
                        bruteforce_db.delete(key)
                        for op, key, *args in operations
                    ]
                )
            
            # Average the results
            results['bplustree']['time'][size] = bplustree_time / num_runs
            results['bruteforce']['time'][size] = bruteforce_time / num_runs
        
        self.results['random_operations'] = results
        return results
    
    def run_all_benchmarks(self, sizes: List[int], num_runs: int = 3) -> Dict[str, Dict[str, Dict[int, float]]]:
        """
        Run all benchmarks.
        
        Args:
            sizes: A list of data sizes to benchmark
            num_runs: The number of runs to average over
            
        Returns:
            A dictionary containing all benchmark results
        """
        self.benchmark_insertion(sizes, num_runs)
        self.benchmark_search(sizes, num_runs)
        self.benchmark_range_query(sizes, num_runs)
        self.benchmark_deletion(sizes, num_runs)
        self.benchmark_random_operations(sizes, num_runs)
        
        return self.results
    
    def plot_results(self, benchmark: str, metric: str = 'time') -> None:
        """
        Plot the results of a benchmark.
        
        Args:
            benchmark: The name of the benchmark to plot
            metric: The metric to plot ('time' or 'memory')
        """
        if benchmark not in self.results:
            print(f"No results for benchmark '{benchmark}'")
            return
        
        results = self.results[benchmark]
        
        plt.figure(figsize=(10, 6))
        
        for structure, metrics in results.items():
            if metric in metrics:
                sizes = sorted(metrics[metric].keys())
                times = [metrics[metric][size] for size in sizes]
                plt.plot(sizes, times, marker='o', label=structure)
        
        plt.title(f"{benchmark.capitalize()} {metric} vs. Data Size")
        plt.xlabel("Data Size")
        plt.ylabel(f"{metric.capitalize()} (seconds)" if metric == 'time' else f"{metric.capitalize()} (MB)")
        plt.grid(True)
        plt.legend()
        
        # Save the plot
        plt.savefig(f"{benchmark}_{metric}.png")
        plt.close()
    
    def plot_all_results(self) -> None:
        """Plot all benchmark results."""
        for benchmark in self.results:
            for metric in ['time', 'memory']:
                if any(metric in metrics for _, metrics in self.results[benchmark].items()):
                    self.plot_results(benchmark, metric)
