# FujiDOS

FujiDOS is a disk ROM for the Tandy Color Computer with a FujiNet. It is
HDB-DOS 1.5 (DriveWire over the Becker port) with FujiNet commands added.
It is built from the CoCo 3 HDB-DOS image, which checks for a CoCo 3 at run
time and also runs on a CoCo 2.

## Commands

| Command | What it does |
|---|---|
| `CONFIG` | Puts the FujiNet CONFIG disk back in drive 0 and reboots into CONFIG |
| `LOBBY` | Puts the FujiNet game lobby disk in drive 0 and reboots into the lobby |
| `TIME$` | The FujiNet's time as `HH:MM:SS` (24-hour), or `""` if it doesn't answer |
| `DATE$` | The FujiNet's date as `YYYY-MM-DD`, or `""` if it doesn't answer |
| `GUID$` | A new random GUID from the FujiNet, 36 lowercase characters, or `""` if it doesn't answer |
| `UCASE$(s$)` | `s$` with a-z in capitals |
| `FPRINT ON`, `FPRINT OFF` | Sends printer output (`PRINT #-2`, `LLIST`) to the FujiNet printer, or back to the serial port |
| `BACKUP #s TO #d` | Copies the disk image in FujiNet drive `s` (0-3) to the root of the SD card and mounts the copy in drive `d` |
| `DSKINI #d,"NAME"` | Creates blank disk image `NAME.DSK` in the root of the SD card and mounts it in FujiNet drive `d` |

CoCo 3 BASIC leaves almost no free command tokens, so FujiDOS commands are
plain words. They are reserved like BASIC keywords: `CONFIG=1` is a syntax
error, not an assignment, and so is `TIME$="12:00:00"`.

Get the printout from the printer page of the FujiNet's web interface. Each
download starts a new printout.

The `BACKUP #` copy keeps the image's file name. Both commands give
`?AE ERROR` if the file is already on the card. Without the `#`, `BACKUP` and
`DSKINI` are Disk BASIC's.

## Network files

A file name starting `N:` opens a FujiNet network device on an ordinary file
number, for `PRINT #`, `INPUT #`, `LINE INPUT #`, `EOF`, `LOF` and `CLOSE`:

```
OPEN "I",#1,"N:https://icanhazdadjoke.com/"
```

`N:` uses the network unit matching the file number (1-8); `N1:`-`N8:` picks
one. Two open files can't share a unit. A protocol name must follow the
colon, so `"N:1"` is still disk file `N` on drive 1.

| Mode | Use |
|---|---|
| `I` | Read (HTTP GET) |
| `O` | Write (HTTP PUT, sent at `CLOSE`) |
| `D`, `R` | Read and write (HTTP GET that takes headers, TCP) |
| `P` | HTTP POST: `PRINT #` the body, then read the reply |
| `K` | HTTP DELETE, then read the reply |

An optional last argument sets the line ending, `OPEN "D",#1,"N:...",e`: 0 raw,
1 CR, 2 LF, 3 CR LF (the default). `PRINT #` ends lines with it; reading
accepts CR, LF or CR LF unless it is 0.

| Command | What it does |
|---|---|
| `HEADER #f,"Name: value"` | Adds an HTTP request header (modes `D`, `R` and `P`) |
| `JSONPARSE #f`, `XMLPARSE #f`, `HTMLPARSE #f` | Parses the file's data for queries |
| `JSONQUERY$(f,q$)`, `XMLQUERY$(f,q$)`, `HTMLQUERY$(f,q$)` | The value `q$` selects, at most 255 characters |
| `LOF(f)` | Bytes ready to read |
| `LOC(f)` | -1 while connected, else 0 |
| `NETERR(f)` | The FujiNet's error code: 1 OK, 136 end of data, 170 not found, 200 connection refused |
| `NETERR(0)` | The last network `OPEN`'s error code, 1 if it worked |

A failed `OPEN` gives `?IO ERROR`. Disk BASIC has no `ON ERROR`, so check
`NETERR(0)` after the program stops.

Query results come back as plain ASCII: entities decoded and accented letters
folded to plain ones. XML and HTML parsing, ASCII results and the reason for a
failed `OPEN` need FujiNet firmware newer than 1.6.1.

## Building

Needs `lwasm` from [LWTOOLS](http://lwtools.projects.l-w.ca).

```
make
```

This produces `fujidos.rom`, a 16K image for $C000-$FEFF; the last 256 bytes
are unused. A CoCo 3 keeps the upper 8K in RAM block $37, which BASIC leaves
unused. Every statement and expression runs through it, so a program that
overwrites that block crashes BASIC.

`make disk` builds `fdtests.dsk` from `tests/*.bas` (needs `decb` from
ToolShed): WEATHER, DADJOKE and NETTEST, a self-check against httpbin.org.

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
