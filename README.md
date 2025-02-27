# Ramsey Theory Graph Visualizations

This repository contains two Python scripts for interactive graph visualization:
- [testingFile.py](graph.py): A script to visualize test features before modifying  the working version.
- [ramsey.py](ramsey.py): A script focused on Ramsey theory with additional interactive capabilities.

These scripts (and the readme) were written with the help of github copilot

## Overview

Both scripts use:
- **NetworkX** for graph data structures and analysis.
- **Matplotlib** for drawing graphs and interactive controls (buttons, sliders, etc.).
- **NumPy** for numerical operations.
- **Random** for edge color selection.

The visualizers allow you to generate graphs, add vertices, and interact with edges (change color, toggle bold, remove edges, create edges, and move vertices).

## Running the Application

### Option 1: Standalone Executable (No Python Installation Required)

1. **Download the Executable**
   - For Windows: Download `RamseyTheory.exe` from the Releases section
   - For macOS: Download `RamseyTheory` from the Releases section
   
2. **Run the Application**
   - Windows: Double-click on `RamseyTheory.exe`
   - macOS: 
     1. Open Terminal
     2. Navigate to where you downloaded the file: `cd /path/to/downloaded/file`
     3. Make the file executable: `chmod +x RamseyTheory`
     4. To remove apple security flag(if you trust this project): `xattr -d com.apple.quarantine RamseyTheory`
     5. Run the file: `./RamseyTheory`
   - Linux:
     1. Open Terminal
     2. Navigate to where you downloaded the file: `cd /path/to/downloaded/file`
     3. Make the file executable: `chmod +x RamseyTheory`
     4. Run the file: `./RamseyTheory`

3. **Troubleshooting**
   - Windows: If you get a warning about an unrecognized app, click "More info" then "Run anyway"
   - macOS: If you get a security warning, go to System Preferences > Security & Privacy and click "Open Anyway"

### Option 2: Setting Up a Python Environment

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
   ```

## Using the Application

### Controls
- **Number of Vertices slider**: Adjust the number of vertices in the graph
- **Generate Graph button**: Create a new graph with the specified number of vertices
- **Clear button**: Remove all edges from the graph
- **Left-click on edge**: Change edge color
- **Right-click on edge**: Toggle bold appearance
- **Shift + Left-click on edge**: Remove edge
- **Command/Ctrl + Left-click on two vertices**: Add edge between them
- **a + Left-click on empty space**: Add a new vertex
- **Option/Alt + Left-click and drag vertex**: Move vertex to new position
