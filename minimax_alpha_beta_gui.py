import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font

class Node:
    def __init__(self, value=None, is_max_node=True):
        self.value = value
        self.children = []
        self.is_max_node = is_max_node
        self.x = None
        self.y = None
    
    def is_leaf(self):
        return len(self.children) == 0

class MinimaxGUI:
    def __init__(self, master):
        self.master = master
        self.setup_gui_elements()
        self.setup_canvas_interactions()

        self.optimal_path = []
        self.alpha_beta_path = []
        self.tree = None  
        self.leaf_values = [] 

    def setup_gui_elements(self):
        self.master.title("Minimax Tree Visualization")
        self.master.geometry("1000x700")
        self.master.configure(bg="#f0f0f0")

        self.header_font = Font(family="Helvetica", size=40, weight="bold")
        self.body_font = Font(family="Helvetica", size=18)
        self.button_font = Font(family="Helvetica", size=20, weight="bold")

        self.depth_label = tk.Label(self.master, text="Enter Tree Depth :", font=self.header_font, bg="#f0f0f0", fg="#333333")
        self.depth_label.pack(pady=20)
        self.depth_entry = tk.Entry(self.master, font=self.body_font, bd=0, relief="flat", bg="#e0e0e0", fg="#333333")
        self.depth_entry.pack(pady=10, padx=20)

        self.generate_button = tk.Button(self.master, text="Generate Tree", command=self.generate_tree, font=self.button_font,bg="#3498db", fg="white", relief="flat", activebackground="#2980b9", cursor="hand2")
        self.generate_button.pack(pady=20)
        self.alpha_beta_button = tk.Button(self.master, text="Alpha-Beta Pruning", command=self.alpha_beta_pruning, font=self.button_font,bg="#FFA500", fg="white", relief="flat", activebackground="#FF8C00", cursor="hand2")
        self.alpha_beta_button.pack(pady=20)

        self.canvas_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.canvas_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="#ffffff", bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.color_info = tk.Label(self.master, text="Bright Purple : Max Node (Circle)\nElectric Blue : Min Node (Square)\nNeon Green : Leaf Node", font=self.body_font, bg="#f0f0f0", fg="#333333")
        self.color_info.pack(pady=10)

    def setup_canvas_interactions(self):
        self.zoom_scale = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0

        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-2>", self.pan_start)
        self.canvas.bind("<B2-Motion>", self.pan_move)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def generate_tree(self):
        depth = self.get_tree_depth()
        if depth is not None:
            self.get_leaf_values(depth)

    def get_tree_depth(self):
        try:
            depth = int(self.depth_entry.get())
            if depth < 1:
                raise ValueError
            return depth
        except ValueError:
            messagebox.showerror("INPUT ERROR", "PLEASE ENTER A VALID POSITIVE INTEGER FOR DEPTH.")
            return None

    def get_leaf_values(self, depth):
        num_leaves = 2 ** depth
        self.leaf_window = tk.Toplevel(self.master)
        self.leaf_window.title("ENTER LEAF NODES")
        self.leaf_window.geometry("400x600")
        self.leaf_window.configure(bg="#f0f0f0")

        canvas = tk.Canvas(self.leaf_window, bg="#f0f0f0")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.leaf_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        scrollable_frame.bind("<Configure>", self.on_frame_configure)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.leaf_entries = []
        for i in range(num_leaves):
            self.create_leaf_entry(scrollable_frame, i)

        submit_button = tk.Button(scrollable_frame, text="Submit", command=self.collect_leaf_values, font=self.button_font,bg="#FFA500", fg="white", relief="flat", activebackground="#FF8C00", cursor="hand2")
        submit_button.pack(pady=20)
        self.depth = depth

    def create_leaf_entry(self, frame, index):
        label = tk.Label(frame, text="Value for Leaf " + str(index + 1) + ":", font=self.body_font, bg="#f0f0f0", fg="#333333")
        label.pack(pady=10)
        entry = tk.Entry(frame, font=self.body_font, bd=0, relief="flat", bg="#e0e0e0", fg="#333333")
        entry.pack(pady=10, padx=20)
        self.leaf_entries.append(entry)

    def on_frame_configure(self, event):
        event.widget.master.configure(scrollregion=event.widget.master.bbox("all"))

    def collect_leaf_values(self):
        if self.validate_leaf_values():
            self.leaf_window.destroy()
            self.tree = self.build_tree(self.leaf_values, self.depth)
            self.optimal_path = []  
            self.alpha_beta_path = []  
            self.visualize_tree(self.tree, self.depth)
            self.master.after(2500, self.highlight_optimal_path)

    def validate_leaf_values(self):
        try:
            self.leaf_values = []
            for entry in self.leaf_entries:
                self.leaf_values.append(int(entry.get()))
            return True
        except ValueError:
            messagebox.showerror("INPUT ERROR", "PLEASE ENTER A VALID INTEGER FOR ALL LEAF VALUES.")
            return False

    def build_tree(self, leaf_values, depth):
        nodes = self.create_nodes(leaf_values, depth)
        root = nodes[0]
        self.minimax(root, depth, True)
        return root

    def create_nodes(self, values, depth):
        if depth == 0:
            return [Node(value=value, is_max_node=False) for value in values]

        mid = len(values) // 2
        left_nodes = self.create_nodes(values[:mid], depth - 1)
        right_nodes = self.create_nodes(values[mid:], depth - 1)

        parent_node = Node(is_max_node=(depth % 2 == 1))
        parent_node.children = [left_nodes[0], right_nodes[0]]
        return [parent_node] + left_nodes + right_nodes

    def minimax(self, node, depth, is_maximizing):
        if depth == 0 or node.is_leaf():
            return node.value

        if is_maximizing:
            return self.maximize_value(node, depth)
        else:
            return self.minimize_value(node, depth)

    def maximize_value(self, node, depth):
        best_value = -float('inf')
        for child in node.children:
            value = self.minimax(child, depth - 1, False)
            if value > best_value:
                best_value = value
                best_child = child
        node.value = best_value
        self.optimal_path.append((node, best_child))
        return best_value

    def minimize_value(self, node, depth):
        best_value = float('inf')
        for child in node.children:
            value = self.minimax(child, depth - 1, True)
            if value < best_value:
                best_value = value
                best_child = child
        node.value = best_value
        self.optimal_path.append((node, best_child))
        return best_value

    def alpha_beta_pruning(self):
        self.alpha_beta_path = []
        if self.tree:
            self.alpha_beta(self.tree, self.depth, -float('inf'), float('inf'), True)
            self.visualize_alpha_beta_tree(self.tree, self.depth)
        else:
            messagebox.showerror("ERROR", "No tree was generated! Please generate a tree first")

    def alpha_beta(self, node, depth, alpha, beta, is_maximizing):
        if depth == 0 or node.is_leaf():
            return node.value

        if is_maximizing:
            return self.maximize_alpha_beta(node, depth, alpha, beta)
        else:
            return self.minimize_alpha_beta(node, depth, alpha, beta)

    def maximize_alpha_beta(self, node, depth, alpha, beta):
        best_value = -float('inf')
        for child in node.children:
            value = self.alpha_beta(child, depth - 1, alpha, beta, False)
            best_value = max(best_value, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                self.alpha_beta_path.append((node, child, "pruned"))
                break
            self.alpha_beta_path.append((node, child, "kept"))
        node.value = best_value
        return best_value

    def minimize_alpha_beta(self, node, depth, alpha, beta):
        best_value = float('inf')
        for child in node.children:
            value = self.alpha_beta(child, depth - 1, alpha, beta, True)
            best_value = min(best_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                self.alpha_beta_path.append((node, child, "pruned"))
                break
            self.alpha_beta_path.append((node, child, "kept"))
        node.value = best_value
        return best_value

    def visualize_tree(self, root, depth):
        self.canvas.delete("all")
        self.node_positions = {}
        level_nodes = [(root, self.canvas.winfo_width() // 2, 40)]
        vertical_gap = 100
        horizontal_gap = 40

        for d in range(depth + 1):
            next_level = []
            for node, x, y in level_nodes:
                self.draw_node(node, x, y)

                if not node.is_leaf():
                    left_x = x - horizontal_gap * (2 ** (depth - d - 1))
                    right_x = x + horizontal_gap * (2 ** (depth - d - 1))
                    next_level.append((node.children[0], left_x, y + vertical_gap))
                    next_level.append((node.children[1], right_x, y + vertical_gap))
                    self.canvas.create_line(x, y + 20, left_x, y + vertical_gap - 20, fill="#333333")
                    self.canvas.create_line(x, y + 20, right_x, y + vertical_gap - 20, fill="#333333")

            level_nodes = next_level

    def draw_node(self, node, x, y):
        if node.is_leaf():
            color = "#39FF14"
        elif node.is_max_node:
            color = "#800080"
        else:
            color = "#007FFF"

        if node.is_max_node:
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="")
        else:
            self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill=color, outline="")

        self.canvas.create_text(x, y, text=str(node.value), font=self.body_font, fill="#ffffff")
        self.node_positions[(x, y)] = node
        node.x = x
        node.y = y

    def visualize_alpha_beta_tree(self, root, depth):
        self.visualize_tree(root, depth)

        for parent, child, status in self.alpha_beta_path:
            if status == "pruned":
                self.canvas.create_line(parent.x, parent.y, child.x, child.y, fill="red", width=2)
            else:
                self.canvas.create_line(parent.x, parent.y, child.x, child.y, fill="green", width=2)

    def highlight_optimal_path(self):
        self.minimax(self.tree, self.depth, self.tree.is_max_node)
        path_color = "#FF5733"

        for parent, child in self.optimal_path:
            self.canvas.create_line(parent.x, parent.y, child.x, child.y, fill=path_color, width=2)
            self.highlight_node(parent, path_color)
            self.highlight_node(child, path_color)

        path_values = [str(parent.value) for parent, child in self.optimal_path]
        path_values.append(str(self.optimal_path[-1][1].value))
        path_info = " -> ".join(path_values)
        messagebox.showinfo("Optimal Path", "Optimal Path : " + path_info)

    def highlight_node(self, node, color):
        if node.x is not None and node.y is not None:
            if node.is_max_node:
                self.canvas.create_oval(node.x - 20, node.y - 20, node.x + 20, node.y + 20, fill=color, outline="")
            else:
                self.canvas.create_rectangle(node.x - 20, node.y - 20, node.x + 20, node.y + 20, fill=color, outline="")
            self.canvas.create_text(node.x, node.y, text=str(node.value), font=self.body_font, fill="#ffffff")

    def on_canvas_click(self, event):
        closest_node = self.find_closest_node(event.x, event.y)
        if closest_node is not None:
            self.show_node_info(closest_node)

    def find_closest_node(self, click_x, click_y):
        closest_node = None
        min_distance = float('inf')
        for position in self.node_positions:
            x, y = position
            node = self.node_positions[position]
            distance = ((x - click_x) ** 2 + (y - click_y) ** 2) ** 0.5
            if distance < min_distance and distance < 20:
                min_distance = distance
                closest_node = node
        return closest_node

    def show_node_info(self, node):
        node_type = "Max" if node.is_max_node else "Min"
        info = "Value : " + str(node.value) + "\nType : " + node_type
        messagebox.showinfo("Node Information", info)

    def zoom(self, event):
        if event.delta > 0:
            factor = 1.1
        else:
            factor = 1 / 1.1
        self.canvas.scale("all", event.x, event.y, factor, factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def pan_start(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def pan_move(self, event):
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        self.canvas.move("all", dx, dy)
        self.pan_start_x = event.x
        self.pan_start_y = event.y

if __name__ == "__main__":
    root = tk.Tk()
    gui = MinimaxGUI(root)
    root.mainloop()
