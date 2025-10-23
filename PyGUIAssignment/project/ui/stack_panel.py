"""Stack control panel"""
import tkinter as tk
from tkinter import messagebox
from config import COLORS

class StackPanel:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.colors = COLORS
        
        # Create frame
        right_frame = tk.Frame(parent, bg=self.colors['mantle'], relief=tk.FLAT)
        right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        right_inner = tk.Frame(right_frame, bg=self.colors['mantle'])
        right_inner.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        self.create_widgets(right_inner)
    
    def create_widgets(self, parent):
        """Create all widgets"""
        tk.Label(parent, text="Stack (peek/pop head)", 
                bg=self.colors['mantle'], fg=self.colors['mauve'], 
                font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))
        
        tk.Label(parent, text="Value to push:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack()
        
        entry_frame2 = tk.Frame(parent, bg=self.colors['surface0'])
        entry_frame2.pack(pady=5)
        self.push_entry = tk.Entry(entry_frame2, width=28, bg=self.colors['surface0'], 
                                   fg=self.colors['text'], font=("Segoe UI", 10),
                                   relief=tk.FLAT, insertbackground=self.colors['text'])
        self.push_entry.pack(padx=2, pady=2)
        
        # Stack operations
        stack_frame = tk.Frame(parent, bg=self.colors['mantle'])
        stack_frame.pack(pady=8)
        
        self.create_button(stack_frame, "Push(n)", self.colors['blue'], 
                          self.push_stack).pack(side=tk.LEFT, padx=3)
        self.create_button(stack_frame, "Pop(List)", self.colors['pink'], 
                          self.pop_stack).pack(side=tk.LEFT, padx=3)
        
        self.create_button(parent, "Clear stack(LL)", self.colors['red'], 
                          self.clear_stack, width=26).pack(pady=3)
    
    def create_button(self, parent, text, color, command, width=12):
        """Create a styled button"""
        btn = tk.Button(parent, text=text, bg=color, fg=self.colors['crust'],
                       font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                       command=command, width=width, cursor="hand2",
                       activebackground=color, activeforeground=self.colors['base'])
        return btn
    
    def push_stack(self):
        value = self.push_entry.get()
        if value:
            try:
                msg = self.main_window.stack_manager.push(value)
                self.main_window.log(f"✅ {msg}")
                self.push_entry.delete(0, tk.END)
                self.main_window.refresh_visualization()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a value to push")
    
    def pop_stack(self):
        try:
            msg = self.main_window.stack_manager.pop()
            self.main_window.log(f"✅ {msg}")
            self.main_window.refresh_visualization()
        except ValueError as e:
            self.main_window.log(f"⚠ {str(e)}")
            messagebox.showinfo("Info", str(e))
    
    def clear_stack(self):
        self.main_window.stack_manager.clear()
        self.main_window.log("✅ Stack cleared!")
        self.main_window.refresh_visualization()