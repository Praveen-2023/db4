"""
Script to generate performance plots for the report.
"""
import os
import matplotlib.pyplot as plt
from database.performance_analyzer import PerformanceAnalyzer

def main():
    """Generate performance plots."""
    # Create the output directory
    os.makedirs('plots', exist_ok=True)
    
    # Create the analyzer
    analyzer = PerformanceAnalyzer()
    
    # Define data sizes to benchmark
    sizes = [100, 500, 1000, 5000]
    
    print("Running benchmarks...")
    
    # Run all benchmarks
    results = analyzer.run_all_benchmarks(sizes, num_runs=3)
    
    print("Generating plots...")
    
    # Plot the results
    analyzer.plot_all_results()
    
    print("Plots saved to the 'plots' directory.")
    
    # Print a summary
    print("\nPerformance Summary:")
    for benchmark in results:
        print(f"\n{benchmark.capitalize()}:")
        for structure in results[benchmark]:
            if 'time' in results[benchmark][structure]:
                times = results[benchmark][structure]['time']
                print(f"  {structure} time (seconds):")
                for size in sorted(times.keys()):
                    print(f"    Size {size}: {times[size]:.6f}")
            
            if 'memory' in results[benchmark][structure]:
                memory = results[benchmark][structure]['memory']
                print(f"  {structure} memory (MB):")
                for size in sorted(memory.keys()):
                    print(f"    Size {size}: {memory[size]:.2f}")

if __name__ == '__main__':
    main()
