import sys

'''
* `LDI`: load "immediate", store a value in a register, or "set this register to
  this value".
* `PRN`: a pseudo-instruction that prints the numeric value stored in a
  register.
* `HLT`: halt the CPU and exit the emulator.
'''
# day 1
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

# day 2
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
DIV = 0b10100011

# day 3
PUSH = 0b01000101
POP = 0b01000110

# day 4
CALL = 0b01010000
RET = 0b00010001


class CPU:
  
    def __init__(self):
        """Construct a new CPU."""

        #256 bytes of memory
        self.ram = [0] * 256

        # a word is 8 bit
        self.reg = [0] * 8

        # program counter
        self.program_counter = 0

        # stack pointer lives in register spot 7
        self.stack_pointer = 7

    def ram_read(self,mem_address):
        return self.ram[mem_address]

    def ram_write(self, mem_data, mem_address):
        self.ram[mem_address] = mem_data

    def stack_push(self, value):
        '''
        * decrement the stack pointer(sp)
        * copy the value in the given register to the address pointed to by stack pointer(sp)
        '''
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = value

    def stack_pop(self):
        '''
        * copy the value from the address pointed to by the stack pointer(sp) to the given register
        * increment stack pointer(sp)
        '''
        popped_val = self.ram[self.stack_pointer]
        self.stack_pointer += 1
        return popped_val


    def load(self, filename):
        """Load a program into memory."""

        address = 0

        program = []

        with open(filename) as f:
            #read all the lines
                for line in f:
                    # parse out comments
                    # print(line)
                    split = line.split('#')
                    # ignore blank lines

                    #cast numbers from strings to ints
                    value = split[0].strip()
                    if value == "":
                        continue
                    final_val = int(value, 2)
                    self.ram[address] = final_val
                    address += 1 # iterates!

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            if self.reg[reg_b] == 0:
                print("Error: cannot divide by 0 silly")
                sys.exit()
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.program_counter,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.program_counter),
    #         self.ram_read(self.program_counter + 1),
    #         self.ram_read(self.program_counter + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def run(self):
        halted = False
        program_counter = self.program_counter

        while not halted:

            #command = memory[program_counter]
            instruction_register = self.ram_read(program_counter)

            # Using `ram_read()`,read the bytes at `program_counter+1` and `program_counter+2` from RAM into variables `operand_a` and
            # `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(program_counter + 1)
            operand_b = self.ram_read(program_counter + 2)

            if instruction_register == HLT:
                #* `HLT`: halt the CPU and exit the emulator.
                self.program_counter += 1
                halted = True

            elif instruction_register == PRN:
                # `PRN`: a pseudo-instruction that prints the numeric value stored in a register.
                # a is register_index. print reg a
                print('printed', self.reg[operand_a])
                program_counter += 2

            elif instruction_register == LDI:
                #* `LDI`: load "immediate", store a value in a register, or "set this register to this value".
                # a is register, b is the value. add b to reg[a]
                self.reg[operand_a] = operand_b
                program_counter += 3

            elif instruction_register == PUSH:

                    ##### abstracted push into a method ######

                # # Grab the register argument
                # register = self.ram[program_counter + 1] # the argument, telling us what the register is
                # value = self.reg[register]
                # # Decrement the SP.
                # self.reg[self.stack_pointer] -= 1
                # # Copy the value in the given self.reg to the address pointed to by self.sp.
                # self.ram[self.reg[self.stack_pointer]] = value

                value = self.reg[operand_a]
                self.stack_push(value)
                program_counter += 2

            elif instruction_register == POP:

                    ##### abstracted push into a method ###

                # # Grab the value from the top of the stack
                # register = self.ram[program_counter + 1] # the argument, telling us what the register is 
                # value = self.ram[self.reg[self.stack_pointer]]
                # # Copy the value from the address pointed to by SP to the given register.
                # self.reg[register] = value
                # # Increment SP.
                # self.reg[self.stack_pointer] += 1 # stack pointer value is stored in register

                print('popped', self.stack_pop())
                program_counter += 2

                # multiply the values in two registers together
                # store the results in reg A
            elif instruction_register == MUL:
                self.alu(MUL, operand_a, operand_b)
                program_counter += 3

            
            elif instruction_register == CALL:
                return_address = self.program_counter + 2
                self.reg[self.stack_pointer] -= 1
                self.ram[self.reg[self.stack_pointer]] = return_address

                reg_num = operand_a
                self.program_counter = self.reg[reg_num]

            elif instruction_register == RET:
                self.program_counter = self.ram[self.reg[self.stack_pointer]]
                self.reg[self.stack_pointer] += 1

            else:
                print('Bad instruction register', instruction_register)
                halted = True