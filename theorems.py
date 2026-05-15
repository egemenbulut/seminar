import statistics
from typing import List
import random
import math
import statistics

class Theorems():

    def __init__(self, number_of_machines : int, mean_list : List[float]) -> None:
        """
        This method is the constructor of the class.
        It initializes the machines list. The list contains tuples of (machine_id, mean, number_of_pulls, reward_list).
        If the number of machines is greater than the length of the mean list, the last mean is used for the remaining machines.
        
        Args:
            number_of_machines (int): The number of machines.
            mean_list (List[float]): The list of means of the machines.
        
        Returns:
            None

        Example:
            >>> theorems = Theorems(number_of_machines=3, mean_list=[0.1, 0.2, 0.3])
            >>> theorems.machines
            [(1, 0.1, 0, []), (2, 0.2, 0, []), (3, 0.3, 0, [])]

            >>> theorems = Theorems(number_of_machines=5, mean_list=[0.1, 0.2, 0.3])
            >>> theorems.machines
            [(1, 0.1, 0, []), (2, 0.2, 0, []), (3, 0.3, 0, []), (4, 0.3, 0, []), (5, 0.3, 0, [])]
        """
        self.machines = []
        for i in range(1, number_of_machines + 1):
            if i <= len(mean_list):
                mean = mean_list[i - 1]
            else:
                mean = mean_list[-1]
            self.machines.append((i, mean, 0, []))

    def reset(self) -> None:
        """
        This method resets the machines list.
        """
        for i in range(len(self.machines)):
            self.machines[i] = (self.machines[i][0], self.machines[i][1], 0, [])

    def pull_machine(self, machine_id : int) -> None:
        """
        Pulls the machine with the given id.
        Increments the number_of_pulls by 1 and appends 1 (reward) or 0 (no reward)
        to the reward_list with a probability equal to the machine's mean value.

        Args:
            machine_id (int): The id of the machine to pull.
        """        
        for i in range(len(self.machines)):
            if self.machines[i][0] == machine_id:
                mid, mean, pulls, reward_list = self.machines[i]
                pulls += 1
                if random.random() < mean:
                    reward_list.append(1)
                else:
                    reward_list.append(0)
                self.machines[i] = (mid, mean, pulls, reward_list)
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
            for mid, mean, pulls, reward_list in self.machines:
                avg_reward = statistics.mean(reward_list)
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
            for mid, mean, pulls, reward_list in self.machines:
                avg_reward = statistics.mean(reward_list)
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
    def en_greedy(self) -> None:
        pass

    #Theorem-4
    def ucb1_normal(self) -> None:
        pass
    
    #Extra 
    def ucb_tuned(self, number_of_pulls: int) -> None:
        """
        Implements the UCB-Tuned algorithm.
        First, each machine is pulled once. Then, until number_of_pulls is reached,
        the machine with the highest UCB-Tuned score is selected and pulled.
        UCB-Tuned score = average_reward + sqrt((ln(n) / pulls) * min(0.25, V(machine)))

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
            for idx, (mid, mean, pulls, reward_list) in enumerate(self.machines):
                avg_reward = statistics.mean(reward_list)
                ucb_tuned_score = avg_reward + math.sqrt((math.log(total_pulls) / pulls) * min(0.25, self.v(idx, total_pulls)))
                if ucb_tuned_score > best_score or (ucb_tuned_score == best_score and mid < best_id):
                    best_score = ucb_tuned_score
                    best_id = mid
            self.pull_machine(best_id)

    def v(self, machine_id: int, total_pulls : int) -> float:
        mid, mean, pulls, reward_list = self.machines[machine_id]
        return ((1/pulls) * sum(reward**2 for reward in reward_list)) - statistics.mean(reward_list)**2 + math.sqrt((2 * math.log(total_pulls)) / pulls)
 
        
