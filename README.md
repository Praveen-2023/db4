# Lightweight DBMS with B+ Tree Index

This project implements a lightweight database management system (DBMS) in Python that supports basic operations (insert, update, delete, select, aggregation, range queries) on tables stored with a B+ Tree index.

## Features

- B+ Tree implementation for efficient indexing
- Basic CRUD operations on tables
- Range queries
- Performance comparison with brute force approach
- Visualization of B+ Tree structure
- Persistence of database
- Web UI for interacting with the database

## Project Structure

```
db4/
├── database/
│   ├── __init__.py
│   ├── db_manager.py       # Database manager
│   ├── table.py            # Table implementation
│   ├── bplustree.py        # B+ Tree implementation
│   ├── bruteforce.py       # BruteForceDB
│   └── performance_analyzer.py  # Performance analysis
├── templates/              # HTML templates for the web UI
├── static/                 # Static files for the web UI
├── create_tables.py        # Script to create tables
├── insert_sample_data.py   # Script to insert sample data
├── app.py                  # Web UI
├── run_dbms.py             # Main script
├── report.ipynb            # Report and Visualizations
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```
python run_dbms.py
```

This will display a menu with the following options:
1. Create database tables
2. Insert sample data
3. Run performance analysis
4. Visualize B+ Tree structure
5. Query database
6. Run web UI
7. Exit

## Web UI

The web UI provides a user-friendly interface for interacting with the database. To run the web UI, select option 6 from the main menu or run:
```
python app.py
```

The web UI provides the following functionality:
- Database setup (create tables and insert sample data)
- Table management (view, insert, update, delete rows)
- Range queries
- Performance analysis
- Visualization of B+ Tree structure

## Implementation Details

### B+ Tree

The B+ Tree implementation supports the following operations:
- Insertion
- Deletion
- Search
- Range queries

### Database Manager

The database manager provides the following functionality:
- Creating and managing tables
- Persistence of database
- CRUD operations on tables

### Performance Analysis

The performance analyzer compares the B+ Tree with a brute force approach by measuring:
- Insertion time
- Search time
- Deletion time
- Range query time
- Random operations time
- Memory usage

### Visualization

The visualization module uses text representation to visualize the B+ Tree structure.