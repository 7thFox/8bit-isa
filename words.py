
class Flags:
    NO_FLAG = 0b000
    ZERO = 0b001
    CARRY = 0b010
    UNASSIGNED = 0b100
    
    NOT_ZERO = 0b110
    NOT_CARRY = 0b101

class OpCodes: # 00-3F (OO-1F80)
    NOP = 0x00 # 0x00   000000
    HLT = 0x01 # 0x80   000001
    RST = 0x02 # 0x100  000010
    
    ADD = 0x08 # 0x400  001000
    SUB = 0x09 # 0x480  001001
    LST = 0x0A # 0x500  001010
    RST = 0x0B # 0x580  001011
    
    PSH = 0x10 # 0x800  010000
    POP = 0x11 # 0x880  010001
    DUP = 0x12 # 0x900  010010
    
    CAL = 0x18 # 0xc00  011000
    RTN = 0x19 # 0xc80  011001
    
    BR  = 0x20 # 0x1000 100000
    BNE = 0x21 # 0x1080 100001
    BEQ = 0x22 # 0x1100 100010


class CtlWrd:
    # Chip 1
    HALT = 1 << 0
    A_S0 = 1 << 1
    A_S1 = 1 << 2
    RST = 1 << 3
    INC_PC = 1 << 4
    FLG = 1 << 5
    ROM2A_NC = 1 << 6
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
    PC_OE = 1 << 16 + 3
    PC_IN = 1 << 16 + 4
    # Helpers
    A_IN = A_S0 | A_S1
    B_IN = B_S0 | B_S1
    