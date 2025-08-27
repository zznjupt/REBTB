import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def simulate_eviction(i=10, t=9, w=12, x_start=0, x_end=448000, x_step=32000,
                      num_experiments=1000, num_samples=50000, save_pdf='Target_Eviction.pdf'):
    """
    Simulate and plot the eviction CDF for given parameters.
    Defaults: i=10, t=5, w=12
    """
    space_size = 2**i
    tag_space = 2**t
    space = 2**(i+t)
    p = 0.515625/space
    # X-axis for theoretical CDF
    N_values = np.arange(x_start, x_end + 1, x_step)
    N_theory = np.arange(x_start, x_end + 1, 100)  # smaller step for smooth curve

    cdf_theory = 1 - (1 - p)**N_theory

    trials = []
    for _ in range(num_experiments):
        target = np.random.randint(0, space)
        offset = np.random.randint(0, 2**5)
        count = 0
        while True:
            count += 1
            guess = np.random.randint(0, space)
            guess_offset = np.random.randint(0, 2**5)
            if guess == target:  
                if guess_offset <= offset:
                    trials.append(count)
                    break

    trials = np.array(trials)
    xx_ticks = np.arange(x_start, x_end + 1, 1000)
    cdf_sim_ticks = [np.mean(trials <= ki) for ki in xx_ticks]

    x_labels = [f"{N//1000}k" for N in N_values]

    # --- Plot ---
    plt.figure(figsize=(12,6))
    plt.plot(N_theory, cdf_theory, color='blue', linewidth=2, label='Theoretical CDF')
    plt.scatter(xx_ticks, cdf_sim_ticks, color='red', s=80, marker='*', label='Simulated CDF')
    plt.xlabel("Number of Branch Executions (N)", fontsize=16)
    plt.ylabel("Probability of the Target being Evicted", fontsize=16)
    plt.title(f"{i}-bit index, {t}-bit tag, {w}-way", fontsize=18)
    plt.xlim(x_start, x_end)
    plt.ylim(0,1)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(N_values, x_labels, rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)
    plt.savefig(save_pdf, format='pdf', bbox_inches='tight')
    plt.close()

    return N_values, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks


# --- Run with default parameters if script is executed directly ---
if __name__ == "__main__":
    simulate_eviction()
