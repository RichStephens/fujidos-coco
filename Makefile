AS    = lwasm -r --pragma=condundefzero,nodollarlocal,noindex0tonone
ROM   = fujidos.rom
DISK  = fdtests.dsk
FLAGS = -DDW -DLevel=2 -DBECKER

all: $(ROM)

$(ROM): ecb_equates.asm fujidos.asm dwdefs.d dwread.asm dwwrite.asm
	$(AS) ecb_equates.asm fujidos.asm -o$@ $(FLAGS)
	@test $$(stat -c %s $@) -eq 16384 || { echo "$@ is not 16384 bytes"; rm -f $@; exit 1; }

# BASIC test programs, to mount in a FujiNet slot
disk: $(DISK)

$(DISK): tests/*.bas
	rm -f $@
	decb dskini $@
	for f in $^; do n=$$(basename $$f .bas | tr a-z A-Z); decb copy -0 -a -t $$f $@,$$n.BAS || exit 1; done

clean:
	rm -f $(ROM) $(DISK)

.PHONY: all disk clean
