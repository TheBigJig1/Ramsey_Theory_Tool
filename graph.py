import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons
import numpy as np
import random

class GraphVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.02, bottom=0.15, right=0.98, top=0.98)
        self.G = nx.Graph()
        self.pos = {}
        self.num_vertices = 5  # Default number of vertices
        self.edge_probability = 0.5  # Default edge probability
        self.graph_type = "Complete"
        self.edge_colors = {}
        self.edge_widths = {}  # Track edge widths for bold/normal states
        self.colors = ['r', 'b']  # Red and blue coloring for edges
        self.drawing_edge = False
        self.start_vertex = None
        self.vertex_radius = 0.1  # Radius for vertex hit detection
        
        # Initialize controls
        self.setup_controls()
        self.create_graph()
        self.draw_graph()
        
        # Register mouse event handlers
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
    def setup_controls(self):
        # Vertex count slider
        vertex_slider_ax = plt.axes([0.2, 0.02, 0.65, 0.03])
        self.vertex_slider = Slider(
            ax=vertex_slider_ax,
            label='Number of Vertices',
            valmin=3,
            valmax=20,
            valinit=self.num_vertices,
            valstep=1
        )
        self.vertex_slider.on_changed(self.update_num_vertices)
        
        # Buttons
        gen_button_ax = plt.axes([0.7, 0.07, 0.2, 0.06])
        self.gen_button = Button(gen_button_ax, 'Generate Graph')
        self.gen_button.on_clicked(self.generate_new_graph)
        
        clear_button_ax = plt.axes([0.1, 0.07, 0.2, 0.06])
        self.clear_button = Button(clear_button_ax, 'Clear')
        self.clear_button.on_clicked(self.clear_graph)
    
    def create_graph(self):
        self.G.clear()
        self.edge_colors = {}
        self.edge_widths = {}
        self.pos = {}
        
        # Add vertices
        for i in range(self.num_vertices):
            self.G.add_node(i)
        
        # Create positions on a circle
        for i in range(self.num_vertices):
            angle = 2 * np.pi * i / self.num_vertices
            self.pos[i] = (np.cos(angle), np.sin(angle))
        
        # Add edges based on graph type
        if self.graph_type == "Complete":
            for i in range(self.num_vertices):
                for j in range(i+1, self.num_vertices):
                    self.G.add_edge(i, j)
                    color_idx = random.randint(0, len(self.colors)-1)
                    self.edge_colors[(i, j)] = self.colors[color_idx]
                    self.edge_widths[(i, j)] = 2  # Default width
    
    def draw_graph(self):
        self.ax.clear()
        self.edge_lines = {}  # Store line objects for edge detection
        
        # Draw edges with their colors
        for u, v in self.G.edges():
            edge = (u, v) if (u, v) in self.edge_colors else (v, u)
            color = self.edge_colors.get(edge, 'k')
            width = self.edge_widths.get(edge, 2)
            
            edge_x = [self.pos[u][0], self.pos[v][0]]
            edge_y = [self.pos[u][1], self.pos[v][1]]
            line = self.ax.plot(edge_x, edge_y, color=color, linewidth=width, picker=True, pickradius=5)[0]
            
            # Store the line object with its endpoints for later reference
            self.edge_lines[line] = (u, v)
        
        # Draw nodes
        for node, position in self.pos.items():
            self.ax.scatter(position[0], position[1], s=300, color='lightgray', edgecolors='black', zorder=10)
            self.ax.text(position[0], position[1], str(node), 
                        fontsize=12, ha='center', va='center', zorder=11)
        
        # Draw preview line while drawing edge
        if self.drawing_edge and self.start_vertex is not None:
            start_pos = self.pos[self.start_vertex]
            self.ax.plot([start_pos[0]], [start_pos[1]], 'g--', alpha=0.5)
        
        # Set the limits and remove ticks
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Add status information
        info_text = (f"Graph Type: Custom\n"
                    f"Vertices: {self.num_vertices}\n"
                    f"Edges: {self.G.number_of_edges()}\n"
                    f"Right-click: Add vertex\n"
                    f"Left-click vertices: Draw edge\n"
                    f"Clear: Reset graph")
        self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes,
                   fontsize=10, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.7))
        
        self.fig.canvas.draw_idle()
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
            
        if event.button == 3:  # Right click
            # Create new vertex at cursor position
            new_vertex = len(self.G.nodes)
            self.G.add_node(new_vertex)
            self.pos[new_vertex] = (event.xdata, event.ydata)
            self.draw_graph()
            
        elif event.button == 1:  # Left click
            # Check if clicked on a vertex
            clicked_vertex = self.find_vertex_at_position(event.xdata, event.ydata)
            
            if clicked_vertex is not None:
                if not self.drawing_edge:
                    # Start drawing edge
                    self.drawing_edge = True
                    self.start_vertex = clicked_vertex
                else:
                    # Complete edge drawing
                    end_vertex = clicked_vertex
                    if self.start_vertex != end_vertex:
                        self.G.add_edge(self.start_vertex, end_vertex)
                        edge = (self.start_vertex, end_vertex)
                        self.edge_colors[edge] = self.colors[0]
                        self.edge_widths[edge] = 2
                    self.drawing_edge = False
                    self.start_vertex = None
                self.draw_graph()
    
    def find_vertex_at_position(self, x, y):
        for vertex, pos in self.pos.items():
            if np.sqrt((pos[0] - x)**2 + (pos[1] - y)**2) < self.vertex_radius:
                return vertex
        return None
    
    def update_num_vertices(self, val):
        self.num_vertices = int(val)
    
    def generate_new_graph(self, event):
        self.create_graph()
        self.draw_graph()
    
    def clear_graph(self, event):
        self.G.clear()
        self.edge_colors = {}
        self.edge_widths = {}
        self.num_vertices = int(self.vertex_slider.val)
        # Create positions on a circle for the specified number of vertices
        for i in range(self.num_vertices):
            self.G.add_node(i)
            angle = 2 * np.pi * i / self.num_vertices
            self.pos[i] = (np.cos(angle), np.sin(angle))
            self.draw_graph()
    
    def show(self):
        plt.show()

if __name__ == "__main__":
    print("Interactive Graph Visualization for Ramsey Theory")
    print("------------------------------------------------")
    print("Controls:")
    print("- Adjust the number of vertices with the slider")
    print("- Generate new graph configurations")
    print("- Left-click on an edge to change its color")
    print("- Right-click on an edge to toggle bold appearance")
    print("- Clear the graph to start fresh")
    
    visualizer = GraphVisualizer()
    visualizer.show()