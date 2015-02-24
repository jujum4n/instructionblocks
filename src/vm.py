import hashlib
import pybitcointools

pbtc=pybitcointools
hs=hashlib
fails=0

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

    #Test to see if it an operation or not, if it is set flags
    def i_test(self, op, *rest):
        if getattr(self, 'o_'+op)(*rest):
            self.flag = True
        else:
            self.flag = False

    #Jump to line if flag is set
    def i_branch(self, line):
        if self.flag: self.pc = line

    #Jumps the code pointer to the specified line number 0 = first line
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

    #Generates a private key given a register and leaves the key in that register
    def i_pvtkey(self, a):
        priv_key = pbtc.random_key()
        setattr(self, a, priv_key)

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

#Bitcoin Key generation
def key_test():
    prog_description = "Clears a given register with None data"

    vm = BlockMachine((
        ('pvtkey', 'reg_a'),                    # Create a private key and store it in register a
        ('copy', 'reg_t', 'reg_a'),             # Copy the private key in register A to register T
        ('jump', None),                         # Exit the program
        ), prog_description)
    vm.execute()
    privatekey = str(vm.reg_a)
    publickey = pbtc.privtopub(privatekey)
    address = pbtc.pubtoaddr(publickey)
    print "Private Key: " + privatekey
    print "Public Key: " + publickey
    print "Address: " + address

#Test for sha256
def hashtesting():
    prog_description = "Returns a SHA256 of a given register as the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'sha256', 'reg_t'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 1

    vm.execute()

    if not vm.reg_t == '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b':
        global fails
        fails+=1
        print "FAILURE: sha256 Test has failed"

#Test to verify the clr function works
def clr_test():
    prog_description = "Clears a given register with None data"

    vm = BlockMachine((
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('clr', 'reg_t'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 10
    vm.reg_b = 10
    vm.reg_t = 10

    vm.execute()

    if not vm.reg_t== None and vm.reg_a == None and vm.reg_b == None:
        global fails
        fails+=1
        print "FAILURE: clr Test has failed"

#Test to verify the zro function works by setting all registers to 0
def zro_test():
    prog_description = "Clears a given register with 0 as the register value"

    vm = BlockMachine((
        ('zro', 'reg_b'),
        ('zro', 'reg_a'),
        ('zro', 'reg_t'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 10
    vm.reg_b = 10
    vm.reg_t = 10

    vm.execute()

    if not vm.reg_t== 0 and vm.reg_a == 0 and vm.reg_b == 0:
        global fails
        fails+=1
        print "FAILURE: zro Test has failed"

#Test to verify that multiplication works
def multiplication_test():
    prog_description = "Multiplies two registers together and returns the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'mult', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 10
    vm.reg_b = 10

    vm.execute()

    if not vm.reg_t==100:
        global fails
        fails+=1
        print "FAILURE: Multiplication Test has failed"

#Test to verify that power works
def pow_test():
    prog_description = "Takes a given register to the other given register and takes it to the power"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'pow', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 10
    vm.reg_b = 3

    vm.execute()

    if not vm.reg_t==1000:
        global fails
        fails+=1
        print "FAILURE: Power Test has failed"

#Test to verify that division works
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

    vm.reg_a = 10
    vm.reg_b = 1

    vm.execute()

    if not vm.reg_t==10:
        global fails
        fails+=1
        print "FAILURE: Division Test has failed"

#Test to verify that addition works
def addition_test():
    prog_description = "Adds two registers together and returns the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'add', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 12
    vm.reg_b = 30

    vm.execute()

    if not vm.reg_t == 42:
        global fails
        fails+=1
        print "FAILURE: Addition Test has failed"

#Test to verify subtraction works
def subtraction_test():
    prog_description = "Adds two registers together and returns the result"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'sub', 'reg_t', 'reg_b'),
        ('clr', 'reg_b'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 30
    vm.reg_b = 12

    vm.execute()

    if not vm.reg_t == 18:
        global fails
        fails+=1
        print "FAILURE: Subtraction Test has failed"

#Test to verify that increment and decrement works
def increment_decrement_test():
    prog_description = "Increments a given register by 1 then decrements it by 1"

    vm = BlockMachine((
        ('copy', 'reg_t', 'reg_a'),
        ('exec', 'reg_t', 'inc', 'reg_t'),
        ('exec', 'reg_t', 'dec', 'reg_t'),
        ('clr', 'reg_a'),
        ('jump', None),
        ), prog_description)

    vm.reg_a = 0

    vm.execute()

    if not vm.reg_t == 0:
        global fails
        fails+=1
        print "FAILURE: Increment Test has failed"

#Test all the functions with simple programs verifying register ouput
def tests():
    #Run all the tests
    key_test()
    zro_test()
    clr_test()
    addition_test()
    multiplication_test()
    hashtesting()
    subtraction_test()
    increment_decrement_test()
    division_test()

    #Grab the global fails variable and report the pass/failure
    global fails
    print_bars()
    if not fails == 0:
        print "Failure: " + str(fails) + " test(s) have failed."
    else:
        print "Success: All tests have passed."
    print_bars()


#Execute all tests
tests()
