"""author: Jose Mondragon
Title: Game Theory War Game
This program is designed to simulate a two-player war game using game theory and matrices. Honestly, don't know what I'm doing.
Edit 1: It was a pain to install all the things to get this to work but it finally works. Edit 1.5: Nevermind have to install some packages appearently to get
to do what I want it to do.
Edit 2: This is frustrating and I wish I hadn't put it off for so long since I'm essentially working all day to do this.
Edit 3: I'm done. Broken in some places but works.
Edit 4: Found out I needed to comment on the code. I'm not doing that. I don't have time or feel like it.

"""
import numpy as np
from scipy.optimize import linprog

# Define strategies
USA_STRATEGIES = ["Attack", "Defend", "Mobilize troops"]
CHINA_STRATEGIES = ["Counter-attack", "Fortify", "Withdraw"]

def war_game_simulation(payoff_usa, payoff_china, usa_strategies, china_strategies):
    num_strategies_usa, num_strategies_china = payoff_usa.shape

    if not np.array_equal(payoff_usa, -payoff_china):
        payoff_usa = (payoff_usa - payoff_china) / 2
        payoff_china = -payoff_usa

    c = [-1] + [0] * num_strategies_usa
    A_ub = np.hstack((np.ones((num_strategies_china, 1)), -payoff_usa.T))
    b_ub = np.zeros(num_strategies_china)
    A_eq = np.array([[0] + [1] * num_strategies_usa])
    b_eq = [1]
    bounds = [(None, None)] + [(0, 1)] * num_strategies_usa

    result = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds, method="highs")
    strategy_usa = result.x[1:]
    game_value = result.fun * -1

    strategy_china = linprog(
        [-1] + [0] * num_strategies_china,
        np.hstack((np.ones((num_strategies_usa, 1)), -payoff_china)),
        np.zeros(num_strategies_usa),
        [[0] + [1] * num_strategies_china],
        [1],
        [(None, None)] + [(0, 1)] * num_strategies_china,
        method="highs"
    ).x[1:]

    return {
        "USA Strategy Probabilities": strategy_usa,
        "China Strategy Probabilities": strategy_china,
        "Game Value (Payoff for USA)": game_value
    }

def get_valid_matrix():
    while True:
        try:
            print("Choose a matrix size (maximum 3x3):")
            rows = int(input("Enter the number of strategies for USA (1-3): "))
            cols = int(input("Enter the number of strategies for China (1-3): "))
            if rows <= 0 or rows > 3 or cols <= 0 or cols > 3:
                raise ValueError("Number of strategies must be between 1 and 3.")
            
            usa_strategies = USA_STRATEGIES[:rows]
            china_strategies = CHINA_STRATEGIES[:cols]

            print(f"USA Strategies: {', '.join(usa_strategies)}")
            print(f"China Strategies: {', '.join(china_strategies)}")

            print("Enter the payoff matrix row by row (space-separated values):")
            matrix = []
            for i in range(rows):
                row = list(map(float, input(f"Row {i + 1}: ").split()))
                if len(row) != cols:
                    raise ValueError(f"Each row must have exactly {cols} values.")
                matrix.append(row)
            
            return np.array(matrix), usa_strategies, china_strategies
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def explain_results(result, usa_strategies, china_strategies):
    usa_probs = result["USA Strategy Probabilities"]
    china_probs = result["China Strategy Probabilities"]
    game_value = result["Game Value (Payoff for USA)"]

    print("\n--- War Game Results ---")
    print("USA Strategy Probabilities:")
    for i, prob in enumerate(usa_probs):
        print(f"  {usa_strategies[i]}: {prob:.2f}")

    print("\nChina Strategy Probabilities:")
    for i, prob in enumerate(china_probs):
        print(f"  {china_strategies[i]}: {prob:.2f}")

    print(f"\nGame Value (Payoff for USA): {game_value:.2f}")

    print("\nInterpretation:")
    if game_value > 0:
        print("  - The USA has an advantage in this game, as the game value is positive.")
        print(f"  - By following the optimal strategy mix, the USA can expect an average gain of {game_value:.2f} units.")
    elif game_value < 0:
        print("  - China has an advantage in this game, as the game value is negative.")
        print(f"  - By following the optimal strategy mix, the USA will likely lose on average by {-game_value:.2f} units.")
    else:
        print("  - The game is evenly balanced, with no clear advantage for either side.")
        print("  - Both sides can follow their mixed strategies to avoid being exploited.")

    print("\nUSA Optimal Strategy:")
    for i, prob in enumerate(usa_probs):
        if prob > 0:
            print(f"  - Allocate {prob:.2f} probability to '{usa_strategies[i]}'.")

    print("\nChina Optimal Strategy:")
    for i, prob in enumerate(china_probs):
        if prob > 0:
            print(f"  - Allocate {prob:.2f} probability to '{china_strategies[i]}'.")

payoff_usa, usa_strategies, china_strategies = get_valid_matrix()
payoff_china = -payoff_usa

result = war_game_simulation(payoff_usa, payoff_china, usa_strategies, china_strategies)
explain_results(result, usa_strategies, china_strategies)
