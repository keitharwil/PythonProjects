"""Visualization canvas for drawing linked lists and RPS game"""
import tkinter as tk
from config import COLORS

class VisualizationCanvas:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.colors = COLORS
        self.reverse_mode = False
        
        # Visualization area
        viz_frame = tk.Frame(parent, bg=self.colors['mantle'], relief=tk.FLAT)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas for drawing linked list and RPS
        self.canvas = tk.Canvas(viz_frame, bg=self.colors['mantle'], 
                               highlightthickness=0, highlightbackground=self.colors['surface0'])
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        self.create_button(parent, "Refresh visualization", self.colors['lavender'], 
                          self.main_window.refresh_visualization, width=60).pack(pady=5)
    
    def create_button(self, parent, text, color, command, width=12):
        """Create a styled button"""
        btn = tk.Button(parent, text=text, bg=color, fg=self.colors['crust'],
                       font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                       command=command, width=width, cursor="hand2",
                       activebackground=color, activeforeground=self.colors['base'])
        return btn
    
    def set_reverse_mode(self, is_reverse):
        """Set reverse visualization mode"""
        self.reverse_mode = is_reverse
    
    def draw(self):
        """Main draw method"""
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 1000
        if canvas_height <= 1:
            canvas_height = 600
        
        if self.main_window.rps_game.is_active:
            # Draw RPS game visualization
            self.draw_rps_game(canvas_width, canvas_height)
        else:
            # Draw linked list based on type
            list_type = self.main_window.current_list_type
            if list_type == "Singly":
                self.draw_singly_list(canvas_width, canvas_height)
            elif list_type == "Doubly":
                self.draw_doubly_list(canvas_width, canvas_height)
            elif list_type == "Circular Singly":
                self.draw_circular_singly_list(canvas_width, canvas_height)
            elif list_type == "Circular Doubly":
                self.draw_circular_doubly_list(canvas_width, canvas_height)
            
            # Draw stack at bottom
            self.draw_stack_bottom(canvas_width, canvas_height)
    
    def draw_curved_arrow(self, x1, y1, x2, y2, color, direction="forward"):
        """Draw a curved arrow between two points"""
        # Calculate control point for curve
        mid_x = (x1 + x2) / 2
        if direction == "forward":
            control_y = min(y1, y2) - 20
        else:
            control_y = max(y1, y2) + 20
        
        # Create smooth curve
        self.canvas.create_line(x1, y1, mid_x, control_y, x2, y2,
                               arrow=tk.LAST, fill=color, width=3, smooth=True)
    
    def draw_singly_list(self, canvas_width, canvas_height):
        """Draw singly linked list"""
        y_pos = canvas_height // 4
        self.canvas.create_text(60, 35, text="Singly Linked List:", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        singly_list = self.main_window.list_manager.get_singly_list()
        
        if singly_list:
            node_width = 60
            node_height = 50
            spacing = 100
            start_x = 80
            
            for i, value in enumerate(singly_list):
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
                
                # Draw curved arrow to next node
                if i < len(singly_list) - 1:
                    arrow_start_x = x + node_width + 5
                    arrow_end_x = x + spacing - 5
                    arrow_y = y_pos + node_height//2
                    self.draw_curved_arrow(arrow_start_x, arrow_y, arrow_end_x, arrow_y, 
                                          self.colors['sapphire'], "forward")
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
        title = "Doubly Linked List (Reversed)" if self.reverse_mode else "Doubly Linked List:"
        self.canvas.create_text(60, 35, text=title, 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        nodes = self.main_window.list_manager.get_doubly_list()
        
        # Reverse the visualization if in reverse mode
        if self.reverse_mode:
            nodes = list(reversed(nodes))
        
        if not nodes:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
            return
        
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
            
            # Draw curved arrows to next node
            if i < len(nodes) - 1:
                arrow_start_x = x + node_width + 5
                arrow_end_x = x + spacing - 5
                arrow_y_forward = y_pos + node_height//2
                
                # Forward arrow (top curve)
                self.draw_curved_arrow(arrow_start_x, arrow_y_forward, arrow_end_x, arrow_y_forward,
                                      self.colors['blue'], "forward")
                
                # Backward arrow (bottom curve)
                self.draw_curved_arrow(arrow_end_x, arrow_y_forward, arrow_start_x, arrow_y_forward,
                                      self.colors['pink'], "backward")
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
        """Draw circular singly linked list with circular arrow"""
        y_pos = canvas_height // 4
        self.canvas.create_text(60, 35, text="Circular Singly Linked List:", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        circular_list = self.main_window.list_manager.get_circular_singly_list()
        
        if not circular_list:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
            return
        
        node_width = 60
        node_height = 50
        spacing = 100
        start_x = 80
        
        for i, value in enumerate(circular_list):
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
            
            # Draw curved arrow to next node
            if i < len(circular_list) - 1:
                arrow_start_x = x + node_width + 5
                arrow_end_x = x + spacing - 5
                arrow_y = y_pos + node_height//2
                self.draw_curved_arrow(arrow_start_x, arrow_y, arrow_end_x, arrow_y,
                                      self.colors['peach'], "forward")
        
        # Draw circular arrow from last node back to first node
        if len(circular_list) > 0:
            last_x = start_x + ((len(circular_list) - 1) * spacing) + node_width
            first_x = start_x
            last_node_center_y = y_pos + node_height // 2
            first_node_center_y = y_pos + node_height // 8
            
            # Starting point: right side of last node
            arrow_start_x = last_x
            arrow_start_y = last_node_center_y
            
            # Ending point: left side of first node
            arrow_end_x = first_x
            arrow_end_y = first_node_center_y
            
            # Create curved path going up and around
            # Calculate control points for smooth curve
            mid_x = (arrow_start_x + arrow_end_x) / 2
            control_y = y_pos - 60  # Height of the arc above nodes
            
            # Draw the curved arrow using smooth bezier curve with arrow
            self.canvas.create_line(
                arrow_start_x, arrow_start_y,
                arrow_start_x + 30, control_y,
                mid_x, control_y - 20,
                arrow_end_x - 30, control_y,
                arrow_end_x, arrow_end_y,
                smooth=True, fill=self.colors['peach'], width=3, arrow=tk.LAST
            )
            
            # Label at the top
            self.canvas.create_text(mid_x, control_y - 35,
                                  text="🔄 Circular", fill=self.colors['yellow'],
                                  font=("Segoe UI", 11, "bold"))
    
    # Replace the draw_circular_doubly_list method in visualization.py with this:

    def draw_circular_doubly_list(self, canvas_width, canvas_height):
        """Draw circular doubly linked list"""
        y_pos = canvas_height // 4
        title = "Circular Doubly Linked List (Reversed)" if self.reverse_mode else "Circular Doubly Linked List:"
        self.canvas.create_text(60, 35, text=title, 
                            fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                            anchor="w")
        
        nodes = self.main_window.list_manager.get_circular_doubly_list()
        
        # Reverse the visualization if in reverse mode
        if self.reverse_mode:
            nodes = list(reversed(nodes))
        
        if not nodes:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                fill=self.colors['surface2'], 
                                font=("Segoe UI", 12, "italic"), anchor="w")
            return
        
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
            
            # Draw curved arrows to next node
            if i < len(nodes) - 1:
                arrow_start_x = x + node_width + 5
                arrow_end_x = x + spacing - 5
                arrow_y = y_pos + node_height//2
                
                # Forward arrow (top curve)
                self.draw_curved_arrow(arrow_start_x, arrow_y, arrow_end_x, arrow_y,
                                    self.colors['blue'], "forward")
                
                # Backward arrow (bottom curve)
                self.draw_curved_arrow(arrow_end_x, arrow_y, arrow_start_x, arrow_y,
                                    self.colors['pink'], "backward")
        
        # Draw circular connections with proper arrows
        if len(nodes) > 1:
            last_x = start_x + ((len(nodes) - 1) * spacing) + node_width
            first_x = start_x
            
            # Forward circular arrow (top) - from last node to first node
            arrow_start_x = last_x
            arrow_start_y = y_pos + node_height // 3
            arrow_end_x = first_x
            arrow_end_y = y_pos + node_height // 9
            
            mid_x = (arrow_start_x + arrow_end_x) / 2
            control_y = y_pos - 40
            
            self.canvas.create_line(
                arrow_start_x, arrow_start_y,
                arrow_start_x + 30, control_y,
                mid_x, control_y - 10,
                arrow_end_x - 30, control_y,
                arrow_end_x, arrow_end_y,
                smooth=True, fill=self.colors['blue'], width=4, arrow=tk.LAST
            )
            
            # Backward circular arrow (bottom) - from first node to last node
            arrow_start_x2 = first_x
            arrow_start_y2 = y_pos + (node_height * 1) // 2
            arrow_end_x2 = last_x
            arrow_end_y2 = y_pos + (node_height * 1) // 1
            
            control_y2 = y_pos + node_height + 40
            
            self.canvas.create_line(
                arrow_start_x2, arrow_start_y2,
                arrow_start_x2 - 30, control_y2,
                mid_x, control_y2 + 10,
                arrow_end_x2 + 30, control_y2,
                arrow_end_x2, arrow_end_y2,
                smooth=True, fill=self.colors['pink'], width=3, arrow=tk.LAST
            )
            
            self.canvas.create_text(mid_x, control_y - 25,
                                text="🔄 Circular Doubly", fill=self.colors['teal'],
                                font=("Segoe UI", 10, "bold"))
    
    def draw_stack_bottom(self, canvas_width, canvas_height):
        """Draw stack at the bottom of canvas"""
        y_pos = (canvas_height * 3) // 4
        self.canvas.create_text(60, y_pos - 35, 
                               text="Stack (peek/pop head):", 
                               fill=self.colors['mauve'], font=("Segoe UI", 12, "bold"), 
                               anchor="w")
        
        stack = self.main_window.stack_manager.get_stack()
        
        if stack:
            node_width = 60
            node_height = 50
            spacing = 100
            start_x = 80
            
            for i, value in enumerate(stack):
                x = start_x + (i * spacing)
                
                # Draw shadow
                self.canvas.create_rectangle(x + 3, y_pos + 3, 
                                            x + node_width + 3, y_pos + node_height + 3,
                                            fill=self.colors['crust'], outline="")
                
                # Draw node
                color = self.colors['pink'] if i == len(stack) - 1 else self.colors['mauve']
                self.canvas.create_rectangle(x, y_pos, 
                                            x + node_width, y_pos + node_height,
                                            fill=color, outline=self.colors['lavender'], 
                                            width=3)
                self.canvas.create_text(x + node_width//2, y_pos + node_height//2,
                                       text=str(value), fill=self.colors['crust'], 
                                       font=("Segoe UI", 12, "bold"))
                
                # Draw curved arrow to next node
                if i < len(stack) - 1:
                    arrow_start_x = x + node_width + 5
                    arrow_end_x = x + spacing - 1
                    arrow_y = y_pos + node_height//2
                    self.draw_curved_arrow(arrow_start_x, arrow_y, arrow_end_x, arrow_y,
                                          self.colors['flamingo'], "forward")
            
            # Draw "TOP" indicator for stack
            top_x = start_x + ((len(stack) - 1) * spacing) + node_width//2
            self.canvas.create_text(top_x, y_pos - 15, text="TOP ↑", 
                                   fill=self.colors['green'], font=("Segoe UI", 11, "bold"))
        else:
            self.canvas.create_text(60, y_pos + 30, text="Empty", 
                                   fill=self.colors['surface2'], 
                                   font=("Segoe UI", 12, "italic"), anchor="w")
    
    def draw_rps_game(self, canvas_width, canvas_height):
        """Draw Rock Paper Scissors game visualization"""
        self.canvas.config(bg=self.colors['surface0'])
        
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Title
        self.canvas.create_text(center_x, 50, text="Rock Paper Scissors", 
                               fill=self.colors['mauve'], font=("Segoe UI", 24, "bold"))
        
        # Rounds left
        self.canvas.create_text(center_x, 100, 
                               text=f"Rounds Left: {self.main_window.rps_game.rounds_left}", 
                               fill=self.colors['yellow'], font=("Segoe UI", 16, "bold"))
        
        # Score display
        score_y = 150
        
        # Player section
        self.canvas.create_rectangle(center_x - 220, score_y - 20, 
                                    center_x - 80, score_y + 90,
                                    fill=self.colors['surface1'], outline=self.colors['green'], width=3)
        
        self.canvas.create_text(center_x - 150, score_y, text="PLAYER", 
                               fill=self.colors['green'], font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(center_x - 150, score_y + 40, 
                               text=str(self.main_window.rps_game.player_score), 
                               fill=self.colors['text'], font=("Segoe UI", 36, "bold"))
        
        self.canvas.create_text(center_x, score_y + 20, text="VS", 
                               fill=self.colors['subtext'], font=("Segoe UI", 20, "bold"))
        
        # Computer section
        self.canvas.create_rectangle(center_x + 80, score_y - 20, 
                                    center_x + 220, score_y + 90,
                                    fill=self.colors['surface1'], outline=self.colors['red'], width=3)
        
        self.canvas.create_text(center_x + 150, score_y, text="COMPUTER", 
                               fill=self.colors['red'], font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(center_x + 150, score_y + 40, 
                               text=str(self.main_window.rps_game.computer_score), 
                               fill=self.colors['text'], font=("Segoe UI", 36, "bold"))
        
        # Show last choices
        if (self.main_window.rps_game.last_player_choice and 
            self.main_window.rps_game.last_computer_choice):
            choice_y = center_y + 20
            
            # Player choice
            self.canvas.create_rectangle(center_x - 220, choice_y - 60, 
                                        center_x - 80, choice_y + 100,
                                        fill=self.colors['crust'], outline=self.colors['green'], width=4)
            
            player_emoji = self.main_window.rps_game.get_choice_emoji(
                self.main_window.rps_game.last_player_choice)
            self.canvas.create_text(center_x - 150, choice_y, text=player_emoji, 
                                   fill=self.colors['yellow'], font=("Segoe UI", 72))
            self.canvas.create_text(center_x - 150, choice_y + 80, 
                                   text=self.main_window.rps_game.last_player_choice.upper(), 
                                   fill=self.colors['green'], font=("Segoe UI", 14, "bold"))
            
            # Computer choice
            self.canvas.create_rectangle(center_x + 80, choice_y - 60, 
                                        center_x + 220, choice_y + 100,
                                        fill=self.colors['crust'], outline=self.colors['red'], width=4)
            
            computer_emoji = self.main_window.rps_game.get_choice_emoji(
                self.main_window.rps_game.last_computer_choice)
            self.canvas.create_text(center_x + 150, choice_y, text=computer_emoji, 
                                   fill=self.colors['yellow'], font=("Segoe UI", 72))
            self.canvas.create_text(center_x + 150, choice_y + 80, 
                                   text=self.main_window.rps_game.last_computer_choice.upper(), 
                                   fill=self.colors['red'], font=("Segoe UI", 14, "bold"))
        
        # Instructions
        self.canvas.create_text(center_x, canvas_height - 50, 
                               text="Choose Rock, Paper, or Scissors!", 
                               fill=self.colors['lavender'], font=("Segoe UI", 14, "italic"))