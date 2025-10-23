"""Visualization canvas for drawing linked lists and RPS game"""
import tkinter as tk
from config import COLORS

class VisualizationCanvas:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.colors = COLORS
        
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
                
                # Draw arrow to next node
                if i < len(singly_list) - 1:
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
        
        nodes = self.main_window.list_manager.get_doubly_list()
        
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
            
            # Draw arrow to next node
            if i < len(circular_list) - 1:
                arrow_start_x = x + node_width + 5
                arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                arrow_y = y_pos + node_height//2
                self.canvas.create_line(arrow_start_x, arrow_y,
                                      arrow_end_x, arrow_y,
                                      arrow=tk.LAST, fill=self.colors['peach'], 
                                      width=3, smooth=True)
        
        # Draw circular arrow from last to first
        if len(circular_list) > 1:
            last_x = start_x + ((len(circular_list) - 1) * spacing) + node_width
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
        
        nodes = self.main_window.list_manager.get_circular_doubly_list()
        
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
                
                # Draw arrow to next node
                if i < len(stack) - 1:
                    arrow_start_x = x + node_width + 5
                    arrow_end_x = arrow_start_x + (spacing - node_width - 15)
                    arrow_y = y_pos + node_height//2
                    self.canvas.create_line(arrow_start_x, arrow_y,
                                          arrow_end_x, arrow_y,
                                          arrow=tk.LAST, fill=self.colors['flamingo'], 
                                          width=3, smooth=True)
            
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