# SPDX-FileCopyrightText: 2023-2026, NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Main script for pyopmnearwell"""

import argparse
import os
import pathlib
import warnings
from typing import Any

from pyopmnearwell.utils.inputvalues import process_input
from pyopmnearwell.utils.runs import simulations
from pyopmnearwell.utils.writefile import reservoir_files


def main(argv: list[str] | None = None) -> None:
    """Main function for the pyopmnearwell executable"""
    cmdargs = load_parser(argv)
    check_cmdargs(cmdargs)
    if int(cmdargs.warnings) == 0:
        warnings.filterwarnings("ignore")
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
        os.makedirs(dic["fprep"], exist_ok=True)
        reservoir_files(dic)
    if mode in ["all", "flow", "single"]:
        os.makedirs(dic["foutp"], exist_ok=True)
        simulations(dic)


def load_parser(argv: list[str] | None) -> argparse.Namespace:
    """CLI arguments"""
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
    parser.add_argument(
        "-w",
        "--warnings",
        type=str.strip,
        choices=["0", "1"],
        default="0",
        help="Print Python warnings",
    )
    return parser.parse_args(argv)


def check_cmdargs(cmdargs: argparse.Namespace) -> None:
    """Validate command-line arguments.

    The checks cover the input configuration file and output folder.

    Parameters
    ----------
    cmdargs
        Parsed arguments returned by :mod:`argparse`.

    Raises
    ------
    SystemExit
        If an argument is invalid.
    """
    input_file = cmdargs.input
    if not input_file:
        print("\nInvalid value for '-i', the input file cannot be empty.\n")
        raise SystemExit(1)
    if not input_file.lower().endswith(".toml"):
        print(
            f"\nInvalid extension for input file '-i {input_file}', "
            "the valid extension is .toml.\n"
        )
        raise SystemExit(1)
    if not cmdargs.output:
        print("\nInvalid value for '-o', the output folder cannot be empty.\n")
        raise SystemExit(1)
