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
# e_n-greedy with different c values tested on distribution 1 (easy 2-armed)
eng1_005 = simulation.run_simulations(5, data1, "en_greedy", c=0.05, d=0.3)
eng1_010 = simulation.run_simulations(5, data1, "en_greedy", c=0.10, d=0.3)
eng1_015 = simulation.run_simulations(5, data1, "en_greedy", c=0.15, d=0.3)
eng1_020 = simulation.run_simulations(5, data1, "en_greedy", c=0.20, d=0.3)
graphs.multi_regret_plot([
    (eng1_005[0], eng1_005[1], "ε-GREEDY c=0.05"),
    (eng1_010[0], eng1_010[1], "ε-GREEDY c=0.10"),
    (eng1_015[0], eng1_015[1], "ε-GREEDY c=0.15"),
    (eng1_020[0], eng1_020[1], "ε-GREEDY c=0.20")
], title="ε-GREEDY c Comparison (Dist 1)", filename="en_greedy_c_dist1_regret")
graphs.multi_best_machine_ratio_plot([
    (eng1_005[0], eng1_005[2], "ε-GREEDY c=0.05"),
    (eng1_010[0], eng1_010[2], "ε-GREEDY c=0.10"),
    (eng1_015[0], eng1_015[2], "ε-GREEDY c=0.15"),
    (eng1_020[0], eng1_020[2], "ε-GREEDY c=0.20")
], title="ε-GREEDY c Comparison (Dist 1)", filename="en_greedy_c_dist1_ratio")
print("Done with Distribution 1.")


# e_n-greedy with different c values tested on distribution 2 (hard 2-armed)
eng2_005 = simulation.run_simulations(5, data2, "en_greedy", c=0.05, d=0.1)
eng2_010 = simulation.run_simulations(5, data2, "en_greedy", c=0.10, d=0.1)
eng2_015 = simulation.run_simulations(5, data2, "en_greedy", c=0.15, d=0.1)
eng2_020 = simulation.run_simulations(5, data2, "en_greedy", c=0.20, d=0.1)
graphs.multi_regret_plot([
    (eng2_005[0], eng2_005[1], "ε-GREEDY c=0.05"),
    (eng2_010[0], eng2_010[1], "ε-GREEDY c=0.10"),
    (eng2_015[0], eng2_015[1], "ε-GREEDY c=0.15"),
    (eng2_020[0], eng2_020[1], "ε-GREEDY c=0.20")
], title="ε-GREEDY c Comparison (Dist 2)", filename="en_greedy_c_dist2_regret")
graphs.multi_best_machine_ratio_plot([
    (eng2_005[0], eng2_005[2], "ε-GREEDY c=0.05"),
    (eng2_010[0], eng2_010[2], "ε-GREEDY c=0.10"),
    (eng2_015[0], eng2_015[2], "ε-GREEDY c=0.15"),
    (eng2_020[0], eng2_020[2], "ε-GREEDY c=0.20")
], title="ε-GREEDY c Comparison (Dist 2)", filename="en_greedy_c_dist2_ratio")
print("Done with Distribution 2.")

# e_n-greedy with different c values tested on distribution 12 (varied 10-armed) -> data5
eng5_005 = simulation.run_simulations(5, data5, "en_greedy", c=0.05, d=0.1)
eng5_010 = simulation.run_simulations(5, data5, "en_greedy", c=0.10, d=0.1)
eng5_015 = simulation.run_simulations(5, data5, "en_greedy", c=0.15, d=0.1)
eng5_020 = simulation.run_simulations(5, data5, "en_greedy", c=0.20, d=0.1)
graphs.multi_regret_plot([
    (eng5_005[0], eng5_005[1], "ε-GREEDY c=0.05"),
    (eng5_010[0], eng5_010[1], "ε-GREEDY c=0.10"),
    (eng5_015[0], eng5_015[1], "ε-GREEDY c=0.15"),
    (eng5_020[0], eng5_020[1], "ε-GREEDY c=0.20")
], title="ε-GREEDY c Comparison (Dist 12)", filename="en_greedy_c_dist12_regret")
graphs.multi_best_machine_ratio_plot([
    (eng5_005[0], eng5_005[2], "ε-GREEDY c=0.05"),
    (eng5_010[0], eng5_010[2], "ε-GREEDY c=0.10"),
    (eng5_015[0], eng5_015[2], "ε-GREEDY c=0.15"),
    (eng5_020[0], eng5_020[2], "ε-GREEDY c=0.20")
], title="ε-GREEDY c Comparison (Dist 12)", filename="en_greedy_c_dist12_ratio")
print("Done with Distribution 12.")

# e_n-greedy with different c values tested on distribution 14 (hard high-variance 10-armed) -> data7
eng7_010 = simulation.run_simulations(5, data7, "en_greedy", c=0.10, d=0.1)
eng7_020 = simulation.run_simulations(5, data7, "en_greedy", c=0.20, d=0.1)
eng7_030 = simulation.run_simulations(5, data7, "en_greedy", c=0.30, d=0.1)
eng7_040 = simulation.run_simulations(5, data7, "en_greedy", c=0.40, d=0.1)
graphs.multi_regret_plot([
    (eng7_010[0], eng7_010[1], "ε-GREEDY c=0.10"),
    (eng7_020[0], eng7_020[1], "ε-GREEDY c=0.20"),
    (eng7_030[0], eng7_030[1], "ε-GREEDY c=0.30"),
    (eng7_040[0], eng7_040[1], "ε-GREEDY c=0.40")
], title="ε-GREEDY c Comparison (Dist 14)", filename="en_greedy_c_dist14_regret")
graphs.multi_best_machine_ratio_plot([
    (eng7_010[0], eng7_010[2], "ε-GREEDY c=0.10"),
    (eng7_020[0], eng7_020[2], "ε-GREEDY c=0.20"),
    (eng7_030[0], eng7_030[2], "ε-GREEDY c=0.30"),
    (eng7_040[0], eng7_040[2], "ε-GREEDY c=0.40")
], title="ε-GREEDY c Comparison (Dist 14)", filename="en_greedy_c_dist14_ratio")
print("Done with Distribution 14.")
"""

"""
# UCB-Tuned vs UCB1 (2)

ucb_tuned_2 = simulation.run_simulations(5, data2, "ucb_tuned")
ucb1_2 = simulation.run_simulations(5, data2, "ucb1")

graphs.multi_regret_plot([(ucb_tuned_2[0], ucb_tuned_2[1], "UCB-Tuned"), 
    (ucb1_2[0], ucb1_2[1], "UCB1")], 
    title = "UCB-Tuned vs UCB1 (Dist 2)", filename = "ucb_tuned_vs_ucb1_regret_dist2")

graphs.multi_best_machine_ratio_plot([(ucb_tuned_2[0], ucb_tuned_2[2], "UCB-Tuned"), 
    (ucb1_2[0], ucb1_2[2], "UCB1")], 
    title = "UCB-Tuned vs UCB1 (Dist 2)", filename = "ucb_tuned_vs_ucb1_ratio_dist2") 
"""

"""
# UCB-Tuned vs UCB1 (2)

ucb_tuned_2 = simulation.run_simulations(5, data2, "ucb_tuned")
ucb1_2 = simulation.run_simulations(5, data2, "ucb1")

graphs.multi_regret_plot([(ucb_tuned_2[0], ucb_tuned_2[1], "UCB-Tuned"), 
    (ucb1_2[0], ucb1_2[1], "UCB1")], 
    title = "UCB-Tuned vs UCB1 (Dist 2)", filename = "ucb_tuned_vs_ucb1_regret_dist2")

graphs.multi_best_machine_ratio_plot([(ucb_tuned_2[0], ucb_tuned_2[2], "UCB-Tuned"), 
    (ucb1_2[0], ucb1_2[2], "UCB1")], 
    title = "UCB-Tuned vs UCB1 (Dist 2)", filename = "ucb_tuned_vs_ucb1_ratio_dist2") 
"""