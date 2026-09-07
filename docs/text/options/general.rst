General options
===============

.. program:: pyopmnearwell

Input configuration
-------------------

.. option:: -i <file>, --input <file>

   Path to the TOML configuration file.

   **Default:** ``input.toml``

   The value is stripped of leading and trailing whitespace. It must be
   non-empty and use the ``.toml`` extension. The extension check is
   case-insensitive.

   Examples:

   .. code-block:: console

      pyopmnearwell -i examples/h2o.toml
      pyopmnearwell --input examples/co2.toml

Output directory
----------------

.. option:: -o <directory>, --output <directory>

   Base output directory for generated deck files and simulation results.

   **Default:** ``output``

   The value is stripped of leading and trailing whitespace and must be
   non-empty. pyopmnearwell converts it to an absolute path and creates it when
   needed.

   The internal layout depends on :option:`--mode`. The ``single`` mode writes
   generated input and simulation files directly in this directory. Other
   modes use ``preprocessing`` and ``output`` subdirectories where applicable.

   Examples:

   .. code-block:: console

      pyopmnearwell -i examples/co2.toml -o co2
      pyopmnearwell -i examples/h2o.toml --output test_outputs/h2o

Execution mode
--------------

.. option:: -m <mode>, --mode <mode>

   Select which workflow stages to run.

   **Choices:** ``deck``, ``flow``, ``single``, ``all``

   **Default:** ``all``

   ``deck``
      Generate the OPM Flow deck and required include files without running the
      simulator.

   ``flow``
      Run OPM Flow using the selected configuration and the expected generated
      input files.

   ``single``
      Generate the deck and run OPM Flow with both input and result files in the
      selected output directory.

   ``all``
      Generate the deck under ``preprocessing`` and run OPM Flow with results
      under ``output``.

   See :doc:`modes` for workflow diagrams, expected directories, and examples.

Cell-result vectors
-------------------

.. option:: -v <choice>, --vectors <choice>

   Control whether OPM Flow writes cell-result vectors.

   **Choices:** ``0``, ``1``

   **Default:** ``1``

   ``1``
      Request cell-result files such as EGRID, INIT, and UNRST.

   ``0``
      Disable those cell-result vectors when they are not needed.


Option summary
--------------

The complete short-form invocation is:

.. code-block:: console

   pyopmnearwell -i <file.toml> -o <directory> -m <mode> -v <0-or-1>

The equivalent long-form invocation is:

.. code-block:: console

   pyopmnearwell --input <file.toml> --output <directory> --mode <mode> --vectors <0-or-1>
