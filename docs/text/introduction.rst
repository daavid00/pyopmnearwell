============
Introduction
============

.. image:: ./figs/saturation.gif
    :scale: 50%

This documentation describes the **pyopmnearwell** package hosted in `https://github.com/cssr-tools/pyopmnearwell <https://github.com/cssr-tools/pyopmnearwell>`_.

Concept
-------
Simplified and flexible testing framework for near-well simulations via a
:doc:`configuration file <./configuration_file>` using the `OPM Flow simulator <https://opm-project.org/?page_id=19>`_:

- Set the physical model (current ones are co2store, co2eor, h2store, saltprec, co2eor, and foam).
- Choose a `specific template <https://github.com/cssr-tools/pyopmnearwell/blob/main/src/pyopmnearwell/templates>`_ inside the folder for the chosen physical model.
- Define the grid refinement in the x/y and z directions.
- Define the number of different rocks along the z direction.
- Define the number of layers (heterogeneity around the well) and its length.
- Set the rock and fluid properties.
- Define the injection schedule.
- Run the simulations.
- Inspect the results by looking at the generated figures.

Overview
--------

The current implementation supports the following executable with the argument options:

.. code-block:: bash

    pyopmnearwell -i configuration_file.toml

where 

-i  The base name of the :doc:`configuration file <./configuration_file>` ('input.toml' by default).
-o  The base name of the :doc:`output folder <./output_folder>` ('output' by default).
-p  Using the 'resdata' or 'opm' Python package to generate the figures ('resdata' by default, 'off' to skip the plotting).
-c  Compare the results from different output folders (write any name to actiate, '' by default).
-g  Run the whole framework ('all'), only run flow ('flow'), only write the deck and run flow together in the output folder ('single'), or only create plots ('plot') ('all' by default).
-v  Write cell values, i.e., EGRID, INIT, UNRST ('1' by default).
-z  xlim in meters for the zoomed in plots (20 by default).
-s  Scale for the x axis in the figures: 'normal' or 'log' ('normal' by default).
-m  Simulated model (5th row in the configuration file). This is used for the plotting compare method (it gets overwritten by the configuration file) ('co2store' by default).
-w  Set to 1 to print warnings ('0' by default).
-l  Set to 0 to not use LaTeX formatting ('1' by default).

.. note::
    The plotting functionality works for co2store, h2store, and saltprec models, and all grids except the core sample. To generate
    PNGs and GIFs of the other models and core samples, you could use `plopm <https://github.com/cssr-tools/plopm>`_.

.. warning::
    The H2CH4 template in the h2store model folder is under development and it is based on an input deck available in 
    `opm-tests <https://github.com/OPM/opm-tests/blob/master/diffusion/BO_DIFFUSE_CASE1.DATA>`_. In addition, the templates 
    in the co2eor/foam model are based on an input deck available in `opm-publications <https://github.com/OPM/opm-publications/blob/master/dynamic_blackoil/SPE5.BASE>`_. 
    Currently the PVT tables in those examples are used, limiting the range of reservoir pressure and temperature, it is in the TODO list to extend
    this.