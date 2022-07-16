from __future__ import annotations

from dataclasses import dataclass

from n2t.core.hack_processor import HackProcessor


@dataclass
class HackSimulator:
    file_or_directory: str

    @classmethod
    def load_from(cls, file_or_directory_name: str) -> HackSimulator:
        cls.file_or_directory = file_or_directory_name
        return cls()

    def __init__(self) -> None:
        pass

    def simulate(self) -> None:
        HackProcessor(self.file_or_directory)
