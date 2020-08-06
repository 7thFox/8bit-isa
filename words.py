
class Flags:
    ZERO = 1 << 3
    CARRY = 1 << 2

class OpCodes: # 00-40
    NOP = 0x01
    HLT = 0x02
    ADD = 0x03

class CtlWrd:
    # Chip 1
    HALT = 1 << 0
    A_S0 = 1 << 1
    A_S1 = 1 << 2
    RST = 1 << 3
    INC_PC = 1 << 4
    FLG = 1 << 5
    DAT = 1 << 6
    SET_PC = 1 << 7
    # Chip 2
    A_OE = 1 << 8 + 0
    B_S0 = 1 << 8 + 1
    B_S1 = 1 << 8 + 2
    B_OE = 1 << 8 + 3
    SUM_OE = 1 << 8 + 4
    SUB = 1 << 8 + 5
    INC_SC = 1 << 8 + 6
    DEC_SC = 1 << 8 + 7
    # Chip 3
    ROM_OE = 1 << 16 + 0
    STC_OE = 1 << 16 + 1
    STC_IN = 1 << 16 + 2
    # Helpers
    A_IN = A_S0 | A_S1
    B_IN = B_S0 | B_S1
    