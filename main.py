from Player import Player
from MonteCarloPlayer import MonteCarloPlayer
from ExpectiMinimaxPlayer import ExpectiMinimaxPlayer
from Match import Match
import numpy as np
import json
import os

def save_dict_to_file(data_dict, filename):
    """
    Saves a dictionary to a newly created JSON file.
    If the file already exists, it raises an error.
    """
    if os.path.exists(filename):
        raise FileExistsError(f"File '{filename}' already exists.")

    with open("stats/" + filename, 'w') as f:
        json.dump(data_dict, f, indent=4)


def full_game_evaluation(p1 : Player, p2 : Player, games : int, score_to_win: int = 200):
    p1_match = 0
    p2_match = 0
    p1_game = 0
    p2_game = 0
    matches = 0
    full_match_move_times_p1 = []
    full_match_move_times_p2 = []

    for j in range(games):
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

    games_default = 1#100
    games_exploration = 1#30
    games_comparison = 1#100

    # ExpectiMinimax Agent Evaluation (Against Random Player)
    p1 = ExpectiMinimaxPlayer("ExpectiMinimax Player")
    p2 = Player("Random Player")

    print("\nEvaluating ExpectiMinimax Player vs Random Player")
    results = full_game_evaluation(p1, p2, games_default)
    save_dict_to_file(results, "expectiminimax_vs_random_stats_default.json")

    # Monte Carlo Agent Evaluation (Against Random Player)
    p1 = MonteCarloPlayer("Monte Carlo Player")
    p2 = Player("Random Player")

    print("\nEvaluating Monte Carlo Player vs Random Player")
    results = full_game_evaluation(p1, p2, games_default)
    save_dict_to_file(results, "montecarlo_vs_random_stats_default.json")

    # ExpectiMinimax - Hyperparameter Exploration
    depths = [4, 5, 6, 7]
    for depth in depths:
        p1 = ExpectiMinimaxPlayer(f"ExpectiMinimax Player", depth=depth)
        p2 = Player("Random Player")

        print(f"\nEvaluating ExpectiMinimax Player (Depth={depth}) vs Random Player")
        results = full_game_evaluation(p1, p2, games_exploration)
        save_dict_to_file(results, f"expectiminimax_vs_random_stats_depth_{depth}.json")
    
    # Monte Carlo - Hyperparameter Exploration (Iterations)
    iterations_list = [1000, 2000, 3000, 4000]
    for iterations in iterations_list:
        p1 = MonteCarloPlayer(f"Monte Carlo Player", n=iterations)
        p2 = Player("Random Player")

        print(f"\nEvaluating Monte Carlo Player (Iterations={iterations}) vs Random Player")
        results = full_game_evaluation(p1, p2, games_exploration)
        save_dict_to_file(results, f"montecarlo_vs_random_stats_iterations_{iterations}.json")
    
    # Monte Carlo - Hyperparameter Exploration (Exploration Constant)
    exploration_constants = [0.5, 0.7, 0.9]
    for c in exploration_constants:
        p1 = MonteCarloPlayer(f"Monte Carlo Player", c=c)
        p2 = Player("Random Player")

        print(f"\nEvaluating Monte Carlo Player (Exploration Constant={c}) vs Random Player")
        results = full_game_evaluation(p1, p2, games_exploration)
        save_dict_to_file(results, f"montecarlo_vs_random_stats_exploration_{c}.json")

    # Comparison between ExpectiMinimax and Monte Carlo
    p1 = ExpectiMinimaxPlayer("ExpectiMinimax Player", depth=5)
    p2 = MonteCarloPlayer("Monte Carlo Player", n=3000)

    print("\nEvaluating ExpectiMinimax Player vs Monte Carlo Player")
    results = full_game_evaluation(p1, p2, games_comparison)
    save_dict_to_file(results, "expectiminimax_vs_montecarlo_stats.json")