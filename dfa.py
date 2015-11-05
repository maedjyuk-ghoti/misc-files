
# Take in a file and parse instructions for their level of execution.
#    0 - can be executed immediately
#    1 - dependent on 0 that can be executed after one-cycle-delay
#    2+ - etc

# Instruction can take the following forms:
#    add <dest_reg>, <src1_reg>, <src2_reg>
#    sub <dest_reg>, <src1_reg>, <src2_reg>
#    addi <dest_reg>, <src1_reg>, <immediate>  # no src2 register
#    subi <dest_reg>, <src1_reg>, <immediate>  # no src2 register
#    lw <dest_reg>, <offset>(<src1_reg>)  # no src2 register
#    sw <src1_reg>, <offset>(<src2_reg>)  # no src2 register

# Running this program
#    dfa.py [-r] [-l<cycles>] <input-file-name>
#    -r - register renaming
#    -l<cycles> - load delay of specified cycles, default of 1 (ex. -l3)
#    input-file-name

# Register renaming
#    The architecture registers are $0 - $7.
#    If renaming is requested, physical registers start at 10

#!/bin/python
import sys
import copy


def read_in_file(filename):
    ''' Reads the file specified by filename into an array '''
    count = 0
    array = []
    with open(filename, 'r') as file_handle:
        for line in file_handle:
            line = "{0} ".format(count) + line
            array.append(line.replace(',', ' ').replace('\n', '').split())
            count += 1
    return array


def rename(array):
    ''' renames all desitnation registers and references to them througout the
        instructions contained in array '''
    renamed = {}
    register = '10'
    for line in array:
        if "(" in line[3]:
            line.append("-")
            if line[3][3:4] in renamed:
                line[3] = renamed[line[3][3:4]]
            else:
                line[3] = line[3][3]
        elif line[3] in renamed:
            line[3] = renamed[line[3]]
        else:
            line[3] = line[3][1]
        if line[1] == "add" or line[1] == "sub":
            if line[4] in renamed:
                line[4] = renamed[line[4]]
            else:
                line[4] = line[4][1]
        elif line[1] == "addi" or line[1] == "subi":
            line[4] = "-"

        renamed[line[2]] = register
        line[2] = renamed[line[2]]
        register = str(int(register) + 1)
    return array


def dest_register_finder(instruction):
    ''' Returns the index of the destination register for the instruction '''
    return 3 if instruction[1] == "sw" else 2


def src1_register_finder(instruction):
    ''' Returns the index of the first source register for the instruction '''
    return 2 if instruction[1] == "sw" else 3


def src2_register_finder(instruction):
    ''' Returns the index of the second source register for the instruction '''
    return 4 if instruction[1] == "add" or instruction[1] == "sub" else -1


def raw(inst1, inst2):
    ''' Returns true if a read after write dependency is found '''
    #add dest src1 src2
    #sub dest src1 src2
    if inst1[1] == "add" or inst1[1] == "sub":
        if inst1[3] == inst2[dest_register_finder(inst2)] or\
                inst1[4] == inst2[dest_register_finder(inst2)]:
            return True

    #addi dest src1 const
    #subi dest src1 const
    #lw   dest src1
    if inst1[1] == "addi" or inst1[1] == "subi" or inst1[1] == "lw":
        if inst1[3] == inst2[dest_register_finder(inst2)]:
            return True

    #sw src1 dest
    if inst1[1] == "sw":
        if inst1[2] == inst2[dest_register_finder(inst2)]:
            return True

    #No raw dependency
    return False


def war(inst1, inst2):
    ''' Returns true if a write after read dependency is found '''
    #sw src1 dest
    if inst1[1] == "sw":
        if inst1[3] == inst2[src1_register_finder(inst2)]:
            return True
        if src2_register_finder(inst2) != -1:
            if inst1[3] == inst2[src2_register_finder(inst2)]:
                return True

    #add  dest src1 src2
    #sub  dest src1 src2
    #addi dest src1 const
    #subi dest src1 const
    #lw   dest src1
    else:
        if inst1[2] == inst2[src1_register_finder(inst2)]:
            return True
        if src2_register_finder(inst2) != -1:
            if inst1[2] == inst2[src2_register_finder(inst2)]:
                return True

    #No war dependency
    return False


def waw(inst1, inst2):
    ''' Returns true if a read after write dependency is found '''
    #sw src1 dest
    if inst1[1] == "sw":
        if inst1[3] == inst2[dest_register_finder(inst2)]:
            return True

    #add  dest src1 src2
    #sub  dest src1 src2
    #addi dest src1 const
    #subi dest src1 const
    #lw   dest src1
    else:
        if inst1[2] == inst2[dest_register_finder(inst2)]:
            return True

    #No war dependency
    return False


def dependency_finder(instruction, other_insts):
    ''' returns true instruction is dependent on any of the items in other_insts
        returns false if it is independent of the items in other_insts '''
    for other_inst in other_insts:
        if raw(instruction, other_inst) or\
                war(instruction, other_inst) or\
                waw(instruction, other_inst):
            return True
    return False


def reformat(array):
    ''' takes in a 2D array and returns a 1D array '''
    temp = []
    for item in array:
        temp.append(item[0])
    return temp


if __name__ == "__main__":
    #Only checking for number of args, not an exhaustive check
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        sys.exit("\tIncorrect number of args.\n\
                  \tUsage: {0} [-r] [-l<cycles>] <input-file-name>\n"
                  .format(sys.argv[0]))

    #Argument collection
    renaming = False
    load_delay = 1
    file_name = ""
    for i in range(1, len(sys.argv)):
        if "-r" in sys.argv[i]:
            renaming = True
        elif "-l" in sys.argv[i]:
            load_delay = int(sys.argv[i][2:])
        else:
            file_name = sys.argv[i]

    #Output file name, load delay, and whether renaming will be used
    print(("output for \"./{0}\"".format(str(sys.argv[0:])
            .translate(None, ''.join(['[', ']', '\'', ','])))))
    print(("load delay set to {}".format(load_delay)))

    #####################
    ### DFA work area ###
    #####################

    #Instuctions that have not been determined to execute
    real_insts = read_in_file(file_name)

    #Rename the registers right away if required
    instructions_waiting = rename(copy.deepcopy(real_insts))\
            if renaming else copy.deepcopy(real_insts)

    step_buffer = []             # Stores instructions that have not executed
    instructions_completed = []  # Stores instructions that have executed
    delete_buffer = []           # Used to delete instructions from step_buffer
    cycle = 0                    # Cycle that is currently being considered
    delay = 0                    # Delay the instruction will have
    first = True                 # True if first print of cycle, False otherwise

    #loop until all instructions are associated with a step
    while len(instructions_waiting) > 0:
        #Pass through the loop once to check if any instructions dependencies
        #  have been met/none exist
        for instruction in instructions_waiting:
            #If it is the first instruction then it has no instructions before
            #  itself to depend on
            if instructions_waiting.index(instruction) == 0:
                pass
            #Compare to instructions that come before it
            elif dependency_finder(instruction,
                    instructions_waiting[:instructions_waiting.
                        index(instruction)]):
                continue
            #Compare to instructions waiting to finish
            if dependency_finder(instruction, reformat(step_buffer)):
                continue

            #If no dependincies, determine delay; always 1 unless a lw inst
            if instruction[1] == "lw":
                delay = load_delay
            else:
                delay = 1

            #Add to step_buffer with its delay time
            step_buffer.append([instruction, delay])

            if first:
                print(("level {0} instructions:".format(cycle)))
                first = False

            if renaming:
                print(("   {0} {1}\t{2} with renaming d/s1/s2 regs to {3}"
                        .format(real_insts[int(instruction[0])][0],
                        real_insts[int(instruction[0])][1],
                        ','.join(real_insts[int(instruction[0])][2:]),
                        ' '.join(instruction[2:]))))
            else:
                print(("   {0} {1}\t{2}".format(instruction[0],
                        instruction[1], ','.join(instruction[2:]))))

        #Clean up before next cycle/level
        #Remove instructions that are in step_buffer from instructions_waiting
        for buffered in step_buffer:
            try:
                instructions_waiting.remove(buffered[0])
            except ValueError:
                # do nothing
                pass

            #Decrement delay time remaining for instructions in step_buffer
            buffered[-1] -= 1

            #Check if delay time expired
            if buffered[-1] == 0:
                instructions_completed.append(buffered[0])
                delete_buffer.append(buffered)

        #Housekeeping: remove completed items from step_buffer
        for deleted in delete_buffer:
            try:
                step_buffer.remove(deleted)
            except ValueError:
                pass
        delete_buffer = []

        #End of one cycle
        cycle += 1
        first = True

    #All instructions executed
    print(("the data flow can be executed in {} cycles".format(cycle)))
