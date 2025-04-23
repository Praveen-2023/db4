"""
Main script to run the lightweight DBMS with B+ Tree index.
"""
import os
import sys


def print_menu():
    """Print the main menu."""
    print("\nLightweight DBMS with B+ Tree Index")
    print("==================================")
    print("1. Create database tables")
    print("2. Insert sample data")
    print("3. Run performance analysis")
    print("4. Visualize B+ Tree structure")
    print("5. Query database")
    print("6. Run web UI")
    print("7. Exit")
    print("==================================")


def create_tables():
    """Create database tables."""
    print("\nCreating database tables...")
    import create_tables
    create_tables.main()


def insert_sample_data():
    """Insert sample data into the database."""
    print("\nInserting sample data...")
    import insert_sample_data
    insert_sample_data.main()


def run_performance_analysis():
    """Run performance analysis."""
    print("\nRunning performance analysis...")
    import matplotlib.pyplot as plt
    from database.performance_analyzer import PerformanceAnalyzer
    
    # Create the output directory
    os.makedirs('plots', exist_ok=True)
    
    # Create the analyzer
    analyzer = PerformanceAnalyzer()
    
    # Define data sizes to benchmark
    sizes = [100, 500, 1000]
    
    # Run all benchmarks
    results = analyzer.run_all_benchmarks(sizes, num_runs=3)
    
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


def visualize_tree():
    """Visualize B+ Tree structure."""
    print("\nVisualizing B+ Tree structure...")
    
    # Create the output directory
    os.makedirs('visualizations', exist_ok=True)
    
    from database.db_manager import Database
    from database.bplustree import BPlusTree
    
    # Load the database
    db = Database.load('retail_db')
    
    if db is None:
        print("Database not found. Please run create_tables.py first.")
        return
    
    # Create a sample B+ Tree
    tree = BPlusTree(order=5)
    
    # Insert some keys
    for i in range(1, 21):
        tree.insert(i, f"value_{i}")
    
    # Generate a text representation of the tree
    def generate_tree_text(node, level=0, prefix=""):
        if node is None:
            return ""
        
        text = ""
        
        # Add the current node
        if node.is_leaf:
            # For leaf nodes, show keys and values
            values = [f"{key}: {value}" for key, value in zip(node.keys, node.children)]
            text += f"{prefix}{'  ' * level}Leaf: {', '.join(values)}\n"
        else:
            # For internal nodes, show only keys
            text += f"{prefix}{'  ' * level}Node: {', '.join(map(str, node.keys))}\n"
        
        # Add child nodes
        if not node.is_leaf:
            for i, child in enumerate(node.children):
                text += generate_tree_text(child, level + 1, prefix)
        
        return text
    
    # Print the tree
    print("\nSample B+ Tree:")
    print(generate_tree_text(tree.root))
    
    # Visualize the index of each table
    for table_name in db.list_tables():
        table = db.get_table(table_name)
        print(f"\nB+ Tree for {table_name} table:")
        print(generate_tree_text(table.index.root))
    
    print("\nText representations of the trees have been printed above.")
    print("For graphical visualizations, please run the web UI.")


def query_database():
    """Query the database."""
    from database.db_manager import Database
    
    # Load the database
    db = Database.load('retail_db')
    
    if db is None:
        print("Database not found. Please run create_tables.py first.")
        return
    
    # Print the list of tables
    print("\nAvailable tables:")
    for table_name in db.list_tables():
        print(f"- {table_name}")
    
    # Get the table name
    table_name = input("\nEnter table name: ")
    
    # Get the table
    table = db.get_table(table_name)
    
    if table is None:
        print(f"Table '{table_name}' not found")
        return
    
    # Print the query options
    print("\nQuery options:")
    print("1. Select all")
    print("2. Select by primary key")
    print("3. Select by range")
    print("4. Insert row")
    print("5. Update row")
    print("6. Delete row")
    print("7. Back to main menu")
    
    # Get the option
    option = input("\nEnter option: ")
    
    if option == '1':
        # Select all
        rows = table.select_all()
        print(f"\nFound {len(rows)} rows:")
        for row in rows:
            print(row)
    
    elif option == '2':
        # Select by primary key
        key = input(f"\nEnter {table.primary_key} value: ")
        
        # Convert the key to the appropriate type
        if table.schema[table.primary_key] == 'int':
            key = int(key)
        elif table.schema[table.primary_key] == 'float':
            key = float(key)
        
        row = table.select(key)
        
        if row is None:
            print(f"No row found with {table.primary_key} = {key}")
        else:
            print("\nFound row:")
            print(row)
    
    elif option == '3':
        # Select by range
        start_key = input(f"\nEnter start {table.primary_key} value: ")
        end_key = input(f"Enter end {table.primary_key} value: ")
        
        # Convert the keys to the appropriate type
        if table.schema[table.primary_key] == 'int':
            start_key = int(start_key)
            end_key = int(end_key)
        elif table.schema[table.primary_key] == 'float':
            start_key = float(start_key)
            end_key = float(end_key)
        
        rows = table.select_range(start_key, end_key)
        
        print(f"\nFound {len(rows)} rows:")
        for row in rows:
            print(row)
    
    elif option == '4':
        # Insert row
        row = {}
        
        # Get values for each column
        for column, column_type in table.schema.items():
            value = input(f"\nEnter {column} ({column_type}): ")
            
            # Convert the value to the appropriate type
            if column_type == 'int':
                value = int(value)
            elif column_type == 'float':
                value = float(value)
            elif column_type == 'bool':
                value = value.lower() in ('true', 'yes', '1')
            
            row[column] = value
        
        # Insert the row
        if table.insert(row):
            print("\nRow inserted successfully")
            db.save()
        else:
            print("\nFailed to insert row")
    
    elif option == '5':
        # Update row
        key = input(f"\nEnter {table.primary_key} value: ")
        
        # Convert the key to the appropriate type
        if table.schema[table.primary_key] == 'int':
            key = int(key)
        elif table.schema[table.primary_key] == 'float':
            key = float(key)
        
        # Get the existing row
        row = table.select(key)
        
        if row is None:
            print(f"No row found with {table.primary_key} = {key}")
            return
        
        print("\nCurrent row:")
        print(row)
        
        # Get the columns to update
        columns = input("\nEnter columns to update (comma-separated): ").split(',')
        
        # Get new values
        new_values = {}
        for column in columns:
            column = column.strip()
            
            if column not in table.schema:
                print(f"Column '{column}' not found in table schema")
                continue
            
            value = input(f"\nEnter new {column} ({table.schema[column]}): ")
            
            # Convert the value to the appropriate type
            if table.schema[column] == 'int':
                value = int(value)
            elif table.schema[column] == 'float':
                value = float(value)
            elif table.schema[column] == 'bool':
                value = value.lower() in ('true', 'yes', '1')
            
            new_values[column] = value
        
        # Update the row
        if table.update(key, new_values):
            print("\nRow updated successfully")
            db.save()
        else:
            print("\nFailed to update row")
    
    elif option == '6':
        # Delete row
        key = input(f"\nEnter {table.primary_key} value: ")
        
        # Convert the key to the appropriate type
        if table.schema[table.primary_key] == 'int':
            key = int(key)
        elif table.schema[table.primary_key] == 'float':
            key = float(key)
        
        # Delete the row
        if table.delete(key):
            print("\nRow deleted successfully")
            db.save()
        else:
            print("\nFailed to delete row")
    
    elif option == '7':
        # Back to main menu
        return
    
    else:
        print("\nInvalid option")


def run_web_ui():
    """Run the web UI."""
    print("\nRunning web UI...")
    print("Press Ctrl+C to stop the server.")
    
    # Import the app
    from app import app
    
    # Run the app
    app.run(debug=True)


def main():
    """Run the main program."""
    while True:
        print_menu()
        option = input("\nEnter option: ")
        
        if option == '1':
            create_tables()
        elif option == '2':
            insert_sample_data()
        elif option == '3':
            run_performance_analysis()
        elif option == '4':
            visualize_tree()
        elif option == '5':
            query_database()
        elif option == '6':
            run_web_ui()
        elif option == '7':
            print("\nExiting...")
            sys.exit(0)
        else:
            print("\nInvalid option")


if __name__ == '__main__':
    main()
