from typing import List
import random
import math

class Theorems():

    def __init__(self, number_of_machines : int, mean_list : List[float]) -> None:
        """
        This method is the constructor of the class.
        It initializes the machines list. The list contains tuples of 
        (machine_id, mean, number_of_pulls, sum_reward, sum_reward_2).
        sum_reward keeps the total rewards we got from the machine.
        sum_reward_2 keeps the total squared rewards (needed for ucb_tuned variance).
        If the number of machines is greater than the length of the mean list, 
        the last mean is used for the remaining machines.
        
        Args:
            number_of_machines (int): The number of machines.
            mean_list (List[float]): The list of means of the machines.
        
        Returns:
            None
 
        Example:
            >>> theorems = Theorems(number_of_machines=3, mean_list=[0.1, 0.2, 0.3])
            >>> theorems.machines
            [(1, 0.1, 0, 0, 0), (2, 0.2, 0, 0, 0), (3, 0.3, 0, 0, 0)]
 
            >>> theorems = Theorems(number_of_machines=5, mean_list=[0.1, 0.2, 0.3])
            >>> theorems.machines
            [(1, 0.1, 0, 0, 0), (2, 0.2, 0, 0, 0), (3, 0.3, 0, 0, 0), (4, 0.3, 0, 0, 0), (5, 0.3, 0, 0, 0)]
        """
        self.machines = []
        for i in range(1, number_of_machines + 1):
            if i <= len(mean_list):
                mean = mean_list[i - 1]
            else:
                mean = mean_list[-1]
            self.machines.append((i, mean, 0, 0, 0))

    def reset(self) -> None:
        """
        This method resets the machines list.
        """
        for i in range(len(self.machines)):
            self.machines[i] = (self.machines[i][0], self.machines[i][1], 0, 0, 0)

    def pull_machine(self, machine_id : int) -> None:
        """
        Pulls the machine with the given id.
        Increments the number_of_pulls by 1.
        With probability equal to machine's mean we get reward 1, otherwise 0.
        We add the reward to sum_reward and the squared reward to sum_reward_2.

        Args:
            machine_id (int): The id of the machine to pull.
        """        
        for i in range(len(self.machines)):
            if self.machines[i][0] == machine_id:
                mid, mean, pulls, sum_reward, sum_reward_2 = self.machines[i]
                pulls += 1
                if random.random() < mean:
                    sum_reward += 1
                    sum_reward_2 += 1
                self.machines[i] = (mid, mean, pulls, sum_reward,sum_reward_2)
                break
    
    def regret(self) -> float:
        """
        Calculates the regret value.
        Regret = (best_mean * total_pulls) - sum(machine_j_pulls * machine_j_mean) for all machines.

        Returns:
            float: The regret value.
        """
        best_mean = max(m[1] for m in self.machines)
        total_pulls = sum(m[2] for m in self.machines)
        weighted_sum = sum(m[2] * m[1] for m in self.machines)
        return (best_mean * total_pulls) - weighted_sum

    def best_machine_ratio(self) -> float:
        """
        Calculates the ratio of plays on the best machine (highest mean) to total plays.

        Returns:
            float: The ratio (0.0 to 1.0). Returns 0.0 if no plays have been made.
        """
        best_mean = max(m[1] for m in self.machines)
        total_pulls = sum(m[2] for m in self.machines)
        if total_pulls == 0:
            return 0.0
        best_machine_pulls = sum(m[2] for m in self.machines if m[1] == best_mean)
        return best_machine_pulls / total_pulls

    #Theorem-1
    def ucb1(self, number_of_pulls: int) -> None:
        """
        Implements the UCB1 algorithm.
        First, each machine is pulled once. Then, until number_of_pulls is reached,
        the machine with the highest UCB1 score is selected and pulled.
        UCB1 score = average_reward + sqrt(2 * ln(total_pulls_so_far) / machine_pulls)

        Args:
            number_of_pulls (int): The total number of pulls to perform.
        """
        # Phase 1: Pull each machine once
        for machine in self.machines:
            self.pull_machine(machine[0])

        # Phase 2: Pull the machine with the highest UCB1 score
        for _ in range(number_of_pulls - len(self.machines)):
            total_pulls = sum(m[2] for m in self.machines)
            best_score = -1
            best_id = -1
            for mid, mean, pulls, sum_reward, sum_reward_2 in self.machines:
                avg_reward = sum_reward/pulls
                ucb1_score = avg_reward + math.sqrt(2 * math.log(total_pulls) / pulls)
                if ucb1_score > best_score or (ucb1_score == best_score and mid < best_id):
                    best_score = ucb1_score
                    best_id = mid
            self.pull_machine(best_id)

    #Theorem-2
    def ucb2(self, number_of_pulls: int, alpha: float) -> None:
        """
        Implements the UCB2 algorithm.
        Each machine has an r-value initialized to 0. First, each machine is pulled once.
        Then, the machine with the highest (average_reward + a_n_r) score is selected
        and pulled tau(r+1) - tau(r) times (or until number_of_pulls is reached).
        After that, the selected machine's r-value is incremented by 1.

        Args:
            number_of_pulls (int): The total number of pulls to perform.
            alpha (float): The alpha parameter for UCB2.
        """
        # Initialize r-values for each machine (keyed by machine id)
        r_values = {m[0]: 0 for m in self.machines}

        # Phase 1: Pull each machine once
        for machine in self.machines:
            self.pull_machine(machine[0])

        remaining = number_of_pulls - len(self.machines)

        # Phase 2: Select and pull based on UCB2 score
        while remaining > 0:
            total_pulls = sum(m[2] for m in self.machines)
            best_score = -1
            best_id = -1
            for mid, mean, pulls, sum_reward, sum_reward_2 in self.machines:
                avg_reward = sum_reward/pulls
                score = avg_reward + self.a_n_r(total_pulls, r_values[mid], alpha)
                if score > best_score or (score == best_score and mid < best_id):
                    best_score = score
                    best_id = mid

            # Pull the selected machine tau(r+1) - tau(r) times
            r = r_values[best_id]
            pulls_to_do = min(self.tau(r + 1, alpha) - self.tau(r, alpha), remaining)
            for _ in range(pulls_to_do):
                self.pull_machine(best_id)
            remaining -= pulls_to_do

            # Increment r-value for the selected machine
            r_values[best_id] += 1

    def tau(self, r: int, alpha: float) -> int:
        """
        Calculates tau = ceil((1 + alpha) ^ r).
        If the result is not an integer, it is rounded up to the next integer.

        Args:
            r (int): The r parameter.
            alpha (float): The alpha parameter.

        Returns:
            int: The tau value.
        """
        return math.ceil((1 + alpha) ** r)

    def a_n_r(self, n: int, r: int, alpha: float) -> float:
        """
        Calculates the exploration bonus for UCB2.
        a_n_r = sqrt((1 + alpha) * ln(e * n / tau(r, alpha)) / (2 * tau(r, alpha)))

        Args:
            n (int): The total number of pulls so far.
            r (int): The round number.
            alpha (float): The alpha parameter.

        Returns:
            float: The exploration bonus value.
        """
        t = self.tau(r, alpha)
        return math.sqrt((1 + alpha) * math.log(math.e * n / t) / (2 * t))
 
    #Theorem-3
    def en_greedy(self, number_of_pulls:int, c:float, d:float) -> None:
        # Notes on parameters:
        # number_of_pulls: total rounds to run
        # d: the smallest gap between the best arm and any other arm (0 < d ≤ min Δ_i)
        #    practically we set it to (best mean - second best mean)
        #    unlike UCBs you need o know the gap in advance -> weakness
        # c: control the exploration rate (how aggresively we explore)
        #    no formula given in paper, we tune it per distribution
        #    by trial and error (like in the paper)
        #    too small -> less exploration, fast growing regret early
        #    too big -> too much exploration, wasting pulls on suboptimal machines
          
        machine_id = [m[0] for m in self.machines]
        machine_count = len(self.machines)
        
        # main loop: n is the current play number, goes from 1 to number_of_pulls
        for n in range(1, number_of_pulls + 1):
            # epsilon_n is our exploration probability for this round
            # formula straight from the paper: min(1, cK / (d^2 * n))
            # early on n is small so epsilon_n is close to 1 -> lots of exploration
            # as n grows epsilon_n shrinks -> more exploitation
            epsilon_n = min(1.0, (c*machine_count)/((d**2)* n))
 
            if random.random() < epsilon_n:
                # Exploration: pick a random machine with probability epsilon_n 
                next_id = random.choice(machine_id)
            else:
                # Exploitation: pick the machine with the highest average reward so far
                best_avg = -1.0
                best_id = -1
 
                for mid, mean, pulls, sum_reward, sum_reward_2 in self.machines:
                    if pulls > 0:
                        avg_reward = sum_reward/pulls
                    else:
                        avg_reward = 0.0
                    # update best if this machine is strictly better
                    # or equal avg but lower id (same tie breaking as ucb1/ucb2)
                    if avg_reward > best_avg or (avg_reward == best_avg and mid < best_id):
                        best_avg = avg_reward
                        best_id = mid
                next_id = best_id
 
            # pull the chosen machine
            self.pull_machine(next_id)
    
    #Extra 
    def ucb_tuned(self, number_of_pulls: int) -> None:
        """
        Implements the UCB-Tuned algorithm.
        First, each machine is pulled once. Then, until number_of_pulls is reached,
        the machine with the highest UCB-Tuned score is selected and pulled.
        UCB-Tuned score = average_reward + sqrt((ln(n) / pulls) * min(0.25, Var(machine)))
        where Var is te sample variance plus a confidence term.

        Args:
            number_of_pulls (int): The total number of pulls to perform.
        """
        # Phase 1: Pull each machine once
        for machine in self.machines:
            self.pull_machine(machine[0])

        # Phase 2: Pull the machine with the highest UCB-Tuned score
        for _ in range(number_of_pulls - len(self.machines)):
            total_pulls = sum(m[2] for m in self.machines)
            best_score = -1
            best_id = -1
            for idx, (mid, mean, pulls, sum_reward, sum_reward_2) in enumerate(self.machines):
                avg_reward = sum_reward/pulls
                # variance estimate from paper:
                # Var_j(s) = (1/s) * sum_reward_2 - avg_reward^2 + sqrt(2lnt /s)
                var = (sum_reward_2/pulls) - (avg_reward**2) + math.sqrt((2*math.log(total_pulls))/pulls)
                # 0.25 is the variance upper bound for a Bernoulli Random Variable -> p(1-p) <= 1/4
                # so we bound our estimate at 0.25 to avoid blowing up when the estimate is bad
                ucb_tuned_score = avg_reward + math.sqrt((math.log(total_pulls)/pulls) * min(0.25, var))
                if ucb_tuned_score > best_score or (ucb_tuned_score == best_score and mid < best_id):
                    best_score = ucb_tuned_score
                    best_id = mid
            self.pull_machine(best_id)

