import os
from typing import Any

from n2t.core.rules import COMP_0, COMP_1, DEST, JUMP, NUM_REGISTERS


class HackProcessor:
    def __init__(self, file_path: Any) -> None:
        # ROM
        file: Any = open(file_path, "r")
        self.lines: Any = file.readlines()
        # CPU
        self.ram: [] = [0] * NUM_REGISTERS
        self.a: int = 0
        self.d: int = 0
        self.pc: int = 0

        # output
        self.output_file = None
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
        x = 0
        while x < 1000000 and self.pc < len(self.lines):
            x += 1
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
            dest: str = DEST[instruction[10:13]]
            jump: str = JUMP[instruction[13:16]]
            if jump == "NO":
                if dest == "M":
                    self.ram[self.a] = comp_value
                elif dest == "D":
                    self.d = comp_value
                elif dest == "DM":
                    self.ram[self.a] = comp_value
                    self.d = comp_value
                elif dest == "A":
                    self.a = comp_value
                elif dest == "AM":
                    self.a = comp_value
                    self.ram[self.a] = comp_value
                elif dest == "AD":
                    self.a = comp_value
                    self.d = comp_value
                elif dest == "ADM":
                    self.a = comp_value
                    self.d = comp_value
                    self.ram[self.a] = comp_value
                self.pc += 1
            else:
                if jump == "JGT":
                    if comp_value > 0:
                        self.pc = self.a
                    else:
                        self.pc += 1
                elif jump == "JEQ":
                    if comp_value == 0:
                        self.pc = self.a
                    else:
                        self.pc += 1
                elif jump == "JGE":
                    if comp_value >= 0:
                        self.pc = self.a
                    else:
                        self.pc += 1
                elif jump == "JLT":
                    if comp_value < 0:
                        self.pc = self.a
                    else:
                        self.pc += 1
                elif jump == "JNE":
                    if comp_value != 0:
                        self.pc = self.a
                    else:
                        self.pc += 1
                elif jump == "JLE":
                    if comp_value <= 0:
                        self.pc = self.a
                    else:
                        self.pc += 1
                elif jump == "JMP":
                    self.pc = self.a
                else:
                    self.pc += 1

    def get_comp_value(self, comp) -> int:
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
            if self.ram[i] != 0:
                print(i, end=":  ")
                print(self.ram[i])
