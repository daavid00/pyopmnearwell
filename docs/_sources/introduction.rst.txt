.. _introduction:

Introduction
============

.. image:: figs/saturation.gif
   :alt: Near-well gas-saturation simulation generated with pyopmnearwell
   :align: center
   :width: 65%

**pyopmnearwell** is a flexible framework for generating and running near-well
models with the `OPM Flow simulator <https://opm-project.org/?page_id=19>`_. A
:doc:`configuration file <configuration_file>` selects the physical model,
template, grid, properties, and operational schedule.

Core workflow
-------------

#. Select a physical model and compatible Mako template.
#. Choose a radial, Cartesian, tensor, coordinate, core, or corner-point grid.
#. Define x, y, and z refinement and near-well geometry.
#. Define vertical rock layers, permeability, porosity, and saturation functions.
#. Configure perforations, boundary behavior, and the injection schedule.
#. Generate the OPM Flow deck and include files.
#. Run OPM Flow and inspect the generated vectors with external tools.

Physical models
---------------

The current validator accepts ``co2store``, ``co2eor``, ``foam``, ``h2store``,
and ``saltprec``. Model-specific templates are stored under
``src/pyopmnearwell/templates``. Requirements differ by model and template, as
described in :doc:`configuration_file`.

Core workflows
--------------

* Generate only the deck and include files.
* Run OPM Flow from previously generated files.
* Generate and run using separate preprocessing and output directories.
* Generate and run in one output directory.
* Write EGRID, INIT, and UNRST cell vectors when requested.
* Generate saturation and porosity-permeability tables without running Flow.

Basic usage
-----------

.. code-block:: console

   pyopmnearwell -i examples/co2.toml -o co2
   pyopmnearwell -i examples/co2.toml -o co2 -m deck
   pyopmnearwell -i examples/co2.toml -o co2 -m single

Use :doc:`command-line` for exact syntax and :doc:`examples` for complete workflows.

Visualization
-------------

The built-in plotting functionality was retired in release 2025.04. Use
`plopm <https://github.com/cssr-tools/plopm>`_ or
`ResInsight <https://resinsight.org>`_ for PNGs, GIFs, variable profiles, and
distance-to-boundary visualizations. ParaView can be used when Flow is run with
``--enable-vtk-output=true``.

Development limitations
-----------------------

.. warning::

   The ``H2CH4`` template under ``h2store`` remains under development and is
   based on ``BO_DIFFUSE_CASE1.DATA`` from ``opm-tests``. The ``co2eor`` and
   ``foam`` templates are based on ``SPE5.BASE`` from ``opm-publications``.
   Their current PVT data limit the usable pressure and temperature ranges.

About the project
-----------------

.. image:: figs/graphical.png
   :alt: pyopmnearwell graphical project overview
   :align: center
   :width: 80%

**pyopmnearwell** is funded by the `HPC Simulation Software for the Gigatonne
Storage Challenge project <https://www.norceresearch.no/en/projects/hpc-simulation-software-for-the-gigatonne-storage-challenge>`_
(project 622059) and the `Center for Sustainable Subsurface Resources
<https://cssr.no>`_ (project 331841).

Where to continue
-----------------

* Complete the :doc:`installation` and verify pyopmnearwell and OPM Flow.
* Use :doc:`configuration_file` for models, grids, properties, schedules, and tables.
* Browse :doc:`examples` for water injection, cyclic CO2, ML, and publication studies.
* Use :doc:`command-line` for exact modes, defaults, and vector output controls.
* Review :doc:`output_folder` for mode-dependent file layouts.
* Browse :doc:`api` for Python modules and functions.
* See :doc:`contributing` to report issues or contribute.
* Explore :doc:`related` for complementary tools.
