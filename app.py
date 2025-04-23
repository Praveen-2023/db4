"""
Web UI for the lightweight DBMS with B+ Tree index.
"""
import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database.db_manager import Database
import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid GUI issues
import matplotlib.pyplot as plt
import io
import base64
from database.performance_analyzer import PerformanceAnalyzer

app = Flask(__name__, template_folder='templates', static_folder='static')

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)
os.makedirs('static/images', exist_ok=True)

# Global database instance
db = None

@app.route('/')
def index():
    """Render the home page."""
    global db
    if db is None:
        # Try to load the database
        db = Database.load('retail_db')
        if db is None:
            # Database doesn't exist, create it
            return redirect(url_for('setup'))
    
    # Get the list of tables
    tables = db.list_tables()
    return render_template('index.html', tables=tables)

@app.route('/setup')
def setup():
    """Render the setup page."""
    return render_template('setup.html')

@app.route('/create_tables', methods=['POST'])
def create_tables():
    """Create the database tables."""
    global db
    db = Database('retail_db')
    
    # Create the tables
    from create_tables import (
        create_member_table, create_shop_table, create_customer_table,
        create_supplier_table, create_product_table, create_order_table,
        create_order_details_table, create_employee_table, create_payment_table,
        create_attendance_table, create_loyalty_table
    )
    
    create_member_table(db)
    create_shop_table(db)
    create_customer_table(db)
    create_supplier_table(db)
    create_product_table(db)
    create_order_table(db)
    create_order_details_table(db)
    create_employee_table(db)
    create_payment_table(db)
    create_attendance_table(db)
    create_loyalty_table(db)
    
    # Save the database
    db.save()
    
    return jsonify({"success": True, "message": "Tables created successfully"})

@app.route('/insert_sample_data', methods=['POST'])
def insert_sample_data():
    """Insert sample data into the database."""
    global db
    if db is None:
        return jsonify({"success": False, "message": "Database not initialized"})
    
    # Insert sample data
    from insert_sample_data import (
        insert_member_data, insert_shop_data, insert_customer_data,
        insert_supplier_data, insert_product_data, insert_order_data,
        insert_order_details_data
    )
    
    insert_member_data(db)
    insert_shop_data(db)
    insert_customer_data(db)
    insert_supplier_data(db)
    insert_product_data(db)
    insert_order_data(db)
    insert_order_details_data(db)
    
    # Save the database
    db.save()
    
    return jsonify({"success": True, "message": "Sample data inserted successfully"})

@app.route('/table/<table_name>')
def view_table(table_name):
    """View a table."""
    global db
    if db is None:
        return redirect(url_for('setup'))
    
    # Get the table
    table = db.get_table(table_name)
    if table is None:
        return render_template('error.html', message=f"Table '{table_name}' not found")
    
    # Get all rows
    rows = table.select_all()
    
    # Get the schema
    schema = table.schema
    
    return render_template('table.html', table_name=table_name, rows=rows, schema=schema, primary_key=table.primary_key)

@app.route('/table/<table_name>/insert', methods=['GET', 'POST'])
def insert_row(table_name):
    """Insert a row into a table."""
    global db
    if db is None:
        return redirect(url_for('setup'))
    
    # Get the table
    table = db.get_table(table_name)
    if table is None:
        return render_template('error.html', message=f"Table '{table_name}' not found")
    
    if request.method == 'POST':
        # Get the form data
        row = {}
        for column, column_type in table.schema.items():
            value = request.form.get(column)
            
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
            # Save the database
            db.save()
            return redirect(url_for('view_table', table_name=table_name))
        else:
            return render_template('error.html', message="Failed to insert row")
    
    # Render the insert form
    return render_template('insert.html', table_name=table_name, schema=table.schema)

@app.route('/table/<table_name>/update/<primary_key_value>', methods=['GET', 'POST'])
def update_row(table_name, primary_key_value):
    """Update a row in a table."""
    global db
    if db is None:
        return redirect(url_for('setup'))
    
    # Get the table
    table = db.get_table(table_name)
    if table is None:
        return render_template('error.html', message=f"Table '{table_name}' not found")
    
    # Convert the primary key value to the appropriate type
    if table.schema[table.primary_key] == 'int':
        primary_key_value = int(primary_key_value)
    elif table.schema[table.primary_key] == 'float':
        primary_key_value = float(primary_key_value)
    
    # Get the row
    row = table.select(primary_key_value)
    if row is None:
        return render_template('error.html', message=f"Row with {table.primary_key}={primary_key_value} not found")
    
    if request.method == 'POST':
        # Get the form data
        new_values = {}
        for column, column_type in table.schema.items():
            if column != table.primary_key:  # Don't update the primary key
                value = request.form.get(column)
                
                # Convert the value to the appropriate type
                if column_type == 'int':
                    value = int(value)
                elif column_type == 'float':
                    value = float(value)
                elif column_type == 'bool':
                    value = value.lower() in ('true', 'yes', '1')
                
                new_values[column] = value
        
        # Update the row
        if table.update(primary_key_value, new_values):
            # Save the database
            db.save()
            return redirect(url_for('view_table', table_name=table_name))
        else:
            return render_template('error.html', message="Failed to update row")
    
    # Render the update form
    return render_template('update.html', table_name=table_name, row=row, schema=table.schema, primary_key=table.primary_key)

@app.route('/table/<table_name>/delete/<primary_key_value>', methods=['POST'])
def delete_row(table_name, primary_key_value):
    """Delete a row from a table."""
    global db
    if db is None:
        return redirect(url_for('setup'))
    
    # Get the table
    table = db.get_table(table_name)
    if table is None:
        return render_template('error.html', message=f"Table '{table_name}' not found")
    
    # Convert the primary key value to the appropriate type
    if table.schema[table.primary_key] == 'int':
        primary_key_value = int(primary_key_value)
    elif table.schema[table.primary_key] == 'float':
        primary_key_value = float(primary_key_value)
    
    # Delete the row
    if table.delete(primary_key_value):
        # Save the database
        db.save()
        return redirect(url_for('view_table', table_name=table_name))
    else:
        return render_template('error.html', message="Failed to delete row")

@app.route('/table/<table_name>/range', methods=['GET', 'POST'])
def range_query(table_name):
    """Perform a range query on a table."""
    global db
    if db is None:
        return redirect(url_for('setup'))
    
    # Get the table
    table = db.get_table(table_name)
    if table is None:
        return render_template('error.html', message=f"Table '{table_name}' not found")
    
    if request.method == 'POST':
        # Get the form data
        start_key = request.form.get('start_key')
        end_key = request.form.get('end_key')
        
        # Convert the keys to the appropriate type
        if table.schema[table.primary_key] == 'int':
            start_key = int(start_key)
            end_key = int(end_key)
        elif table.schema[table.primary_key] == 'float':
            start_key = float(start_key)
            end_key = float(end_key)
        
        # Perform the range query
        rows = table.select_range(start_key, end_key)
        
        # Render the results
        return render_template('range_results.html', table_name=table_name, rows=rows, schema=table.schema, primary_key=table.primary_key, start_key=start_key, end_key=end_key)
    
    # Render the range query form
    return render_template('range.html', table_name=table_name, primary_key=table.primary_key)

@app.route('/performance')
def performance():
    """Run performance analysis."""
    # Create the analyzer
    analyzer = PerformanceAnalyzer()
    
    # Define data sizes to benchmark
    sizes = [100, 500, 1000]
    
    # Run all benchmarks
    results = analyzer.run_all_benchmarks(sizes, num_runs=1)
    
    # Generate plots
    plots = {}
    for benchmark in results:
        for metric in ['time', 'memory']:
            if any(metric in metrics for _, metrics in results[benchmark].items()):
                # Create a plot
                plt.figure(figsize=(10, 6))
                
                for structure, metrics in results[benchmark].items():
                    if metric in metrics:
                        sizes = sorted(metrics[metric].keys())
                        values = [metrics[metric][size] for size in sizes]
                        plt.plot(sizes, values, marker='o', label=structure)
                
                plt.title(f"{benchmark.capitalize()} {metric} vs. Data Size")
                plt.xlabel("Data Size")
                plt.ylabel(f"{metric.capitalize()} ({'seconds' if metric == 'time' else 'MB'})")
                plt.grid(True)
                plt.legend()
                
                # Save the plot to a bytes buffer
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                
                # Convert the buffer to a base64 string
                plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                plots[f"{benchmark}_{metric}"] = plot_data
                
                plt.close()
    
    return render_template('performance.html', plots=plots, results=results)

@app.route('/visualize')
def visualize():
    """Visualize the B+ Tree structure."""
    global db
    if db is None:
        return redirect(url_for('setup'))
    
    # Get the list of tables
    tables = db.list_tables()
    
    # Create a sample B+ Tree
    from database.bplustree import BPlusTree
    tree = BPlusTree(order=5)
    
    # Insert some keys
    for i in range(1, 21):
        tree.insert(i, f"value_{i}")
    
    # Generate a text representation of the tree
    tree_text = generate_tree_text(tree.root)
    
    return render_template('visualize.html', tables=tables, tree_text=tree_text)

def generate_tree_text(node, level=0, prefix=""):
    """Generate a text representation of a B+ Tree node."""
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

@app.route('/table/<table_name>/visualize')
def visualize_table(table_name):
    """Visualize the B+ Tree structure of a table."""
    global db
    if db is None:
        return redirect(url_for('setup'))
    
    # Get the table
    table = db.get_table(table_name)
    if table is None:
        return render_template('error.html', message=f"Table '{table_name}' not found")
    
    # Generate a text representation of the tree
    tree_text = generate_tree_text(table.index.root)
    
    return render_template('visualize_table.html', table_name=table_name, tree_text=tree_text)

if __name__ == '__main__':
    app.run(debug=True)
