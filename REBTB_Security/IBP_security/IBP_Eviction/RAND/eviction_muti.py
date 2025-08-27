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

    N_values = np.arange(x_start, x_end + 1, x_step)
    N_theory = np.arange(x_start, x_end + 1, 10)

    # --- Theoretical CDF ---
    p_b = 1 / space_size
    p_new = (tag_space - w) / tag_space
    q = p_b * p_new / w
    cdf_theory = [(1 - (1 - q)**n)**num_targets for n in N_theory]

    # --- Simulated experiments ---
    trials = []
    for _ in range(num_experiments):
        targets = [np.random.randint(0, space_size) for _ in range(num_targets)]
        target_ways = [np.random.randint(0, w) for _ in range(num_targets)]
        buckets = [list(np.random.choice(range(tag_space), size=w, replace=False)) for _ in range(num_targets)]
        total_trials = 0
        evicted = [False] * num_targets

        while not all(evicted):
            total_trials += 1
            guess = np.random.randint(0, space_size)
            guess_tag = np.random.randint(0, tag_space)
            for idx, target in enumerate(targets):
                if evicted[idx]:
                    continue
                if guess == target:
                    if guess_tag not in buckets[idx]:
                        evict_idx = np.random.randint(w)
                        buckets[idx][evict_idx] = guess_tag
                        if evict_idx == target_ways[idx]:
                            evicted[idx] = True
        trials.append(total_trials)

    xx_ticks = np.arange(x_start, x_end + 1, 100)
    cdf_sim_ticks = [np.mean(np.array(trials) <= ki) for ki in xx_ticks]

    return N_values, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks


def plot_multi_target_eviction(i=10, t=5, w=12, x_start=0, x_end=30000, x_step=2000,
                               num_experiments=1000, num_samples=50000,
                               save_pdf='Multi_Targets.pdf', max_targets=3):
    """Plot eviction CDF for 1~max_targets on the same figure, read CSV if available."""
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
            N_values = list(range(x_start, x_end+1, x_step))
        else:
            N_values, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks = simulate_eviction_core(
                i, t, w, num_experiments, num_samples, num_targets,
                x_start, x_end, x_step
            )
            save_csv(theory_csv, N_theory, cdf_theory)
            save_csv(sim_csv, xx_ticks, cdf_sim_ticks)

        color = colors[idx % len(colors)]
        marker = markers[idx % len(markers)]

        plt.plot(N_theory, cdf_theory, color=color, linewidth=2,
                 label=f"RAND, {i}-bit index, {t}-bit tag, {w}-way, {num_targets}-target(s) theo.")
        plt.scatter(xx_ticks, cdf_sim_ticks, color=color, s=60, marker=marker,
                    alpha=0.7,
                    label=f"RAND, {i}-bit index, {t}-bit tag, {w}-way, {num_targets}-target(s) sim.")

    x_labels = [f"{N//1000}k" for N in N_values]
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
