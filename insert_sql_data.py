"""
Script to insert SQL data into the database.
"""
import re
import datetime
from database.db_manager import Database

def parse_sql_insert(sql_statement):
    """Parse a SQL INSERT statement and extract table name, columns, and values."""
    # Extract table name
    table_match = re.search(r'INSERT INTO\s+(?:`?(\w+)`?)', sql_statement, re.IGNORECASE)
    if not table_match:
        return None, None, None
    
    table_name = table_match.group(1)
    
    # Extract columns
    columns_match = re.search(r'\(([^)]+)\)\s+VALUES', sql_statement, re.IGNORECASE)
    if not columns_match:
        return table_name, None, None
    
    columns = [col.strip() for col in columns_match.group(1).split(',')]
    
    # Extract values
    values_pattern = r'VALUES\s+(\([^)]+\))'
    if 'VALUES' in sql_statement.upper():
        values_matches = re.findall(values_pattern, sql_statement, re.IGNORECASE)
        if not values_matches:
            # Try multi-row format
            multi_values_pattern = r'VALUES\s+((?:\([^)]+\),?\s*)+)'
            multi_values_match = re.search(multi_values_pattern, sql_statement, re.IGNORECASE)
            if multi_values_match:
                values_str = multi_values_match.group(1)
                values_matches = re.findall(r'\(([^)]+)\)', values_str)
                values = []
                for value_match in values_matches:
                    value_items = []
                    # Split by comma, but respect quotes
                    in_quote = False
                    current_item = ""
                    for char in value_match:
                        if char == "'" or char == '"':
                            in_quote = not in_quote
                            current_item += char
                        elif char == ',' and not in_quote:
                            value_items.append(current_item.strip())
                            current_item = ""
                        else:
                            current_item += char
                    if current_item:
                        value_items.append(current_item.strip())
                    values.append(value_items)
            else:
                return table_name, columns, None
        else:
            # Single row format
            values = []
            for value_match in values_matches:
                value_items = value_match.strip('()').split(',')
                values.append([item.strip() for item in value_items])
    else:
        return table_name, columns, None
    
    return table_name, columns, values

def convert_value(value, column_type):
    """Convert a string value to the appropriate Python type."""
    value = value.strip()
    
    # Remove quotes
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        value = value[1:-1]
    
    # Handle special values
    if value.upper() == 'NULL':
        return None
    elif value.upper() == 'NOW()':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert to appropriate type
    if column_type == 'int':
        try:
            return int(value)
        except ValueError:
            return 0
    elif column_type == 'float':
        try:
            return float(value)
        except ValueError:
            return 0.0
    elif column_type == 'bool':
        return value.lower() in ('true', 'yes', '1')
    else:
        return value

def insert_sql_data(db, sql_statements):
    """Insert data from SQL statements into the database."""
    for statement in sql_statements:
        if not statement.strip() or statement.strip().startswith('--') or statement.strip().startswith('SHOW'):
            continue
        
        table_name, columns, values_list = parse_sql_insert(statement)
        
        if not table_name or not columns or not values_list:
            print(f"Skipping statement: {statement[:50]}...")
            continue
        
        table = db.get_table(table_name)
        if not table:
            print(f"Table '{table_name}' not found")
            continue
        
        for values in values_list:
            if len(columns) != len(values):
                print(f"Column count ({len(columns)}) doesn't match value count ({len(values)}) for table '{table_name}'")
                continue
            
            row = {}
            for i, column in enumerate(columns):
                column = column.strip()
                value = values[i].strip() if i < len(values) else None
                row[column] = convert_value(value, table.schema.get(column, 'str'))
            
            if table.insert(row):
                print(f"Inserted row into '{table_name}': {row}")
            else:
                print(f"Failed to insert row into '{table_name}': {row}")
    
    # Save the database
    db.save()
    print("Database saved")

def main():
    """Insert SQL data into the database."""
    # Load the database
    db = Database.load('retail_db')
    
    if db is None:
        print("Database not found. Please run create_tables.py first.")
        return
    
    # Read SQL statements from file
    with open('sql_data.sql', 'r') as f:
        sql_data = f.read()
    
    # Split into individual statements
    sql_statements = sql_data.split(';')
    
    # Insert data
    insert_sql_data(db, sql_statements)

if __name__ == '__main__':
    main()
