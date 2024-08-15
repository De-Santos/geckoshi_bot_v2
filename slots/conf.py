import os

# Slot symbols
symbols = ["🦎", "🏜️", "🏖️", "🏕️", "✈️", "🚀", "🪲", "🐞", "🐝"]

# Define multipliers (combinations that result in a win)
COMBINATIONS = [
    ("🦎🦎🦎", 10, 0.001),
    ("🏜️🏜️🏜️", 5, 0.01),
    ("🏖️🏖️🏖️", 3, 0.05),
    ("🏕️🏕️🏕️", 2, 0.10),
    ("✈️✈️✈️", 1.8, 0.18),
    ("🚀🚀🚀", 1.7, 0.22),
    ("🪲🪲🪲", 1.5, 0.25),
    ("🐞🐞🐞", 1.2, 0.35),
    ("🐝🐝🐝", 1.05, 0.55),
]

BET_AMOUNTS = [100, 250, 500, 1000, 2500, 5000, 10000]

# Define the probabilities of winning/losing
win_probability = float(os.getenv("CASINO_WIN_PROBABILITY"))
