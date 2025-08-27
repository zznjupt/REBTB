import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Configuration: file paths and labels ---
baseline_file = "./ipc_data/baseline.txt"          # Baseline IPC data file
compare_files = [
    "./ipc_data/random.txt",
    "./ipc_data/rekey4.txt",                        
    "./ipc_data/rekey1.txt",                         
    "./ipc_data/rekey3.txt",
    "./ipc_data/rekey2.txt"
]
compare_labels = [
    "Randomazition without Rekeying",
    "P = 0.5, TH_MainBTB = 230000, TH_IBP = 230000",
    "P = 0.2, TH_MainBTB = 230000, TH_IBP = 230000",  
    "P = 0.5, TH_MainBTB = 16500, TH_IBP = 2900", 
    "P = 0.2, TH_MainBTB = 13000, TH_IBP = 2000",     
]  
output_pdf = "ipc_decrease_multi_with_avg.pdf"     # Output PDF file

# --- Read baseline file ---
df_base = pd.read_csv(baseline_file, sep=r'\s+', engine='python')
df_base = df_base[~df_base['Bench/IPC'].isin(['avg.', '---------'])]
df_base['x86'] = pd.to_numeric(df_base['x86'], errors='coerce')
df_base = df_base.dropna(subset=['x86'])

benches = list(df_base['Bench/IPC'])   
baseline_ipc = df_base['x86']          

# --- Prepare figure ---
plt.figure(figsize=(24, 6))   # Slightly narrower than before
width = 0.8 / len(compare_files)  # Make bars thicker
x = list(range(len(benches)))     

# --- Loop through all comparison files ---
avg_values = []  
bar_colors = []  

for i, (file, label) in enumerate(zip(compare_files, compare_labels)):
    df_cmp = pd.read_csv(file, sep=r'\s+', engine='python')
    df_cmp = df_cmp[~df_cmp['Bench/IPC'].isin(['avg.', '---------'])]
    df_cmp['x86'] = pd.to_numeric(df_cmp['x86'], errors='coerce')
    df_cmp = df_cmp.dropna(subset=['x86'])

    compare_ipc = df_cmp['x86']
    ipc_drop_percent = (baseline_ipc - compare_ipc) / baseline_ipc * 100
    avg_value = ipc_drop_percent.mean()
    avg_values.append(avg_value)

    bars = plt.bar([p + i*width for p in x], ipc_drop_percent, width=width, label=label)
    bar_colors.append(bars[0].get_facecolor())

#     for bar, value in zip(bars, ipc_drop_percent):
#         plt.text(bar.get_x() + bar.get_width()/2, value + 0.1, f'{value:.1f}', 
#                  ha='center', fontsize=6)

# --- Plot average values with arrows pointing to left-upper space ---
avg_x = len(benches)
for i, avg_value in enumerate(avg_values):
    bar = plt.bar(avg_x + i*width, avg_value, width=width, color=bar_colors[i], alpha=0.8)[0]

    # set different offsets for higher bars to avoid overlap
    if avg_value < 1:
        dx, dy = -0.2, 0.5
    elif avg_value < 3:
        dx, dy = -0.2, 0.5
    elif avg_value < 4.6:
        dx, dy = -0.2, 0.5
    else:
        dx, dy = -0.2, 1.2

    # annotate with arrow
    plt.annotate(f'{avg_value:.1f}',
                 xy=(bar.get_x() + bar.get_width()/2, avg_value),  # 指向柱顶
                 xytext=(bar.get_x() + bar.get_width()/2 + dx, avg_value + dy),  # 左上方显示
                 ha='right', va='bottom',
                 fontsize=12,
                 arrowprops=dict(arrowstyle='-|>', color='black', lw=1.2))



# --- Update x-axis labels ---
benches_with_avg = benches + ["Average"]
total_width = width * len(compare_files)
mid_offset = total_width / 2 - width / 2
plt.xticks([p + mid_offset for p in range(len(benches_with_avg))], 
           benches_with_avg, rotation=45, fontsize=16, ha='right')

# --- Customize plot appearance ---
plt.ylabel("Normalized IPC Decrease (%)", fontsize=20)
plt.yticks(fontsize=16)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=16, framealpha=0.2, loc='upper left')

plt.tight_layout()
plt.xlim(-0.2, len(benches_with_avg)-0.2)  # Reduce left/right margin

# --- Save figure to PDF ---
plt.savefig(output_pdf)
plt.close()

print(f"Multi-file IPC decrease plot with arithmetic average saved to {output_pdf}")
