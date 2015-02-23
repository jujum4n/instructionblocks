import hashlib
hs=hashlib

def print_registers(vm):
    print "     Register a = " + str(vm.reg_a)
    print "     Register b = " + str(vm.reg_b)
    print "     Register t = " + str(vm.reg_t)

def print_bars():
    print "+-------------------------------------------------------------+"

class BlockMachine(object):
    def __init__(self, program, description):
        # The program--a tuple of tuples which represent instructions.
        self.program = program
        #The program as a string used to hash the application
        self.program_as_string = str(program)
        self.program_description = str(description)
        self.program_hash = hs.sha256(self.program_description+self.program_as_string).hexdigest()

        # Registers
        self.reg_a = self.reg_b = self.reg_t = None

        # Whether to branch
        self.flag = False

        # Code pointer
        self.pc = 0
    #Executes the instructions
    def execute(self):
        while self.pc is not None:
            i = self.program[self.pc]
            #print self.pc, self.reg_a, self.reg_b, self.reg_t, self.flag, i
            instr, rest = i[0], i[1:]
            self.pc += 1 # Don't forget to increment the counter
            getattr(self, 'i_'+instr)(*rest)

    #Duplicates register b in register a
    def i_copy(self, a, b):
        setattr(self, a, getattr(self, b))
    #Sets register a to the value b
    def i_set(self, a, b):
        setattr(self, a, b)

    #Calls op and stores the result in reg
    def i_exec(self, reg, op, *args):
        setattr(self, reg, getattr(self, 'o_'+op)(*args))

    def i_test(self, op, *rest):
        if getattr(self, 'o_'+op)(*rest):
            self.flag = True
        else:
            self.flag = False

    #Jump to line if flag is set
    def i_branch(self, line):
        if self.flag: self.pc = line

    def i_jump(self, line):
        self.pc = line
    #Checks to see if the given register is 0
    def o_zero(self, reg):
        return getattr(self, reg) == 0

    #Checks to see if the registers are equivalent
    def o_eq(self, a, b):
        return getattr(self, a) == getattr(self, b)

    #Clears the given register and puts None into it
    def i_clr(self, a):
        setattr(self, a, None)

    #Sets the given register to 0
    def i_zro(self, a):
        setattr(self, a, 0)
    #Checks if a is less than b
    def o_lt(self, a, b):
        return getattr(self, a) < getattr(self, b)

    #Checks if a is greather than b
    def o_gt(self, a, b):
        return getattr(self, a) > getattr(self, b)

    #Subtracts a from b
    def o_sub(self, a, b):
        return getattr(self, a) - getattr(self, b)

    #Adds a to b
    def o_add(self, a, b):
        return getattr(self, a) + getattr(self, b)

    #Multiplies a times b
    def o_mult(self, a, b):
        return getattr(self, a) * getattr(self, b)

    #Divides a over b
    def o_div(self, a, b):
        return getattr(self, a) / getattr(self, b)

    #Takes a to the power of b
    def o_pow(self, a, b):
        return getattr(self, a) ^ getattr(self, b)

    #Decrments 1 from the given register
    def o_dec(self, a):
        return getattr(self, a) - 1

    #Increments 1 to the given register
    def o_inc(self, a):
        return getattr(self, a) + 1

    #Returns a sha256 hash of a string version of a given register
    def o_sha256(self, a):
        temp = getattr(self, a)
        temp = str(temp)
        return hs.sha256(temp).hexdigest()

def hashtesting():
    prog_description = "Returns a SHA256 of a given register as the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'sha256', 'reg_t'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    # Set our Registers for the Addition program to act upon
    vm.reg_a = 1

    #Printing output for testing
    print_bars()
    print "Description: " + vm.program_description
    print_bars()
    print_registers(vm)
    print_bars()
    print "Executing: " + vm.program_as_string
    print_bars()
    vm.execute()
    print_registers(vm)
    print_bars()

def multiplication_test():
    prog_description = "Multiplies two registers together and returns the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'mult', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    # Set our Registers for the Addition program to act upon
    vm.reg_a = 10
    vm.reg_b = 10

    #Printing output for testing
    print_bars()
    print "Description: " + vm.program_description
    print_bars()
    print_registers(vm)
    print_bars()
    print "Executing: " + vm.program_as_string
    print_bars()
    vm.execute()
    print_registers(vm)
    print_bars()

    if not vm.reg_t==100:
        print "FAILURE: Multiplication Test has failed"

def division_test():
    prog_description = "Divides two registers and returns the result"

    vm = BlockMachine((
        ('test', 'zero', 'reg_b'),
        ('branch', None),
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'div', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    # Set our Registers for the Addition program to act upon
    vm.reg_a = 10
    vm.reg_b = 1

    #Printing output for testing
    print_bars()
    print "Description: " + vm.program_description
    print_bars()
    print_registers(vm)
    print_bars()
    print "Executing: " + vm.program_as_string
    print_bars()
    vm.execute()
    print_registers(vm)
    print_bars()

    if not vm.reg_t==10:
        print "FAILURE: Division Test has failed"

def addition_test():
    prog_description = "Adds two registers together and returns the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'add', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    # Set our Registers for the Addition program to act upon
    vm.reg_a = 12
    vm.reg_b = 30

    #Printing output for testing
    print_bars()
    print "Description: " + vm.program_description
    print_bars()
    print_registers(vm)
    print_bars()
    print "Executing: " + vm.program_as_string
    print_bars()
    vm.execute()
    print_registers(vm)
    print_bars()

    if not vm.reg_t == 42:
        print "FAILURE: Addition Test has failed"

def subtraction_test():
    prog_description = "Adds two registers together and returns the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'sub', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    # Set our Registers for the Addition program to act upon
    vm.reg_a = 30
    vm.reg_b = 12

    #Printing output for testing
    print_bars()
    print "Description: " + vm.program_description
    print_bars()
    print_registers(vm)
    print_bars()
    print "Executing: " + vm.program_as_string
    print_bars()
    vm.execute()
    print_registers(vm)
    print_bars()

    if not vm.reg_t == 18:
        print "FAILURE: Subtraction Test has failed"

def increment_decrement_test():
    prog_description = "Increments a given register by 1 then decrements it by 1"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'inc', 'reg_t'),
        ('exec', 'reg_t', 'dec', 'reg_t'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    # Set our Registers for the Addition program to act upon
    vm.reg_a = 0

    #Printing output for testing
    print_bars()
    print "Description: " + vm.program_description
    print_bars()
    print_registers(vm)
    print_bars()
    print "Executing: " + vm.program_as_string
    print_bars()
    vm.execute()
    print_registers(vm)
    print_bars()

    if not vm.reg_t == 0:
        print "FAILURE: Increment Test has failed"

def test():
    addition_test()
    multiplication_test()
    hashtesting()
    subtraction_test()
    increment_decrement_test()
    division_test()

test()
