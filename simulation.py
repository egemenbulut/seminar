from theorems import Theorems
import numpy as np
import random

def run_simulations(n: int, data: Theorems, alg: str, alpha: float = 0.001, 
                        c: float = 0.15, d: float = None, number_of_simulations: int = 100) -> tuple[list[int], list[float], list[float]]:
    """
    Run simulations for the given algorithm.

    Args:
        n: The exponent for the maximum pull count (max pulls = 10^n).
        data: Theorems instance to use for simulations.
        alg: Algorithm to use ("ucb1", "ucb2", "en_greedy", "ucb_tuned").
        alpha: Alpha parameter for UCB2 algorithm.
        c: C parameter for epsilon-greedy algorithm.
        d: D parameter for epsilon-greedy algorithm. If None, computed
           as the difference between the two highest means.
        number_of_simulations: Number of simulations to average over.

    Returns:
        Tuple of (pulls, regrets, best_ratios) where each is a list.
        pulls: sorted list of pull counts (logarithmic schedule).
        regrets: average regret at each pull count.
        best_ratios: average best-machine ratio at each pull count.
    """
    
    # If d is None, compute from the two highest means
    if d is None:
        means = sorted([m[1] for m in data.machines], reverse=True)
        d = means[0] - means[1]

    # Build pulls list: 10^0, 10^1, ..., 10^n with 20 log-spaced points between each pair
    pulls_set = set()
    for i in range(n + 1):
        pulls_set.add(int(10 ** i))
    for i in range(n):
        low = 10 ** i
        high = 10 ** (i + 1)
        log_points = np.logspace(np.log10(low), np.log10(high), num=22)  # 22 = 20 interior + 2 endpoints
        for p in log_points:
            pulls_set.add(int(round(p)))
    
    pulls = sorted(pulls_set)

    # Initialize accumulators
    regrets = [0.0] * len(pulls)
    best_ratios = [0.0] * len(pulls)

    # Run simulations
    for sim in range(number_of_simulations):
        print(f"Simulation {sim + 1}/{number_of_simulations} ({alg})")

        for idx, pull_count in enumerate(pulls):
            print(f"Pulls: {pull_count}")

            data.reset()
            random.seed(sim)
            
            # Run the selected algorithm
            if alg == "ucb1":
                data.ucb1(pull_count)
            elif alg == "ucb2":
                data.ucb2(pull_count, alpha)
            elif alg == "en_greedy":
                data.en_greedy(pull_count, c, d)
            elif alg == "ucb_tuned":
                data.ucb_tuned(pull_count)
            
            regrets[idx] += data.regret()
            best_ratios[idx] += data.best_machine_ratio()

    # Average over all simulations
    for idx in range(len(pulls)):
        regrets[idx] /= number_of_simulations
        best_ratios[idx] /= number_of_simulations

    return (pulls, regrets, best_ratios)


    
    