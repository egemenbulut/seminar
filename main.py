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
# UCB2 with different alpha values

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

"""
eng_005 = simulation.run_simulations(5, data2, "en_greedy", c=0.05, d=0.1)
eng_010 = simulation.run_simulations(5, data2, "en_greedy", c=0.10, d=0.1)
eng_015 = simulation.run_simulations(5, data2, "en_greedy", c=0.15, d=0.1)
eng_020 = simulation.run_simulations(5, data2, "en_greedy", c=0.20, d=0.1)
eng_025 = simulation.run_simulations(5, data2, "en_greedy", c=0.25, d=0.1)
eng_030 = simulation.run_simulations(5, data2, "en_greedy", c=0.30, d=0.1)

graphs.multi_regret_plot([
    (eng_005[0], eng_005[1], "ε-GREEDY c=0.05"),
    (eng_010[0], eng_010[1], "ε-GREEDY c=0.10"),
    (eng_015[0], eng_015[1], "ε-GREEDY c=0.15"),
    (eng_020[0], eng_020[1], "ε-GREEDY c=0.20"),
    (eng_025[0], eng_025[1], "ε-GREEDY c=0.25"),
    (eng_030[0], eng_030[1], "ε-GREEDY c=0.30"),
], title="ε-GREEDY c Comparison (Dist 2)", filename="en_greedy_c_dist2_regret")

graphs.multi_best_machine_ratio_plot([
    (eng_005[0], eng_005[1], "ε-GREEDY c=0.05"),
    (eng_010[0], eng_010[1], "ε-GREEDY c=0.10"),
    (eng_015[0], eng_015[1], "ε-GREEDY c=0.15"),
    (eng_020[0], eng_020[1], "ε-GREEDY c=0.20"),
    (eng_025[0], eng_025[1], "ε-GREEDY c=0.25"),
    (eng_030[0], eng_030[1], "ε-GREEDY c=0.30"),
], title="ε-GREEDY c Comparison (Dist 2)", filename="en_greedy_c_dist2_ratio")

print("Done.")

"""