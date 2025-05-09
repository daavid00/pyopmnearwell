# SPDX-FileCopyrightText: 2023 NORCE
# SPDX-License-Identifier: GPL-3.0

"""
Utility functions to run the studies.
"""
import math as mt
import os
import sys

import numpy as np

from pyopmnearwell.visualization.plotting import plot_results


def simulations(dic):
    """
    Function to run Flow

    Args:
        dic (dict): Global dictionary with required parameters

    """
    if not "foutp" in dic:
        dic["foutp"] = f"{dic['fol']}/output"
    if not "generate" in dic:
        dic["generate"] = "all"
    os.chdir(dic["foutp"])
    os.system(
        f"{dic['flow']} --output-dir={dic['foutp']} "
        f"{dic['fprep']}/{dic['runname'].upper()}.DATA  & wait\n"
    )
    if dic["generate"] in ["all", "plot"]:
        # We save few variables for the plotting methods
        np.save("xspace", dic["xcor"])
        np.save("zspace", dic["zcor"])
        np.save("ny", dic["nocells"][1])
        schedule = [0]
        for nrst in dic["inj"]:
            for _ in range(round(nrst[0] / nrst[1])):
                schedule.append(schedule[-1] + nrst[1] * 86400.0)
        np.save("schedule", schedule)
        np.save("radius", 0.5 * dic["diameter"])
        if dic["grid"] in ["cartesian2d", "cartesian"]:
            np.save("angle", 360.0)
        else:
            np.save("angle", dic["dims"][1])
        if dic["grid"] == "cartesian":
            np.save(
                "position",
                (dic["nocells"][0] - 1) * (mt.floor(dic["nocells"][0] / 2) + 1),
            )
        else:
            np.save("position", 0)


def plotting(dic):
    """
    Function to run the plotting.py file

    Args:
        dic (dict): Global dictionary with required parameters

    """
    if dic["grid"] in ["core"]:
        print(
            f"Grid type {dic['grid']} not supported for plotting results. "
            "As an alternative you can use https://github.com/cssr-tools/plopm"
        )
        sys.exit()
    if dic["model"] in ["co2eor", "foam"]:
        print(
            f"Model type {dic['model']} not supported for plotting results. "
            "As an alternative you can use https://github.com/cssr-tools/plopm"
        )
        sys.exit()
    dic["folders"] = [dic["fol"]]
    os.chdir(f"{dic['fol']}/postprocessing")
    plot_exe = [
        "python3",
        f"{dic['pat']}/visualization/plotting.py",
        f"-f {dic['fol']}",
        f"-p {dic['plot']}",
        f"-m {dic['model']}",
        f"-s {dic['scale']}",
        f"-z {dic['zoom']}",
        f"-l {dic['latex']}",
    ]
    print(" ".join(plot_exe))
    plot_results(dic)
