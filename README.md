# Ramsey Theory Graph Visualizations

This repository contains two Python scripts for interactive graph visualization:
- [graph.py](graph.py): A script to visualize and interact with graphs.
- [ramsey.py](ramsey.py): A script focused on Ramsey theory with additional interactive capabilities.

## Overview

Both scripts use:
- **NetworkX** for graph data structures and analysis.
- **Matplotlib** for drawing graphs and interactive controls (buttons, sliders, etc.).
- **NumPy** for numerical operations.
- **Random** for edge color selection.

The visualizers allow you to generate graphs, add vertices, and interact with edges (change color, toggle bold, remove edges, create edges, and move vertices).

## Setting Up a Python Environment

1. **Install Python**  
   Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Create a Virtual Environment**  
   Create and activate a virtual environment to manage dependencies:
   ```sh
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   pip install networkx matplotlib numpy
   python ramsey.py
