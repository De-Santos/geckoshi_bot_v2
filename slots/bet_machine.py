import random

from database import BetType
from slots.conf import win_probability, COMBINATIONS, symbols


# Helper function to generate a random non-winning combination
def random_now_combination() -> list[str]:
    while True:
        # Generate a random combination of 3 symbols
        r = random.choices(symbols, k=3)
        # If the generated combination is not a winning combination, return it
        if r not in [comb[0] for comb in COMBINATIONS]:
            return r


# Function to play the slot game
def play_slots(amount: int) -> (list[str], int, BetType):
    # Determine if the player wins or loses
    if random.random() <= win_probability:
        # Determine which combination the player wins with
        roll = random.random()
        cumulative_probability = 0.0
        for combo, multiplier, probability in COMBINATIONS:
            cumulative_probability += probability
            if roll <= cumulative_probability:
                # Player wins, return the combination and the win amount
                return combo, int(amount * multiplier), BetType.WIN
    # Player loses, return a random combination and 0 win
    return random_now_combination(), 0, BetType.LOSS
