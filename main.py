from Player import Player
from MonteCarloPlayer import MonteCarloPlayer
from ExpectiMinimaxPlayer import ExpectiMinimaxPlayer
from HumanPlayer import HumanPlayer
from Match import Match
import numpy as np
import json
from functools import partial

# Set number of games for each evaluation type
games_default = 100 # Default number of games for standard evaluations against Random Player
games_exploration = 30 # Number of games for hyperparameter exploration evaluations
games_comparison = 50 # Number of games for comparison evaluations between two intelligent agents

def save_dict_to_file(data_dict, filename):
    with open("stats/" + filename, 'w') as f:
        json.dump(data_dict, f, indent=4)


def full_game_evaluation(p1_class : type['Player'], p2_class : type['Player'], games : int, score_to_win: int = 200):
    p1_match = 0
    p2_match = 0
    p1_game = 0
    p2_game = 0
    matches = 0
    full_match_move_times_p1 = []
    full_match_move_times_p2 = []

    for j in range(games):
        p1 = p1_class()
        p2 = p2_class()
        m = Match(p1, p2, False)
        i = 1
        print(f"\nGame #{j+1}")
        while p1.score < score_to_win and p2.score < score_to_win:
            matches += 1
            print(f"\nMatch #{i}")

            result, p1_times, p2_times  = m.play()
            full_match_move_times_p1 += p1_times
            full_match_move_times_p2 += p2_times

            print(f"Result: {result}")
            m.boneyard.print_boneyard_tiles()
            print(f"{p1.name}: {m.player_1.hand}, Score: {m.player_1.score}")
            print(f"{p2.name}: {m.player_2.hand}, Score: {m.player_2.score}")
            if result == p1.name:
                p1_match += 1
            if result == p2.name:
                p2_match += 1
            i += 1

        print()
        if p1.score >= score_to_win:
            print(f"{p1.name} is the winner")
            p1_game += 1
        else:
            print(f"{p2.name} is the winner")
            p2_game += 1
        
    print("\n Match Stats")
    print(f"{p1.name} Match Winning Ratio: {p1_match / matches} after playing {matches} matches")
    print(f"{p2.name} Match Winning Ratio: {p2_match / matches} after playing {matches} matches")

    print("\n Game Stats")
    print(f"{p1.name} Game Winning Ratio: {p1_game / games} after playing {games} games")
    print(f"{p2.name} Game Winning Ratio: {p2_game / games} after playing {games} games")

    print("\n Move Time Stats")
    print(f"{p1.name} Move Time: Mean = {np.mean(full_match_move_times_p1)}s, Std = {np.std(full_match_move_times_p1)}s, Max = {np.max(full_match_move_times_p1)}s, Min = {np.min(full_match_move_times_p1)}s")
    print(f"{p2.name} Move Time: Mean = {np.mean(full_match_move_times_p2)}s, Std = {np.std(full_match_move_times_p2)}s, Max = {np.max(full_match_move_times_p2)}s, Min = {np.min(full_match_move_times_p2)}s")

    stats = {
        "p1_match_win_ratio": p1_match / matches,
        "p2_match_win_ratio": p2_match / matches,
        "p1_game_win_ratio": p1_game / games,
        "p2_game_win_ratio": p2_game / games,
        "p1_move_time_mean": np.mean(full_match_move_times_p1),
        "p1_move_time_std": np.std(full_match_move_times_p1),
        "p1_move_time_max": np.max(full_match_move_times_p1),
        "p1_move_time_min": np.min(full_match_move_times_p1),
        "p2_move_time_mean": np.mean(full_match_move_times_p2),
        "p2_move_time_std": np.std(full_match_move_times_p2),
        "p2_move_time_max": np.max(full_match_move_times_p2),
        "p2_move_time_min": np.min(full_match_move_times_p2),
        "matches_played": matches,
        "games_played": games
    }

    return stats



if __name__ == "__main__":
    print("Main Program for Dominos Game")
    options = input("Options: \n1. Run Full Game Evaluations\n2. Run Default Evaluations\n3. Run Exploratory Evaluations\n4. Run Comparison Evaluations\n5. Human Player (one game of 50 points) \nSelect Option #: ")

    if options == "1" or options == "2":
        # ExpectiMinimax Agent Evaluation (Against Random Player)
        p1 = ExpectiMinimaxPlayer
        p2 = Player

        print("\nEvaluating ExpectiMinimax Player vs Random Player")
        results = full_game_evaluation(p1, p2, games_default)
        save_dict_to_file(results, "expectiminimax_vs_random_stats_default.json")

        # Monte Carlo Agent Evaluation (Against Random Player)
        p1 = MonteCarloPlayer
        p2 = Player

        print("\nEvaluating Monte Carlo Player vs Random Player")
        results = full_game_evaluation(p1, p2, games_default)
        save_dict_to_file(results, "montecarlo_vs_random_stats_default.json")

    if options == "1" or options == "3":
        # ExpectiMinimax - Hyperparameter Exploration
        depths = [4, 5, 6, 7]
        for depth in depths:
            p1 = partial(ExpectiMinimaxPlayer, depth=depth)
            p2 = Player

            print(f"\nEvaluating ExpectiMinimax Player (Depth={depth}) vs Random Player")
            results = full_game_evaluation(p1, p2, games_exploration)
            save_dict_to_file(results, f"expectiminimax_vs_random_stats_depth_{depth}.json")
        
        # Monte Carlo - Hyperparameter Exploration (Iterations)
        iterations_list = [1000, 2000, 3000, 4000]
        for iterations in iterations_list:
            p1 = partial(MonteCarloPlayer, n=iterations)
            p2 = Player

            print(f"\nEvaluating Monte Carlo Player (Iterations={iterations}) vs Random Player")
            results = full_game_evaluation(p1, p2, games_exploration)
            save_dict_to_file(results, f"montecarlo_vs_random_stats_iterations_{iterations}.json")
        
        # Monte Carlo - Hyperparameter Exploration (Exploration Constant)
        exploration_constants = [0.5, 0.7, 0.9]
        for c in exploration_constants:
            p1 = partial(MonteCarloPlayer, c=c)
            p2 = Player

            print(f"\nEvaluating Monte Carlo Player (Exploration Constant={c}) vs Random Player")
            results = full_game_evaluation(p1, p2, games_exploration)
            save_dict_to_file(results, f"montecarlo_vs_random_stats_exploration_{c}.json")

    if options == "1" or options == "4":
        # Comparison between ExpectiMinimax and Monte Carlo
        p1 = partial(ExpectiMinimaxPlayer, depth=5)
        p2 = partial(MonteCarloPlayer, n=1000)

        print("\nEvaluating ExpectiMinimax Player (Depth = 5) vs Monte Carlo Player (Iterations = 1000)")
        results = full_game_evaluation(p1, p2, games_comparison)
        save_dict_to_file(results, "expectiminimax(d5)_vs_montecarlo(n1000)_stats.json")

        # Comparison between ExpectiMinimax and Monte Carlo
        p1 = partial(ExpectiMinimaxPlayer, depth=5)
        p2 = partial(MonteCarloPlayer, n=2000)

        print("\nEvaluating ExpectiMinimax Player (Depth = 5) vs Monte Carlo Player (Iterations = 2000)")
        results = full_game_evaluation(p1, p2, games_comparison)
        save_dict_to_file(results, "expectiminimax(d5)_vs_montecarlo(n2000)_stats.json")

        # Comparison between ExpectiMinimax and Monte Carlo
        p1 = partial(ExpectiMinimaxPlayer, depth=6)
        p2 = partial(MonteCarloPlayer, n=4000)

        print("\nEvaluating ExpectiMinimax Player (Depth = 6) vs Monte Carlo Player (Iterations = 4000)")
        results = full_game_evaluation(p1, p2, games_comparison)
        save_dict_to_file(results, "expectiminimax(d6)_vs_montecarlo(n4000)_stats.json")

    if options == "5":
        opponent_type = input("Select Opponent Type: \n1. Random Player\n2. ExpectiMinimax Player\n3. Monte Carlo Player\nSelect Option #: ")
        
        # Human Player vs Agent
        p1 = HumanPlayer
        if opponent_type == "1":
            p2 = Player
            print("\nHuman Player vs Random Player")
            results = full_game_evaluation(p1, p2, 1, score_to_win=50)
            save_dict_to_file(results, "human_vs_random_stats.json")
        elif opponent_type == "2":
            p2 = partial(ExpectiMinimaxPlayer, depth=5)
            print("\nHuman Player vs ExpectiMinimax Player (Depth = 5)")
            results = full_game_evaluation(p1, p2, 1, score_to_win=50)
            save_dict_to_file(results, "human_vs_expectiminimax_stats.json")
        elif opponent_type == "3":
            p2 = partial(MonteCarloPlayer, n=1000)
            print("\nHuman Player vs Monte Carlo Player (Iterations = 1000)")
            results = full_game_evaluation(p1, p2, 1, score_to_win=50)
            save_dict_to_file(results, "human_vs_montecarlo_stats.json")
        else:
            print("Invalid Option Selected")