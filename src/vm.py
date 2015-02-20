
def print_registers(vm):
    print "     Register a = " + str(vm.reg_a)
    print "     Register b = " + str(vm.reg_b)
    print "     Register t = " + str(vm.reg_t)

def print_bars():
    print "+-------------------------------------------------------------+"

class BlockMachine(object):
    def __init__(self, program):
        # The program--a tuple of tuples which represent instructions.
        self.program = program

        # Registers
        self.reg_a = self.reg_b = self.reg_t = None

        # Whether to branch
        self.flag = False

        # Code pointer
        self.pc = 0

    def execute(self):
        while self.pc is not None:
            i = self.program[self.pc]
            #print self.pc, self.reg_a, self.reg_b, self.reg_t, self.flag, i
            instr, rest = i[0], i[1:]
            self.pc += 1 # Don't forget to increment the counter
            getattr(self, 'i_'+instr)(*rest)

    def i_copy(self, a, b):
        """Duplicates register b in register a"""
        setattr(self, a, getattr(self, b))

    def i_set(self, a, b):
        """Sets register a to the value b"""
        setattr(self, a, b)

    def i_exec(self, reg, op, *args):
        """Calls op and stores the result in reg."""
        setattr(self, reg, getattr(self, 'o_'+op)(*args))

    def i_test(self, op, *rest):
        if getattr(self, 'o_'+op)(*rest):
            self.flag = True
        else:
            self.flag = False

    def i_branch(self, line):
        """Jump to line if flag is set"""
        if self.flag: self.pc = line

    def i_jump(self, line):
        """Jump to line"""
        self.pc = line

    def o_zero(self, reg):
        """Is reg zero?"""
        return getattr(self, reg) == 0

    def o_lt(self, a, b):
        return getattr(self, a) < getattr(self, b)

    def o_sub(self, a, b):
        """reg a - reg b"""
        return getattr(self, a) - getattr(self, b)

    def o_add(self, a, b):
        """reg a - reg b"""
        return getattr(self, a) + getattr(self, b)

def test():
    vm = BlockMachine((
        ('test', 'zero', 'reg_b'),
        ('branch', None),
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'add', 'reg_t', 'reg_b'),
        ('set', 'reg_b', 0),
        ('copy', 'reg_a', 'reg_t'),
        ('jump', 0),
        ))

    prog_description = "Adds a to b and returns the product"
    code_as_string = """
        ('test', 'zero', 'reg_b'),
        ('branch', None),
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'add', 'reg_t', 'reg_b'),
        ('set', 'reg_b', 0),
        ('copy', 'reg_a', 'reg_t'),
        ('jump', 0),
    """

    # Set our Registers for the Addition program to act upon
    vm.reg_a = 12
    vm.reg_b = 30
    vm.reg_t = 0

    #Printing output for testing
    print_bars()
    print "Description: " + prog_description
    print_registers(vm)
    print_bars()
    print "Executing code:"
    print_bars()
    print code_as_string
    print_bars()
    vm.execute()
    print_registers(vm)
    print_bars()

test()