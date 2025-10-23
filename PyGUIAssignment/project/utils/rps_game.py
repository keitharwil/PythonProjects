"""Rock Paper Scissors game logic"""
import random
from config import RPS_ROUNDS, RPS_CHOICES

class RPSGame:
    def __init__(self):
        self.rounds_left = 0
        self.player_score = 0
        self.computer_score = 0
        self.last_player_choice = None
        self.last_computer_choice = None
        self.is_active = False
    
    def start_game(self):
        """Initialize and start the game"""
        self.rounds_left = RPS_ROUNDS
        self.player_score = 0
        self.computer_score = 0
        self.last_player_choice = None
        self.last_computer_choice = None
        self.is_active = True
        return f"Rock Paper Scissors game started! {RPS_ROUNDS} rounds to go."
    
    def play_round(self, player_choice):
        """Play one round"""
        if self.rounds_left <= 0:
            return None
        
        computer_choice = random.choice(RPS_CHOICES)
        result = self.determine_winner(player_choice, computer_choice)
        
        self.last_player_choice = player_choice
        self.last_computer_choice = computer_choice
        
        if result == 'win':
            self.player_score += 1
        elif result == 'lose':
            self.computer_score += 1
        
        self.rounds_left -= 1
        
        round_num = RPS_ROUNDS - self.rounds_left
        message = f"Round {round_num}: You chose {player_choice.upper()}, Computer chose {computer_choice.upper()} - {result.upper()}!"
        
        return {
            'message': message,
            'result': result,
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'game_over': self.rounds_left <= 0
        }
    
    def determine_winner(self, player, computer):
        """Determine the winner of a round"""
        if player == computer:
            return 'tie'
        
        win_conditions = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
        
        return 'win' if win_conditions[player] == computer else 'lose'
    
    def get_final_result(self):
        """Get the final game result"""
        if self.player_score > self.computer_score:
            return "🎉 YOU WIN THE GAME!", 'win'
        elif self.player_score < self.computer_score:
            return "💔 COMPUTER WINS THE GAME!", 'lose'
        else:
            return "🤝 IT'S A TIE!", 'tie'
    
    def end_game(self):
        """End the game"""
        self.is_active = False
        self.last_player_choice = None
        self.last_computer_choice = None
    
    @staticmethod
    def get_choice_emoji(choice):
        """Return emoji for each choice"""
        emojis = {
            'rock': '✊',
            'paper': '✋',
            'scissors': '✌'
        }
        return emojis.get(choice, '❓')