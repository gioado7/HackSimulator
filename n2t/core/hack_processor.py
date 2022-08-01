import ctypes
import os
from typing import Any

from n2t.core.hack_specification import COMP_0, COMP_1, DEST, JUMP, NUM_REGISTERS


class HackProcessor:
    def __init__(self, file_path: Any, num_cycles: int) -> None:
        # ROM and helpers
        file: Any = open(file_path, "r")
        self.lines: Any = file.readlines()
        self.num_cycles: int = num_cycles
        self.been: Any = [False] * NUM_REGISTERS

        # CPU
        self.ram: Any = [0] * NUM_REGISTERS
        self.a: int = 0
        self.d: int = 0
        self.pc: int = 0

        # output
        self.output_file: Any = None
        self.open_output(file_path)
        self.simulate()
        self.close_output()

    def open_output(self, path: Any) -> None:
        output_directory = os.path.dirname(path)
        file = os.path.join(output_directory, os.path.basename(path))
        try:
            os.mkdir(output_directory)
        except OSError:
            pass
        self.output_file = open(file.replace(".hack", ".out"), "w")

    def close_output(self) -> None:
        self.output_file.close()

    def simulate(self) -> None:
        num_iterations = 0
        while num_iterations < self.num_cycles and self.pc < len(self.lines):
            num_iterations += 1
            self.process_instruction(self.lines[self.pc])
        self.write_result()

    def process_instruction(self, instruction: Any) -> Any:
        if instruction[0] == "0":
            self.a = int(instruction, 2)
            self.pc += 1
        else:
            comp: str = COMP_0[instruction[4:10]]
            if instruction[3] == "1":
                comp = COMP_1[instruction[4:10]]
            comp_value: int = self.get_comp_value(comp)
            comp_value = ctypes.c_short(comp_value).value
            dest: str = DEST[instruction[10:13]]
            jump: str = JUMP[instruction[13:16]]
            if jump == "NO":
                self.process_dest(dest, comp_value)
            else:
                self.process_jump(jump, comp_value)

    def process_dest(self, dest: Any, comp_value: Any) -> None:
        if dest == "M":
            self.ram[self.a] = comp_value
            self.been[self.a] = True
        elif dest == "D":
            self.d = comp_value
        elif dest == "DM":
            self.ram[self.a] = comp_value
            self.been[self.a] = True
            self.d = comp_value
        elif dest == "A":
            self.a = comp_value
        elif dest == "AM":
            self.ram[self.a] = comp_value
            self.been[self.a] = True
            self.a = comp_value
        elif dest == "AD":
            self.d = comp_value
            self.a = comp_value
        elif dest == "ADM":
            self.ram[self.a] = comp_value
            self.been[self.a] = True
            self.d = comp_value
            self.a = comp_value
        self.pc += 1

    def process_jump(self, jump: Any, comp_value: Any) -> None:
        if jump == "JGT" and comp_value > 0:
            self.pc = self.a
        elif jump == "JEQ" and comp_value == 0:
            self.pc = self.a
        elif jump == "JGE" and comp_value >= 0:
            self.pc = self.a
        elif jump == "JLT" and comp_value < 0:
            self.pc = self.a
        elif jump == "JNE" and comp_value != 0:
            self.pc = self.a
        elif jump == "JLE" and comp_value <= 0:
            self.pc = self.a
        elif jump == "JMP":
            self.pc = self.a
        else:
            self.pc += 1

    def get_comp_value(self, comp: str) -> Any:
        if comp == "0":
            return 0
        if comp == "1":
            return 1
        if comp == "-1":
            return -1
        if comp == "D":
            return self.d
        if comp == "A":
            return self.a
        if comp == "M":
            return self.ram[self.a]
        if comp == "!D":
            return ~self.d
        if comp == "!A":
            return ~self.a
        if comp == "!M":
            return ~self.ram[self.a]
        if comp == "-D":
            return -self.d
        if comp == "-A":
            return -self.a
        if comp == "-M":
            return -self.ram[self.a]
        if comp == "D+1":
            return self.d + 1
        if comp == "A+1":
            return self.a + 1
        if comp == "M+1":
            return self.ram[self.a] + 1
        if comp == "D-1":
            return self.d - 1
        if comp == "A-1":
            return self.a - 1
        if comp == "M-1":
            return self.ram[self.a] - 1
        if comp == "D+A":
            return self.d + self.a
        if comp == "D+M":
            return self.d + self.ram[self.a]
        if comp == "D-A":
            return self.d - self.a
        if comp == "D-M":
            return self.d - self.ram[self.a]
        if comp == "A-D":
            return self.a - self.d
        if comp == "M-D":
            return self.ram[self.a] - self.d
        if comp == "D&A":
            return self.d & self.a
        if comp == "D&M":
            return self.d & self.ram[self.a]
        if comp == "D|A":
            return self.d | self.a
        if comp == "D|M":
            return self.d | self.ram[self.a]

    def write_result(self) -> None:
        for i in range(0, NUM_REGISTERS):
            if self.been[i]:
                self.output_file.write(str('{0:032b}'.format(self.ram[i])[16:]) + "\n")
            else:
                self.output_file.write("\n")
