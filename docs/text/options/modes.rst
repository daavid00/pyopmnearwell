Execution modes
===============

The execution mode controls whether pyopmnearwell generates an OPM Flow deck,
runs the simulator, and separates generated inputs from simulation results.

All mode
--------

``all`` is the default and runs the complete workflow:

#. Read and validate the TOML configuration.
#. Create the selected output directory.
#. Generate the deck and include files under ``preprocessing``.
#. Run OPM Flow.
#. Write simulation results under ``output``.

.. code-block:: console

   pyopmnearwell -i examples/co2.toml -o co2 -m all

Expected layout:

.. code-block:: text

   co2/
   ├── preprocessing/
   │   ├── CO2.DATA
   │   └── generated include files
   └── output/
       └── OPM Flow results

Deck mode
---------

``deck`` generates the simulator inputs but does not run OPM Flow. Use it to
inspect or edit the generated DATA and include files before simulation.

.. code-block:: console

   pyopmnearwell -i examples/co2.toml -o co2 -m deck

Generated files are written under:

.. code-block:: text

   co2/preprocessing/

The precise include files depend on the model, template, grid, and properties.
They can include ``GRID.INC``, ``DRV.INC``, ``DX.INC``, ``DY.INC``,
``TABLES.INC``, ``GEOLOGY.INC``, ``FLUXNUM.INC``, ``MULTPV.INC``,
``PERMFACT.INC``, and ``PCFACT.INC``.

Flow mode
---------

``flow`` runs OPM Flow without regenerating the deck. Use it after a deck has
already been generated, including when you have manually edited the generated
OPM files.

.. code-block:: console

   pyopmnearwell -i examples/co2.toml -o co2 -m flow

For the standard separated layout, pyopmnearwell expects the generated input
under ``co2/preprocessing`` and writes simulation results under ``co2/output``.
The TOML configuration is still read and validated because it contains the Flow
command and runtime settings.

Single mode
-----------

``single`` generates the deck and runs OPM Flow in one directory rather than
creating separate ``preprocessing`` and ``output`` subdirectories.

.. code-block:: console

   pyopmnearwell -i examples/co2.toml -o co2 -m single

Expected layout:

.. code-block:: text

   co2/
   ├── CO2.DATA
   ├── generated include files
   └── OPM Flow results

Use this mode for a compact standalone case. Use ``all`` when you want generated
inputs and simulation results separated.

Mode and vector combinations
----------------------------

Generate a full set of cell-result vectors:

.. code-block:: console

   pyopmnearwell -i examples/co2.toml -o co2 -m all -v 1

Generate only the deck and suppress cell-result vectors in its output settings:

.. code-block:: console

   pyopmnearwell -i examples/co2.toml -o co2 -m deck -v 0

Run a compact single-directory workflow:

.. code-block:: console

   pyopmnearwell -i examples/h2o.toml -o hello_world -m single -v 1

Choosing a mode
---------------

Use ``all``
   For the standard complete workflow with separated generated and simulation
   files.

Use ``deck``
   To generate, inspect, or customize OPM Flow inputs before simulation.

Use ``flow``
   To rerun an existing generated deck without regenerating it.

Use ``single``
   For a self-contained case with all files in one directory.
