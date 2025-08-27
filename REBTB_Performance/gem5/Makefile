# run: riscv x86 aarch64 spec17

run: x86 spec17

spec17:
	@for bp in $(BP_LIST); do \
		echo "Running with $$bp..."; \
		bash ./run/scripts/run_spec17suit.sh $$bp; \
		bash ./run/scripts/err.sh $$bp; \
		bash ./run/scripts/stats.sh $$bp; \
	done

BP_LIST = Raptor_Cove

# LocalBP BiModeBP TournamentBP LTAGE MultiperspectivePerceptron64KB MultiperspectivePerceptronTAGE64KB TAGE_SC_L_64KB

# spec17:
# 	@for bp in $(BP_LIST); do \
# 		echo "Running with $$bp..."; \
# 		bash ./run/scripts/run_spec17suit.sh $$bp; \
# 		bash ./run/scripts/err.sh $$bp; \
# 		bash ./run/scripts/stats.sh $$bp; \
# 	done

build: all riscv x86 aarch64

all:
	scons ./build/ALL/gem5.opt -j16

riscv:
	scons ./build/RISCV/gem5.opt -j16

x86:
	scons ./build/X86/gem5.opt -j16

aarch64:
	scons ./build/ARM/gem5.opt -j16

