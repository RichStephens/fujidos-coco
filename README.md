# FujiDOS

FujiDOS is a disk ROM for the Tandy Color Computer with a FujiNet. It is
HDB-DOS 1.5 (DriveWire over the Becker port) with FujiNet commands added.
It is built from the CoCo 3 HDB-DOS image, which checks for a CoCo 3 at run
time and also runs on a CoCo 2.

## Commands

| Command | What it does |
|---|---|
| `CONFIG` | Puts the FujiNet CONFIG disk back in drive 0 and reboots into CONFIG |
| `TIME$` | The FujiNet's time as `HH:MM:SS` (24-hour), or `""` if it doesn't answer |
| `DATE$` | The FujiNet's date as `YYYY-MM-DD`, or `""` if it doesn't answer |
| `GUID$` | A new random GUID from the FujiNet, 36 lowercase characters, or `""` if it doesn't answer |

CoCo 3 BASIC leaves almost no free command tokens, so FujiDOS commands are
plain words. They are reserved like BASIC keywords: `CONFIG=1` is a syntax
error, not an assignment, and so is `TIME$="12:00:00"`.

## Building

Needs `lwasm` from [LWTOOLS](http://lwtools.projects.l-w.ca).

```
make
```

This produces `fujidos.rom`, a 16K image for $C000-$FEFF; the last 256 bytes
are unused. A CoCo 3 keeps the upper 8K in RAM block $37, which BASIC leaves
unused. Every statement and expression runs through it, so a program that
overwrites that block crashes BASIC.

## Credits

FujiDOS is almost entirely HDB-DOS. All credit for it goes to its authors:

- **HDB-DOS**: Copyright (C) 2004 Boisy G. Pitre. Its source began as a 2002
  disassembly of Roger Krupski's binary.
- **Contributors** named in the HDB-DOS history: Robert Gault, David Ladd,
  and Darren Atkinson, who also wrote the DriveWire read and write routines
  (`dwread.asm`, `dwwrite.asm`).
- **Disk Extended Color BASIC**: Tandy, under license from Microsoft and
  Microware. HDB-DOS's copy of its source was taken from Spectral Associates'
  *Disk Color BASIC Unravelled*.
- **FlexiKey**: Copyright (C) 1984 Colin J. Stearman.

HDB-DOS lives in the NitrOS-9 project's ToolShed, along with its full source
and change history:
<https://github.com/nitros9project/toolshed/tree/main/hdbdos>.
`ecb_equates.asm` comes from the same repository's `cocoroms`.
