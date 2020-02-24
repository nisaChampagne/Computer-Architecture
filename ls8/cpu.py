"""CPU functionality."""

import sys

'''
MAY NEED VARIABLES FOR THESE LATER
* `LDI`: load "immediate", store a value in a register, or "set this register to
  this value".
* `PRN`: a pseudo-instruction that prints the numeric value stored in a
  register.
* `HLT`: halt the CPU and exit the emulator.
'''


class CPU:
    """Main CPU class."""

    '''
    Add list properties to the `CPU` class to hold 256 bytes of memory and 8
    general-purpose registers.

    > Hint: you can make a list of a certain number of zeros with this syntax:
    >
    > ```python
    > x = [0] * 25  # x is a list of 25 zeroes
    > ```

    Also add properties for any internal registers you need, e.g. `PC`.

    Later on, you might do further initialization here, e.g. setting the initial
    value of the stack pointer.
    '''
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    '''
    In `CPU`, add method `ram_read()` and `ram_write()` that access the RAM inside
    the `CPU` object.

    `ram_read()` should accept the address to read and return the value stored
    there.

    `raw_write()` should accept a value to write, and the address to write it to.

    > Inside the CPU, there are two internal registers used for memory operations:
    > the _Memory Address Register_ (MAR) and the _Memory Data Register_ (MDR). The
    > MAR contains the address that is being read or written to. The MDR contains
    > the data that was read or the data to write. You don't need to add the MAR or
    > MDR to your `CPU` class, but they would make handy paramter names for
    > `ram_read()` and `ram_write()`, if you wanted.
    '''

    def ram_read(self,mem_address):
        return self.ram[mem_address]

    def ram_write(self, value, mem_address):
        self.ram[mem_address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        '''
        It needs to read the memory address that's stored in register `PC`, and store
        that result in `IR`, the _Instruction Register_. This can just be a local
        variable in `run()`.

        Some instructions requires up to the next two bytes of data _after_ the `PC` in
        memory to perform operations on. Sometimes the byte value is a register number,
        other times it's a constant value (in the case of `LDI`). Using `ram_read()`,
        read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
        `operand_b` in case the instruction needs them.

        Then, depending on the value of the opcode, perform the actions needed for the
        instruction per the LS-8 spec. Maybe an `if-elif` cascade...? There are other
        options, too.

        After running code for any particular instruction, the `PC` needs to be updated
        to point to the next instruction for the next iteration of the loop in `run()`.
        The number of bytes an instruction uses can be determined from the two high bits
        (bits 6-7) of the instruction opcode. See the LS-8 spec for details.
        '''
        pass
