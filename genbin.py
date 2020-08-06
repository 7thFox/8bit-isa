import numpy as np
from words import OpCodes, CtlWrd, Flags

microcode = {
    OpCodes.NOP: [],
    OpCodes.HLT: [CtlWrd.HALT],
    OpCodes.ADD: [
        CtlWrd.A_IN | CtlWrd.STC_OE | CtlWrd.DEC_SC,
        CtlWrd.B_IN | CtlWrd.STC_OE,
        CtlWrd.SUM_OE | CtlWrd.STC_IN | CtlWrd.INC_PC,
        {
            Flags.ZERO: 5,
            Flags.CARRY: 4
        }
    ],
}

ADDR_BITS = 13
STEPS = 4
FLAGS = 3

# 3 * 8 = 24 bits
rom = [np.uint32(0x00)] * (2**ADDR_BITS)

def expandOp(op):
    if isinstance(op, int):
        return [op] * (2**FLAGS)
    elif isinstance(op, dict):
        return [op.get(x, 0x00) for x in range(0, 2**FLAGS)]
    else:
        assert False, "Unsupported op"

for opcode in microcode:
    addr_start = np.uint16(opcode & 0b111111) << 7
    addr_end = addr_start | 0b1111111
    ops = microcode[opcode]
    ops = ops + [0x00] * (2 ** STEPS - len(ops))
    assert not any(op != 0x00 for op in rom[addr_start:addr_end +1])
    ops = sum([expandOp(op) for op in ops], [])
    rom[addr_start:addr_end + 1] = ops
    
with open("rom1.bin", "wb") as out:
    out.write(bytearray([v & 0xFF for v in rom]))
with open("rom2.bin", "wb") as out:
    out.write(bytearray([v >> 8 & 0xFF for v in rom]))
with open("rom3.bin", "wb") as out:
    out.write(bytearray([v >> 16 & 0xFF for v in rom]))
