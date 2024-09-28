# Minimax Tree Visualization with Alpha-Beta Pruning

This Python script implements a GUI application using Tkinter that allows users to visualize a Minimax tree with Alpha-Beta pruning. The application enables users to input the depth of the tree and manually enter the leaf node values. It then computes the Minimax values for each node, visualizes the tree, and highlights the optimal path and pruned branches.

## Features
- **Minimax Algorithm**: Computes the Minimax values for each node and highlights the optimal path for the maximizing player.
- **Alpha-Beta Pruning**: Implements Alpha-Beta pruning to improve efficiency by pruning unnecessary branches.
- **Tree Visualization**: Visualizes the Minimax tree structure with different shapes for Max and Min nodes.
- **Interactive GUI**: Users can input tree depth and leaf node values through a Tkinter-based interface.

## How to Run

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/minimax-tree-visualization.git
    ```
2. Install the required libraries:
    ```bash
    pip install tkinter
    ```
3. Run the application:
    ```bash
    python minimax_tree_visualization.py
    ```

## Application Details

1. **GUI Interface**: The GUI is built with Tkinter and includes input fields for tree depth and leaf node values. Users can generate the Minimax tree by clicking buttons, and the tree is visualized on a canvas.

2. **Minimax Tree Creation**: A function generates the Minimax tree recursively based on the user-specified depth. Users manually input values for the leaf nodes, which are used to build the tree structure.

3. **Minimax Computation**: The Minimax algorithm is applied to compute values at each node, determining the optimal path for the maximizing player. Alpha-Beta pruning is used to skip unnecessary branches.

4. **Visualization**: The tree is drawn on the canvas with circles representing Max nodes, squares representing Min nodes, and lines connecting them. The computed Minimax values are displayed, and the optimal path is highlighted. Pruned branches are visually distinguished.

## Additional Features

- **Optimal Path Highlighting**: After the Minimax computation, the optimal path is highlighted.
- **Error Handling**: Includes error handling for invalid inputs.
- **Interactive Node Information**: Clicking on nodes in the tree visualization displays their value and type (Max or Min).
