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
        
        # Push section
        tk.Label(parent, text="Value to push:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack()
        
        entry_frame2 = tk.Frame(parent, bg=self.colors['surface0'])
        entry_frame2.pack(pady=5)
        self.push_entry = tk.Entry(entry_frame2, width=28, bg=self.colors['surface0'], 
                                   fg=self.colors['text'], font=("Segoe UI", 10),
                                   relief=tk.FLAT, insertbackground=self.colors['text'])
        self.push_entry.pack(padx=2, pady=2)
        
        # Stack operations - Row 1: Push, Pop, Size (all same width as Clear)
        stack_frame_row1 = tk.Frame(parent, bg=self.colors['mantle'])
        stack_frame_row1.pack(pady=5)
        
        # Push button
        push_btn = self.create_button(stack_frame_row1, "Push(n)", self.colors['blue'], 
                                     self.push_stack, width=12)
        push_btn.pack(side=tk.LEFT, padx=3)
        
        # Pop button
        pop_btn = self.create_button(stack_frame_row1, "Pop(List)", self.colors['pink'], 
                                    self.pop_stack, width=12)
        pop_btn.pack(side=tk.LEFT, padx=3)
        
        self.create_button(parent, "Size", self.colors['yellow'], 
                          self.get_stack_size, width=26).pack(pady=3)

        clear_btn = self.create_button(parent, "Clear stack(LL)", self.colors['red'], 
                                      self.clear_stack, width=26)
        clear_btn.pack(pady=3)
        
        # Search section
        tk.Label(parent, text="Search value:", bg=self.colors['mantle'], 
                fg=self.colors['text'], font=("Segoe UI", 10)).pack(pady=(10, 0))
        
        search_frame = tk.Frame(parent, bg=self.colors['surface0'])
        search_frame.pack(pady=5)
        self.search_entry = tk.Entry(search_frame, width=28, bg=self.colors['surface0'], 
                                     fg=self.colors['text'], font=("Segoe UI", 10),
                                     relief=tk.FLAT, insertbackground=self.colors['text'])
        self.search_entry.pack(padx=2, pady=2)
        
        search_button_frame = tk.Frame(parent, bg=self.colors['mantle'])
        search_button_frame.pack(pady=5)
        self.create_button(search_button_frame, "Search", self.colors['green'], 
                          self.search_stack).pack(side=tk.LEFT, padx=3)
    
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
    
    def search_stack(self):
        """Search for a value in the stack and show result in popup"""
        value = self.search_entry.get()
        if value:
            try:
                position = self.main_window.stack_manager.search(value)
                if position != -1:
                    result_msg = f"Value '{value}' found at position {position} from top (0-indexed)"
                    title = "Search Found"
                    color = self.colors['green']
                else:
                    result_msg = f"Value '{value}' not found in stack"
                    title = "Search Not Found"
                    color = self.colors['red']
                
                # Create popup window
                self.show_popup(title, result_msg, color)
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a value to search")
    
    def get_stack_size(self):
        """Get and display the size of the stack in a popup"""
        try:
            size = self.main_window.stack_manager.size()
            msg = f"Stack size: {size}"
            title = "Stack Size"
            color = self.colors['yellow']
            
            # Create popup window
            self.show_popup(title, msg, color)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_popup(self, title, message, color):
        """Show a small popup window with the result"""
        popup = tk.Toplevel(self.main_window.root)
        popup.title(title)
        popup.configure(bg=color)
        popup.resizable(False, False)
        
        # Center the popup relative to main window
        popup_width = 300
        popup_height = 120
        main_x = self.main_window.root.winfo_x()
        main_y = self.main_window.root.winfo_y()
        main_width = self.main_window.root.winfo_width()
        main_height = self.main_window.root.winfo_height()
        
        x = main_x + (main_width // 2) - (popup_width // 2)
        y = main_y + (main_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        # Message label
        label = tk.Label(popup, text=message, bg=color, fg=self.colors['crust'], 
                        font=("Segoe UI", 11, "bold"), wraplength=280)
        label.pack(expand=True, pady=20)
        
        # Close button
        close_btn = tk.Button(popup, text="OK", command=popup.destroy,
                             bg=self.colors['base'], fg=self.colors['text'],
                             font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                             cursor="hand2")
        close_btn.pack(pady=(0, 10))
        
        # Make popup modal (blocks interaction with main window)
        popup.transient(self.main_window.root)
        popup.grab_set()
        popup.focus_set()
        
        # Log the result as well
        if "Size" in title:
            self.main_window.log(f"📊 {message}")
        else:
            self.main_window.log(f"🔍 {message}")