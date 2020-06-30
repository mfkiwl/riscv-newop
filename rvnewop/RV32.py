from . import I32
from . import M32
from . import RVFormatParser
from . import V32
from . import C32
from bitarray import bitarray


class RV32:
    """ General class for RISC-V 32bit """

    def __init__(self, isa="32I"):
        """ A constructor for RV32
            isa is a string containing which instruction sets and extensions to use, by default this will use 32I"""

        # a mapping from frozenbitarray of opcode --> function that returns an RVInstruction
        self.instructionTable = {}
        self.instructionNameSet = set()

        if "32I" in isa:
            self.instructionTable.update(I32.instructionTable)
            self.instructionNameSet.update(I32.instructionNameSet)
        if "M" in isa:
            self.instructionTable.update(M32.instructionTable)
            self.instructionNameSet.update(M32.instructionNameSet)
        if "V" in isa:
            self.instructionTable.update(V32.instructionTable)
            # TODO add inst name set
        if "C" in isa:
            self.instructionTable.update(C32.instructionTable)
            self.instructionNameSet.update(C32.instructionNameSet)

    def decodeHex(self, hex):
        bstr = bitarray(bin(int(hex, 16))[2:]).to01()
        size = 32

        # compressed instructions NEVER end in 11
        if bstr[-2:] != "11":
            size = 16

        bstr = bstr.zfill(size)
        ba = bitarray(bstr)

        return self.decode(ba)

    def decode(self, ba):
        return self.instructionTable[RVFormatParser.getOpcode(ba)](ba)
