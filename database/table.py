"""
Table implementation for the lightweight DBMS.
"""
import json
import os
from typing import Any, List, Dict, Tuple, Optional, Union
from .bplustree import BPlusTree


class Table:
    """
    A table in the database, using B+ Tree for indexing.
    """
    
    def __init__(self, name: str, schema: Dict[str, str], primary_key: str):
        """
        Initialize a table with the given schema.
        
        Args:
            name: The name of the table
            schema: A dictionary mapping column names to their types
            primary_key: The name of the primary key column
        """
        self.name = name
        self.schema = schema
        self.primary_key = primary_key
        self.index = BPlusTree(order=5)  # B+ Tree index on the primary key
        self.rows = []  # List to store all rows for persistence
    
    def insert(self, row: Dict[str, Any]) -> bool:
        """
        Insert a row into the table.
        
        Args:
            row: A dictionary mapping column names to values
            
        Returns:
            True if the row was inserted, False otherwise
        """
        # Validate the row against the schema
        if not self._validate_row(row):
            return False
        
        # Check if the primary key exists
        if self.primary_key not in row:
            return False
        
        # Check if the primary key is unique
        if self.index.search(row[self.primary_key]) is not None:
            return False
        
        # Insert the row
        self.index.insert(row[self.primary_key], row)
        self.rows.append(row)
        return True
    
    def update(self, primary_key_value: Any, new_values: Dict[str, Any]) -> bool:
        """
        Update a row in the table.
        
        Args:
            primary_key_value: The value of the primary key for the row to update
            new_values: A dictionary mapping column names to new values
            
        Returns:
            True if the row was updated, False otherwise
        """
        # Get the existing row
        row = self.index.search(primary_key_value)
        if row is None:
            return False
        
        # Create a copy of the row with updated values
        updated_row = row.copy()
        for key, value in new_values.items():
            if key in self.schema:
                updated_row[key] = value
        
        # Validate the updated row
        if not self._validate_row(updated_row):
            return False
        
        # Check if the primary key is being updated
        if self.primary_key in new_values and new_values[self.primary_key] != primary_key_value:
            # Delete the old row and insert the new one
            self.delete(primary_key_value)
            return self.insert(updated_row)
        
        # Update the row
        self.index.update(primary_key_value, updated_row)
        
        # Update the row in the rows list
        for i, r in enumerate(self.rows):
            if r[self.primary_key] == primary_key_value:
                self.rows[i] = updated_row
                break
        
        return True
    
    def delete(self, primary_key_value: Any) -> bool:
        """
        Delete a row from the table.
        
        Args:
            primary_key_value: The value of the primary key for the row to delete
            
        Returns:
            True if the row was deleted, False otherwise
        """
        # Check if the row exists
        if self.index.search(primary_key_value) is None:
            return False
        
        # Delete the row
        self.index.delete(primary_key_value)
        
        # Delete the row from the rows list
        self.rows = [r for r in self.rows if r[self.primary_key] != primary_key_value]
        
        return True
    
    def select(self, primary_key_value: Any) -> Optional[Dict[str, Any]]:
        """
        Select a row from the table by primary key.
        
        Args:
            primary_key_value: The value of the primary key for the row to select
            
        Returns:
            The row as a dictionary, or None if not found
        """
        return self.index.search(primary_key_value)
    
    def select_range(self, start_key: Any, end_key: Any) -> List[Dict[str, Any]]:
        """
        Select rows from the table where the primary key is in the given range.
        
        Args:
            start_key: The lower bound of the range (inclusive)
            end_key: The upper bound of the range (inclusive)
            
        Returns:
            A list of rows as dictionaries
        """
        return [row for _, row in self.index.range_query(start_key, end_key)]
    
    def select_all(self) -> List[Dict[str, Any]]:
        """
        Select all rows from the table.
        
        Returns:
            A list of all rows as dictionaries
        """
        return [row for _, row in self.index.get_all()]
    
    def select_where(self, condition: callable) -> List[Dict[str, Any]]:
        """
        Select rows from the table that satisfy the given condition.
        
        Args:
            condition: A function that takes a row and returns a boolean
            
        Returns:
            A list of rows as dictionaries that satisfy the condition
        """
        return [row for row in self.select_all() if condition(row)]
    
    def _validate_row(self, row: Dict[str, Any]) -> bool:
        """
        Validate a row against the schema.
        
        Args:
            row: A dictionary mapping column names to values
            
        Returns:
            True if the row is valid, False otherwise
        """
        # Check if all required columns are present
        for column in self.schema:
            if column not in row:
                return False
        
        # Check if all values have the correct type
        for column, value in row.items():
            if column not in self.schema:
                return False
            
            expected_type = self.schema[column]
            
            # Basic type checking
            if expected_type == 'int' and not isinstance(value, int):
                return False
            elif expected_type == 'float' and not isinstance(value, (int, float)):
                return False
            elif expected_type == 'str' and not isinstance(value, str):
                return False
            elif expected_type == 'bool' and not isinstance(value, bool):
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the table to a dictionary for persistence.
        
        Returns:
            A dictionary representation of the table
        """
        return {
            'name': self.name,
            'schema': self.schema,
            'primary_key': self.primary_key,
            'rows': self.rows
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Table':
        """
        Create a table from a dictionary.
        
        Args:
            data: A dictionary representation of the table
            
        Returns:
            A new Table instance
        """
        table = cls(data['name'], data['schema'], data['primary_key'])
        
        # Insert all rows
        for row in data['rows']:
            table.insert(row)
        
        return table
