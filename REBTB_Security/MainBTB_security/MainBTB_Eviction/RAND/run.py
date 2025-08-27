import matplotlib.pyplot as plt
import csv
import os
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
    """Read CSV and return two lists: x_values, y_values."""
    x_values, y_values = [], []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            x_values.append(float(row[0]))
            y_values.append(float(row[1]))
    return x_values, y_values

def plot_eviction_case(param_name, param_values, fixed_params, x_start, x_end, x_step, filename, add_inset=False):
    colors = ['blue', 'green', 'orange', 'red']
    markers = ['*', 'o', 's', 'd']

    plt.figure(figsize=(14,6))
    all_data = []

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

        theory_csv = f"data/theory_i{params.get('i')}_t{params.get('t')}_w{params.get('w')}_{x_start}_{x_end}.csv"
        sim_csv = f"data/sim_i{params.get('i')}_t{params.get('t')}_w{params.get('w')}_{x_start}_{x_end}.csv"

        if os.path.exists(theory_csv) and os.path.exists(sim_csv):
            N_theory, cdf_theory = read_csv(theory_csv)
            xx_ticks, cdf_sim_ticks = read_csv(sim_csv)
            N_values = list(range(x_start, x_end+1, x_step))
        else:
            N_values, N_theory, cdf_theory, xx_ticks, cdf_sim_ticks = simulate_eviction(
                i=params.get('i',10),
                t=params.get('t',5),
                w=params.get('w',12),
                x_start=x_start,
                x_end=x_end,
                x_step=x_step,
                save_pdf='temp.pdf'
            )
            save_csv(theory_csv, N_theory, cdf_theory)
            save_csv(sim_csv, xx_ticks, cdf_sim_ticks)

        legend_str = f"RAND, {params['i']}-bit index, {params['t']}-bit tag, {params['w']}-way"
        plt.plot(N_theory, cdf_theory, color=color, linewidth=2, label=f"{legend_str}, no offset theo.")
        plt.scatter(xx_ticks, cdf_sim_ticks, color=color, s=60, marker=marker, alpha=0.5,
                    label=f"{legend_str}, 5-bit offset sim.")

        all_data.append((N_theory, cdf_theory, xx_ticks, cdf_sim_ticks, color, marker))

    x_labels = [f"{N//1000}k" for N in N_values]
    plt.xlabel("# of Trials", fontsize=20)
    plt.ylabel("Probability of the Target is Evicted", fontsize=20)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(N_values, x_labels, rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlim(x_start, x_end)
    plt.ylim(0,1)
    plt.legend(fontsize=16, framealpha=0.5)

    if add_inset:
        axins = inset_axes(plt.gca(), width="40%", height="40%", loc='upper right')
        axins.patch.set_alpha(0.3)
        for N_theory, cdf_theory, xx_ticks, cdf_sim_ticks, color, marker in all_data:
            axins.plot(N_theory, cdf_theory, color=color, linewidth=2)
            axins.scatter(xx_ticks, cdf_sim_ticks, color=color, s=60, marker=marker, alpha=0.5)
        axins.set_xlim(2000, 4000)
        axins.set_ylim(0.4, 0.6)
        axins.grid(True, linestyle='--', alpha=0.5)

    plt.savefig(f"figures/{filename}", bbox_inches='tight')
    plt.close()


# --- Example cases ---
plot_eviction_case(
    param_name='t',
    param_values=[5,7,9,11],
    fixed_params={'i':10,'w':12},
    x_start=0, x_end=16000, x_step=2000,
    filename='case1_i10_w12_t5-11.pdf',
)

plot_eviction_case(
    param_name=['i','w'],
    param_values=[(10,12), (9,24), (8,48), (7,96)],
    fixed_params={'t':9},
    x_start=0, x_end=30000, x_step=2000,
    filename='case_multi_iw.pdf',
)
