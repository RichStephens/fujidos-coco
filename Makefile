AS    = lwasm -r --pragma=condundefzero,nodollarlocal,noindex0tonone
ROM   = fujidos.rom
FLAGS = -DDW -DLevel=2 -DBECKER

all: $(ROM)

$(ROM): ecb_equates.asm fujidos.asm dwdefs.d dwread.asm dwwrite.asm
	$(AS) ecb_equates.asm fujidos.asm -o$@ $(FLAGS)
	@test $$(stat -c %s $@) -eq 8192 || { echo "$@ is not 8192 bytes"; rm -f $@; exit 1; }

clean:
	rm -f $(ROM)

.PHONY: all clean
