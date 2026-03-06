import random
from collections import defaultdict
import time

class RockPaperScissors:
    def __init__(self, ai_mode="advanced"):
        """
        Initialize the game
        ai_mode: "basic" for random AI, "advanced" for learning AI
        """
        self.choices = ["rock", "paper", "scissors"]
        self.winning_combinations = {
            "rock": "scissors",
            "paper": "rock", 
            "scissors": "paper"
        }
        
        # Statistics tracking
        self.player_history = []
        self.ai_history = []
        self.player_stats = {
            "rock": 0,
            "paper": 0, 
            "scissors": 0
        }
        
        # Pattern recognition for advanced AI
        self.patterns = defaultdict(lambda: defaultdict(int))
        self.pattern_length = 2  # Look for patterns of 2 moves
        self.ai_mode = ai_mode
        
        self.scores = {"player": 0, "ai": 0, "ties": 0}
    
    def get_player_choice(self):
        """Get and validate player's choice"""
        while True:
            print("\nEnter your choice (rock/paper/scissors or 'quit' to exit):")
            choice = input().lower().strip()
            
            if choice == 'quit':
                return None
            
            if choice in self.choices:
                return choice
            
            print("Invalid choice! Please enter rock, paper, or scissors.")
    
    def get_basic_ai_choice(self):
        """Simple random AI choice"""
        return random.choice(self.choices)
    
    def get_advanced_ai_choice(self):
        """AI that learns from player patterns"""
        if len(self.player_history) < self.pattern_length:
            # Not enough history, use random choice with weighted probabilities
            return self.get_weighted_random_choice()
        
        # Look for patterns in player's history
        last_moves = tuple(self.player_history[-self.pattern_length:])
        
        if last_moves in self.patterns and self.patterns[last_moves]:
            # Predict player's next move based on patterns
            predicted_move = max(self.patterns[last_moves], 
                               key=self.patterns[last_moves].get)
            
            # Choose the move that beats the predicted move
            for move, beats in self.winning_combinations.items():
                if beats == predicted_move:
                    return move
        
        # Fallback to weighted random
        return self.get_weighted_random_choice()
    
    def get_weighted_random_choice(self):
        """Generate random choice based on player's preferences"""
        if sum(self.player_stats.values()) == 0:
            return random.choice(self.choices)
        
        # Calculate probabilities based on player's history
        total = sum(self.player_stats.values())
        probabilities = [self.player_stats[choice] / total for choice in self.choices]
        
        return random.choices(self.choices, weights=probabilities)[0]
    
    def determine_winner(self, player_choice, ai_choice):
        """Determine the winner of the round"""
        if player_choice == ai_choice:
            return "tie"
        elif self.winning_combinations[player_choice] == ai_choice:
            return "player"
        else:
            return "ai"
    
    def update_patterns(self):
        """Update pattern recognition database"""
        if len(self.player_history) >= self.pattern_length + 1:
            # Get the pattern and the following move
            for i in range(len(self.player_history) - self.pattern_length):
                pattern = tuple(self.player_history[i:i + self.pattern_length])
                next_move = self.player_history[i + self.pattern_length]
                self.patterns[pattern][next_move] += 1
    
    def display_round_result(self, player_choice, ai_choice, winner):
        """Display the result of the current round"""
        print(f"\nYou chose: {player_choice}")
        print(f"AI chose: {ai_choice}")
        
        if winner == "tie":
            print("It's a tie!")
        elif winner == "player":
            print("You win this round!")
        else:
            print("AI wins this round!")
    
    def display_statistics(self):
        """Display game statistics"""
        print("\n" + "="*50)
        print("GAME STATISTICS")
        print("="*50)
        print(f"Player wins: {self.scores['player']}")
        print(f"AI wins: {self.scores['ai']}")
        print(f"Ties: {self.scores['ties']}")
        
        total_rounds = sum(self.scores.values())
        if total_rounds > 0:
            print(f"\nWin rates:")
            print(f"Player: {(self.scores['player']/total_rounds)*100:.1f}%")
            print(f"AI: {(self.scores['ai']/total_rounds)*100:.1f}%")
        
        if self.player_history:
            print(f"\nYour move preferences:")
            for move, count in self.player_stats.items():
                percentage = (count/len(self.player_history)) * 100
                print(f"{move.capitalize()}: {count} times ({percentage:.1f}%)")
    
    def play_round(self):
        """Play a single round"""
        # Get player choice
        player_choice = self.get_player_choice()
        if player_choice is None:
            return False
        
        # Get AI choice based on mode
        if self.ai_mode == "advanced":
            ai_choice = self.get_advanced_ai_choice()
        else:
            ai_choice = self.get_basic_ai_choice()
        
        # Determine winner
        winner = self.determine_winner(player_choice, ai_choice)
        
        # Update scores
        if winner == "player":
            self.scores["player"] += 1
        elif winner == "ai":
            self.scores["ai"] += 1
        else:
            self.scores["ties"] += 1
        
        # Update history and statistics
        self.player_history.append(player_choice)
        self.ai_history.append(ai_choice)
        self.player_stats[player_choice] += 1
        
        # Update patterns for advanced AI
        if self.ai_mode == "advanced":
            self.update_patterns()
        
        # Display result
        self.display_round_result(player_choice, ai_choice, winner)
        
        return True
    
    def play_game(self):
        """Main game loop"""
        print("="*50)
        print("WELCOME TO ROCK-PAPER-SCISSORS")
        print("="*50)
        print(f"AI Mode: {self.ai_mode.upper()}")
        print("\nRules:")
        print("- Rock beats Scissors")
        print("- Paper beats Rock")
        print("- Scissors beats Paper")
        print("\nType 'quit' at any time to exit.")
        
        if self.ai_mode == "advanced":
            print("\nAdvanced AI is learning your patterns...")
            time.sleep(1)
        
        # Game loop
        rounds_played = 0
        while True:
            rounds_played += 1
            print(f"\n--- Round {rounds_played} ---")
            
            if not self.play_round():
                break
        
        # Display final statistics
        print("\n" + "="*50)
        print("GAME OVER")
        print("="*50)
        self.display_statistics()
        
        # Additional advanced AI insights
        if self.ai_mode == "advanced" and len(self.player_history) > self.pattern_length:
            print("\nAI Insights:")
            print("Patterns detected in your play:")
            for pattern, next_moves in list(self.patterns.items())[:5]:  # Show top 5 patterns
                if sum(next_moves.values()) > 1:
                    moves_str = " → ".join(pattern)
                    most_common = max(next_moves, key=next_moves.get)
                    print(f"  After {moves_str}, you often play {most_common}")

def main():
    """Main function to run the game"""
    print("Choose AI difficulty:")
    print("1. Basic (Random)")
    print("2. Advanced (Learning AI)")
    
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            ai_mode = "basic"
            break
        elif choice == "2":
            ai_mode = "advanced"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    # Create and play game
    game = RockPaperScissors(ai_mode=ai_mode)
    
    try:
        game.play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        game.display_statistics()
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()