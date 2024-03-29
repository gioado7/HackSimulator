import filecmp
from pathlib import Path

import pytest

from n2t.runner.cli import run_hack_simulator

TEST_PROGRAMS = [
    "add",
    "FibonacciElement",
    "max",
    "NestedCall",
    "pong",
    "pong10000",
    "rect",
    "StaticsTest",
    "WorkAround",
]


@pytest.mark.parametrize("program", TEST_PROGRAMS)
def test_should_simulate(program: str, hack_directory: Path) -> None:
    hack_file = str(hack_directory.joinpath(f"{program}.hack"))

    if program == "pong10000":
        run_hack_simulator(hack_file, 10000)
    else:
        run_hack_simulator(hack_file)

    assert filecmp.cmp(
        shallow=False,
        f1=str(hack_directory.joinpath(f"{program}.cmp")),
        f2=str(hack_directory.joinpath(f"{program}.out")),
    )
