import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

class StackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Linked List Operations GUI")
        self.root.geometry("1920x1080")
        
        # Catppuccin Mocha color palette
        self.colors = {
            'base': '#1e1e2e',
            'mantle': '#181825',
            'crust': '#11111b',
            'surface0': '#313244',
            'surface1': '#45475a',
            'surface2': '#585b70',
            'text': '#cdd6f4',
            'subtext': '#a6adc8',
            'lavender': '#b4befe',
            'blue': '#89b4fa',
            'sapphire': '#74c7ec',
            'sky': '#89dceb',
            'teal': '#94e2d5',
            'green': '#a6e3a1',
            'yellow': '#f9e2af',
            'peach': '#fab387',
            'maroon': '#eba0ac',
            'red': '#f38ba8',
            'mauve': '#cba6f7',
            'pink': '#f5c2e7',
            'flamingo': '#f2cdcd',
            'rosewater': '#f5e0dc'
        }
        
        self.root.configure(bg=self.colors['base'])
        
        # Stack data structures
        self.stack_queue = []
        self.linked_list_stack = []
        
        # Create main container
        main_container = tk.Frame(root, bg=self.colors['base'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top section for controls
        top_frame = tk.Frame(main_container, bg=self.colors['base'])
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 15))
        
        # Left side - Stack (queue)
        left_frame = tk.Frame(top_frame, bg=self.colors['mantle'], relief=tk.FLAT)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        left_inner = tk.Frame(left_frame, bg=self.colors['mantle'])
        left_inner.pack(padx=15, pady=15)
        
        tk.Label(left_inner, text="Stack (queue)", bg=self.colors['mantle'], 
                fg=self.colors['mauve'], font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))
        
        tk.Label(left_inner, text="Node value:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack()
        
        entry_frame1 = tk.Frame(left_inner, bg=self.colors['surface0'])
        entry_frame1.pack(pady=5)
        self.node_entry = tk.Entry(entry_frame1, width=28, bg=self.colors['surface0'], 
                                   fg=self.colors['text'], font=("Segoe UI", 10),
                                   relief=tk.FLAT, insertbackground=self.colors['text'])
        self.node_entry.pack(padx=2, pady=2)
        
        # Node operations
        node_frame = tk.Frame(left_inner, bg=self.colors['mantle'])
        node_frame.pack(pady=8)
        
        self.create_button(node_frame, "Append", self.colors['red'], 
                          self.append_node).pack(side=tk.LEFT, padx=3)
        self.create_button(node_frame, "Prepend", self.colors['sapphire'], 
                          self.prepend_node).pack(side=tk.LEFT, padx=3)
        
        self.create_button(left_inner, "Random nodes", self.colors['teal'], 
                          self.random_nodes, width=26).pack(pady=3)
        self.create_button(left_inner, "Recursive traverse", self.colors['green'], 
                          self.recursive_traverse, width=26).pack(pady=3)
        self.create_button(left_inner, "Iterative traverse", self.colors['yellow'], 
                          self.iterative_traverse, width=26).pack(pady=3)
        self.create_button(left_inner, "Recursive reverse", self.colors['peach'], 
                          self.recursive_reverse, width=26).pack(pady=3)
        self.create_button(left_inner, "Clear linked list", self.colors['red'], 
                          self.clear_linked_list, width=26).pack(pady=3)
        
        # Right side - Stack built on LinkedList
        right_frame = tk.Frame(top_frame, bg=self.colors['mantle'], relief=tk.FLAT)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        right_inner = tk.Frame(right_frame, bg=self.colors['mantle'])
        right_inner.pack(padx=15, pady=15)
        
        tk.Label(right_inner, text="Stack (peek/pop head)", 
                bg=self.colors['mantle'], fg=self.colors['mauve'], 
                font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))
        
        tk.Label(right_inner, text="Value to push:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack()
        
        entry_frame2 = tk.Frame(right_inner, bg=self.colors['surface0'])
        entry_frame2.pack(pady=5)
        self.push_entry = tk.Entry(entry_frame2, width=28, bg=self.colors['surface0'], 
                                   fg=self.colors['text'], font=("Segoe UI", 10),
                                   relief=tk.FLAT, insertbackground=self.colors['text'])
        self.push_entry.pack(padx=2, pady=2)
        
        # Stack operations
        stack_frame = tk.Frame(right_inner, bg=self.colors['mantle'])
        stack_frame.pack(pady=8)
        
        self.create_button(stack_frame, "Push(n)", self.colors['blue'], 
                          self.push_stack).pack(side=tk.LEFT, padx=3)
        self.create_button(stack_frame, "Pop(List)", self.colors['pink'], 
                          self.pop_stack).pack(side=tk.LEFT, padx=3)
        
        self.create_button(right_inner, "Clear stack(LL)", self.colors['red'], 
                          self.clear_stack, width=26).pack(pady=3)
        
        # Middle section - Visualization area
        viz_frame = tk.Frame(main_container, bg=self.colors['mantle'], relief=tk.FLAT)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Canvas for drawing linked list
        self.canvas = tk.Canvas(viz_frame, bg=self.colors['mantle'], 
                               highlightthickness=0, highlightbackground=self.colors['surface0'])
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bottom - Refresh and Output
        bottom_frame = tk.Frame(main_container, bg=self.colors['base'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.create_button(bottom_frame, "Refresh visualization", self.colors['lavender'], 
                          self.refresh_visualization, width=80).pack(pady=8)
        
        tk.Label(bottom_frame, text="Output / Log", bg=self.colors['base'], 
                fg=self.colors['mauve'], font=("Segoe UI", 11, "bold")).pack(pady=(5, 3))
        
        text_frame = tk.Frame(bottom_frame, bg=self.colors['surface0'])
        text_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, height=7, 
                                                     bg=self.colors['crust'], 
                                                     fg=self.colors['text'], 
                                                     font=("Consolas", 9),
                                                     relief=tk.FLAT,
                                                     insertbackground=self.colors['text'])
        self.output_text.pack(fill=tk.BOTH, padx=1, pady=1)
        
        # Initial draw
        self.refresh_visualization()
        
    def create_button(self, parent, text, color, command, width=12):
        btn = tk.Button(parent, text=text, bg=color, fg=self.colors['crust'],
                       font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                       command=command, width=width, cursor="hand2",
                       activebackground=color, activeforeground=self.colors['base'])
        return btn
        
    def draw_visualization(self):
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 1000
        if canvas_height <= 1:
            canvas_height = 350
            
        # Draw Stack (queue) - Top half
        y_pos_queue = canvas_height // 4
        self.canvas.create_text(60, 35, text="Stack (queue):", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        if self.stack_queue:
            node_radius = 30
            spacing = 100
            start_x = 80
            
            for i, value in enumerate(self.stack_queue):
                x = start_x + (i * spacing)
                
                # Draw circular shadow
                self.canvas.create_oval(x + 3, y_pos_queue + 3, 
                                       x + node_radius*2 + 3, y_pos_queue + node_radius*2 + 3,
                                       fill=self.colors['crust'], outline="")
                
                # Draw circular node
                self.canvas.create_oval(x, y_pos_queue, 
                                       x + node_radius*2, y_pos_queue + node_radius*2,
                                       fill=self.colors['blue'], outline=self.colors['lavender'], 
                                       width=3)
                self.canvas.create_text(x + node_radius, y_pos_queue + node_radius,
                                       text=str(value), fill=self.colors['crust'], 
                                       font=("Segoe UI", 12, "bold"))
                
                # Draw arrow to next node
                if i < len(self.stack_queue) - 1:
                    arrow_start_x = x + node_radius*2 + 5
                    arrow_end_x = arrow_start_x + (spacing - node_radius*2 - 15)
                    arrow_y = y_pos_queue + node_radius
                    self.canvas.create_line(arrow_start_x, arrow_y,
                                          arrow_end_x, arrow_y,
                                          arrow=tk.LAST, fill=self.colors['sapphire'], 
                                          width=3, smooth=True)
        else:
            self.canvas.create_text(60, y_pos_queue + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
        
        # Draw Stack (LinkedList) - Bottom half
        y_pos_stack = (canvas_height // 4) * 3
        self.canvas.create_text(60, y_pos_stack - 35, 
                               text="Stack (peek/pop head):", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        if self.linked_list_stack:
            node_radius = 30
            spacing = 100
            start_x = 80
            
            for i, value in enumerate(self.linked_list_stack):
                x = start_x + (i * spacing)
                
                # Draw circular shadow
                self.canvas.create_oval(x + 3, y_pos_stack + 3, 
                                       x + node_radius*2 + 3, y_pos_stack + node_radius*2 + 3,
                                       fill=self.colors['crust'], outline="")
                
                # Draw circular node with gradient effect
                color = self.colors['pink'] if i == len(self.linked_list_stack) - 1 else self.colors['mauve']
                self.canvas.create_oval(x, y_pos_stack, 
                                       x + node_radius*2, y_pos_stack + node_radius*2,
                                       fill=color, outline=self.colors['lavender'], 
                                       width=3)
                self.canvas.create_text(x + node_radius, y_pos_stack + node_radius,
                                       text=str(value), fill=self.colors['crust'], 
                                       font=("Segoe UI", 12, "bold"))
                
                # Draw arrow to next node
                if i < len(self.linked_list_stack) - 1:
                    arrow_start_x = x + node_radius*2 + 5
                    arrow_end_x = arrow_start_x + (spacing - node_radius*2 - 15)
                    arrow_y = y_pos_stack + node_radius
                    self.canvas.create_line(arrow_start_x, arrow_y,
                                          arrow_end_x, arrow_y,
                                          arrow=tk.LAST, fill=self.colors['flamingo'], 
                                          width=3, smooth=True)
                
            # Draw "TOP" indicator for stack
            top_x = start_x + ((len(self.linked_list_stack) - 1) * spacing) + node_radius
            self.canvas.create_text(top_x, y_pos_stack - 15, text="TOP ↓", 
                                   fill=self.colors['green'], font=("Segoe UI", 11, "bold"))
        else:
            self.canvas.create_text(60, y_pos_stack + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
        
    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        
    def append_node(self):
        value = self.node_entry.get()
        if value:
            self.stack_queue.append(value)
            self.log(f"✓ Appended node with value: {value}")
            self.node_entry.delete(0, tk.END)
            self.refresh_visualization()
        else:
            messagebox.showwarning("Input Error", "Please enter a node value")
            
    def prepend_node(self):
        value = self.node_entry.get()
        if value:
            self.stack_queue.insert(0, value)
            self.log(f"✓ Prepended node with value: {value}")
            self.node_entry.delete(0, tk.END)
            self.refresh_visualization()
        else:
            messagebox.showwarning("Input Error", "Please enter a node value")
            
    def random_nodes(self):
        values = [str(random.randint(1, 99)) for _ in range(5)]
        self.stack_queue.extend(values)
        self.log("✓ Added random nodes: " + ", ".join(values))
        self.refresh_visualization()
        
    def recursive_traverse(self):
        if not self.stack_queue:
            self.log("⚠ List is empty!")
            return
        self.log("→ Recursive traverse: " + " → ".join(self.stack_queue))
        
    def iterative_traverse(self):
        if not self.stack_queue:
            self.log("⚠ List is empty!")
            return
        self.log("→ Iterative traverse (using stack):")
        for value in self.stack_queue:
            self.log(f"  • Visiting node: {value}")
        
    def recursive_reverse(self):
        if not self.stack_queue:
            self.log("⚠ List is empty!")
            return
        self.stack_queue.reverse()
        self.log("✓ List reversed!")
        self.refresh_visualization()
        
    def clear_linked_list(self):
        self.stack_queue.clear()
        self.log("✓ Linked list cleared!")
        self.refresh_visualization()
        
    def push_stack(self):
        value = self.push_entry.get()
        if value:
            self.linked_list_stack.append(value)
            self.log(f"✓ Pushed node with value: {value}")
            self.push_entry.delete(0, tk.END)
            self.refresh_visualization()
        else:
            messagebox.showwarning("Input Error", "Please enter a value to push")
            
    def pop_stack(self):
        if self.linked_list_stack:
            value = self.linked_list_stack.pop()
            self.log(f"✓ Popped value: {value}")
            self.refresh_visualization()
        else:
            self.log("⚠ Stack is empty!")
            messagebox.showinfo("Info", "Stack is empty!")
            
    def clear_stack(self):
        self.linked_list_stack.clear()
        self.log("✓ Stack cleared!")
        self.refresh_visualization()
        
    def refresh_visualization(self):
        self.draw_visualization()
        self.log("🔄 Visualization refreshed")

if __name__ == "__main__":
    root = tk.Tk()
    app = StackGUI(root)
    root.mainloop()