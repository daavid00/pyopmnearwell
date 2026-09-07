"""Render Mako templates used by pyopmnearwell."""

import pathlib

from mako import exceptions
from mako.template import Template

from pyopmnearwell.utils.terminal import pyopmnearwell_error


def fill_template(
    var: dict, filename: str | pathlib.Path | None = None, text: str | None = None
) -> str:
    """Fill a Mako template with the given variables.

    The template is loaded from ``filename`` or supplied directly through ``text``.
    If rendering fails, the formatted Mako traceback is reported through the
    pyopmnearwell command-line error helper so the template can be debugged.

    Parameters
    ----------
    var : dict
        Variables exposed to the Mako template during rendering.
    filename : str | pathlib.Path | None, optional
        Path to the template file. This may be omitted when ``text`` is supplied.
    text : str | None, optional
        Template source supplied directly as a string. This may be omitted when
        ``filename`` is supplied.

    Returns
    -------
    str
        Rendered template text.

    Raises
    ------
    SystemExit
        If the template cannot be rendered.
    """
    # Convert filename to str
    if isinstance(filename, pathlib.Path):
        filename = str(filename)

    mytemplate: Template = Template(filename=filename, text=text)
    try:
        filledtemplate = mytemplate.render(**var)
    except ValueError:
        pyopmnearwell_error(exceptions.text_error_template().render())
    return filledtemplate
