# SPDX-FileCopyrightText: 2023-2026, NORCE Research AS
# SPDX-License-Identifier: GPL-3.0
# pylint: disable=R0912,R0913,R0914,R0915,R0917,C0302
"""Read, validate, and initialize pyopmnearwell configuration values.

The module loads TOML input, applies defaults, validates full simulations and
table-only configurations, reports ineffective values, checks expressions used
by table generation, normalizes optional TUNING records, and derives grid and
runtime values stored in the shared configuration dictionary.
"""

import ast
import tomllib
from typing import Any

import numpy as np

from pyopmnearwell.utils.terminal import (
    cli_correct_value,
    cli_error_value,
    cli_warning_value,
    pyopmnearwell_error,
    pyopmnearwell_warning,
)


def process_input(dic, in_file):
    """Load, validate, and initialize the shared configuration dictionary.

    Parameters
    ----------
    dic : Any
        Shared pyopmnearwell configuration dictionary.
    in_file : Any
        Path to the TOML configuration file.

    Returns
    -------
    Any
        Result produced by the operation.

    Raises
    ------
    SystemExit
        If the documented validation or operation fails.
    """
    for name in [
        "ehystr",
        "rockcomp",
        "xflow",
        "confact",
        "removecells",
        "econ",
        "xfac",
        "pcfact",
        "salinity",
    ]:
        dic[name] = 0
    dic["zxy"] = "0*x"
    dic["adim"] = 1
    dic["perforations"] = [0, 0, 0]
    dic["ycn"] = [1]
    with open(in_file, "rb") as file:
        cfg_file = _validate_toml(tomllib.load(file))
    dic.update(cfg_file)
    if "flow" not in dic:
        if "safu" not in dic:
            dic["safu"] = [1]
        if "template" not in dic:
            dic["template"] = "base"
        if "model" not in dic:
            dic["model"] = "co2store"
        dic["imbnum"] = 2 if dic["ehystr"] != 0 else 1
        return dic
    dic["satnum"] = len(dic["rock"]) - dic["perforations"][0]
    dic["fluxnum"] = len(dic["rock"]) > 1
    dic["imbnum"] = 2 if dic["ehystr"] != 0 else 1
    zdim, znc, dic["homo"], tmp = 0.0, 0, True, dic["rock"][0][3]
    for index, rock in enumerate(dic["rock"]):
        if len(rock) > 3:
            zdim += rock[3]
            znc += rock[4]
            if index > 0 and tmp != rock[3] and dic["homo"]:
                dic["homo"] = False
            tmp = rock[3]
    dic["zcn"] = [znc]
    if dic["grid"] in ["coord2d", "coord3d"]:
        dic["nocells"] = [len(dic["xcn"]) - 1, 1, np.sum(dic["zcn"])]
    else:
        dic["nocells"] = [np.sum(dic["xcn"]), 1, np.sum(dic["zcn"])]
    dic["dims"] = [dic["xdim"], dic["adim"], zdim]
    process_tuning(dic)
    return dic


def process_tuning(dic):
    """Detect Flow TUNING support and normalize TUNING records in the injection schedule.

    Parameters
    ----------
    dic : Any
        Shared pyopmnearwell configuration dictionary.

    Returns
    -------
    Any
        Result produced by the operation.
    """
    dic["tuning"] = any(
        value.lower() in {"--enable-tuning=true", "--enable-tuning=1"}
        for value in dic["flow"].split()
    )
    for index, inj in enumerate(dic["inj"]):
        is_bhp = len(inj) > 4 and not isinstance(inj[4], str) and inj[4] > 0
        size = 6 if dic["model"] == "h2store" and (inj[3] < 0 or is_bhp) else 5
        if len(inj) == size:
            if not isinstance(inj[-1], str):
                pyopmnearwell_error(
                    "After the 2025.04 release, column 3 for the maximum solver "
                    "time step in the injection has been moved to the end of the "
                    "column, including the items for the TUNING keyword, which "
                    "gives more control when setting the simulations. Please see "
                    "the configuration files in the examples and online "
                    "documentation (Configuration file->Well-related parameters), "
                    "and update your configuration file accordingly."
                )
            parts = inj[-1].split("/")
            dic["inj"][index][-1] = parts[0].strip()
            dic["inj"][index].extend(value.strip() for value in parts[1:])


def _is_finite_number(value: Any) -> bool:
    """Return whether a value is a finite, non-Boolean number.

    Parameters
    ----------
    value : Any
        Value used by the operation.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and bool(np.isfinite(value))
    )


def _is_integer(value: Any) -> bool:
    """Return whether a value is a non-Boolean integer.

    Parameters
    ----------
    value : Any
        Value used by the operation.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    return isinstance(value, int) and not isinstance(value, bool)


def _add_validation_error(errors: list[str], message: str) -> None:
    """Append a TOML validation message to the collected errors.

    Parameters
    ----------
    errors : list[str]
        Validation messages collected so far.
    message : str
        Value used by the operation.
    """
    errors.append(message)


def _validate_string(cfg_file: dict[str, Any], key: str, errors: list[str]) -> bool:
    """Validate a non-empty TOML string.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    key : str
        Name of the TOML variable.
    errors : list[str]
        Validation messages collected so far.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    if key not in cfg_file:
        return False
    value = cfg_file[key]
    if not isinstance(value, str) or not value.strip():
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} has invalid value "
            f"{cli_error_value(str(value))}, expected "
            f"{cli_correct_value('a non-empty string')}.",
        )
        return False
    return True


def _validate_number(
    cfg_file: dict[str, Any],
    key: str,
    errors: list[str],
    minimum: float | None = None,
    strict: bool = False,
) -> bool:
    """Validate a finite TOML number and its optional lower bound.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    key : str
        Name of the TOML variable.
    errors : list[str]
        Validation messages collected so far.
    minimum : float | None, optional
        Optional inclusive or exclusive lower bound.
    strict : bool, optional
        Whether ``minimum`` is an exclusive bound.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    if key not in cfg_file:
        return False
    value = cfg_file[key]
    if not _is_finite_number(value):
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} has invalid value "
            f"{cli_error_value(str(value))}, expected "
            f"{cli_correct_value('a finite number')}.",
        )
        return False
    if minimum is None:
        return True
    valid = value > minimum if strict else value >= minimum
    if valid:
        return True
    condition = (
        f"a value greater than {minimum}"
        if strict
        else f"a value greater than or equal to {minimum}"
    )
    _add_validation_error(
        errors,
        f"variable {cli_error_value(key)} has invalid value "
        f"{cli_error_value(str(value))}, expected "
        f"{cli_correct_value(condition)}.",
    )
    return False


def _validate_array(
    cfg_file: dict[str, Any],
    key: str,
    errors: list[str],
    length: int | None = None,
    integer: bool = False,
    minimum: float | None = None,
    strict: bool = False,
    nonempty: bool = False,
) -> bool:
    """Validate a numeric TOML array, its shape, and its entries.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    key : str
        Name of the TOML variable.
    errors : list[str]
        Validation messages collected so far.
    length : int | None, optional
        Required array length.
    integer : bool, optional
        Whether every array entry must be an integer.
    minimum : float | None, optional
        Optional inclusive or exclusive lower bound.
    strict : bool, optional
        Whether ``minimum`` is an exclusive bound.
    nonempty : bool, optional
        Whether at least one array entry is required.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    if key not in cfg_file:
        return False
    value = cfg_file[key]
    if not isinstance(value, list):
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} has invalid type "
            f"{cli_error_value(type(value).__name__)}, expected "
            f"{cli_correct_value('an array')}.",
        )
        return False
    if length is not None and len(value) != length:
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} has "
            f"{cli_error_value(str(len(value)))} entries, expected "
            f"{cli_correct_value(str(length))}.",
        )
        return False
    if nonempty and not value:
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} must contain "
            f"{cli_correct_value('at least one entry')}.",
        )
        return False
    valid = True
    for index, entry in enumerate(value):
        correct_type = _is_integer(entry) if integer else _is_finite_number(entry)
        expected = "an integer" if integer else "a finite number"
        if not correct_type:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'{key}[{index}]')} has invalid "
                f"value {cli_error_value(str(entry))}, expected "
                f"{cli_correct_value(expected)}.",
            )
            valid = False
            continue
        if minimum is None:
            continue
        in_range = entry > minimum if strict else entry >= minimum
        if not in_range:
            condition = (
                f"a value greater than {minimum}"
                if strict
                else f"a value greater than or equal to {minimum}"
            )
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'{key}[{index}]')} has invalid "
                f"value {cli_error_value(str(entry))}, expected "
                f"{cli_correct_value(condition)}.",
            )
            valid = False
    return valid


def _validate_expression(cfg_file: dict[str, Any], key: str, errors: list[str]) -> None:
    """Validate a saturation expression with a restricted Python AST.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    key : str
        Name of the TOML variable.
    errors : list[str]
        Validation messages collected so far.
    """
    if not _validate_string(cfg_file, key, errors):
        return
    allowed_names = {
        "krn",
        "krw",
        "nkrn",
        "nkrw",
        "npen",
        "np",
        "pen",
        "sni",
        "sw",
        "swi",
    }
    allowed_functions = {
        "abs",
        "clip",
        "exp",
        "log",
        "log10",
        "max",
        "maximum",
        "min",
        "minimum",
        "power",
        "sqrt",
        "where",
    }
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Attribute,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.UAdd,
        ast.USub,
    )
    try:
        tree = ast.parse(cfg_file[key], mode="eval")
    except SyntaxError as err:
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} contains invalid Python "
            f"expression {cli_error_value(cfg_file[key])}: {err.msg}.",
        )
        return
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    if "sw" not in names:
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} must reference "
            f"{cli_correct_value('sw')}.",
        )
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            _add_validation_error(
                errors,
                f"variable {cli_error_value(key)} contains unsafe expression "
                f"element {cli_error_value(type(node).__name__)}.",
            )
            return
        if isinstance(node, ast.Name) and node.id not in allowed_names:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(key)} contains unsupported name "
                f"{cli_error_value(node.id)}.",
            )
            return
        if isinstance(node, ast.Attribute):
            valid = (
                isinstance(node.value, ast.Name)
                and node.value.id == "np"
                and node.attr in allowed_functions
            )
            if not valid:
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(key)} contains unsupported "
                    f"attribute {cli_error_value(ast.unparse(node))}.",
                )
                return
        if isinstance(node, ast.Call):
            valid = (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "np"
                and node.func.attr in allowed_functions
                and not node.keywords
                and not any(isinstance(argument, ast.Starred) for argument in node.args)
            )
            if not valid:
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(key)} contains an unsafe "
                    "function call, expected a positional call to an approved "
                    f"NumPy function such as {cli_correct_value('np.maximum')}.",
                )
                return


def _validate_rock(cfg_file: dict[str, Any], errors: list[str]) -> bool:
    """Validate rock-property records.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    errors : list[str]
        Validation messages collected so far.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    if "rock" not in cfg_file:
        return False
    rock = cfg_file["rock"]
    if not isinstance(rock, list) or not rock:
        _add_validation_error(
            errors,
            f"variable {cli_error_value('rock')} must contain "
            f"{cli_correct_value('at least one rock record')}.",
        )
        return False
    valid = True
    for row_index, row in enumerate(rock):
        if not isinstance(row, list) or len(row) not in {3, 5}:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'rock[{row_index}]')} must be "
                f"{cli_correct_value('an array with 3 or 5 entries')}.",
            )
            valid = False
            continue
        if len(row) == 3 and row_index != len(rock) - 1:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'rock[{row_index}]')} has 3 "
                "entries, but only the final boundary-rock record may omit "
                f"thickness and cell count {cli_correct_value('(5 entries)')}.",
            )
            valid = False
        for column_index, entry in enumerate(row):
            if not _is_finite_number(entry):
                _add_validation_error(
                    errors,
                    f"variable "
                    f"{cli_error_value(f'rock[{row_index}][{column_index}]')} "
                    f"has invalid value {cli_error_value(str(entry))}, expected "
                    f"{cli_correct_value('a finite number')}.",
                )
                valid = False
        if not all(_is_finite_number(entry) for entry in row):
            continue
        if row[0] < 0 or row[1] < 0:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'rock[{row_index}]')} must have "
                f"{cli_correct_value('non-negative permeabilities')}.",
            )
            valid = False
        if not 0 <= row[2] <= 1:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'rock[{row_index}][2]')} has "
                f"invalid value {cli_error_value(str(row[2]))}, expected "
                f"{cli_correct_value('a value between 0 and 1')}.",
            )
            valid = False
        if len(row) == 5:
            if row[3] <= 0:
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(f'rock[{row_index}][3]')} must "
                    f"be {cli_correct_value('positive')}.",
                )
                valid = False
            if not _is_integer(row[4]) or row[4] <= 0:
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(f'rock[{row_index}][4]')} must "
                    f"be {cli_correct_value('a positive integer')}.",
                )
                valid = False
    if isinstance(rock[0], list) and len(rock[0]) != 5:
        _add_validation_error(
            errors,
            f"variable {cli_error_value('rock[0]')} must include thickness and "
            "cell count because it defines the first physical layer.",
        )
        valid = False
    return valid


def _validate_safu(cfg_file: dict[str, Any], errors: list[str]) -> None:
    """Validate saturation-function parameter records.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    errors : list[str]
        Validation messages collected so far.
    """
    if "safu" not in cfg_file:
        return
    safu = cfg_file["safu"]
    if not isinstance(safu, list) or not safu:
        _add_validation_error(
            errors,
            f"variable {cli_error_value('safu')} must contain "
            f"{cli_correct_value('at least one record')}.",
        )
        return
    for row_index, row in enumerate(safu):
        if not isinstance(row, list) or len(row) != 11:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'safu[{row_index}]')} must be "
                f"{cli_correct_value('an array with 11 entries')}.",
            )
            continue
        numeric = True
        for column_index, entry in enumerate(row):
            if not _is_finite_number(entry):
                _add_validation_error(
                    errors,
                    f"variable "
                    f"{cli_error_value(f'safu[{row_index}][{column_index}]')} "
                    f"has invalid value {cli_error_value(str(entry))}, expected "
                    f"{cli_correct_value('a finite number')}.",
                )
                numeric = False
        if not numeric:
            continue
        if not 0 <= row[0] <= 1 or not 0 <= row[1] <= 1:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'safu[{row_index}]')} has invalid "
                f"endpoint saturations, expected {cli_correct_value('values between 0 and 1')}.",
            )
        if row[0] + row[1] > 1:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'safu[{row_index}]')} has endpoint "
                "saturations with a combined value greater than "
                f"{cli_correct_value('1')}.",
            )
        for column_index in range(2, 10):
            if row[column_index] < 0:
                _add_validation_error(
                    errors,
                    f"variable "
                    f"{cli_error_value(f'safu[{row_index}][{column_index}]')} "
                    f"must be {cli_correct_value('non-negative')}.",
                )
        if not _is_integer(row[10]) or row[10] < 2:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'safu[{row_index}][10]')} must be "
                f"{cli_correct_value('an integer greater than or equal to 2')}.",
            )


def _validate_injection(cfg_file: dict[str, Any], errors: list[str]) -> bool:
    """Validate injection schedule records and detect TUNING values.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    errors : list[str]
        Validation messages collected so far.

    Returns
    -------
    bool
        Whether at least one injection record defines TUNING values.
    """
    if "inj" not in cfg_file:
        return False
    inj = cfg_file["inj"]
    if not isinstance(inj, list) or not inj:
        _add_validation_error(
            errors,
            f"variable {cli_error_value('inj')} must contain "
            f"{cli_correct_value('at least one injection record')}.",
        )
        return False
    tuning_defined = False
    model = cfg_file.get("model")
    for row_index, row in enumerate(inj):
        valid_lengths = {4, 5, 6} if model == "h2store" else {4, 5}
        if not isinstance(row, list) or len(row) not in valid_lengths:
            expected = "4, 5, or 6 entries" if model == "h2store" else "4 or 5 entries"
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'inj[{row_index}]')} has invalid "
                f"structure, expected {cli_correct_value(expected)}.",
            )
            continue
        for column_index in range(4):
            entry = row[column_index]
            variable = f"inj[{row_index}][{column_index}]"
            if column_index == 2:
                if not _is_integer(entry) or entry not in {0, 1}:
                    _add_validation_error(
                        errors,
                        f"variable {cli_error_value(variable)} has invalid value "
                        f"{cli_error_value(str(entry))}, expected "
                        f"{cli_correct_value('0 or 1')}.",
                    )
            elif not _is_finite_number(entry):
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(variable)} has invalid value "
                    f"{cli_error_value(str(entry))}, expected "
                    f"{cli_correct_value('a finite number')}.",
                )
        for column_index in (0, 1):
            entry = row[column_index]
            if _is_finite_number(entry) and entry <= 0:
                _add_validation_error(
                    errors,
                    f"variable "
                    f"{cli_error_value(f'inj[{row_index}][{column_index}]')} "
                    f"must be {cli_correct_value('positive')}.",
                )
        if model != "h2store" and _is_finite_number(row[3]) and row[3] < 0:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'inj[{row_index}][3]')} must be "
                f"{cli_correct_value('non-negative')} for model "
                f"{cli_error_value(str(model))}.",
            )
        extras = row[4:]
        if extras and _is_finite_number(extras[0]):
            if model != "h2store" or extras[0] <= 0:
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(f'inj[{row_index}][4]')} has "
                    f"invalid value {cli_error_value(str(extras[0]))}, expected "
                    f"{cli_correct_value('a positive h2store BHP limit')}.",
                )
            extras = extras[1:]
        if extras:
            tuning_defined = True
            if (
                len(extras) != 1
                or not isinstance(extras[0], str)
                or not extras[0].strip()
            ):
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(f'inj[{row_index}]')} has an "
                    f"invalid TUNING value, expected "
                    f"{cli_correct_value('a non-empty final string')}.",
                )
        if len(row) == 5 and isinstance(row[4], str):
            tuning_defined = True
        if len(row) == 6 and isinstance(row[5], str):
            tuning_defined = True
    return tuning_defined


def _validate_records(
    cfg_file: dict[str, Any],
    key: str,
    errors: list[str],
    columns: int,
    minimum: float | None = None,
) -> bool:
    """Validate a non-empty matrix of fixed-width numeric records.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    key : str
        Name of the TOML variable.
    errors : list[str]
        Validation messages collected so far.
    columns : int
        Required number of values in each record.
    minimum : float | None, optional
        Optional inclusive or exclusive lower bound.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    if key not in cfg_file:
        return False
    records = cfg_file[key]
    if not isinstance(records, list) or not records:
        _add_validation_error(
            errors,
            f"variable {cli_error_value(key)} must contain "
            f"{cli_correct_value('at least one record')}.",
        )
        return False
    valid = True
    for row_index, row in enumerate(records):
        if not isinstance(row, list) or len(row) != columns:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'{key}[{row_index}]')} must have "
                f"{cli_correct_value(str(columns))} entries.",
            )
            valid = False
            continue
        for column_index, entry in enumerate(row):
            if not _is_finite_number(entry):
                _add_validation_error(
                    errors,
                    f"variable "
                    f"{cli_error_value(f'{key}[{row_index}][{column_index}]')} "
                    f"must be {cli_correct_value('a finite number')}.",
                )
                valid = False
            elif minimum is not None and entry < minimum:
                _add_validation_error(
                    errors,
                    f"variable "
                    f"{cli_error_value(f'{key}[{row_index}][{column_index}]')} "
                    f"must be at least {cli_correct_value(str(minimum))}.",
                )
                valid = False
    return valid


def _validate_popevals(cfg_file: dict[str, Any], errors: list[str]) -> None:
    """Validate porosity-permeability evaluation properties.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    errors : list[str]
        Validation messages collected so far.
    """
    if "popevals" not in cfg_file:
        return
    popevals = cfg_file["popevals"]
    if not isinstance(popevals, list) or not popevals:
        _add_validation_error(
            errors,
            f"variable {cli_error_value('popevals')} must contain "
            f"{cli_correct_value('at least one layer record')}.",
        )
        return
    for layer_index, layer in enumerate(popevals):
        if not isinstance(layer, list) or not layer:
            _add_validation_error(
                errors,
                f"variable {cli_error_value(f'popevals[{layer_index}]')} must "
                f"contain {cli_correct_value('at least one name-value pair')}.",
            )
            continue
        names: set[str] = set()
        for pair_index, pair in enumerate(layer):
            variable = f"popevals[{layer_index}][{pair_index}]"
            if not isinstance(pair, list) or len(pair) != 2:
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(variable)} must be "
                    f"{cli_correct_value('a two-entry name-value pair')}.",
                )
                continue
            if not isinstance(pair[0], str) or not pair[0].strip():
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(f'{variable}[0]')} must be "
                    f"{cli_correct_value('a non-empty string')}.",
                )
            elif pair[0] in names:
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(variable)} repeats property "
                    f"name {cli_error_value(pair[0])} in the same layer.",
                )
            else:
                names.add(pair[0])
            if not _is_finite_number(pair[1]):
                _add_validation_error(
                    errors,
                    f"variable {cli_error_value(f'{variable}[1]')} must be "
                    f"{cli_correct_value('a finite number')}.",
                )


def _is_tuning_enabled(flow: Any) -> bool:
    """Return whether the Flow command enables TUNING.

    Parameters
    ----------
    flow : Any
        OPM Flow command and command-line options.

    Returns
    -------
    bool
        Whether the requested validation condition is satisfied.
    """
    if not isinstance(flow, str):
        return False
    return any(
        value.lower() in {"--enable-tuning=true", "--enable-tuning=1"}
        for value in flow.split()
    )


def _warn_ignored(cfg_file: dict[str, Any], keys: set[str], reason: str) -> None:
    """Warn about ineffective TOML variables and remove them.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.
    keys : set[str]
        Candidate variables to warn about and remove.
    reason : str
        Explanation included in the warning.
    """
    ignored = sorted(keys & cfg_file.keys())
    if not ignored:
        return
    formatted = ", ".join(cli_warning_value(key) for key in ignored)
    plural = len(ignored) != 1
    pyopmnearwell_warning(
        f"variable{'s' if plural else ''} {formatted} "
        f"{'are' if plural else 'is'} {reason} and will be ignored."
    )
    for key in ignored:
        cfg_file.pop(key)


def _validate_toml(cfg_file: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize all supported TOML configuration values.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML values to validate or normalize.

    Returns
    -------
    dict[str, Any]
        Whether the requested validation condition is satisfied.

    Raises
    ------
    SystemExit
        If the documented validation or operation fails.
    """
    if not isinstance(cfg_file, dict):
        pyopmnearwell_error(
            f"invalid TOML content "
            f"{cli_error_value(type(cfg_file).__name__)}, expected "
            f"{cli_correct_value('a dictionary of configuration variables')}."
        )
    cfg_file = cfg_file.copy()
    errors: list[str] = []
    configurable = {
        "adim",
        "biof",
        "confact",
        "diameter",
        "econ",
        "ehystr",
        "flow",
        "grid",
        "initialphase",
        "inj",
        "injbhp",
        "krn",
        "krw",
        "model",
        "pcap",
        "pcfact",
        "perforations",
        "popevals",
        "poroperm",
        "pressure",
        "probhp",
        "pvmult",
        "removecells",
        "rock",
        "rockcomp",
        "safu",
        "salinity",
        "saltprops",
        "template",
        "temperature",
        "xcn",
        "xdim",
        "xfac",
        "xflow",
        "ycn",
        "zxy",
    }
    internal = {
        "dims",
        "fol",
        "foutp",
        "fprep",
        "fluxnum",
        "homo",
        "imbnum",
        "mode",
        "nocells",
        "pat",
        "runname",
        "satnum",
        "tuning",
        "write",
        "zcn",
    }
    _warn_ignored(
        cfg_file,
        internal,
        "managed internally by pyopmnearwell",
    )
    unknown = sorted(cfg_file.keys() - configurable)
    if unknown:
        formatted = ", ".join(cli_warning_value(key) for key in unknown)
        plural = len(unknown) != 1
        pyopmnearwell_warning(
            f"unknown TOML variable{'s' if plural else ''} {formatted} "
            f"will be ignored."
        )
        for key in unknown:
            cfg_file.pop(key)
    if "flow" not in cfg_file:
        simulation_only = configurable - {
            "model",
            "template",
            "krw",
            "krn",
            "pcap",
            "safu",
            "poroperm",
            "popevals",
        }
        _warn_ignored(
            cfg_file,
            simulation_only,
            "not effective when flow is omitted for table-only generation",
        )
        for key in ("model", "template"):
            if key in cfg_file:
                _validate_string(cfg_file, key, errors)
        for key in ("krw", "krn", "pcap"):
            if key in cfg_file:
                _validate_expression(cfg_file, key, errors)
        _validate_safu(cfg_file, errors)
        if "poroperm" in cfg_file:
            _validate_string(cfg_file, "poroperm", errors)
        _validate_popevals(cfg_file, errors)
        if errors:
            details = "\n".join(f"  - {error}" for error in errors)
            pyopmnearwell_error(f"invalid TOML configuration:\n{details}")
        return cfg_file
    required = {
        "diameter",
        "flow",
        "grid",
        "inj",
        "model",
        "pressure",
        "rock",
        "template",
        "xcn",
        "xdim",
    }
    model = cfg_file.get("model")
    template = cfg_file.get("template")
    if model in {"co2store", "h2store", "saltprec"}:
        required.update(
            {"initialphase", "krn", "krw", "pcap", "pvmult", "safu", "temperature"}
        )
    if model in {"co2eor", "foam"}:
        required.update({"injbhp", "probhp"})
    if model == "saltprec" or template == "nosaltprec":
        required.add("saltprops")
    if model == "saltprec":
        required.update({"popevals", "poroperm"})
    if template == "biofilm":
        required.update({"biof", "popevals", "poroperm"})
    for key in sorted(required - cfg_file.keys()):
        _add_validation_error(
            errors,
            f"missing required TOML variable {cli_error_value(key)}.",
        )
    for key in ("flow", "model", "template", "grid"):
        _validate_string(cfg_file, key, errors)
    allowed_models = {"co2eor", "co2store", "foam", "h2store", "saltprec"}
    allowed_grids = {
        "cake",
        "cartesian",
        "cartesian2d",
        "cave",
        "coord2d",
        "coord3d",
        "core",
        "cpg3d",
        "radial",
        "tensor2d",
        "tensor3d",
    }
    if isinstance(model, str) and model not in allowed_models:
        _add_validation_error(
            errors,
            f"variable {cli_error_value('model')} has invalid value "
            f"{cli_error_value(model)}, expected one of "
            f"{cli_correct_value(', '.join(sorted(allowed_models)))}.",
        )
    grid = cfg_file.get("grid")
    if isinstance(grid, str) and grid not in allowed_grids:
        _add_validation_error(
            errors,
            f"variable {cli_error_value('grid')} has invalid value "
            f"{cli_error_value(grid)}, expected one of "
            f"{cli_correct_value(', '.join(sorted(allowed_grids)))}.",
        )
    saturation_values = {
        "ehystr",
        "initialphase",
        "krn",
        "krw",
        "pcap",
        "pcfact",
        "pvmult",
        "safu",
        "salinity",
        "temperature",
    }
    if model in {"co2eor", "foam"}:
        _warn_ignored(
            cfg_file,
            saturation_values,
            f"not effective for {cli_warning_value(f'model = {model}')}",
        )
    else:
        _warn_ignored(
            cfg_file,
            {"injbhp", "probhp"},
            f"not effective for {cli_warning_value(f'model = {model}')}",
        )
    if model != "h2store":
        _warn_ignored(
            cfg_file,
            {"econ"},
            f"not effective for {cli_warning_value(f'model = {model}')}",
        )
    if model != "saltprec" and template != "nosaltprec":
        _warn_ignored(
            cfg_file,
            {"saltprops"},
            f"not effective for {cli_warning_value(f'model = {model}')} with "
            f"{cli_warning_value(f'template = {template}')}",
        )
    if template != "biofilm":
        _warn_ignored(
            cfg_file,
            {"biof"},
            f"not effective for {cli_warning_value(f'template = {template}')}",
        )
    if model != "saltprec" and template != "biofilm":
        _warn_ignored(
            cfg_file,
            {"popevals", "poroperm"},
            "only effective for salt precipitation or the biofilm template",
        )
    if grid != "core":
        _warn_ignored(
            cfg_file,
            {"confact"},
            f"not effective for {cli_warning_value(f'grid = {grid}')}",
        )
    for key in ("diameter", "pressure", "xdim"):
        _validate_number(cfg_file, key, errors, minimum=0, strict=True)
    for key in ("adim", "confact", "econ", "xfac"):
        if key in cfg_file:
            _validate_number(cfg_file, key, errors, minimum=0)
    for key in ("injbhp", "probhp"):
        if key in cfg_file:
            _validate_number(cfg_file, key, errors, minimum=0, strict=True)
    if "pvmult" in cfg_file:
        _validate_number(cfg_file, "pvmult", errors, minimum=-1)
    if "temperature" in cfg_file:
        _validate_array(cfg_file, "temperature", errors, length=2)
    if "saltprops" in cfg_file:
        valid_salt = _validate_array(cfg_file, "saltprops", errors, length=3, minimum=0)
        if valid_salt and cfg_file["saltprops"][1] < cfg_file["saltprops"][0]:
            _add_validation_error(
                errors,
                f"variable {cli_error_value('saltprops[1]')} must be greater "
                "than or equal to the initial concentration in "
                f"{cli_error_value('saltprops[0]')}.",
            )
    if "perforations" in cfg_file:
        _validate_array(
            cfg_file,
            "perforations",
            errors,
            length=3,
            integer=True,
            minimum=0,
        )
    if "initialphase" in cfg_file:
        value = cfg_file["initialphase"]
        if not _is_integer(value) or value not in {0, 1}:
            _add_validation_error(
                errors,
                f"variable {cli_error_value('initialphase')} has invalid value "
                f"{cli_error_value(str(value))}, expected "
                f"{cli_correct_value('0 or 1')}.",
            )
    if grid in {"coord2d", "coord3d"}:
        valid_xcn = _validate_array(cfg_file, "xcn", errors, nonempty=True)
        if valid_xcn and len(cfg_file["xcn"]) < 2:
            _add_validation_error(
                errors,
                f"variable {cli_error_value('xcn')} must contain "
                f"{cli_correct_value('at least two coordinates')}.",
            )
        elif valid_xcn and any(
            right <= left for left, right in zip(cfg_file["xcn"], cfg_file["xcn"][1:])
        ):
            _add_validation_error(
                errors,
                f"variable {cli_error_value('xcn')} must contain "
                f"{cli_correct_value('strictly increasing coordinates')}.",
            )
    else:
        _validate_array(
            cfg_file,
            "xcn",
            errors,
            integer=True,
            minimum=0,
            strict=True,
            nonempty=True,
        )
    if "ycn" in cfg_file:
        _validate_array(
            cfg_file,
            "ycn",
            errors,
            integer=True,
            minimum=0,
            strict=True,
            nonempty=True,
        )
    for key in ("zxy", "poroperm"):
        if key in cfg_file:
            _validate_string(cfg_file, key, errors)
    for key in ("krw", "krn", "pcap"):
        if key in cfg_file:
            _validate_expression(cfg_file, key, errors)
    _validate_rock(cfg_file, errors)
    _validate_safu(cfg_file, errors)
    if "biof" in cfg_file:
        _validate_records(cfg_file, "biof", errors, 9, minimum=0)
    _validate_popevals(cfg_file, errors)
    tuning_defined = _validate_injection(cfg_file, errors)
    if tuning_defined and not _is_tuning_enabled(cfg_file.get("flow")):
        pyopmnearwell_warning(
            f"TUNING values are defined in {cli_warning_value('inj')}, but "
            f"{cli_warning_value('--enable-tuning=true')} is not set in "
            f"{cli_correct_value('flow')}. The TUNING values may not be effective."
        )
    if errors:
        details = "\n".join(f"  - {error}" for error in errors)
        pyopmnearwell_error(f"invalid TOML configuration:\n{details}")
    return cfg_file
