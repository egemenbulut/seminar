import os
import matplotlib.pyplot as plt

def regret_plot(number_of_pulls_list: list[int], regrets: list[float], title: str = "Regret vs Pulls", label: str = None, filename: str = None) -> None:
    """
    Plots regret values as a line chart with a logarithmic x-axis.

    Args:
        number_of_pulls_list (list[int]): The x-axis values (number of pulls).
        regrets (list[float]): The y-axis values (average regret).
        title (str): The title of the graph.
        label (str): Optional label for the line.
        filename (str): Custom filename (without extension). If None, derived from title.
    """
    plt.figure()
    plt.plot(number_of_pulls_list, regrets, label=label)
    plt.xscale("log")
    plt.xlabel("Plays")
    plt.ylabel("Regret")
    plt.title(title)
    if label:
        plt.legend()

    graphs_dir = os.path.join(os.path.dirname(__file__), "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    if filename is None:
        filename = title.lower().replace(" ", "_")
    plt.savefig(os.path.join(graphs_dir, f"{filename}.png"), dpi=150)

def best_machine_ratio_plot(number_of_pulls_list: list[int], ratios: list[float], title: str = "Best Machine Ratio vs Pulls", label: str = None, filename: str = None) -> None:
    """
    Plots best machine played ratio as a line chart with a logarithmic x-axis.

    Args:
        number_of_pulls_list (list[int]): The x-axis values (number of pulls).
        ratios (list[float]): The y-axis values (average best machine ratio).
        title (str): The title of the graph.
        label (str): Optional label for the line.
        filename (str): Custom filename (without extension). If None, derived from title.
    """
    plt.figure()
    plt.plot(number_of_pulls_list, [r * 100 for r in ratios], label=label)
    plt.xscale("log")
    plt.xlabel("Plays")
    plt.ylabel("% Best Machine Played")
    plt.title(title)
    if label:
        plt.legend()

    graphs_dir = os.path.join(os.path.dirname(__file__), "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    if filename is None:
        filename = title.lower().replace(" ", "_")
    plt.savefig(os.path.join(graphs_dir, f"{filename}.png"), dpi=150)

def multi_regret_plot(plots: list[tuple[list[int], list[float], str]], title: str = "Regret vs Plays", filename: str = None) -> None:
    """
    Plots multiple regret lines on the same graph with a logarithmic x-axis.

    Args:
        plots (list[tuple]): List of (number_of_pulls_list, regrets, label) tuples.
        title (str): The title of the graph.
        filename (str): Custom filename (without extension). If None, derived from title.
    """
    plt.figure()
    for number_of_pulls_list, regrets, label in plots:
        plt.plot(number_of_pulls_list, regrets, label=label)
    plt.xscale("log")
    plt.xlabel("Plays")
    plt.ylabel("Regret")
    plt.title(title)
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)

    graphs_dir = os.path.join(os.path.dirname(__file__), "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    if filename is None:
        filename = title.lower().replace(" ", "_")
    plt.savefig(os.path.join(graphs_dir, f"{filename}.png"), dpi=150)

def multi_best_machine_ratio_plot(plots: list[tuple[list[int], list[float], str]], title: str = "Best Machine Ratio vs Plays", filename: str = None) -> None:
    """
    Plots multiple best machine ratio lines on the same graph with a logarithmic x-axis.

    Args:
        plots (list[tuple]): List of (number_of_pulls_list, ratios, label) tuples.
        title (str): The title of the graph.
        filename (str): Custom filename (without extension). If None, derived from title.
    """
    plt.figure()
    for number_of_pulls_list, ratios, label in plots:
        plt.plot(number_of_pulls_list, [r * 100 for r in ratios], label=label)
    plt.xscale("log")
    plt.xlabel("Plays")
    plt.ylabel("% Best Machine Played")
    plt.title(title)
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)

    graphs_dir = os.path.join(os.path.dirname(__file__), "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    if filename is None:
        filename = title.lower().replace(" ", "_")
    plt.savefig(os.path.join(graphs_dir, f"{filename}.png"), dpi=150)