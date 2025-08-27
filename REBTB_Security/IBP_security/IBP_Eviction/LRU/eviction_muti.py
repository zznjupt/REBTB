import numpy as np
import matplotlib.pyplot as plt
import os
import csv

def save_csv(filename, x_values, y_values):
    """Save x and y values to a CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['x', 'y'])
        for x, y in zip(x_values, y_values):
            writer.writerow([x, y])

def read_csv(filename):
    """Read x and y values from a CSV file."""
    x_values, y_values = [], []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            x_values.append(int(row[0]))
            y_values.append(float(row[1]))
    return x_values, y_values

def simulate_eviction_core(i, t, w, num_experiments, num_samples, num_targets,
                           x_start, x_end, x_step):
    """Core logic of simulate_eviction, return results (without plotting)."""
    p = 1/(2**i)
    space_size = 2**i
    tag_space = 2**t

    # X-axis
    N_values = np.arange(x_start, x_end + 1, x_step)
    N_theory = np.arange(x_start, x_end + 1, 10)

    # --- Theoretical CDF for a single target ---
    T_samples = []
    for _ in range(num_samples):
        H = 0
        collected = set()
        while len(collected) < w:
            H += 1
            new_tag_prob = (tag_space - len(collected)) / tag_space
            if np.random.rand() < new_tag_prob:
                collected.add(len(collected))
        T = np.random.negative_binomial(H, p) + H
        T_samples.append(T)
    T_samples = np.array(T_samples)
    cdf_single = [np.mean(T_samples <= n) for n in N_theory]

    # Extend to multiple targets
    cdf_theory = [c**num_targets for c in cdf_single]

    # --- Simulated experiments (buckets initially empty) ---
    trials = []
    for _ in range(num_experiments):
        targets = [np.random.randint(0, space_size) for _ in range(num_targets)]
        labels_sets = [set() for _ in range(num_targets)]
        collected_counts = [0] * num_targets
        total_trials = 0

        while not all(c >= w for c in collected_counts):
            total_trials += 1
            guess = np.random.randint(0, space_size)
            guess_tag = np.random.randint(0, tag_space)
            for idx, target in enumerate(targets):
                if collected_counts[idx] >= w:
                    continue
                if guess == target and guess_tag not in labels_sets[idx]:
                    labels_sets[idx].add(guess_tag)
                    collected_counts[idx] += 1
        trials.append(total_trials)

    xx_ticks = np.arange(x_start, x_end + 1, 100)
    cdf_sim_ticks = [np.mean(np.array(trials) <= ki) for ki in xx_ticks]

    return N_values, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks


def plot_multi_target_eviction(i=10, t=5, w=12, x_start=0, x_end=30000, x_step=2000,
                               num_experiments=1000, num_samples=50000,
                               save_pdf='Multi_Targets.pdf', max_targets=3):
    """
    Plot eviction CDF for 1~max_targets on the same figure.
    If CSV exists, read from CSV; otherwise run simulation and save CSV.
    """
    os.makedirs("multi_data", exist_ok=True)
    plt.figure(figsize=(14,6))
    colors = ['blue', 'green', 'orange']
    markers = ['*', 'o', 's']

    for idx, num_targets in enumerate(range(1, max_targets+1)):
        theory_csv = f"multi_data/theory_targets{num_targets}.csv"
        sim_csv = f"multi_data/sim_targets{num_targets}.csv"

        if os.path.exists(theory_csv) and os.path.exists(sim_csv):
            N_theory, cdf_theory = read_csv(theory_csv)
            xx_ticks, cdf_sim_ticks = read_csv(sim_csv)
            # Generate N_values for x_labels from x_start:x_step:x_end
            N_values = np.arange(x_start, x_end + 1, x_step)
        else:
            N_values, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks = simulate_eviction_core(
                i, t, w, num_experiments, num_samples, num_targets,
                x_start, x_end, x_step
            )
            save_csv(theory_csv, N_theory, cdf_theory)
            save_csv(sim_csv, xx_ticks, cdf_sim_ticks)

        color = colors[idx % len(colors)]
        marker = markers[idx % len(markers)]

        # Plot curves
        plt.plot(N_theory, cdf_theory, color=color, linewidth=2,
                 label=f"LRU, {i}-bit index, {t}-bit tag, {w}-way, {num_targets}-target(s) theo.")
        plt.scatter(xx_ticks, cdf_sim_ticks, color=color, s=60,
                    marker=marker, alpha=0.7,
                    label=f"LRU, {i}-bit index, {t}-bit tag, {w}-way, {num_targets}-target(s) sim.")

    x_labels = [f"{N//500}k" for N in N_values]
    plt.xlabel("# of Trials", fontsize=20)
    plt.ylabel("Probability of the Target is Evicted", fontsize=20)
    plt.xlim(x_start, x_end)
    plt.ylim(0,1)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(N_values, x_labels, rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=16)
    plt.savefig(save_pdf, format='pdf', bbox_inches='tight')
    plt.close()


# --- Example usage ---
if __name__ == "__main__":
    plot_multi_target_eviction(i=9, t=11, w=6, x_start=0, x_end=8000, x_step=500,
                               save_pdf="./figures/Multi_Targets.pdf", max_targets=3)
