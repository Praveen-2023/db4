"""
BruteForceDB implementation for performance comparison with B+ Tree.
"""
from typing import Any, List, Tuple, Optional


class BruteForceDB:
    """
    A simple database implementation using linear search for operations.
    Used as a baseline for performance comparison with B+ Tree.
    """
    
    def __init__(self):
        """Initialize an empty database."""
        self.data = []  # List of (key, value) tuples
    
    def insert(self, key: Any, value: Any) -> None:
        """
        Insert a key-value pair into the database.
        
        Args:
            key: The key to insert
            value: The value associated with the key
        """
        # Check if key already exists
        for i, (k, _) in enumerate(self.data):
            if k == key:
                # Update existing key
                self.data[i] = (key, value)
                return
        
        # Key doesn't exist, append new pair
        self.data.append((key, value))
    
    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the database.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if not found
        """
        for k, v in self.data:
            if k == key:
                return v
        return None
    
    def delete(self, key: Any) -> bool:
        """
        Delete a key-value pair from the database.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False otherwise
        """
        for i, (k, _) in enumerate(self.data):
            if k == key:
                self.data.pop(i)
                return True
        return False
    
    def update(self, key: Any, new_value: Any) -> bool:
        """
        Update the value associated with a key.
        
        Args:
            key: The key to update
            new_value: The new value to associate with the key
            
        Returns:
            True if the key was updated, False otherwise
        """
        for i, (k, _) in enumerate(self.data):
            if k == key:
                self.data[i] = (key, new_value)
                return True
        return False
    
    def range_query(self, start_key: Any, end_key: Any) -> List[Tuple[Any, Any]]:
        """
        Return all key-value pairs where start_key <= key <= end_key.
        
        Args:
            start_key: The lower bound of the range (inclusive)
            end_key: The upper bound of the range (inclusive)
            
        Returns:
            A list of (key, value) tuples in the range
        """
        return [(k, v) for k, v in self.data if start_key <= k <= end_key]
    
    def get_all(self) -> List[Tuple[Any, Any]]:
        """
        Return all key-value pairs in the database.
        
        Returns:
            A list of (key, value) tuples
        """
        return self.data.copy()
