"""
Database manager for the lightweight DBMS.
"""
import os
import json
import pickle
from typing import Any, List, Dict, Tuple, Optional, Union
from .table import Table


class Database:
    """
    A lightweight database management system using B+ Tree for indexing.
    """
    
    def __init__(self, name: str):
        """
        Initialize a database with the given name.
        
        Args:
            name: The name of the database
        """
        self.name = name
        self.tables = {}  # Dictionary mapping table names to Table objects
        self.data_dir = f"data/{name}"
        
        # Create the data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def create_table(self, name: str, schema: Dict[str, str], primary_key: str) -> bool:
        """
        Create a new table in the database.
        
        Args:
            name: The name of the table
            schema: A dictionary mapping column names to their types
            primary_key: The name of the primary key column
            
        Returns:
            True if the table was created, False otherwise
        """
        # Check if the table already exists
        if name in self.tables:
            return False
        
        # Check if the primary key is in the schema
        if primary_key not in schema:
            return False
        
        # Create the table
        self.tables[name] = Table(name, schema, primary_key)
        return True
    
    def drop_table(self, name: str) -> bool:
        """
        Drop a table from the database.
        
        Args:
            name: The name of the table
            
        Returns:
            True if the table was dropped, False otherwise
        """
        if name not in self.tables:
            return False
        
        del self.tables[name]
        return True
    
    def get_table(self, name: str) -> Optional[Table]:
        """
        Get a table from the database.
        
        Args:
            name: The name of the table
            
        Returns:
            The Table object, or None if not found
        """
        return self.tables.get(name)
    
    def list_tables(self) -> List[str]:
        """
        List all tables in the database.
        
        Returns:
            A list of table names
        """
        return list(self.tables.keys())
    
    def save(self) -> bool:
        """
        Save the database to disk.
        
        Returns:
            True if the database was saved, False otherwise
        """
        try:
            # Create a dictionary representation of the database
            db_data = {
                'name': self.name,
                'tables': {name: table.to_dict() for name, table in self.tables.items()}
            }
            
            # Save the database to a file
            with open(f"{self.data_dir}/db.json", 'w') as f:
                json.dump(db_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    @classmethod
    def load(cls, name: str) -> Optional['Database']:
        """
        Load a database from disk.
        
        Args:
            name: The name of the database
            
        Returns:
            A Database object, or None if the database could not be loaded
        """
        data_dir = f"data/{name}"
        db_file = f"{data_dir}/db.json"
        
        # Check if the database file exists
        if not os.path.exists(db_file):
            return None
        
        try:
            # Load the database from the file
            with open(db_file, 'r') as f:
                db_data = json.load(f)
            
            # Create a new database
            db = cls(name)
            
            # Load the tables
            for table_name, table_data in db_data['tables'].items():
                table = Table.from_dict(table_data)
                db.tables[table_name] = table
            
            return db
        except Exception as e:
            print(f"Error loading database: {e}")
            return None
