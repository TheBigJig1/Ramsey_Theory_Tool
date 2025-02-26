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
        self.graph_type = "Complete"
        self.edge_colors = {}
        self.edge_widths = {}  # Track edge widths for bold/normal states
        self.colors = ['r', 'b']  # Red and blue coloring for edges
        self.selected_vertex = None
        self.cmd_pressed = False  # Track if command key is pressed
        self.opt_pressed = False  # Track if option key is pressed
        self.dragging_vertex = None  # Track which vertex is being dragged

        # Initialize controls
        self.setup_controls()
        self.create_graph()
        self.draw_graph()
        
        # Register event handlers
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)
        
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
        
        # Add vertices
        for i in range(self.num_vertices):
            self.G.add_node(i)
        
        # Create positions on a circle
        self.pos = {}
        for i in range(self.num_vertices):
            angle = 2 * np.pi * i / self.num_vertices
            self.pos[i] = (np.cos(angle), np.sin(angle))
        
        # Add edges based on graph type
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
        
        # Set the limits and remove ticks
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Add status information
        info_text = (f"Graph Type: {self.graph_type}\n"
                    f"Vertices: {self.num_vertices}\n"
                    f"Edges: {self.G.number_of_edges()}\n"
                    f"Left-click edge: Change color\n"
                    f"Right-click edge: Toggle bold\n"
                    f"Shift + Left-click: Remove edge\n"
                    f"Command + Click vertices: Add edge\n"
                    f"Option + Click vertex: Move Vertex")
        self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes,
                   fontsize=10, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.7))
        
        self.fig.canvas.draw_idle()
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        # Option-click vertex dragging
        if self.opt_pressed:
            for node, position in self.pos.items():
                dist = np.sqrt((position[0] - event.xdata)**2 + 
                            (position[1] - event.ydata)**2)
                if dist < 0.2:  # Threshold for selecting vertex
                    self.dragging_vertex = node
                    return

        # Command-click vertex selection
        if self.cmd_pressed:
            # Find clicked vertex
            for node, position in self.pos.items():
                dist = np.sqrt((position[0] - event.xdata)**2 + 
                            (position[1] - event.ydata)**2)
                if dist < 0.2:  # Increased click radius for better vertex detection
                    if self.selected_vertex is None:
                        # First vertex selection
                        self.selected_vertex = node
                        self.draw_graph()
                        # Highlight selected vertex
                        self.ax.scatter(self.pos[node][0], self.pos[node][1],
                                    s=400, color='yellow', alpha=0.5, zorder=5)
                        self.fig.canvas.draw_idle()
                    else:
                        # Second vertex selection - create edge
                        if self.selected_vertex != node:  # Prevent self-loops
                            edge = tuple(sorted([self.selected_vertex, node]))
                            if not self.G.has_edge(*edge):
                                self.G.add_edge(*edge)
                                self.edge_colors[edge] = self.colors[0]
                                self.edge_widths[edge] = 2
                        self.selected_vertex = None
                        self.draw_graph()
                    return   

        # Find the closest edge to the click point
        closest_line = None
        min_distance = float('inf')
        
        for line, (u, v) in self.edge_lines.items():
            # Get line data
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            
            # Calculate distance from point to line segment
            p1 = np.array([xdata[0], ydata[0]])
            p2 = np.array([xdata[1], ydata[1]])
            p3 = np.array([event.xdata, event.ydata])
            
            # Vector calculations for distance
            line_vec = p2 - p1
            point_vec = p3 - p1
            line_len = np.linalg.norm(line_vec)
            line_unitvec = line_vec / line_len
            
            # Projection of point onto line
            point_vec_scaled = point_vec / line_len
            t = np.dot(line_unitvec, point_vec_scaled)
            
            # Clamp t to line segment
            t = max(0, min(1, t))
            
            # Closest point on line segment
            nearest = p1 + t * line_vec
            
            # Distance from point to line segment
            distance = np.linalg.norm(nearest - p3)
            
            if distance < min_distance and distance < 0.1:  # Threshold for considering a click "on" the edge
                min_distance = distance
                closest_line = line
        
        if closest_line:
            u, v = self.edge_lines[closest_line]
            edge = (u, v)
            
             # Shift-click: Remove edge
            if event.button == 1 and event.key == 'shift':
                self.G.remove_edge(u, v)
                if edge in self.edge_colors:
                    del self.edge_colors[edge]
                if edge in self.edge_widths:
                    del self.edge_widths[edge]
            # Left-click: Change color
            elif event.button == 1:
                current_color = self.edge_colors.get(edge, self.colors[0])
                next_index = (self.colors.index(current_color) + 1) % len(self.colors)
                self.edge_colors[edge] = self.colors[next_index]
                
            # Right-click: Toggle bold
            elif event.button == 3:
                current_width = self.edge_widths.get(edge, 2)
                self.edge_widths[edge] = 4 if current_width <= 2 else 2
                
            self.draw_graph()
    
    def on_key_press(self, event):
        if event.key == 'cmd' or event.key == 'control':  # Support both Mac and Windows
            self.cmd_pressed = True
        elif event.key == 'alt' or event.key == 'option':  # Support both Mac and Windows
            self.opt_pressed = True

    def on_key_release(self, event):
        if event.key == 'cmd' or event.key == 'control':  # Support both Mac and Windows
            self.cmd_pressed = False
            # Only clear selection if we're deselecting command
            if self.selected_vertex is not None:
                self.selected_vertex = None
                self.draw_graph()
        elif event.key == 'alt' or event.key == 'option':  # Support both Mac and Windows
            self.opt_pressed = False
            self.dragging_vertex = None

    def on_release(self, event):
        self.dragging_vertex = None

    def on_motion(self, event):
        if event.inaxes != self.ax:
            return
            
        if self.dragging_vertex is not None and self.opt_pressed:
            # Update vertex position
            self.pos[self.dragging_vertex] = (event.xdata, event.ydata)
            self.draw_graph()

    def update_num_vertices(self, val):
        self.num_vertices = int(val)
    
    def generate_new_graph(self, event):
        self.create_graph()
        self.draw_graph()
    
    def clear_graph(self, event):
        self.G.clear()
        self.edge_colors = {}
        self.edge_widths = {}
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