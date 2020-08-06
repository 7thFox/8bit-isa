# 8bit-isa
Generates binary files to write to my 3 AT28C64B EEPROMs for my 8-bit computer.

# background
The AT28C64B has a 13-bit address space with 8-bit output, and my computer has ~20 control lines, and will require 3 EEPROMS.
`write_prom.sh` is a small script making use of David Griffith's [open source software](https://gitlab.com/DavidGriffith/minipro) for the MiniPRO TL866xx

# binary layout

The address is shared across all 3 EEPROMs and contains 3 sections:
 - 6-bit opcode (MSB)
 - 4-bit step number
 - 3-bit flags (LSB)

