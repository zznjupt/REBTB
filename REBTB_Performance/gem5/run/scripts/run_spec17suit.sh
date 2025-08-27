#!/bin/bash

BP=$1
GEM5_DIR=/root/gem5

int_rate=(perlbench_r gcc_r mcf_r omnetpp_r xalancbmk_r x264_r deepsjeng_r leela_r exchange2_r xz_r)
frate=(bwaves_r cactuBSSN_r namd_r parest_r povray_r lbm_r wrf_r blender_r cam4_r imagick_r nab_r fotonik3d_r roms_r)


# FLAGS="
# --cpu-type=DerivO3CPU \
# --bp-type=$BP \
# --indirect-bp-type=ITTAGE \
# --caches \
# --l2cache \
# --cacheline=64 \
# --num-l2cache=1 \
# --l1i_size=16kB \
# --l1i_assoc=4 \
# --l1d_size=16kB \
# --l1d_assoc=4 \
# --l2_size=256kB \
# --l2_assoc=16 \
# --mem-size=8192MB \
# --maxinsts=10000000"

FLAGS="
--cpu-type=DerivO3CPU \
--bp-type=TAGE \
--indirect-bp-type=ITTAGE \
--caches \
--l2cache \
--cacheline=64 \
--num-l2cache=1 \
--l1i_size=32kB \
--l1i_assoc=8  \
--l1d_size=32kB \
--l1d_assoc=8 \
--l2_size=1024kB \
--l2_assoc=16 \
--mem-size=8192MB \
--warm=10000000 \
--maxinsts=10000000"

# for i in "${!int_rate[@]}"  
# do 
# cd $GEM5_DIR
# source ./run/scripts/spec2017_riscv64.sh "${int_rate[$i]}" "$FLAGS" "$BP"
# done

# for i in "${!frate[@]}"  
# do 
# cd $GEM5_DIR 
# source ./run/scripts/spec2017_riscv64.sh "${frate[$i]}" "$FLAGS" "$BP"
# done

for i in "${!int_rate[@]}"  
do 
cd $GEM5_DIR
source ./run/scripts/spec2017_x86.sh "${int_rate[$i]}" "$FLAGS" "$BP"
done

for i in "${!frate[@]}"  
do 
cd $GEM5_DIR 
source ./run/scripts/spec2017_x86.sh "${frate[$i]}" "$FLAGS" "$BP"
done

# for i in "${!int_rate[@]}"  
# do 
# cd $GEM5_DIR
# source ./run/scripts/spec2017_aarch64.sh "${int_rate[$i]}" "$FLAGS" "$BP"
# done

# for i in "${!frate[@]}"  
# do 
# cd $GEM5_DIR 
# source ./run/scripts/spec2017_aarch64.sh "${frate[$i]}" "$FLAGS" "$BP"
# done