"""Rock Paper Scissors control panel"""
import tkinter as tk
from tkinter import messagebox
from config import COLORS

class RPSPanel:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.colors = COLORS
        
        # Create frame
        rps_frame = tk.Frame(parent, bg=self.colors['mantle'], relief=tk.FLAT)
        rps_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        rps_inner = tk.Frame(rps_frame, bg=self.colors['mantle'])
        rps_inner.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        self.create_widgets(rps_inner)
    
    def create_widgets(self, parent):
        """Create all widgets"""
        tk.Label(parent, text="Rock Paper Scissors", 
                bg=self.colors['mantle'], fg=self.colors['mauve'], 
                font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))
        
        # Start game button
        self.create_button(parent, "Start Game (5 Rounds)", self.colors['green'], 
                          self.start_rps_game, width=26).pack(pady=5)
        
        # Score display
        self.score_label = tk.Label(parent, text="Player: 0 | Computer: 0", 
                                   bg=self.colors['mantle'], fg=self.colors['text'], 
                                   font=("Segoe UI", 11, "bold"))
        self.score_label.pack(pady=5)
        
        # RPS buttons frame
        rps_btn_frame = tk.Frame(parent, bg=self.colors['mantle'])
        rps_btn_frame.pack(pady=10)
        
        # Create RPS buttons (initially disabled)
        self.rock_btn = self.create_button(rps_btn_frame, "✊ Rock", self.colors['surface1'], 
                                          lambda: self.play_round("rock"))
        self.rock_btn.pack(side=tk.LEFT, padx=3)
        self.rock_btn.config(state=tk.DISABLED)
        
        self.paper_btn = self.create_button(rps_btn_frame, "✋ Paper", self.colors['surface1'], 
                                           lambda: self.play_round("paper"))
        self.paper_btn.pack(side=tk.LEFT, padx=3)
        self.paper_btn.config(state=tk.DISABLED)
        
        self.scissors_btn = self.create_button(rps_btn_frame, "✌ Scissors", self.colors['surface1'], 
                                              lambda: self.play_round("scissors"))
        self.scissors_btn.pack(side=tk.LEFT, padx=3)
        self.scissors_btn.config(state=tk.DISABLED)
    
    def create_button(self, parent, text, color, command, width=12):
        """Create a styled button"""
        btn = tk.Button(parent, text=text, bg=color, fg=self.colors['crust'],
                       font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                       command=command, width=width, cursor="hand2",
                       activebackground=color, activeforeground=self.colors['base'])
        return btn
    
    def start_rps_game(self):
        """Initialize and start the RPS game"""
        msg = self.main_window.rps_game.start_game()
        
        # Enable RPS buttons
        self.rock_btn.config(state=tk.NORMAL, bg=self.colors['blue'])
        self.paper_btn.config(state=tk.NORMAL, bg=self.colors['green'])
        self.scissors_btn.config(state=tk.NORMAL, bg=self.colors['yellow'])
        
        self.update_score_display()
        self.main_window.log(f"🎮 {msg}")
        self.main_window.refresh_visualization()
    
    def play_round(self, player_choice):
        """Play one round of RPS"""
        result = self.main_window.rps_game.play_round(player_choice)
        
        if result is None:
            return
        
        self.main_window.log(result['message'])
        self.update_score_display()
        self.main_window.refresh_visualization()
        
        if result['game_over']:
            self.main_window.root.after(500, self.end_game)
    
    def end_game(self):
        """End the game and return to menu"""
        # Disable RPS buttons
        self.rock_btn.config(state=tk.DISABLED, bg=self.colors['surface1'])
        self.paper_btn.config(state=tk.DISABLED, bg=self.colors['surface1'])
        self.scissors_btn.config(state=tk.DISABLED, bg=self.colors['surface1'])
        
        # Get final result
        result_text, result_type = self.main_window.rps_game.get_final_result()
        
        if result_type == 'win':
            color = self.colors['green']
        elif result_type == 'lose':
            color = self.colors['red']
        else:
            color = self.colors['yellow']
        
        self.main_window.log(f"\n{result_text}")
        self.main_window.log(f"Final Score - Player: {self.main_window.rps_game.player_score} | Computer: {self.main_window.rps_game.computer_score}\n")
        
        # Show result dialog
        messagebox.showinfo("Game Over", 
                           f"{result_text}\n\nFinal Score:\nPlayer: {self.main_window.rps_game.player_score}\nComputer: {self.main_window.rps_game.computer_score}")
        
        # End game
        self.main_window.rps_game.end_game()
        self.main_window.refresh_visualization()
    
    def update_score_display(self):
        """Update the score label"""
        self.score_label.config(text=f"Player: {self.main_window.rps_game.player_score} | Computer: {self.main_window.rps_game.computer_score}")