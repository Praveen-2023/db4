"""
Script to generate tree visualizations for the report.
"""
import os
from database.bplustree import BPlusTree

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

def main():
    """Generate tree visualizations."""
    # Create the output directory
    os.makedirs('visualizations', exist_ok=True)
    
    # Create a sample B+ Tree
    tree = BPlusTree(order=5)
    
    # Insert some keys
    for i in range(1, 21):
        tree.insert(i, f"value_{i}")
    
    # Generate a text representation of the tree
    tree_text = generate_tree_text(tree.root)
    
    # Save the text representation to a file
    with open('visualizations/sample_tree.txt', 'w') as f:
        f.write(tree_text)
    
    print("Tree visualization saved to visualizations/sample_tree.txt")
    
    # Try to generate a graphical visualization
    try:
        dot = tree.visualize_tree()
        dot.render('visualizations/sample_tree', format='png', cleanup=True)
        print("Tree visualization saved to visualizations/sample_tree.png")
    except Exception as e:
        print(f"Failed to generate graphical visualization: {e}")
        print("Using text representation instead.")

if __name__ == '__main__':
    main()
