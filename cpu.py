"""CPU functionality."""
import sys
# print('check here moron', sys.argv)
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
PRA = 0b01001000
AND = 0b10101000
XOR = 0b10101011

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #change to 256
        self.reg = [0] * 8
        self.PC = 0
        self.SP = 7
        self.is_running = True
        self.branchtable = {}
        self.branchtable[PRN] = self.prn
        self.branchtable[ADD] = self.add
        # self.branchtable[SUB] = self.sub
        self.branchtable[MUL] = self.mul
        self.branchtable[LDI] = self.ldi
        self.branchtable[HLT] = self.hlt
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[PRA] = self.pra
        self.branchtable[AND] = self.andd
        self.branchtable[XOR] = self.xor

    def ram_read(self, mar): #MAR (_Memory Address Register_) *ADDRESS*
        return self.ram[mar]
    def ram_write(self, mar, mdr): #MDR (_Memory Data Register_) *DATA VALUE*
        self.ram[mar] = mdr
        return self.ram[mar]
    def load(self):
        """Load a program into memory."""
        ##put this somewhere
        if len(sys.argv) != 2:
            print("Error")
            sys.exit(1)
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for instruction in f:
                    split_excess = instruction.split('#')
                    split = split_excess[0].strip()
                    if split == '':
                        continue # ignores blank lines
                    val = int(split, 2)
                    self.ram_write(address, val)
                    address += 1
        except FileNotFoundError:
            print(f"FileNotFound: {sys.argv}")
            sys.exit(2)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
    def run(self):
        """Run the CPU."""
        while self.is_running:
            r = self.ram[self.PC]
            # print(r, self.ram) 
            self.branchtable[r]()
        # print('areee degub matey', r, self.PC, self.reg, self.ram)
    def hlt(self):
        print('HALTING PLEASE WAIT...')
        self.is_running = False
    def ldi(self):
        mar = self.ram_read(self.PC + 1)
        mdr = self.ram_read(self.PC + 2)
        # print('hi', mar, mdr)
        self.reg[mar] = mdr
        self.PC += 3
    def prn(self):
        mar = self.ram_read(self.PC + 1)
        mdr = self.reg[mar]
        #prints value at that specific address.
        print(f'PRINTING value at register {mar}: {mdr}' )
        self.PC += 2
    def add(self):
        mar1 = self.ram_read(self.PC + 1)
        mar2 = self.ram_read(self.PC + 2)
        self.alu('ADD', mar1, mar2)
        self.PC += 3
    def mul(self):
        mar1 = self.ram_read(self.PC + 1)
        mar2 = self.ram_read(self.PC + 2)
        self.alu('MUL', mar1, mar2)
        self.PC += 3
    def push(self):
        mar = self.ram_read(self.PC + 1)
        mdr = self.reg[mar]
        # Decrement the SP.
        self.reg[self.SP] -= 1
        # print('push', mar, mdr, self.SP, self.reg[self.SP])
        # Copy the value in the given register to the address pointed to by SP.
        self.ram_write(self.reg[self.SP], mdr)
        self.PC += 2
    def pop(self):
        mar = self.ram_read(self.PC + 1)
        # Copy the value from the address pointed to by SP to the given register.
        self.reg[mar] = self.ram_read(self.reg[self.SP])
        self.reg[self.SP] += 1
        # print('pop', mar, mdr,  self.reg[mdr], self.reg[self.SP])
        self.PC += 2
    def call(self):
        val = self.PC
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = val
        reg = self.ram[self.PC + 1]
        subroutine_address = self.reg[reg]
        self.PC = subroutine_address
    def ret(self):
        return_address = self.reg[self.SP]
        self.PC = self.ram[return_address]
        self.reg[self.SP] += 1
        self.PC += 2
    def pra(self):
        mar = self.ram_read(self.PC + 1)
        mdr = self.reg[mar]
        print(chr(mdr))
        self.PC += 2

    def andd(self):
        mar1 = self.ram_read(self.PC + 1)
        mar2 = self.ram_read(self.PC + 2)
        mdr1 = self.reg[mar1]
        mdr2 = self.reg[mar2]
        self.reg[mar1] = mdr1 & mdr2
        self.PC += 3

    def xor(self):
        mar1 = self.ram_read(self.PC + 1)
        mar2 = self.ram_read(self.PC + 2)
        mdr1 = self.reg[mar1]
        mdr2 = self.reg[mar2]
        self.reg[mar1] = mdr1 ^ mdr2
        self.PC += 3