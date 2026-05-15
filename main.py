import theorems
import simulation
import graphs

data1 = theorems.Theorems(2, [0.9, 0.6])
data2 = theorems.Theorems(2, [0.9, 0.8])
data3 = theorems.Theorems(2, [0.55, 0.45])
data4 = theorems.Theorems(10, [0.9, 0.6])
data5 = theorems.Theorems(10, [0.9, 0.8, 0.8, 0.8, 0.7, 0.7, 0.7, 0.6])
data6 = theorems.Theorems(10, [0.9, 0.8])
data7 = theorems.Theorems(10, [0.55, 0.45])

"""
# UCP2 with different alpha values

ucb2_1 = simulation.run_simulations(5, data2, "ucb2", alpha=0.1)
ucb2_01 = simulation.run_simulations(5, data2, "ucb2", alpha=0.01)
ucb2_001 = simulation.run_simulations(5, data2, "ucb2", alpha=0.001)
ucb2_0001 = simulation.run_simulations(5, data2, "ucb2", alpha=0.0001)

graphs.multi_regret_plot([(ucb2_1[0], ucb2_1[1], "UCB2 α = 0.1"), 
    (ucb2_01[0], ucb2_01[1], "UCB2 α = 0.01"), 
    (ucb2_001[0], ucb2_001[1], "UCB2 α = 0.001"), 
    (ucb2_0001[0], ucb2_0001[1], "UCB2 α = 0.0001")], 
    title = "UCB2 Alpha Comparison", filename = "ucb2_alpha_comparison_regret")

graphs.multi_best_machine_ratio_plot([(ucb2_1[0], ucb2_1[2], "UCB2 α = 0.1"), 
    (ucb2_01[0], ucb2_01[2], "UCB2 α = 0.01"), 
    (ucb2_001[0], ucb2_001[2], "UCB2 α = 0.001"), 
    (ucb2_0001[0], ucb2_0001[2], "UCB2 α = 0.0001")], 
    title = "UCB2 Alpha Comparison", filename = "ucb2_alpha_comparison_ratio")    
"""

"""
# UCB-Tuned vs UCB1

ucb_tuned = simulation.run_simulations(5, data5, "ucb_tuned")
ucb1 = simulation.run_simulations(5, data5, "ucb1")

graphs.multi_regret_plot([(ucb_tuned[0], ucb_tuned[1], "UCB-Tuned"), 
    (ucb1[0], ucb1[1], "UCB1")], 
    title = "UCB-Tuned vs UCB1", filename = "ucb_tuned_vs_ucb1_regret")

graphs.multi_best_machine_ratio_plot([(ucb_tuned[0], ucb_tuned[2], "UCB-Tuned"), 
    (ucb1[0], ucb1[2], "UCB1")], 
    title = "UCB-Tuned vs UCB1", filename = "ucb_tuned_vs_ucb1_ratio")    
"""