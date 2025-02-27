import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

class GraphVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = {}
        self.edge_colors = {}
        self.edge_widths = {}
        self.colors = ['r', 'b']  # Red and blue coloring for edges
        
    def create_graph(self, num_vertices):
        self.G.clear()
        self.edge_colors = {}
        self.edge_widths = {}
        
        # Add vertices
        for i in range(num_vertices):
            self.G.add_node(i)
        
        # Create positions on a circle
        self.pos = {}
        for i in range(num_vertices):
            angle = 2 * np.pi * i / num_vertices
            self.pos[i] = (np.cos(angle), np.sin(angle))
        
        # Add edges based on graph type
        for i in range(num_vertices):
            for j in range(i+1, num_vertices):
                self.G.add_edge(i, j)
                color_idx = random.randint(0, len(self.colors)-1)
                self.edge_colors[(i, j)] = self.colors[color_idx]
                self.edge_widths[(i, j)] = 2  # Default width
    
    def draw_graph(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Draw edges with their colors
        for u, v in self.G.edges():
            edge = (u, v) if (u, v) in self.edge_colors else (v, u)
            color = self.edge_colors.get(edge, 'k')
            width = self.edge_widths.get(edge, 2)
            
            edge_x = [self.pos[u][0], self.pos[v][0]]
            edge_y = [self.pos[u][1], self.pos[v][1]]
            ax.plot(edge_x, edge_y, color=color, linewidth=width)
        
        # Draw nodes
        for node, position in self.pos.items():
            ax.scatter(position[0], position[1], s=300, color='lightgray', edgecolors='black', zorder=10)
            ax.text(position[0], position[1], str(node), 
                    fontsize=12, ha='center', va='center', zorder=11)
        
        # Set the limits and remove ticks
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        return fig
    
    def change_edge_color(self, edge_index):
        if edge_index < len(list(self.G.edges())):
            edge = list(self.G.edges())[edge_index]
            current_color = self.edge_colors.get(edge, self.colors[0])
            next_index = (self.colors.index(current_color) + 1) % len(self.colors)
            self.edge_colors[edge] = self.colors[next_index]
    
    def toggle_edge_bold(self, edge_index):
        if edge_index < len(list(self.G.edges())):
            edge = list(self.G.edges())[edge_index]
            current_width = self.edge_widths.get(edge, 2)
            self.edge_widths[edge] = 4 if current_width <= 2 else 2

def main():
    st.title("Interactive Graph Visualization for Ramsey Theory")
    
    # Initialize session state variables
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = GraphVisualizer()
        st.session_state.num_vertices = 5
        
    # Sidebar controls
    st.sidebar.header("Controls")
    num_vertices = st.sidebar.slider("Number of Vertices", 3, 20, st.session_state.num_vertices)
    
    # Update visualization if number of vertices changed
    if num_vertices != st.session_state.num_vertices:
        st.session_state.num_vertices = num_vertices
        st.session_state.visualizer.create_graph(num_vertices)
    
    # Buttons for generating and clearing
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Generate Graph"):
            st.session_state.visualizer.create_graph(st.session_state.num_vertices)
    
    with col2:
        if st.button("Clear"):
            st.session_state.visualizer = GraphVisualizer()
    
    # Generate graph initially if needed
    if not st.session_state.visualizer.G.edges():
        st.session_state.visualizer.create_graph(st.session_state.num_vertices)
    
    # Display the graph
    fig = st.session_state.visualizer.draw_graph()
    st.pyplot(fig)
    
    # Edge interaction section
    st.subheader("Edge Interactions")
    st.write("Select an edge to modify:")
    
    # Format edge list for selection
    edges_list = [f"Edge {i}: ({u}, {v})" for i, (u, v) in enumerate(st.session_state.visualizer.G.edges())]
    
    if edges_list:
        selected_edge = st.selectbox("Select Edge", range(len(edges_list)), format_func=lambda x: edges_list[x])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Change Color"):
                st.session_state.visualizer.change_edge_color(selected_edge)
                st.experimental_rerun()
        
        with col2:
            if st.button("Toggle Bold"):
                st.session_state.visualizer.toggle_edge_bold(selected_edge)
                st.experimental_rerun()
    
    # Instructions
    st.sidebar.markdown("""
    ### Instructions:
    - Use the slider to set the number of vertices
    - Generate a new graph configuration with random edge colors
    - Select edges to change their color or toggle bold appearance
    - Clear the graph to start fresh
    """)

if __name__ == "__main__":
    main()