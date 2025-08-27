# !/bin/bash

BP=$1

GEM5_DIR=/root/gem5
mkdir -p "$GEM5_DIR/run/stat_analysis/$BP"
IPC=$GEM5_DIR/run/stat_analysis/$BP/ipc.list
MPKI=$GEM5_DIR/run/stat_analysis/$BP/mpki.list

> "$IPC"
> "$MPKI"


# IPC 
printf "%-20s %-12s %-12s %-12s\n" "Bench/IPC" "riscv64" "x86" "aarch64" >> "$IPC"
printf "%-20s %-12s %-12s %-12s\n" "---------" "--------" "--------" "--------" >> "$IPC"

declare -A riscv_ipc_map
declare -A x86_ipc_map
declare -A arm_ipc_map
declare -A all_benchmarks

# RISCV IPC
while read -r stats_file; do
    bench_name=$(basename "$(dirname "$stats_file")")
    ipc=$(grep "^system.cpu.ipc" "$stats_file" | awk '{print $2}')
    riscv_ipc_map["$bench_name"]=$ipc
    all_benchmarks["$bench_name"]=1
done < <(find "$GEM5_DIR/run/output_riscv64/$BP" -type f -name "stats.txt")

# X86 IPC
while read -r stats_file; do
    bench_name=$(basename "$(dirname "$stats_file")")
    ipc=$(grep "^system.cpu.ipc" "$stats_file" | awk '{print $2}')
    x86_ipc_map["$bench_name"]=$ipc
    all_benchmarks["$bench_name"]=1
done < <(find "$GEM5_DIR/run/output_x86/$BP" -type f -name "stats.txt")

# AARCH64 IPC
while read -r stats_file; do
    bench_name=$(basename "$(dirname "$stats_file")")
    ipc=$(grep "^system.cpu.ipc" "$stats_file" | awk '{print $2}')
    arm_ipc_map["$bench_name"]=$ipc
    all_benchmarks["$bench_name"]=1
done < <(find "$GEM5_DIR/run/output_aarch64/$BP" -type f -name "stats.txt")


for bench in "${!all_benchmarks[@]}"; do
    riscv_ipc=${riscv_ipc_map[$bench]:-"N/A"}
    x86_ipc=${x86_ipc_map[$bench]:-"N/A"}
    arm_ipc=${arm_ipc_map[$bench]:-"N/A"}
    printf "%-20s %-12s %-12s %-12s\n" "$bench" "$riscv_ipc" "$x86_ipc" "$arm_ipc" >> "$IPC"
done


total_riscv=0; total_x86=0; total_arm=0
count_riscv=0; count_x86=0; count_arm=0

for bench in "${!all_benchmarks[@]}"; do
    val=${riscv_ipc_map[$bench]}
    [[ "$val" != "N/A" ]] && total_riscv=$(awk "BEGIN{print $total_riscv + $val}") && ((count_riscv++))
    val=${x86_ipc_map[$bench]}
    [[ "$val" != "N/A" ]] && total_x86=$(awk "BEGIN{print $total_x86 + $val}") && ((count_x86++))
    val=${arm_ipc_map[$bench]}
    [[ "$val" != "N/A" ]] && total_arm=$(awk "BEGIN{print $total_arm + $val}") && ((count_arm++))
done

avg_riscv=$(awk "BEGIN{printf \"%.6f\", $total_riscv / ($count_riscv ? $count_riscv : 1)}")
avg_x86=$(awk "BEGIN{printf \"%.6f\", $total_x86 / ($count_x86 ? $count_x86 : 1)}")
avg_arm=$(awk "BEGIN{printf \"%.6f\", $total_arm / ($count_arm ? $count_arm : 1)}")

printf "%-20s %-12s %-12s %-12s\n" "avg." "$avg_riscv" "$avg_x86" "$avg_arm" >> "$IPC"



printf "%-20s %-12s %-12s %-12s\n" "Bench/MPKI" "riscv64" "x86" "aarch64" >> "$MPKI"
printf "%-20s %-12s %-12s %-12s\n" "---------" "--------" "--------" "--------" >> "$MPKI"

declare -A riscv_mpki_map
declare -A x86_mpki_map
declare -A arm_mpki_map

# mispred_stat=system.cpu.branchPred.mispredictDueToPredictor_0::total
mispred_stat=system.cpu.commit.branchMispredicts

# RISCV MPKI
while read -r stats_file; do
    bench_name=$(basename "$(dirname "$stats_file")")
    mispredict=$(grep "^$mispred_stat" "$stats_file" | awk '{print $2}')
    if [[ -n "$mispredict" ]]; then
        mpki=$(awk "BEGIN{printf \"%.4f\", $mispredict/10000}")
    else
        mpki="N/A"
    fi
    riscv_mpki_map["$bench_name"]=$mpki
done < <(find "$GEM5_DIR/run/output_riscv64/$BP" -type f -name "stats.txt")

# X86 MPKI
while read -r stats_file; do
    bench_name=$(basename "$(dirname "$stats_file")")
    mispredict=$(grep "^$mispred_stat" "$stats_file" | awk '{print $2}')
    if [[ -n "$mispredict" ]]; then
        mpki=$(awk "BEGIN{printf \"%.4f\", $mispredict/10000}")
    else
        mpki="N/A"
    fi
    x86_mpki_map["$bench_name"]=$mpki
done < <(find "$GEM5_DIR/run/output_x86/$BP" -type f -name "stats.txt")

# AARCH64 MPKI
while read -r stats_file; do
    bench_name=$(basename "$(dirname "$stats_file")")
    mispredict=$(grep "^$mispred_stat" "$stats_file" | awk '{print $2}')
    if [[ -n "$mispredict" ]]; then
        mpki=$(awk "BEGIN{printf \"%.4f\", $mispredict/10000}")
    else
        mpki="N/A"
    fi
    arm_mpki_map["$bench_name"]=$mpki
done < <(find "$GEM5_DIR/run/output_aarch64/$BP" -type f -name "stats.txt")


for bench in "${!all_benchmarks[@]}"; do
    riscv_mpki=${riscv_mpki_map[$bench]:-"N/A"}
    x86_mpki=${x86_mpki_map[$bench]:-"N/A"}
    arm_mpki=${arm_mpki_map[$bench]:-"N/A"}
    printf "%-20s %-12s %-12s %-12s\n" "$bench" "$riscv_mpki" "$x86_mpki" "$arm_mpki" >> "$MPKI"
done


total_riscv=0; total_x86=0; total_arm=0
count_riscv=0; count_x86=0; count_arm=0

for bench in "${!all_benchmarks[@]}"; do
    val=${riscv_mpki_map[$bench]}
    [[ "$val" != "N/A" ]] && total_riscv=$(awk "BEGIN{print $total_riscv + $val}") && ((count_riscv++))
    val=${x86_mpki_map[$bench]}
    [[ "$val" != "N/A" ]] && total_x86=$(awk "BEGIN{print $total_x86 + $val}") && ((count_x86++))
    val=${arm_mpki_map[$bench]}
    [[ "$val" != "N/A" ]] && total_arm=$(awk "BEGIN{print $total_arm + $val}") && ((count_arm++))
done

avg_riscv=$(awk "BEGIN{printf \"%.4f\", $total_riscv / ($count_riscv ? $count_riscv : 1)}")
avg_x86=$(awk "BEGIN{printf \"%.4f\", $total_x86 / ($count_x86 ? $count_x86 : 1)}")
avg_arm=$(awk "BEGIN{printf \"%.4f\", $total_arm / ($count_arm ? $count_arm : 1)}")

printf "%-20s %-12s %-12s %-12s\n" "avg." "$avg_riscv" "$avg_x86" "$avg_arm" >> "$MPKI"