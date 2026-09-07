Hello world
===========

In this example we consider the configuration file `h2o.toml <https://github.com/cssr-tools/pyopmnearwell/blob/main/examples/h2o.toml>`_ available in the 
examples folder, where the co2store model is used and only water is injected in a radial grid.

If the generated files are to be saved in a folder called 'hello_world', then this is achieved by the following command:

.. code-block:: console

    pyopmnearwell -i h2o.toml -o hello_world

To visualize the results, this can be achieved by using plopm, for example:

.. code-block:: console

    plopm -i hello_world/output/H2O -v pressure -s ,,1 -t 'Top view at the end of the simulation' -c bwr -xf .0f -cbf .0f 

.. figure:: ../figs/pressure_1D.png

Both the pyopmnearwell and plopm commands can be run with the
maintained documentation script:

.. code-block:: console

   . ./tests/scripts/docs_hello_world.sh

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. button-link:: https://github.com/cssr-tools/pyopmnearwell/blob/main/tests/scripts/docs_hello_world.sh
         :color: primary
         :outline:
         :expand:

         View script

   .. grid-item::

      .. button-link:: https://raw.githubusercontent.com/cssr-tools/pyopmnearwell/main/tests/scripts/docs_hello_world.sh
         :color: primary
         :outline:
         :expand:

         View raw script

.. button-ref:: ../examples
   :color: primary

   Back to examples gallery
