# SPDX-FileCopyrightText: 2023-2026, NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Command-line entry point and top-level workflow coordination for pyopmnearwell.

pyopmnearwell supports two connected workflows for near-well OPM Flow models:

* Deck generation creates model-specific OPM Flow input and include files from a
  validated TOML configuration.
* Simulation execution runs OPM Flow for the generated deck, either in separate
  preprocessing and output folders or in a shared folder.

This module parses and validates command-line arguments, initializes the shared
configuration dictionary, creates output folders, dispatches the selected deck
and simulation workflows, and reports generated files. Configuration handling,
deck writing, and simulation execution are implemented in the utility modules.
"""

import argparse
import os
import pathlib
from typing import Any

from pyopmnearwell.utils.inputvalues import process_input
from pyopmnearwell.utils.runs import simulations
from pyopmnearwell.utils.terminal import (
    cli_error_value,
    pyopmnearwell_error,
    pyopmnearwell_info,
    pyopmnearwell_success,
)
from pyopmnearwell.utils.writefile import reservoir_files


def main(argv: list[str] | None = None) -> None:
    """Run the pyopmnearwell command-line workflow.

    Parse and validate CLI arguments, initialize the shared configuration, create
    the requested output folders, and dispatch deck generation and OPM Flow
    execution according to the selected mode.

    Parameters
    ----------
    argv : list[str] | None, optional
        Arguments to parse instead of ``sys.argv[1:]``. This is primarily used by
        tests and programmatic callers.
    """
    cmdargs = load_parser(argv)
    check_cmdargs(cmdargs)
    file = cmdargs.input
    fol = os.path.abspath(cmdargs.output)
    mode = cmdargs.mode
    dic: dict[str, Any] = {
        "pat": os.path.split(os.path.dirname(__file__))[0],
        "fol": fol,
        "mode": mode,
        "write": int(cmdargs.vectors),
        "runname": pathlib.Path(file).stem,
    }
    dic = process_input(dic, file)
    os.makedirs(fol, exist_ok=True)
    if mode == "single":
        dic["fprep"] = fol
        dic["foutp"] = fol
    else:
        dic["fprep"] = f"{fol}/preprocessing"
        dic["foutp"] = f"{fol}/output"
    if mode in ["all", "deck", "single"]:
        pyopmnearwell_info("generating the deck files, please wait...")
        os.makedirs(dic["fprep"], exist_ok=True)
        generated_files = reservoir_files(dic)
        pyopmnearwell_success("", dic["fprep"], sorted(generated_files))
    if mode in ["all", "flow", "single"]:
        pyopmnearwell_info("running OPM Flow, please wait...")
        os.makedirs(dic["foutp"], exist_ok=True)
        simulations(dic)
        pyopmnearwell_success(
            "the simulation results have been written to", dic["foutp"], []
        )


def load_parser(argv: list[str] | None) -> argparse.Namespace:
    """Create the CLI parser and parse pyopmnearwell arguments.

    Parameters
    ----------
    argv : list[str] | None
        Arguments to parse instead of ``sys.argv[1:]``. This is primarily used by
        tests and programmatic callers.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Main script to run a near-well system with OPM Flow.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str.strip,
        default="input.toml",
        help="The base name of the input file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str.strip,
        default="output",
        help="The base name of the output folder",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str.strip,
        choices=["deck", "flow", "single", "all"],
        default="all",
        help="Run the whole framework ('all'), only generate the deck ('deck'), "
        "only run flow ('flow'), or generate the deck and run flow in the same "
        "output folder ('single')",
    )
    parser.add_argument(
        "-v",
        "--vectors",
        type=str.strip,
        choices=["0", "1"],
        default="1",
        help="Write cell values, i.e., EGRID, INIT, UNRST",
    )
    return parser.parse_args(argv)


def check_cmdargs(cmdargs: argparse.Namespace) -> None:
    """Validate pyopmnearwell command-line arguments.

    Validation covers the input configuration filename and the output directory.

    Parameters
    ----------
    cmdargs : argparse.Namespace
        Parsed command-line arguments.

    Raises
    ------
    SystemExit
        If the input filename is empty, does not use the ``.toml`` extension, or
        the output directory is empty.
    """
    input_file = cmdargs.input
    if not input_file:
        pyopmnearwell_error(
            f"Invalid value for {cli_error_value('-i')}, the input file cannot be empty."
        )
    if not input_file.lower().endswith(".toml"):
        pyopmnearwell_error(
            f"Invalid extension {cli_error_value(f'-i {input_file}')}, "
            "the valid extension is .toml."
        )
    if not cmdargs.output:
        pyopmnearwell_error(
            f"invalid value {cli_error_value('-o')}, the output folder cannot be empty."
        )
