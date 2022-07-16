import os
from typing import Any

from n2t.core.rules import *


class HackProcessor:
    def __init__(self, file_path: Any) -> None:
        # ROM
        file: Any = open(file_path, "r")
        self.lines: Any = file.readlines()
        # CPU
        self.ram: [] = [0] * NUM_REGISTERS
        self.a: int = 0
        self.d: int = 0

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
        self.write_result()

    def write_result(self) -> None:
        for line in self.lines:
            self.output_file.write(line)
