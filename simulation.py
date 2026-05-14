from theorems import Theorems

def simulate(data: Theorems, algo: str, number_of_pulls: int, number_of_simulations: int = 100, 
                alpha: float = 0.0001, c: float = 0.1, d: float = None) -> tuple[float, float]:
    """
    Simulates the given algorithm multiple times and returns the average regret
    and the average best machine played ratio.

    Args:
        data (Theorems): The data object containing machines.
        algo (str): The algorithm to use ("ucb1", "ucb2", "en_greedy", "ucb1_normal", "ucb_tuned").
        number_of_pulls (int): The total number of pulls per simulation.
        number_of_simulations (int): Number of simulations to average over (default 100).
        alpha (float): The alpha parameter for UCB2 (default 0.0001).
        c (float): The c parameter for ε-greedy (default 0.1).
        d (float): The d parameter. If None, set to the difference between the
                   highest and second highest mean values.

    Returns:
        tuple[float, float]: (average_regret, average_best_machine_ratio)
    """
    # If d is None, calculate it as the gap between the top two means
    if d is None:
        means = sorted(set(m[1] for m in data.machines), reverse=True)
        if len(means) >= 2:
            d = means[0] - means[1]
        else:
            d = 0.0

    total_regret = 0.0
    total_ratio = 0.0

    for _ in range(number_of_simulations):
        data.reset()
        if algo == "ucb1":
            data.ucb1(number_of_pulls)
        elif algo == "ucb2":
            data.ucb2(number_of_pulls, alpha)
        elif algo == "en_greedy":
            data.en_greedy(number_of_pulls, c, d)
        elif algo == "ucb1_normal":
            data.ucb1_normal(number_of_pulls)
        elif algo == "ucb_tuned":
            data.ucb_tuned(number_of_pulls)
        total_regret += data.regret()
        total_ratio += data.best_machine_ratio()

    avg_regret = total_regret / number_of_simulations
    avg_ratio = total_ratio / number_of_simulations
    return avg_regret, avg_ratio

def run_simulations(n: int, data: Theorems, algo: str, number_of_simulations: int = 100, 
            alpha: float = 0.0001, c: float = 0.1, d: float = None) -> tuple[list[int], list[float], list[float]]:
    """
    Runs simulations for logarithmically spaced number_of_pulls values.
    Uses exact powers of 10 (10^0, 10^1, ..., 10^n) and divides each
    interval from 10^k to 10^(k+1) (for k >= 1) into 20 logarithmically spaced points.

    Args:
        n (int): Exponent upper bound. Pulls range from 10^0 to 10^n.
        data (Theorems): The data object containing machines.
        algo (str): The algorithm to use.
        number_of_simulations (int): Number of simulations per data point (default 100).
        alpha (float): The alpha parameter for UCB2.
        c (float): The c parameter for ε-greedy.
        d (float): The d parameter. If None, auto-calculated.

    Returns:
        tuple[list[int], list[float], list[float]]: (number_of_pulls_list, regrets, ratios)
    """
    import numpy as np

    # Generate logarithmically spaced play values
    all_plays = set()
    # Exact powers of 10: 10^0, 10^1, ..., 10^n
    for k in range(0, n + 1):
        all_plays.add(10 ** k)
    # 20 points per decade from 10^1 onward
    for k in range(1, n):
        decade_points = np.logspace(k, k + 1, num=20, endpoint=True)
        for val in decade_points:
            all_plays.add(int(round(val)))
    number_of_pulls_list = sorted(all_plays)

    regrets = []
    ratios = []
    for pulls in number_of_pulls_list:

        # Print info about the simulation
        machines_info = [(m[0], m[1]) for m in data.machines]
        params = f"algo={algo}, pulls={pulls}, simulations={number_of_simulations}"
        if algo == "ucb2":
            params += f", alpha={alpha}"
        elif algo == "en_greedy":
            params += f", c={c}, d={d}"
        print(f"[run_simulations] Starting: {params}")
        print(f"  Machines: {machines_info}")
        avg_regret, avg_ratio = simulate(data, algo, pulls, number_of_simulations, alpha, c, d)
        regrets.append(avg_regret)
        ratios.append(avg_ratio)

    return number_of_pulls_list, regrets, ratios