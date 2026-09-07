CO2 cyclic injection
====================

In this example we consider the configuration file described in the
:doc:`configuration file <../configuration_file>` section, which is available in the 
examples folder as `co2.toml <https://github.com/cssr-tools/pyopmnearwell/blob/main/examples/co2.toml>`_.

If the generated files are to be saved in a folder called 'co2', then this is achieved by the following command:

.. code-block:: console

    pyopmnearwell -i co2.toml -o co2

The execution time was approximately 20 seconds and the following is an animation using `ResInsight <https://resinsight.org>`_ to visualize the gas saturation:

.. figure:: ../figs/saturation.gif

    Visualization of the gas saturation using ResInsight.

To generate a gif using plopm, this can be achieved by executing:

.. code-block:: console

    plopm -i CO2 -v sgas -m gif -dpi 1000 -gi 50 -gl 1 -fs 10,5 -yf .0f -fz 20 -cbn 6 -t "Cyclic injection"

.. figure:: ../figs/co2_sgas.gif

    Visualization of the gas saturation using plopm.

Both the pyopmnearwell and plopm commands can be run with the
maintained documentation script:

.. code-block:: console

   . ./tests/scripts/docs_co2_cyclic_injection.sh

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/pyopmnearwell/blob/main/tests/scripts/docs_co2_cyclic_injection.sh
         :color: primary
         :outline:
         :expand:

         View script

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/pyopmnearwell/main/tests/scripts/docs_co2_cyclic_injection.sh
         :color: primary
         :outline:
         :expand:

         View raw script

.. button-ref:: ../examples
   :color: primary

   Back to examples gallery
