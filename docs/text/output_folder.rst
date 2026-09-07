Output folder
=============

The layout depends on the selected mode.

Separate preprocessing and simulation output
--------------------------------------------

``all``, ``deck``, and ``flow`` use separate locations where applicable:

.. code-block:: text

   output/
   ├── preprocessing/
   │   ├── CASE.DATA
   │   └── generated include files
   └── output/
       └── OPM Flow results

.. figure:: figs/output.png
   :alt: Generated pyopmnearwell output files

Single-folder mode
------------------

``-m single`` writes generated deck files and simulation results directly in the selected output folder.

Generated files
---------------

Depending on model and grid, generation can create ``GRID.INC``, ``DRV.INC``,
``DX.INC``, ``DY.INC``, ``TABLES.INC``, ``GEOLOGY.INC``, ``FLUXNUM.INC``,
``MULTPV.INC``, ``PERMFACT.INC``, and ``PCFACT.INC``. Generated OPM files may
be edited and rerun directly, for example to add summary variables.

Use ResInsight or plopm to visualize OPM Flow results.
