import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import random

class Node:
    """Node class for doubly linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class StackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 2 - Enhanced Linked Lists")
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
        
        # Linked list data structures
        self.singly_list = []
        self.doubly_head = None
        self.circular_singly_list = []
        self.circular_doubly_head = None
        
        self.current_list_type = "Singly"
        
        # Rock Paper Scissors game state
        self.rps_mode = False
        self.rps_rounds_left = 0
        self.player_score = 0
        self.computer_score = 0
        self.last_player_choice = None
        self.last_computer_choice = None
        
        # Create main container
        main_container = tk.Frame(root, bg=self.colors['base'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # LEFT SIDE - Controls and Inputs
        left_container = tk.Frame(main_container, bg=self.colors['base'])
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Linked List section with dropdown
        left_frame = tk.Frame(left_container, bg=self.colors['mantle'], relief=tk.FLAT)
        left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        left_inner = tk.Frame(left_frame, bg=self.colors['mantle'])
        left_inner.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(left_inner, text="Linked List Types", bg=self.colors['mantle'], 
                fg=self.colors['mauve'], font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))
        
        # Dropdown for list type
        type_frame = tk.Frame(left_inner, bg=self.colors['mantle'])
        type_frame.pack(pady=5)
        
        tk.Label(type_frame, text="Type:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 5))
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', 
                       fieldbackground=self.colors['surface0'],
                       background=self.colors['surface0'],
                       foreground=self.colors['text'],
                       arrowcolor=self.colors['text'])
        
        self.list_type_var = tk.StringVar(value="Singly")
        self.list_type_dropdown = ttk.Combobox(type_frame, textvariable=self.list_type_var,
                                              values=["Singly", "Doubly", "Circular Singly", "Circular Doubly"],
                                              state="readonly", width=18, font=("Segoe UI", 9))
        self.list_type_dropdown.pack(side=tk.LEFT)
        self.list_type_dropdown.bind("<<ComboboxSelected>>", self.on_list_type_change)
        
        tk.Label(left_inner, text="Node value:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack(pady=(10, 0))
        
        entry_frame1 = tk.Frame(left_inner, bg=self.colors['surface0'])
        entry_frame1.pack(pady=5)
        self.node_entry = tk.Entry(entry_frame1, width=28, bg=self.colors['surface0'], 
                                   fg=self.colors['text'], font=("Segoe UI", 10),
                                   relief=tk.FLAT, insertbackground=self.colors['text'])
        self.node_entry.pack(padx=2, pady=2)
        
        # Position entry for insert/delete
        tk.Label(left_inner, text="Position (optional):", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack()
        
        entry_frame_pos = tk.Frame(left_inner, bg=self.colors['surface0'])
        entry_frame_pos.pack(pady=5)
        self.position_entry = tk.Entry(entry_frame_pos, width=28, bg=self.colors['surface0'], 
                                      fg=self.colors['text'], font=("Segoe UI", 10),
                                      relief=tk.FLAT, insertbackground=self.colors['text'])
        self.position_entry.pack(padx=2, pady=2)
        
        # Operations container (will be updated based on list type)
        self.operations_frame = tk.Frame(left_inner, bg=self.colors['mantle'])
        self.operations_frame.pack(pady=8, fill=tk.BOTH)
        
        self.update_operations_ui()
        
        # Stack (LinkedList) section
        right_frame = tk.Frame(left_container, bg=self.colors['mantle'], relief=tk.FLAT)
        right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        
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
        
        # Rock Paper Scissors section
        rps_frame = tk.Frame(left_container, bg=self.colors['mantle'], relief=tk.FLAT)
        rps_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        rps_inner = tk.Frame(rps_frame, bg=self.colors['mantle'])
        rps_inner.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(rps_inner, text="Rock Paper Scissors", 
                bg=self.colors['mantle'], fg=self.colors['mauve'], 
                font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))
        
        # Start game button
        self.create_button(rps_inner, "Start Game (5 Rounds)", self.colors['green'], 
                          self.start_rps_game, width=26).pack(pady=5)
        
        # Score display
        self.score_label = tk.Label(rps_inner, text="Player: 0 | Computer: 0", 
                                   bg=self.colors['mantle'], fg=self.colors['text'], 
                                   font=("Segoe UI", 11, "bold"))
        self.score_label.pack(pady=5)
        
        # RPS buttons frame
        self.rps_buttons_frame = tk.Frame(rps_inner, bg=self.colors['mantle'])
        self.rps_buttons_frame.pack(pady=10)
        
        # Create RPS buttons (initially disabled)
        rps_btn_frame = tk.Frame(self.rps_buttons_frame, bg=self.colors['mantle'])
        rps_btn_frame.pack()
        
        self.rock_btn = self.create_button(rps_btn_frame, "✊ Rock", self.colors['surface1'], 
                                          lambda: self.play_round_recursive("rock"))
        self.rock_btn.pack(side=tk.LEFT, padx=3)
        self.rock_btn.config(state=tk.DISABLED)
        
        self.paper_btn = self.create_button(rps_btn_frame, "✋ Paper", self.colors['surface1'], 
                                           lambda: self.play_round_recursive("paper"))
        self.paper_btn.pack(side=tk.LEFT, padx=3)
        self.paper_btn.config(state=tk.DISABLED)
        
        self.scissors_btn = self.create_button(rps_btn_frame, "✌ Scissors", self.colors['surface1'], 
                                              lambda: self.play_round_recursive("scissors"))
        self.scissors_btn.pack(side=tk.LEFT, padx=3)
        self.scissors_btn.config(state=tk.DISABLED)
        
        # RIGHT SIDE - Visualization and Output
        right_container = tk.Frame(main_container, bg=self.colors['base'])
        right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(right_container, bg=self.colors['mantle'], relief=tk.FLAT)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas for drawing linked list and RPS
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
    
    def on_list_type_change(self, event=None):
        """Handle list type change"""
        self.current_list_type = self.list_type_var.get()
        self.update_operations_ui()
        self.refresh_visualization()
        self.log(f"📋 Switched to {self.current_list_type} Linked List")
    
    def update_operations_ui(self):
        """Update the operations buttons based on selected list type"""
        # Clear existing buttons
        for widget in self.operations_frame.winfo_children():
            widget.destroy()
        
        if self.current_list_type == "Singly":
            self.create_singly_operations()
        elif self.current_list_type == "Doubly":
            self.create_doubly_operations()
        elif self.current_list_type == "Circular Singly":
            self.create_circular_singly_operations()
        elif self.current_list_type == "Circular Doubly":
            self.create_circular_doubly_operations()
    
    def create_singly_operations(self):
        """Create operations for singly linked list"""
        tk.Label(self.operations_frame, text="Operations:", bg=self.colors['mantle'], 
                fg=self.colors['subtext'], font=("Segoe UI", 9, "italic")).pack(pady=(0, 5))
        
        btn_frame1 = tk.Frame(self.operations_frame, bg=self.colors['mantle'])
        btn_frame1.pack(pady=3)
        self.create_button(btn_frame1, "Insert", self.colors['green'], 
                          self.singly_insert).pack(side=tk.LEFT, padx=3)
        self.create_button(btn_frame1, "Delete", self.colors['red'], 
                          self.singly_delete).pack(side=tk.LEFT, padx=3)
        
        self.create_button(self.operations_frame, "Traverse", self.colors['blue'], 
                          self.singly_traverse, width=26).pack(pady=3)
        self.create_button(self.operations_frame, "Clear List", self.colors['maroon'], 
                          self.singly_clear, width=26).pack(pady=3)
    
    def create_doubly_operations(self):
        """Create operations for doubly linked list"""
        tk.Label(self.operations_frame, text="Operations:", bg=self.colors['mantle'], 
                fg=self.colors['subtext'], font=("Segoe UI", 9, "italic")).pack(pady=(0, 5))
        
        btn_frame1 = tk.Frame(self.operations_frame, bg=self.colors['mantle'])
        btn_frame1.pack(pady=3)
        self.create_button(btn_frame1, "Insert", self.colors['green'], 
                          self.doubly_insert).pack(side=tk.LEFT, padx=3)
        self.create_button(btn_frame1, "Delete", self.colors['red'], 
                          self.doubly_delete).pack(side=tk.LEFT, padx=3)
        
        btn_frame2 = tk.Frame(self.operations_frame, bg=self.colors['mantle'])
        btn_frame2.pack(pady=3)
        self.create_button(btn_frame2, "Forward", self.colors['blue'], 
                          self.doubly_traverse_forward).pack(side=tk.LEFT, padx=3)
        self.create_button(btn_frame2, "Reverse", self.colors['sapphire'], 
                          self.doubly_traverse_reverse).pack(side=tk.LEFT, padx=3)
        
        self.create_button(self.operations_frame, "Clear List", self.colors['maroon'], 
                          self.doubly_clear, width=26).pack(pady=3)
    
    def create_circular_singly_operations(self):
        """Create operations for circular singly linked list"""
        tk.Label(self.operations_frame, text="Circular Operations:", bg=self.colors['mantle'], 
                fg=self.colors['subtext'], font=("Segoe UI", 9, "italic")).pack(pady=(0, 5))
        
        btn_frame1 = tk.Frame(self.operations_frame, bg=self.colors['mantle'])
        btn_frame1.pack(pady=3)
        self.create_button(btn_frame1, "Insert", self.colors['green'], 
                          self.circular_singly_insert).pack(side=tk.LEFT, padx=3)
        self.create_button(btn_frame1, "Delete", self.colors['red'], 
                          self.circular_singly_delete).pack(side=tk.LEFT, padx=3)
        
        self.create_button(self.operations_frame, "Traverse (2 cycles)", self.colors['yellow'], 
                          self.circular_singly_traverse, width=26).pack(pady=3)
        self.create_button(self.operations_frame, "Clear List", self.colors['maroon'], 
                          self.circular_singly_clear, width=26).pack(pady=3)
    
    def create_circular_doubly_operations(self):
        """Create operations for circular doubly linked list"""
        tk.Label(self.operations_frame, text="Circular Doubly Operations:", bg=self.colors['mantle'], 
                fg=self.colors['subtext'], font=("Segoe UI", 9, "italic")).pack(pady=(0, 5))
        
        btn_frame1 = tk.Frame(self.operations_frame, bg=self.colors['mantle'])
        btn_frame1.pack(pady=3)
        self.create_button(btn_frame1, "Insert", self.colors['green'], 
                          self.circular_doubly_insert).pack(side=tk.LEFT, padx=3)
        self.create_button(btn_frame1, "Delete", self.colors['red'], 
                          self.circular_doubly_delete).pack(side=tk.LEFT, padx=3)
        
        btn_frame2 = tk.Frame(self.operations_frame, bg=self.colors['mantle'])
        btn_frame2.pack(pady=3)
        self.create_button(btn_frame2, "Forward", self.colors['blue'], 
                          self.circular_doubly_traverse_forward).pack(side=tk.LEFT, padx=3)
        self.create_button(btn_frame2, "Reverse", self.colors['sapphire'], 
                          self.circular_doubly_traverse_reverse).pack(side=tk.LEFT, padx=3)
        
        self.create_button(self.operations_frame, "Clear List", self.colors['maroon'], 
                          self.circular_doubly_clear, width=26).pack(pady=3)
    
    # Singly Linked List Operations
    def singly_insert(self):
        value = self.node_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a node value")
            return
        
        pos_str = self.position_entry.get()
        if pos_str:
            try:
                pos = int(pos_str)
                if pos < 0 or pos > len(self.singly_list):
                    messagebox.showwarning("Invalid Position", f"Position must be between 0 and {len(self.singly_list)}")
                    return
                self.singly_list.insert(pos, value)
                self.log(f"✓ Inserted '{value}' at position {pos}")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        else:
            self.singly_list.append(value)
            self.log(f"✓ Inserted '{value}' at end")
        
        self.node_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.refresh_visualization()
    
    def singly_delete(self):
        pos_str = self.position_entry.get()
        if not pos_str:
            if self.singly_list:
                value = self.singly_list.pop()
                self.log(f"✓ Deleted '{value}' from end")
                self.position_entry.delete(0, tk.END)
                self.refresh_visualization()
            else:
                messagebox.showinfo("Info", "List is empty!")
            return
        
        try:
            pos = int(pos_str)
            if pos < 0 or pos >= len(self.singly_list):
                messagebox.showwarning("Invalid Position", f"Position must be between 0 and {len(self.singly_list)-1}")
                return
            value = self.singly_list.pop(pos)
            self.log(f"✓ Deleted '{value}' from position {pos}")
            self.position_entry.delete(0, tk.END)
            self.refresh_visualization()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Position must be a number")
    
    def singly_traverse(self):
        if not self.singly_list:
            self.log("⚠ List is empty!")
            return
        self.log("→ Singly Linked List Traverse:")
        for i, value in enumerate(self.singly_list):
            self.log(f"  • Node {i}: {value}")
    
    def singly_clear(self):
        self.singly_list.clear()
        self.log("✓ Singly linked list cleared!")
        self.refresh_visualization()
    
    # Doubly Linked List Operations
    def doubly_insert(self):
        value = self.node_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a node value")
            return
        
        new_node = Node(value)
        pos_str = self.position_entry.get()
        
        if not self.doubly_head:
            self.doubly_head = new_node
            self.log(f"✓ Inserted '{value}' as first node")
        elif not pos_str:
            # Insert at end
            current = self.doubly_head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
            self.log(f"✓ Inserted '{value}' at end")
        else:
            try:
                pos = int(pos_str)
                if pos == 0:
                    new_node.next = self.doubly_head
                    self.doubly_head.prev = new_node
                    self.doubly_head = new_node
                    self.log(f"✓ Inserted '{value}' at position 0")
                else:
                    current = self.doubly_head
                    for i in range(pos - 1):
                        if not current:
                            messagebox.showwarning("Invalid Position", "Position out of range")
                            return
                        current = current.next
                    
                    if not current:
                        messagebox.showwarning("Invalid Position", "Position out of range")
                        return
                    
                    new_node.next = current.next
                    new_node.prev = current
                    if current.next:
                        current.next.prev = new_node
                    current.next = new_node
                    self.log(f"✓ Inserted '{value}' at position {pos}")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        self.node_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.refresh_visualization()
    
    def doubly_delete(self):
        if not self.doubly_head:
            messagebox.showinfo("Info", "List is empty!")
            return
        
        pos_str = self.position_entry.get()
        if not pos_str:
            # Delete last node
            if not self.doubly_head.next:
                value = self.doubly_head.data
                self.doubly_head = None
                self.log(f"✓ Deleted '{value}' (last node)")
            else:
                current = self.doubly_head
                while current.next:
                    current = current.next
                value = current.data
                current.prev.next = None
                self.log(f"✓ Deleted '{value}' from end")
        else:
            try:
                pos = int(pos_str)
                if pos == 0:
                    value = self.doubly_head.data
                    self.doubly_head = self.doubly_head.next
                    if self.doubly_head:
                        self.doubly_head.prev = None
                    self.log(f"✓ Deleted '{value}' from position 0")
                else:
                    current = self.doubly_head
                    for i in range(pos):
                        if not current:
                            messagebox.showwarning("Invalid Position", "Position out of range")
                            return
                        current = current.next
                    
                    if not current:
                        messagebox.showwarning("Invalid Position", "Position out of range")
                        return
                    
                    value = current.data
                    if current.prev:
                        current.prev.next = current.next
                    if current.next:
                        current.next.prev = current.prev
                    self.log(f"✓ Deleted '{value}' from position {pos}")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        self.position_entry.delete(0, tk.END)
        self.refresh_visualization()
    
    def doubly_traverse_forward(self):
        if not self.doubly_head:
            self.log("⚠ List is empty!")
            return
        self.log("→ Doubly Linked List (Forward):")
        current = self.doubly_head
        i = 0
        while current:
            self.log(f"  • Node {i}: {current.data}")
            current = current.next
            i += 1
    
    def doubly_traverse_reverse(self):
        if not self.doubly_head:
            self.log("⚠ List is empty!")
            return
        
        # Go to end
        current = self.doubly_head
        while current.next:
            current = current.next
        
        self.log("← Doubly Linked List (Reverse):")
        i = 0
        while current:
            self.log(f"  • Node: {current.data}")
            current = current.prev
            i += 1
    
    def doubly_clear(self):
        self.doubly_head = None
        self.log("✓ Doubly linked list cleared!")
        self.refresh_visualization()
    
    # Circular Singly Linked List Operations
    def circular_singly_insert(self):
        value = self.node_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a node value")
            return
        
        pos_str = self.position_entry.get()
        if pos_str:
            try:
                pos = int(pos_str)
                if pos < 0 or pos > len(self.circular_singly_list):
                    messagebox.showwarning("Invalid Position", f"Position must be between 0 and {len(self.circular_singly_list)}")
                    return
                self.circular_singly_list.insert(pos, value)
                self.log(f"✓ Inserted '{value}' at position {pos} (circular)")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        else:
            self.circular_singly_list.append(value)
            self.log(f"✓ Inserted '{value}' at end (circular)")
        
        self.node_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.refresh_visualization()
    
    def circular_singly_delete(self):
        pos_str = self.position_entry.get()
        if not pos_str:
            if self.circular_singly_list:
                value = self.circular_singly_list.pop()
                self.log(f"✓ Deleted '{value}' from end (circular)")
                self.position_entry.delete(0, tk.END)
                self.refresh_visualization()
            else:
                messagebox.showinfo("Info", "List is empty!")
            return
        
        try:
            pos = int(pos_str)
            if pos < 0 or pos >= len(self.circular_singly_list):
                messagebox.showwarning("Invalid Position", f"Position must be between 0 and {len(self.circular_singly_list)-1}")
                return
            value = self.circular_singly_list.pop(pos)
            self.log(f"✓ Deleted '{value}' from position {pos} (circular)")
            self.position_entry.delete(0, tk.END)
            self.refresh_visualization()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Position must be a number")
    
    def circular_singly_traverse(self):
        if not self.circular_singly_list:
            self.log("⚠ List is empty!")
            return
        self.log("🔄 Circular Singly Linked List (2 complete cycles):")
        list_len = len(self.circular_singly_list)
        for i in range(list_len * 2):
            idx = i % list_len
            self.log(f"  • Node {i}: {self.circular_singly_list[idx]} (index {idx})")
    
    def circular_singly_clear(self):
        self.circular_singly_list.clear()
        self.log("✓ Circular singly linked list cleared!")
        self.refresh_visualization()
    
    # Circular Doubly Linked List Operations
    def circular_doubly_insert(self):
        value = self.node_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a node value")
            return
        
        new_node = Node(value)
        pos_str = self.position_entry.get()
        
        if not self.circular_doubly_head:
            self.circular_doubly_head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.log(f"✓ Inserted '{value}' as first node (circular doubly)")
        elif not pos_str:
            # Insert at end (before head)
            last = self.circular_doubly_head.prev
            new_node.next = self.circular_doubly_head
            new_node.prev = last
            last.next = new_node
            self.circular_doubly_head.prev = new_node
            self.log(f"✓ Inserted '{value}' at end (circular doubly)")
        else:
            try:
                pos = int(pos_str)
                if pos == 0:
                    last = self.circular_doubly_head.prev
                    new_node.next = self.circular_doubly_head
                    new_node.prev = last
                    last.next = new_node
                    self.circular_doubly_head.prev = new_node
                    self.circular_doubly_head = new_node
                    self.log(f"✓ Inserted '{value}' at position 0 (circular doubly)")
                else:
                    current = self.circular_doubly_head
                    for i in range(pos - 1):
                        current = current.next
                        if current == self.circular_doubly_head:
                            messagebox.showwarning("Invalid Position", "Position out of range")
                            return
                    
                    new_node.next = current.next
                    new_node.prev = current
                    current.next.prev = new_node
                    current.next = new_node
                    self.log(f"✓ Inserted '{value}' at position {pos} (circular doubly)")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        self.node_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.refresh_visualization()
    
    def circular_doubly_delete(self):
        if not self.circular_doubly_head:
            messagebox.showinfo("Info", "List is empty!")
            return
        
        pos_str = self.position_entry.get()
        if not pos_str:
            # Delete last node (node before head)
            if self.circular_doubly_head.next == self.circular_doubly_head:
                value = self.circular_doubly_head.data
                self.circular_doubly_head = None
                self.log(f"✓ Deleted '{value}' (last node in circular doubly)")
            else:
                last = self.circular_doubly_head.prev
                value = last.data
                last.prev.next = self.circular_doubly_head
                self.circular_doubly_head.prev = last.prev
                self.log(f"✓ Deleted '{value}' from end (circular doubly)")
        else:
            try:
                pos = int(pos_str)
                if pos == 0:
                    value = self.circular_doubly_head.data
                    if self.circular_doubly_head.next == self.circular_doubly_head:
                        self.circular_doubly_head = None
                    else:
                        last = self.circular_doubly_head.prev
                        self.circular_doubly_head = self.circular_doubly_head.next
                        last.next = self.circular_doubly_head
                        self.circular_doubly_head.prev = last
                    self.log(f"✓ Deleted '{value}' from position 0 (circular doubly)")
                else:
                    current = self.circular_doubly_head
                    for i in range(pos):
                        current = current.next
                        if current == self.circular_doubly_head and i < pos:
                            messagebox.showwarning("Invalid Position", "Position out of range")
                            return
                    
                    value = current.data
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    self.log(f"✓ Deleted '{value}' from position {pos} (circular doubly)")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        self.position_entry.delete(0, tk.END)
        self.refresh_visualization()
    
    def circular_doubly_traverse_forward(self):
        if not self.circular_doubly_head:
            self.log("⚠ List is empty!")
            return
        
        self.log("🔄 Circular Doubly Linked List (Forward, 2 cycles):")
        current = self.circular_doubly_head
        count = 0
        # Count nodes first
        temp = self.circular_doubly_head
        list_len = 1
        temp = temp.next
        while temp != self.circular_doubly_head:
            list_len += 1
            temp = temp.next
        
        # Traverse 2 complete cycles
        for i in range(list_len * 2):
            self.log(f"  • Node {i}: {current.data}")
            current = current.next
    
    def circular_doubly_traverse_reverse(self):
        if not self.circular_doubly_head:
            self.log("⚠ List is empty!")
            return
        
        self.log("🔄 Circular Doubly Linked List (Reverse, 2 cycles):")
        current = self.circular_doubly_head.prev
        
        # Count nodes first
        temp = self.circular_doubly_head
        list_len = 1
        temp = temp.next
        while temp != self.circular_doubly_head:
            list_len += 1
            temp = temp.next
        
        # Traverse 2 complete cycles backward
        for i in range(list_len * 2):
            self.log(f"  • Node {i}: {current.data}")
            current = current.prev
    
    def circular_doubly_clear(self):
        self.circular_doubly_head = None
        self.log("✓ Circular doubly linked list cleared!")
        self.refresh_visualization()
    
    def draw_visualization(self):
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 1000
        if canvas_height <= 1:
            canvas_height = 600
        
        if self.rps_mode:
            # Draw RPS game visualization
            self.draw_rps_game()
        else:
            # Draw linked list based on type
            if self.current_list_type == "Singly":
                self.draw_singly_list(canvas_width, canvas_height)
            elif self.current_list_type == "Doubly":
                self.draw_doubly_list(canvas_width, canvas_height)
            elif self.current_list_type == "Circular Singly":
                self.draw_circular_singly_list(canvas_width, canvas_height)
            elif self.current_list_type == "Circular Doubly":
                self.draw_circular_doubly_list(canvas_width, canvas_height)
            
            # Draw stack at bottom
            self.draw_stack_bottom(canvas_width, canvas_height)
    
    def draw_singly_list(self, canvas_width, canvas_height):
        """Draw singly linked list"""
        y_pos = canvas_height // 4
        self.canvas.create_text(60, 35, text="Singly Linked List:", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        if self.singly_list:
            node_width = 60
            node_height = 50
            spacing = 100
            start_x = 80
            
            for i, value in enumerate(self.singly_list):
                x = start_x + (i * spacing)
                
                # Draw shadow
                self.canvas.create_rectangle(x + 3, y_pos + 3, 
                                            x + node_width + 3, y_pos + node_height + 3,
                                            fill=self.colors['crust'], outline="")
                
                # Draw node
                self.canvas.create_rectangle(x, y_pos, 
                                            x + node_width, y_pos + node_height,
                                            fill=self.colors['blue'], outline=self.colors['lavender'], 
                                            width=3)
                self.canvas.create_text(x + node_width//2, y_pos + node_height//2,
                                       text=str(value), fill=self.colors['crust'], 
                                       font=("Segoe UI", 12, "bold"))
                
                # Draw arrow to next node
                if i < len(self.singly_list) - 1:
                    arrow_start_x = x + node_width + 5
                    arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                    arrow_y = y_pos + node_height//2
                    self.canvas.create_line(arrow_start_x, arrow_y,
                                          arrow_end_x, arrow_y,
                                          arrow=tk.LAST, fill=self.colors['sapphire'], 
                                          width=3, smooth=True)
                else:
                    # NULL indicator
                    self.canvas.create_text(x + node_width + 30, y_pos + node_height//2,
                                          text="NULL", fill=self.colors['surface2'],
                                          font=("Segoe UI", 10, "italic"))
        else:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
    
    def draw_doubly_list(self, canvas_width, canvas_height):
        """Draw doubly linked list"""
        y_pos = canvas_height // 4
        self.canvas.create_text(60, 35, text="Doubly Linked List:", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        if not self.doubly_head:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
            return
        
        # Convert to list for drawing
        nodes = []
        current = self.doubly_head
        while current:
            nodes.append(current.data)
            current = current.next
        
        node_width = 60
        node_height = 50
        spacing = 120
        start_x = 80
        
        for i, value in enumerate(nodes):
            x = start_x + (i * spacing)
            
            # Draw shadow
            self.canvas.create_rectangle(x + 3, y_pos + 3, 
                                        x + node_width + 3, y_pos + node_height + 3,
                                        fill=self.colors['crust'], outline="")
            
            # Draw node
            self.canvas.create_rectangle(x, y_pos, 
                                        x + node_width, y_pos + node_height,
                                        fill=self.colors['green'], outline=self.colors['lavender'], 
                                        width=3)
            self.canvas.create_text(x + node_width//2, y_pos + node_height//2,
                                   text=str(value), fill=self.colors['crust'], 
                                   font=("Segoe UI", 12, "bold"))
            
            # Draw arrows to next node
            if i < len(nodes) - 1:
                arrow_start_x = x + node_width + 5
                arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                arrow_y_forward = y_pos + node_height//3
                arrow_y_back = y_pos + (node_height * 2)//3
                
                # Forward arrow
                self.canvas.create_line(arrow_start_x, arrow_y_forward,
                                      arrow_end_x, arrow_y_forward,
                                      arrow=tk.LAST, fill=self.colors['blue'], 
                                      width=2, smooth=True)
                
                # Backward arrow
                self.canvas.create_line(arrow_end_x, arrow_y_back,
                                      arrow_start_x, arrow_y_back,
                                      arrow=tk.LAST, fill=self.colors['pink'], 
                                      width=2, smooth=True)
            else:
                # NULL indicators
                self.canvas.create_text(x + node_width + 35, y_pos + node_height//3,
                                      text="NULL", fill=self.colors['surface2'],
                                      font=("Segoe UI", 9, "italic"))
        
        # NULL at beginning
        if nodes:
            self.canvas.create_text(start_x - 35, y_pos + (node_height * 2)//3,
                                  text="NULL", fill=self.colors['surface2'],
                                  font=("Segoe UI", 9, "italic"))
    
    def draw_circular_singly_list(self, canvas_width, canvas_height):
        """Draw circular singly linked list"""
        y_pos = canvas_height // 4
        self.canvas.create_text(60, 35, text="Circular Singly Linked List:", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        if not self.circular_singly_list:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
            return
        
        node_width = 60
        node_height = 50
        spacing = 100
        start_x = 80
        
        for i, value in enumerate(self.circular_singly_list):
            x = start_x + (i * spacing)
            
            # Draw shadow
            self.canvas.create_rectangle(x + 3, y_pos + 3, 
                                        x + node_width + 3, y_pos + node_height + 3,
                                        fill=self.colors['crust'], outline="")
            
            # Draw node
            self.canvas.create_rectangle(x, y_pos, 
                                        x + node_width, y_pos + node_height,
                                        fill=self.colors['yellow'], outline=self.colors['lavender'], 
                                        width=3)
            self.canvas.create_text(x + node_width//2, y_pos + node_height//2,
                                   text=str(value), fill=self.colors['crust'], 
                                   font=("Segoe UI", 12, "bold"))
            
            # Draw arrow to next node
            if i < len(self.circular_singly_list) - 1:
                arrow_start_x = x + node_width + 5
                arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                arrow_y = y_pos + node_height//2
                self.canvas.create_line(arrow_start_x, arrow_y,
                                      arrow_end_x, arrow_y,
                                      arrow=tk.LAST, fill=self.colors['peach'], 
                                      width=3, smooth=True)
        
        # Draw circular arrow from last to first
        if len(self.circular_singly_list) > 1:
            last_x = start_x + ((len(self.circular_singly_list) - 1) * spacing) + node_width
            first_x = start_x
            
            # Draw curved arrow back
            self.canvas.create_arc(first_x, y_pos - 40, last_x, y_pos + 20,
                                  start=45, extent=90, style=tk.ARC,
                                  outline=self.colors['peach'], width=3)
            # Arrow head
            self.canvas.create_line(first_x + 5, y_pos, first_x - 5, y_pos - 10,
                                  arrow=tk.LAST, fill=self.colors['peach'], width=3)
            
            self.canvas.create_text((first_x + last_x)//2, y_pos - 50,
                                  text="🔄 Circular", fill=self.colors['yellow'],
                                  font=("Segoe UI", 10, "bold"))
    
    def draw_circular_doubly_list(self, canvas_width, canvas_height):
        """Draw circular doubly linked list"""
        y_pos = canvas_height // 4
        self.canvas.create_text(60, 35, text="Circular Doubly Linked List:", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        if not self.circular_doubly_head:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
            return
        
        # Convert to list for drawing
        nodes = []
        current = self.circular_doubly_head
        nodes.append(current.data)
        current = current.next
        while current != self.circular_doubly_head:
            nodes.append(current.data)
            current = current.next
        
        node_width = 60
        node_height = 50
        spacing = 120
        start_x = 80
        
        for i, value in enumerate(nodes):
            x = start_x + (i * spacing)
            
            # Draw shadow
            self.canvas.create_rectangle(x + 3, y_pos + 3, 
                                        x + node_width + 3, y_pos + node_height + 3,
                                        fill=self.colors['crust'], outline="")
            
            # Draw node
            self.canvas.create_rectangle(x, y_pos, 
                                        x + node_width, y_pos + node_height,
                                        fill=self.colors['teal'], outline=self.colors['lavender'], 
                                        width=3)
            self.canvas.create_text(x + node_width//2, y_pos + node_height//2,
                                   text=str(value), fill=self.colors['crust'], 
                                   font=("Segoe UI", 12, "bold"))
            
            # Draw arrows to next node
            if i < len(nodes) - 1:
                arrow_start_x = x + node_width + 5
                arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                arrow_y_forward = y_pos + node_height//3
                arrow_y_back = y_pos + (node_height * 2)//3
                
                # Forward arrow
                self.canvas.create_line(arrow_start_x, arrow_y_forward,
                                      arrow_end_x, arrow_y_forward,
                                      arrow=tk.LAST, fill=self.colors['blue'], 
                                      width=2, smooth=True)
                
                # Backward arrow
                self.canvas.create_line(arrow_end_x, arrow_y_back,
                                      arrow_start_x, arrow_y_back,
                                      arrow=tk.LAST, fill=self.colors['pink'], 
                                      width=2, smooth=True)
        
        # Draw circular connections
        if len(nodes) > 1:
            last_x = start_x + ((len(nodes) - 1) * spacing) + node_width
            first_x = start_x
            
            # Forward circular arrow (top)
            self.canvas.create_arc(first_x, y_pos - 50, last_x, y_pos + 10,
                                  start=45, extent=90, style=tk.ARC,
                                  outline=self.colors['blue'], width=2)
            self.canvas.create_line(first_x + 5, y_pos + 5, first_x - 3, y_pos - 5,
                                  arrow=tk.LAST, fill=self.colors['blue'], width=2)
            
            # Backward circular arrow (bottom)
            self.canvas.create_arc(first_x, y_pos + 40, last_x, y_pos + 100,
                                  start=225, extent=90, style=tk.ARC,
                                  outline=self.colors['pink'], width=2)
            self.canvas.create_line(last_x - 5, y_pos + 45, last_x + 3, y_pos + 55,
                                  arrow=tk.LAST, fill=self.colors['pink'], width=2)
            
            self.canvas.create_text((first_x + last_x)//2, y_pos - 60,
                                  text="🔄 Circular Doubly", fill=self.colors['teal'],
                                  font=("Segoe UI", 10, "bold"))
    
    def draw_stack_bottom(self, canvas_width, canvas_height):
        """Draw stack at the bottom of canvas"""
        y_pos = (canvas_height * 3) // 4
        self.canvas.create_text(60, y_pos - 35, 
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
                
                # Draw shadow
                self.canvas.create_rectangle(x + 3, y_pos + 3, 
                                            x + node_width + 3, y_pos + node_height + 3,
                                            fill=self.colors['crust'], outline="")
                
                # Draw node
                color = self.colors['pink'] if i == len(self.linked_list_stack) - 1 else self.colors['mauve']
                self.canvas.create_rectangle(x, y_pos, 
                                            x + node_width, y_pos + node_height,
                                            fill=color, outline=self.colors['lavender'], 
                                            width=3)
                self.canvas.create_text(x + node_width//2, y_pos + node_height//2,
                                       text=str(value), fill=self.colors['crust'], 
                                       font=("Segoe UI", 12, "bold"))
                
                # Draw arrow to next node
                if i < len(self.linked_list_stack) - 1:
                    arrow_start_x = x + node_width + 5
                    arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                    arrow_y = y_pos + node_height//2
                    self.canvas.create_line(arrow_start_x, arrow_y,
                                          arrow_end_x, arrow_y,
                                          arrow=tk.LAST, fill=self.colors['flamingo'], 
                                          width=3, smooth=True)
            
            # Draw "TOP" indicator for stack
            top_x = start_x + ((len(self.linked_list_stack) - 1) * spacing) + node_width//2
            self.canvas.create_text(top_x, y_pos - 15, text="TOP ↑", 
                                   fill=self.colors['green'], font=("Segoe UI", 11, "bold"))
        else:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
    
    def draw_rps_game(self):
        """Draw Rock Paper Scissors game visualization"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 1000
        if canvas_height <= 1:
            canvas_height = 600
        
        self.canvas.config(bg=self.colors['surface0'])
        
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Title
        self.canvas.create_text(center_x, 50, text="Rock Paper Scissors", 
                               fill=self.colors['mauve'], font=("Segoe UI", 24, "bold"))
        
        # Rounds left
        self.canvas.create_text(center_x, 100, 
                               text=f"Rounds Left: {self.rps_rounds_left}", 
                               fill=self.colors['yellow'], font=("Segoe UI", 16, "bold"))
        
        # Score display
        score_y = 150
        
        # Player section
        self.canvas.create_rectangle(center_x - 220, score_y - 20, 
                                    center_x - 80, score_y + 90,
                                    fill=self.colors['surface1'], outline=self.colors['green'], width=3)
        
        self.canvas.create_text(center_x - 150, score_y, text="PLAYER", 
                               fill=self.colors['green'], font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(center_x - 150, score_y + 40, text=str(self.player_score), 
                               fill=self.colors['text'], font=("Segoe UI", 36, "bold"))
        
        self.canvas.create_text(center_x, score_y + 20, text="VS", 
                               fill=self.colors['subtext'], font=("Segoe UI", 20, "bold"))
        
        # Computer section
        self.canvas.create_rectangle(center_x + 80, score_y - 20, 
                                    center_x + 220, score_y + 90,
                                    fill=self.colors['surface1'], outline=self.colors['red'], width=3)
        
        self.canvas.create_text(center_x + 150, score_y, text="COMPUTER", 
                               fill=self.colors['red'], font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(center_x + 150, score_y + 40, text=str(self.computer_score), 
                               fill=self.colors['text'], font=("Segoe UI", 36, "bold"))
        
        # Show last choices
        if self.last_player_choice and self.last_computer_choice:
            choice_y = center_y + 20
            
            # Player choice
            self.canvas.create_rectangle(center_x - 220, choice_y - 60, 
                                        center_x - 80, choice_y + 100,
                                        fill=self.colors['crust'], outline=self.colors['green'], width=4)
            
            player_emoji = self.get_choice_emoji(self.last_player_choice)
            self.canvas.create_text(center_x - 150, choice_y, text=player_emoji, 
                                   fill=self.colors['yellow'], font=("Segoe UI", 72))
            self.canvas.create_text(center_x - 150, choice_y + 80, text=self.last_player_choice.upper(), 
                                   fill=self.colors['green'], font=("Segoe UI", 14, "bold"))
            
            # Computer choice
            self.canvas.create_rectangle(center_x + 80, choice_y - 60, 
                                        center_x + 220, choice_y + 100,
                                        fill=self.colors['crust'], outline=self.colors['red'], width=4)
            
            computer_emoji = self.get_choice_emoji(self.last_computer_choice)
            self.canvas.create_text(center_x + 150, choice_y, text=computer_emoji, 
                                   fill=self.colors['yellow'], font=("Segoe UI", 72))
            self.canvas.create_text(center_x + 150, choice_y + 80, text=self.last_computer_choice.upper(), 
                                   fill=self.colors['red'], font=("Segoe UI", 14, "bold"))
        
        # Instructions
        self.canvas.create_text(center_x, canvas_height - 50, 
                               text="Choose Rock, Paper, or Scissors!", 
                               fill=self.colors['lavender'], font=("Segoe UI", 14, "italic"))
    
    def get_choice_emoji(self, choice):
        """Return emoji for each choice"""
        emojis = {
            'rock': '✊',
            'paper': '✋',
            'scissors': '✌'
        }
        return emojis.get(choice, '❓')
    
    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
    
    # Stack operations
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
    
    # Rock Paper Scissors functions
    def start_rps_game(self):
        """Initialize and start the RPS game"""
        self.rps_mode = True
        self.rps_rounds_left = 5
        self.player_score = 0
        self.computer_score = 0
        self.last_player_choice = None
        self.last_computer_choice = None
        
        # Enable RPS buttons
        self.rock_btn.config(state=tk.NORMAL, bg=self.colors['blue'])
        self.paper_btn.config(state=tk.NORMAL, bg=self.colors['green'])
        self.scissors_btn.config(state=tk.NORMAL, bg=self.colors['yellow'])
        
        self.update_score_display()
        self.log("🎮 Rock Paper Scissors game started! 5 rounds to go.")
        self.refresh_visualization()
    
    def play_round_recursive(self, player_choice):
        """Recursive function to play each round"""
        # Base case: no rounds left
        if self.rps_rounds_left <= 0:
            self.end_game()
            return
        
        # Recursive case: play one round
        computer_choice = random.choice(['rock', 'paper', 'scissors'])
        result = self.determine_winner(player_choice, computer_choice)
        
        # Store last choices for visualization
        self.last_player_choice = player_choice
        self.last_computer_choice = computer_choice
        
        # Update scores
        if result == 'win':
            self.player_score += 1
        elif result == 'lose':
            self.computer_score += 1
        
        # Log the round
        self.log(f"Round {6 - self.rps_rounds_left}: You chose {player_choice.upper()}, Computer chose {computer_choice.upper()} - {result.upper()}!")
        
        # Decrement rounds
        self.rps_rounds_left -= 1
        
        # Update display
        self.update_score_display()
        self.refresh_visualization()
        
        # Check if game should end (recursive termination check)
        if self.rps_rounds_left <= 0:
            # Schedule game end to allow UI to update
            self.root.after(500, self.end_game)
    
    def determine_winner(self, player, computer):
        """Determine the winner of a round"""
        if player == computer:
            return 'tie'
        
        win_conditions = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
        
        if win_conditions[player] == computer:
            return 'win'
        else:
            return 'lose'
    
    def end_game(self):
        """End the game and return to menu"""
        # Disable RPS buttons
        self.rock_btn.config(state=tk.DISABLED, bg=self.colors['surface1'])
        self.paper_btn.config(state=tk.DISABLED, bg=self.colors['surface1'])
        self.scissors_btn.config(state=tk.DISABLED, bg=self.colors['surface1'])
        
        # Determine overall winner
        if self.player_score > self.computer_score:
            result = "🎉 YOU WIN THE GAME!"
            color = self.colors['green']
        elif self.player_score < self.computer_score:
            result = "💔 COMPUTER WINS THE GAME!"
            color = self.colors['red']
        else:
            result = "🤝 IT'S A TIE!"
            color = self.colors['yellow']
        
        self.log(f"\n{result}")
        self.log(f"Final Score - Player: {self.player_score} | Computer: {self.computer_score}\n")
        
        # Show result dialog
        messagebox.showinfo("Game Over", f"{result}\n\nFinal Score:\nPlayer: {self.player_score}\nComputer: {self.computer_score}")
        
        # Reset choices
        self.last_player_choice = None
        self.last_computer_choice = None
        
        # Return to normal mode
        self.rps_mode = False
        self.refresh_visualization()
    
    def update_score_display(self):
        """Update the score label"""
        self.score_label.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")
    
    def refresh_visualization(self):
        self.draw_visualization()
        if not self.rps_mode:
            self.log("🔄 Visualization refreshed")

if __name__ == "__main__":
    root = tk.Tk()
    app = StackGUI(root)
    root.mainloop()