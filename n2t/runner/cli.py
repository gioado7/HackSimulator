from typer import Typer, echo

from n2t.core import HackSimulator

cli = Typer(
    name="N2T Software",
    no_args_is_help=True,
    add_completion=False,
)


@cli.command("execute", no_args_is_help=True)
def run_hack_simulator(hack_file_directory: str, cycles: int = 1000000) -> None:
    echo(f"Simulating {hack_file_directory}")
    HackSimulator.load_from(hack_file_directory).simulate(cycles)
    echo("Done!")


@cli.command("nothing", no_args_is_help=True)
def run_nothing() -> None:
    pass
