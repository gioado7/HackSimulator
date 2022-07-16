# helper constants for hack processing

NUM_REGISTERS = 32768

DEST = {
    "000": "NULL",
    "001": "RAM[A]",
    "010": "D",
    "011": "RAM[A]D",
    "100": "A",
    "101": "RAM[A]A",
    "110": "AD",
    "111": "RAM[A]AD",
}

JUMP = {
    "000": "NO",
    "001": "JGT",
    "010": "JEQ",
    "011": "JGE",
    "100": "JLT",
    "101": "JNE",
    "110": "JLE",
    "111": "JMP",
}
