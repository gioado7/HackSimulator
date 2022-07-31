import glob
import os
from pathlib import Path
from typing import Iterable

import pytest


@pytest.fixture(scope="module")
def hack_directory(pytestconfig: pytest.Config) -> Iterable[Path]:
    name = pytestconfig.rootpath.joinpath("tests", "e2e")

    yield name

    # finally delete generated .out files
    # files = str(name.joinpath("*.out"))
    # for file in glob.glob(files):
    #     os.remove(file)
