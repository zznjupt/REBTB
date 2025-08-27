import matplotlib.pyplot as plt
import csv
import os
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from eviction_sim import simulate_eviction  # Your parameterized script

# Ensure folders exist
os.makedirs('data', exist_ok=True)
os.makedirs('figures', exist_ok=True)

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

def plot_eviction_case(param_name, param_values, fixed_params, x_start, x_end, x_step, filename, add_inset=False):
    """Plot eviction CDF for a range of parameter values."""
    colors = ['blue', 'green', 'orange', 'red']
    markers = ['*', 'o', 's', 'd']

    plt.figure(figsize=(14,6))

    for idx, val in enumerate(param_values):
        color = colors[idx % len(colors)]
        marker = markers[idx % len(markers)]

        # Merge fixed params with varying one(s)
        params = fixed_params.copy()
        if isinstance(val, tuple):
            if isinstance(param_name, (list, tuple)):
                for k, v in zip(param_name, val):
                    params[k] = v
            else:
                raise ValueError("If param_values is tuple, param_name must be list/tuple of keys.")
        else:
            params[param_name] = val

        # Construct CSV filenames
        theory_csv = f"data/theory_i{params.get('i')}_t{params.get('t')}_w{params.get('w')}.csv"
        sim_csv = f"data/sim_i{params.get('i')}_t{params.get('t')}_w{params.get('w')}.csv"

        if os.path.exists(theory_csv) and os.path.exists(sim_csv):
            N_theory, cdf_theory = read_csv(theory_csv)
            xx_ticks, cdf_sim_ticks = read_csv(sim_csv)
        else:
            N_values, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks = simulate_eviction(
                i=params.get('i',10),
                t=params.get('t',5),
                w=params.get('w',12),
                x_start=x_start,
                x_end=x_end,
                x_step=x_step,
                save_pdf='temp.pdf'  # Temporary, not used
            )
            save_csv(theory_csv, N_theory, cdf_theory)
            save_csv(sim_csv, xx_ticks, cdf_sim_ticks)

        # Full legend string
        legend_str = f"LRU, {params['i']}-bit index, {params['t']}-bit tag, {params['w']}-way"

        # Plot theoretical line and simulated points
        plt.plot(N_theory, cdf_theory, color=color, linewidth=2, label=f"{legend_str} theo.")
        plt.scatter(xx_ticks, cdf_sim_ticks, color=color, s=60, marker=marker, label=f"{legend_str} sim.", alpha=0.5)

    # x_labels = [f"{N//1000}k" for N in N_theory]
    plt.xlabel("# of Trials", fontsize=20)
    plt.ylabel("Probability of the Target is Evicted", fontsize=20)

    plt.grid(True, linestyle='--', alpha=0.5)
    # plt.xticks(N_theory, x_labels, rotation=45, fontsize=16)
    x_ticks = list(range(x_start, x_end + 1, x_step))
    x_labels = [f"{x//1000}k" for x in x_ticks]
    plt.xticks(x_ticks, x_labels, rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlim(x_start, x_end)
    plt.ylim(0,1)
    plt.legend(fontsize=16, framealpha=0.5)

    # Add inset if requested
    if add_inset:
        axins = inset_axes(plt.gca(), width="40%", height="40%", loc='upper right')
        axins.patch.set_alpha(0.3)
        for idx, val in enumerate(param_values):
            color = colors[idx % len(colors)]
            marker = markers[idx % len(markers)]
            params = fixed_params.copy()
            if isinstance(val, tuple):
                for k, v in zip(param_name, val):
                    params[k] = v
            else:
                params[param_name] = val

            theory_csv = f"data/theory_i{params.get('i')}_t{params.get('t')}_w{params.get('w')}.csv"
            sim_csv = f"data/sim_i{params.get('i')}_t{params.get('t')}_w{params.get('w')}.csv"
            if os.path.exists(theory_csv) and os.path.exists(sim_csv):
                N_theory, cdf_theory = read_csv(theory_csv)
                xx_ticks, cdf_sim_ticks = read_csv(sim_csv)
            else:
                _, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks = simulate_eviction(
                    i=params.get('i',10),
                    t=params.get('t',5),
                    w=params.get('w',12),
                    x_start=x_start,
                    x_end=x_end,
                    x_step=x_step,
                    save_pdf='temp.pdf'
                )

            axins.plot(N_theory, cdf_theory, color=color, linewidth=2)
            axins.scatter(xx_ticks, cdf_sim_ticks, color=color, s=60, marker=marker, alpha=0.5)
        axins.set_xlim(2000, 4000)
        axins.set_ylim(0.4, 0.6)
        axins.grid(True, linestyle='--', alpha=0.5)

    plt.savefig(f"figures/{filename}", bbox_inches='tight')
    plt.close()


# --- Example usage ---
plot_eviction_case(
    param_name='t',
    param_values=[5,7,9,11],
    fixed_params={'i':9,'w':6},
    x_start=0, x_end=8000, x_step=1000,
    filename='case1_i9_w6_t8-10-12.pdf',
)

plot_eviction_case(
    param_name=['i','w'],
    param_values=[(10,6), (9,12), (8,24), (7,48)],
    fixed_params={'t':11},
    x_start=0, x_end=15000, x_step=1000,
    filename='case_multi.pdf'
)
