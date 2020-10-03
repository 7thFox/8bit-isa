import numpy as np
from words import OpCodes, CtlWrd, Flags

# Program Space:    0x00-0xFF
# Mem Space:        0x100-0x1FF

microcode = {
    OpCodes.NOP: [],
    OpCodes.HLT: [CtlWrd.HALT],
    OpCodes.RST: [CtlWrd.RST],
    OpCodes.ADD: [
        CtlWrd.A_IN | CtlWrd.STC_OE | CtlWrd.DEC_SC,
        CtlWrd.B_IN | CtlWrd.STC_OE,
        CtlWrd.SUM_OE | CtlWrd.STC_IN | CtlWrd.FLG,
        CtlWrd.INC_PC,
    ],
    OpCodes.SUB: [
        CtlWrd.A_IN | CtlWrd.STC_OE | CtlWrd.DEC_SC,
        CtlWrd.B_IN | CtlWrd.STC_OE,
        CtlWrd.SUM_OE | CtlWrd.SUB | CtlWrd.STC_IN | CtlWrd.FLG,
        CtlWrd.INC_PC,
    ],
    OpCodes.LST: [
        CtlWrd.ROM_OE | CtlWrd.A_IN | CtlWrd.INC_SC,
        CtlWrd.A_S1,
        CtlWrd.A_OE | CtlWrd.STC_IN,
        CtlWrd.INC_PC,
    ],
    OpCodes.RST: [
        CtlWrd.ROM_OE | CtlWrd.A_IN | CtlWrd.INC_SC,
        CtlWrd.A_S0,
        CtlWrd.A_OE | CtlWrd.STC_IN,
        CtlWrd.INC_PC,
    ],
    OpCodes.PSH: [
        CtlWrd.ROM2A_NC | CtlWrd.INC_SC,
        0x00,  # Data Load
        CtlWrd.A_OE | CtlWrd.STC_IN,
        CtlWrd.INC_PC,
    ],
    OpCodes.DUP: [
        CtlWrd.STC_OE | CtlWrd.A_IN | CtlWrd.INC_SC,
        CtlWrd.STC_IN | CtlWrd.A_OE,
        CtlWrd.INC_PC,
    ],
    OpCodes.CAL: [
        CtlWrd.INC_SC,
        CtlWrd.PC_OE | CtlWrd.STC_IN | CtlWrd.ROM2A_NC,
        0x00,  # Data Load
        CtlWrd.PC_IN | CtlWrd.A_OE
    ],
    OpCodes.RTN: [
        CtlWrd.STC_OE | CtlWrd.PC_IN | CtlWrd.DEC_SC
    ],
    OpCodes.BR: [
        CtlWrd.ROM2A_NC,
        0x00,  # Data Load
        CtlWrd.PC_IN | CtlWrd.A_OE
    ],
    OpCodes.BEQ: [
        [
            {
                "flags": set([x | Flags.ZERO for x in range(0b000, 0b111)]),
                "op": CtlWrd.ROM2A_NC
            },
            {
                "flags": set([x & Flags.NOT_ZERO for x in range(0b000, 0b111)]),
                "op": CtlWrd.INC_PC
            },
        ],
        [{
            "flags": set([x | Flags.ZERO for x in range(0b000, 0b111)]),
            "op": 0x00, # Data Load
        }],
        [{
            "flags": set([x | Flags.ZERO for x in range(0b000, 0b111)]),
            "op": CtlWrd.PC_IN | CtlWrd.A_OE
        }],
    ],
    OpCodes.BNE: [
        [
            {
                "flags": set([x | Flags.NOT_ZERO for x in range(0b000, 0b111)]),
                "op": CtlWrd.ROM2A_NC
            },
            {
                "flags": set([x & Flags.ZERO for x in range(0b000, 0b111)]),
                "op": CtlWrd.INC_PC
            },
        ],
        [{
            "flags": set([x & Flags.NOT_ZERO for x in range(0b000, 0b111)]),
            "op": 0x00, # Data Load
        }],
        [{
            "flags": set([x & Flags.NOT_ZERO for x in range(0b000, 0b111)]),
            "op": CtlWrd.PC_IN | CtlWrd.A_OE
        }],
    ],
}

ADDR_BITS = 13
STEPS = 4
FLAGS = 3

# 3 * 8 = 24 bits
rom = [np.uint32(0x00)] * (2**ADDR_BITS)

def opt_with_flag(opts, flag):
    for opt in opts:
        if flag in opt["flags"]:
            return opt["op"]
    return 0x00

def expand_op(op):
    if isinstance(op, int):
        return [op] * (2**FLAGS)
    elif isinstance(op, list):
        return [
            opt_with_flag(op, f)
            for f in range(0, 2**FLAGS)]
    else:
        assert False, "Unsupported op"

for opcode in microcode:
    addr_start = np.uint16(opcode & 0b111111) << 7
    addr_end = addr_start | 0b1111111
    ops = microcode[opcode]
    ops = ops + [0x00] * (2 ** STEPS - len(ops))
    assert not any(op != 0x00 for op in rom[addr_start:addr_end +1])
    ops = sum([expand_op(op) for op in ops], [])
    rom[addr_start:addr_end + 1] = ops
    
with open("rom1.bin", "wb") as out:
    out.write(bytearray([v & 0xFF for v in rom]))
with open("rom2.bin", "wb") as out:
    out.write(bytearray([v >> 8 & 0xFF for v in rom]))
with open("rom3.bin", "wb") as out:
    out.write(bytearray([v >> 16 & 0xFF for v in rom]))
