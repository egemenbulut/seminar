from typing import List
class Theorems():

    def __init__(self, number_of_machines : int, mean_list : List[float]) -> None:
        """
        This method is the constructor of the class.
        It initializes the machines list. The list contains tuples of (machine_id, mean, number_of_pulls, total_reward).
        If the number of machines is greater than the length of the mean list, the last mean is used for the remaining machines.
        
        Args:
            number_of_machines (int): The number of machines.
            mean_list (List[float]): The list of means of the machines.
        
        Returns:
            None

        Example:
            >>> theorems = Theorems(number_of_machines=3, mean_list=[0.1, 0.2, 0.3])
            >>> theorems.machines
            [(1, 0.1, 0, 0), (2, 0.2, 0, 0), (3, 0.3, 0, 0)]

            >>> theorems = Theorems(number_of_machines=5, mean_list=[0.1, 0.2, 0.3])
            >>> theorems.machines
            [(1, 0.1, 0, 0), (2, 0.2, 0, 0), (3, 0.3, 0, 0), (4, 0.3, 0, 0), (5, 0.3, 0, 0)]
        """
        self.machines = []
        for i in range(1, number_of_machines + 1):
            if i <= len(mean_list):
                mean = mean_list[i - 1]
            else:
                mean = mean_list[-1]
            self.machines.append((i, mean, 0, 0))

    def reset(self) -> None:
        """
        This method resets the machines list.
        """
        for i in range(len(self.machines)):
            self.machines[i] = (self.machines[i][0], self.machines[i][1], 0, 0)

    def pull_machine(self, machine_id : int) -> bool:
        """
        Pulls the machine with the given id.
        Increments the number_of_pulls by 1 and increments total_reward by 1
        with a probability equal to the machine's mean value.

        Args:
            machine_id (int): The id of the machine to pull.
        """
        import random
        
        rewarded = False
        for i in range(len(self.machines)):
            if self.machines[i][0] == machine_id:
                mid, mean, pulls, reward = self.machines[i]
                pulls += 1
                if random.random() < mean:
                    rewarded = True
                    reward += 1
                self.machines[i] = (mid, mean, pulls, reward)
                break
        return rewarded
    
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
        import math

        # Phase 1: Pull each machine once
        for machine in self.machines:
            self.pull_machine(machine[0])

        # Phase 2: Pull the machine with the highest UCB1 score
        for _ in range(number_of_pulls - len(self.machines)):
            total_pulls = sum(m[2] for m in self.machines)
            best_score = -1
            best_id = -1
            for mid, mean, pulls, reward in self.machines:
                avg_reward = reward / pulls
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
            for mid, mean, pulls, reward in self.machines:
                avg_reward = reward / pulls
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
        import math
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
        import math
        t = self.tau(r, alpha)
        return math.sqrt((1 + alpha) * math.log(math.e * n / t) / (2 * t))
 
    #Theorem-3
    def en_greedy(self) -> None:
        pass

    #Theorem-4
    def ucb1_normal(self) -> None:
        pass
    
    #Extra 
    def ucb_tuned(self) -> None:
        pass