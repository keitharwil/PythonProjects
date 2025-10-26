"""Linked list control panel"""
import tkinter as tk
from tkinter import messagebox, ttk
from config import COLORS, LIST_TYPES

class LinkedListPanel:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.colors = COLORS
        
        # Create frame
        left_frame = tk.Frame(parent, bg=self.colors['mantle'], relief=tk.FLAT)
        left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        left_inner = tk.Frame(left_frame, bg=self.colors['mantle'])
        left_inner.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        self.create_widgets(left_inner)
    
    def create_widgets(self, parent):
        """Create all widgets"""
        tk.Label(parent, text="Linked List Types", bg=self.colors['mantle'], 
                fg=self.colors['mauve'], font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))
        
        # Dropdown for list type
        type_frame = tk.Frame(parent, bg=self.colors['mantle'])
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
                                              values=LIST_TYPES,
                                              state="readonly", width=18, font=("Segoe UI", 9))
        self.list_type_dropdown.pack(side=tk.LEFT)
        self.list_type_dropdown.bind("<<ComboboxSelected>>", self.on_list_type_change)
        
        # Node value entry
        tk.Label(parent, text="Node value:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack(pady=(10, 0))
        
        entry_frame1 = tk.Frame(parent, bg=self.colors['surface0'])
        entry_frame1.pack(pady=5)
        self.node_entry = tk.Entry(entry_frame1, width=28, bg=self.colors['surface0'], 
                                   fg=self.colors['text'], font=("Segoe UI", 10),
                                   relief=tk.FLAT, insertbackground=self.colors['text'])
        self.node_entry.pack(padx=2, pady=2)
        
        # Position entry
        tk.Label(parent, text="Position (optional):", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack()
        
        entry_frame_pos = tk.Frame(parent, bg=self.colors['surface0'])
        entry_frame_pos.pack(pady=5)
        self.position_entry = tk.Entry(entry_frame_pos, width=28, bg=self.colors['surface0'], 
                                      fg=self.colors['text'], font=("Segoe UI", 10),
                                      relief=tk.FLAT, insertbackground=self.colors['text'])
        self.position_entry.pack(padx=2, pady=2)
        
        # Operations container
        self.operations_frame = tk.Frame(parent, bg=self.colors['mantle'])
        self.operations_frame.pack(pady=8, fill=tk.BOTH)
        
        self.update_operations_ui()
    
    def create_button(self, parent, text, color, command, width=12):
        """Create a styled button"""
        btn = tk.Button(parent, text=text, bg=color, fg=self.colors['crust'],
                       font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                       command=command, width=width, cursor="hand2",
                       activebackground=color, activeforeground=self.colors['base'])
        return btn
    
    def on_list_type_change(self, event=None):
        """Handle list type change"""
        list_type = self.list_type_var.get()
        self.main_window.on_list_type_change(list_type)
    
    def update_operations_ui(self):
        """Update the operations buttons based on selected list type"""
        # Clear existing buttons
        for widget in self.operations_frame.winfo_children():
            widget.destroy()
        
        list_type = self.main_window.current_list_type
        
        if list_type == "Singly":
            self.create_singly_operations()
        elif list_type == "Doubly":
            self.create_doubly_operations()
        elif list_type == "Circular Singly":
            self.create_circular_singly_operations()
        elif list_type == "Circular Doubly":
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
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.singly_insert(value, position)
            self.main_window.log(f"✅ {msg}")
            self.node_entry.delete(0, tk.END)
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
    
    def singly_delete(self):
        pos_str = self.position_entry.get()
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.singly_delete(position)
            self.main_window.log(f"✅ {msg}")
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showinfo("Info", str(e))
    
    def singly_traverse(self):
        result = self.main_window.list_manager.singly_traverse()
        if not result:
            self.main_window.log("⚠ List is empty!")
            return
        self.main_window.log("→ Singly Linked List Traverse:")
        for i, value in result:
            self.main_window.log(f"  • Node {i}: {value}")
    
    def singly_clear(self):
        self.main_window.list_manager.singly_clear()
        self.main_window.log("✅ Singly linked list cleared!")
        self.main_window.visualization.set_reverse_mode(False)
        self.main_window.refresh_visualization()
    
    # Doubly Linked List Operations
    def doubly_insert(self):
        value = self.node_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a node value")
            return
        
        pos_str = self.position_entry.get()
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.doubly_insert(value, position)
            self.main_window.log(f"✅ {msg}")
            self.node_entry.delete(0, tk.END)
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
    
    def doubly_delete(self):
        pos_str = self.position_entry.get()
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.doubly_delete(position)
            self.main_window.log(f"✅ {msg}")
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showinfo("Info", str(e))
    
    def doubly_traverse_forward(self):
        result = self.main_window.list_manager.doubly_traverse_forward()
        if not result:
            self.main_window.log("⚠ List is empty!")
            return
        self.main_window.log("→ Doubly Linked List (Forward):")
        for i, value in result:
            self.main_window.log(f"  • Node {i}: {value}")
        self.main_window.visualization.set_reverse_mode(False)
        self.main_window.refresh_visualization()
    
    def doubly_traverse_reverse(self):
        result = self.main_window.list_manager.doubly_traverse_reverse()
        if not result:
            self.main_window.log("⚠ List is empty!")
            return
        self.main_window.log("← Doubly Linked List (Reverse):")
        for i, value in result:
            self.main_window.log(f"  • Node {i}: {value}")
        self.main_window.visualization.set_reverse_mode(True)
        self.main_window.refresh_visualization()
    
    def doubly_clear(self):
        self.main_window.list_manager.doubly_clear()
        self.main_window.log("✅ Doubly linked list cleared!")
        self.main_window.visualization.set_reverse_mode(False)
        self.main_window.refresh_visualization()
    
    # Circular Singly Linked List Operations
    def circular_singly_insert(self):
        value = self.node_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a node value")
            return
        
        pos_str = self.position_entry.get()
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.circular_singly_insert(value, position)
            self.main_window.log(f"✅ {msg}")
            self.node_entry.delete(0, tk.END)
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
    
    def circular_singly_delete(self):
        pos_str = self.position_entry.get()
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.circular_singly_delete(position)
            self.main_window.log(f"✅ {msg}")
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showinfo("Info", str(e))
    
    def circular_singly_traverse(self):
        result = self.main_window.list_manager.circular_singly_traverse()
        if not result:
            self.main_window.log("⚠ List is empty!")
            return
        self.main_window.log("🔄 Circular Singly Linked List (2 complete cycles):")
        for i, value, idx in result:
            self.main_window.log(f"  • Node {i}: {value} (index {idx})")
    
    def circular_singly_clear(self):
        self.main_window.list_manager.circular_singly_clear()
        self.main_window.log("✅ Circular singly linked list cleared!")
        self.main_window.refresh_visualization()
    
    # Circular Doubly Linked List Operations
    def circular_doubly_insert(self):
        value = self.node_entry.get()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a node value")
            return
        
        pos_str = self.position_entry.get()
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.circular_doubly_insert(value, position)
            self.main_window.log(f"✅ {msg}")
            self.node_entry.delete(0, tk.END)
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
    
    def circular_doubly_delete(self):
        pos_str = self.position_entry.get()
        position = None
        if pos_str:
            try:
                position = int(pos_str)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Position must be a number")
                return
        
        try:
            msg = self.main_window.list_manager.circular_doubly_delete(position)
            self.main_window.log(f"✅ {msg}")
            self.position_entry.delete(0, tk.END)
            self.main_window.refresh_visualization()
        except ValueError as e:
            messagebox.showinfo("Info", str(e))
    
    def circular_doubly_traverse_forward(self):
        result = self.main_window.list_manager.circular_doubly_traverse_forward()
        if not result:
            self.main_window.log("⚠ List is empty!")
            return
        self.main_window.log("🔄 Circular Doubly Linked List (Forward, 2 cycles):")
        for i, value in result:
            self.main_window.log(f"  • Node {i}: {value}")
    
    def circular_doubly_traverse_reverse(self):
        result = self.main_window.list_manager.circular_doubly_traverse_reverse()
        if not result:
            self.main_window.log("⚠ List is empty!")
            return
        self.main_window.log("🔄 Circular Doubly Linked List (Reverse, 2 cycles):")
        for i, value in result:
            self.main_window.log(f"  • Node {i}: {value}")
    
    def circular_doubly_clear(self):
        self.main_window.list_manager.circular_doubly_clear()
        self.main_window.log("✅ Circular doubly linked list cleared!")
        self.main_window.refresh_visualization()