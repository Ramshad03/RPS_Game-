import random

WINNING_SCORE = 4

def get_machine_move():
    return random.choice(["rock", "paper", "scissors"])

def get_round_result(user_move, machine_move):
    if user_move == machine_move:
        return "draw"
    
    wins = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }
    
    if wins[user_move] == machine_move:
        return "user"
    else:
        return "machine"

class GameState:
    def __init__(self, username):
        self.username = username
        self.user_score = 0
        self.machine_score = 0

    def update_score(self, result):
        if result == "user":
            self.user_score += 1
        elif result == "machine":
            self.machine_score += 1

    def is_game_over(self):
        return self.user_score >= WINNING_SCORE or self.machine_score >= WINNING_SCORE

    def get_winner(self):
        if self.user_score >= WINNING_SCORE:
            return "user"
        elif self.machine_score >= WINNING_SCORE:
            return "machine"
        return None