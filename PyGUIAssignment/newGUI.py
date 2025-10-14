import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

class StackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BULLSHIT")
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
        
        # LEFT SIDE - Controls and Inputs
        left_container = tk.Frame(main_container, bg=self.colors['base'])
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Stack (queue) section
        left_frame = tk.Frame(left_container, bg=self.colors['mantle'], relief=tk.FLAT)
        left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        left_inner = tk.Frame(left_frame, bg=self.colors['mantle'])
        left_inner.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
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
        
        # Stack (LinkedList) section
        right_frame = tk.Frame(left_container, bg=self.colors['mantle'], relief=tk.FLAT)
        right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        right_inner = tk.Frame(right_frame, bg=self.colors['mantle'])
        right_inner.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
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
        
        # RIGHT SIDE - Visualization and Output
        right_container = tk.Frame(main_container, bg=self.colors['base'])
        right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(right_container, bg=self.colors['mantle'], relief=tk.FLAT)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas for drawing linked list
        self.canvas = tk.Canvas(viz_frame, bg=self.colors['mantle'], 
                               highlightthickness=0, highlightbackground=self.colors['surface0'])
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        self.create_button(right_container, "Refresh visualization", self.colors['lavender'], 
                          self.refresh_visualization, width=60).pack(pady=5)
        
        # Output section
        tk.Label(right_container, text="Output / Log", bg=self.colors['base'], 
                fg=self.colors['mauve'], font=("Segoe UI", 11, "bold")).pack(pady=(10, 3))
        
        text_frame = tk.Frame(right_container, bg=self.colors['surface0'])
        text_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, height=12, 
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
            node_width = 60
            node_height = 50
            spacing = 100
            start_x = 80
            
            for i, value in enumerate(self.stack_queue):
                x = start_x + (i * spacing)
                
                # Draw rectangular shadow
                self.canvas.create_rectangle(x + 3, y_pos_queue + 3, 
                                            x + node_width + 3, y_pos_queue + node_height + 3,
                                            fill=self.colors['crust'], outline="")
                
                # Draw rectangular node
                self.canvas.create_rectangle(x, y_pos_queue, 
                                            x + node_width, y_pos_queue + node_height,
                                            fill=self.colors['blue'], outline=self.colors['lavender'], 
                                            width=3)
                self.canvas.create_text(x + node_width//2, y_pos_queue + node_height//2,
                                       text=str(value), fill=self.colors['crust'], 
                                       font=("Segoe UI", 12, "bold"))
                
                # Draw arrow to next node
                if i < len(self.stack_queue) - 1:
                    arrow_start_x = x + node_width + 5
                    arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                    arrow_y = y_pos_queue + node_height//2
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
            node_width = 60
            node_height = 50
            spacing = 100
            start_x = 80
            
            for i, value in enumerate(self.linked_list_stack):
                x = start_x + (i * spacing)
                
                # Draw rectangular shadow
                self.canvas.create_rectangle(x + 3, y_pos_stack + 3, 
                                            x + node_width + 3, y_pos_stack + node_height + 3,
                                            fill=self.colors['crust'], outline="")
                
                # Draw rectangular node
                color = self.colors['pink'] if i == len(self.linked_list_stack) - 1 else self.colors['mauve']
                self.canvas.create_rectangle(x, y_pos_stack, 
                                            x + node_width, y_pos_stack + node_height,
                                            fill=color, outline=self.colors['lavender'], 
                                            width=3)
                self.canvas.create_text(x + node_width//2, y_pos_stack + node_height//2,
                                       text=str(value), fill=self.colors['crust'], 
                                       font=("Segoe UI", 12, "bold"))
                
                # Draw arrow to next node
                if i < len(self.linked_list_stack) - 1:
                    arrow_start_x = x + node_width + 5
                    arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                    arrow_y = y_pos_stack + node_height//2
                    self.canvas.create_line(arrow_start_x, arrow_y,
                                          arrow_end_x, arrow_y,
                                          arrow=tk.LAST, fill=self.colors['flamingo'], 
                                          width=3, smooth=True)
                
            # Draw "TOP" indicator for stack
            top_x = start_x + ((len(self.linked_list_stack) - 1) * spacing) + node_width//2
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
        
    def _recursive_traverse_helper(self, lst, index=0):
        """Actual recursive traversal helper"""
        if index >= len(lst):
            return
        self.log(f"  • Visiting node: {lst[index]}")
        self._recursive_traverse_helper(lst, index + 1)
    
    def recursive_traverse(self):
        if not self.stack_queue:
            self.log("⚠ List is empty!")
            return
        self.log("→ Recursive traverse:")
        self._recursive_traverse_helper(self.stack_queue)
        
    def iterative_traverse(self):
        if not self.stack_queue:
            self.log("⚠ List is empty!")
            return
        self.log("→ Iterative traverse (using stack):")
        for value in self.stack_queue:
            self.log(f"  • Visiting node: {value}")
    
    def _recursive_reverse_helper(self, lst):
        """Actual recursive reverse helper"""
        if len(lst) <= 1:
            return lst
        # Remove first element and reverse the rest
        first = lst[0]
        rest = self._recursive_reverse_helper(lst[1:])
        # Append first element to the end
        return rest + [first]
        
    def recursive_reverse(self):
        if not self.stack_queue:
            self.log("⚠ List is empty!")
            return
        self.stack_queue = self._recursive_reverse_helper(self.stack_queue)
        self.log("✓ List reversed recursively!")
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