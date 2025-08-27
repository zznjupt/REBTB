# gem5-based REBTB performance evaluation simulator

* Baseline: `./Baseline/gem5`
* REBTB: `./REBTB/gem5`

* The randomization threshold can be modified here: `REBTB/REBTB_Performance/gem5/src/cpu/pred/bpred_unit.hh`
// [Thresholds for different P values]
* Execution method: 
  * modify the gem5 root directory to your own path in the scripts located at `REBTB/REBTB_Performance/gem5/run/scripts/`.
  * modify the SPEC2017 root directory to your own path in the scripts located at `REBTB/REBTB_Performance/gem5/run/scripts/spec2017_x86.sh`.
  * In the `gem5` directory, execute `make run`.
  * The IPC results are collected in `gem5/run/stat_analysis`.