"""Main window controller"""
import tkinter as tk
from tkinter import scrolledtext
from config import COLORS, WINDOW_TITLE, WINDOW_GEOMETRY
from models import LinkedListManager, StackManager
from utils import RPSGame
from .linked_list_panel import LinkedListPanel
from .stack_panel import StackPanel
from .rps_panel import RPSPanel
from .visualization import VisualizationCanvas
from .exit_splash import ExitSplashScreen

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.configure(bg=COLORS['base'])
        
        # Initialize exit splash screen
        self.exit_splash = ExitSplashScreen(root)
        
        # Override window close button
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize managers
        self.list_manager = LinkedListManager()
        self.stack_manager = StackManager()
        self.rps_game = RPSGame()
        
        self.current_list_type = "Singly"
        
        # Create main container
        main_container = tk.Frame(root, bg=COLORS['base'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # LEFT SIDE - Controls and Inputs
        left_container = tk.Frame(main_container, bg=COLORS['base'])
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Create panels
        self.linked_list_panel = LinkedListPanel(left_container, self)
        self.stack_panel = StackPanel(left_container, self)
        self.rps_panel = RPSPanel(left_container, self)
        
        # RIGHT SIDE - Visualization and Output
        right_container = tk.Frame(main_container, bg=COLORS['base'])
        right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Visualization
        self.visualization = VisualizationCanvas(right_container, self)
        
        # Output section
        self.create_output_section(right_container)
        
        # Initial draw
        self.refresh_visualization()
        
        # Welcome message
        self.log("🎉 Welcome to Enhanced Linked Lists!")
        self.log("📋 Select a list type and start exploring!\n")
    
    def on_closing(self):
        """Handle window close event"""
        self.exit_splash.show_exit_confirmation()
    
    def create_output_section(self, parent):
        """Create the output log section"""
        tk.Label(parent, text="Output / Log", bg=COLORS['base'], 
                fg=COLORS['mauve'], font=("Segoe UI", 11, "bold")).pack(pady=(10, 3))
        
        text_frame = tk.Frame(parent, bg=COLORS['surface0'])
        text_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, height=12, 
                                                     bg=COLORS['crust'], 
                                                     fg=COLORS['text'], 
                                                     font=("Consolas", 9),
                                                     relief=tk.FLAT,
                                                     insertbackground=COLORS['text'])
        self.output_text.pack(fill=tk.BOTH, padx=1, pady=1)
    
    def log(self, message):
        """Log a message to the output"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
    
    def refresh_visualization(self):
        """Refresh the visualization"""
        self.visualization.draw()
        if not self.rps_game.is_active:
            self.log("🔄 Visualization refreshed")
    
    def on_list_type_change(self, list_type):
        """Handle list type change"""
        self.current_list_type = list_type
        self.linked_list_panel.update_operations_ui()
        self.refresh_visualization()
        self.log(f"📋 Switched to {list_type} Linked List")