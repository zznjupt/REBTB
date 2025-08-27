# !/bin/bash

BP=$1

GEM5_DIR=/root/gem5/
mkdir -p "$GEM5_DIR/run/stat_analysis/$BP"
OUTPUT_FILE=$GEM5_DIR/run/stat_analysis/$BP/err.list

> "$OUTPUT_FILE"

find $GEM5_DIR/run/output_riscv64/$BP -type f -name "*.err" | while read -r err_file; do
    echo "===== $err_file =====" >> "$OUTPUT_FILE"
    cat "$err_file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

printf "\n" >> "$OUTPUT_FILE"

find $GEM5_DIR/run/output_x86/$BP -type f -name "*.err" | while read -r err_file; do
    echo "===== $err_file =====" >> "$OUTPUT_FILE"
    cat "$err_file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

printf "\n" >> "$OUTPUT_FILE"

find $GEM5_DIR/run/output_aarch64/$BP -type f -name "*.err" | while read -r err_file; do
    echo "===== $err_file =====" >> "$OUTPUT_FILE"
    cat "$err_file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done