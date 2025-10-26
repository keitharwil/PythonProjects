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
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize managers
        self.list_manager = LinkedListManager()
        self.stack_manager = StackManager()
        self.rps_game = RPSGame()
        self.current_list_type = "Singly"
        
        # Main container
        main_container = tk.Frame(root, bg=COLORS['base'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ===== SCROLLABLE LEFT PANEL =====
        # Outer frame for canvas + scrollbar
        left_scroll_container = tk.Frame(main_container, bg=COLORS['base'])
        left_scroll_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Canvas and scrollbar
        self.left_canvas = tk.Canvas(left_scroll_container, bg=COLORS['base'], highlightthickness=0)
        self.left_scrollbar = tk.Scrollbar(left_scroll_container, orient=tk.VERTICAL, command=self.left_canvas.yview)
        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

        # Scrollable frame inside canvas
        self.left_content_frame = tk.Frame(self.left_canvas, bg=COLORS['base'])

        # Bind configure to update scroll region
        self.left_content_frame.bind("<Configure>", self._on_left_frame_configure)
        self.left_canvas.create_window((0, 0), window=self.left_content_frame, anchor="nw")

        # Pack canvas and scrollbar
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel support
        self.left_canvas.bind("<Enter>", self._bind_mousewheel)
        self.left_canvas.bind("<Leave>", self._unbind_mousewheel)

        # Now create panels INSIDE self.left_content_frame (not left_container!)
        self.linked_list_panel = LinkedListPanel(self.left_content_frame, self)
        self.stack_panel = StackPanel(self.left_content_frame, self)
        self.rps_panel = RPSPanel(self.left_content_frame, self)

        # ===== RIGHT SIDE - Visualization and Output =====
        right_container = tk.Frame(main_container, bg=COLORS['base'])
        right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.visualization = VisualizationCanvas(right_container, self)
        self.create_output_section(right_container)

        # Initial draw
        self.refresh_visualization()
        self.log("🎉 Welcome to Enhanced Linked Lists!")
        self.log("📋 Select a list type and start exploring!\n")

    def _on_left_frame_configure(self, event):
        """Update scroll region when content frame changes"""
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

    def _bind_mousewheel(self, event):
        """Enable mouse wheel scrolling when mouse enters canvas"""
        self.left_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        """Disable mouse wheel scrolling when mouse leaves canvas"""
        self.left_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Handle mouse wheel scroll"""
        self.left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # --- Rest of your methods unchanged ---
    def on_closing(self):
        self.exit_splash.show_exit_confirmation()

    def create_output_section(self, parent):
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
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def refresh_visualization(self):
        self.visualization.draw()
        if not self.rps_game.is_active:
            self.log("🔄 Visualization refreshed")

    def on_list_type_change(self, list_type):
        self.current_list_type = list_type
        self.linked_list_panel.update_operations_ui()
        self.refresh_visualization()
        self.log(f"📋 Switched to {list_type} Linked List")
    
    