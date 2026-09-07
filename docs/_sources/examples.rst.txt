Examples
========

The examples cover water injection, cyclic CO2 injection, machine-learning data
generation, and publication workflows.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Hello world
      :class-card: example-card
      :img-top: figs/pressure_1D.png
      :link: examples/hello-world
      :link-type: doc

      Inject water with the ``co2store`` model on a radial grid and visualize
      the final pressure.

   .. grid-item-card:: CO2 cyclic injection
      :class-card: example-card
      :img-top: figs/co2_sgas.gif
      :link: examples/co2-cyclic
      :link-type: doc

      Reproduce the CO2-water-CO2 schedule and gas-saturation animations.

   .. grid-item-card:: CCUS machine learning
      :link: examples/machine-learning
      :link-type: doc

      Generate simulation data for varying inputs and read outputs such as
      production volumes.

.. toctree::
   :hidden:
   :maxdepth: 1

   examples/hello-world
   examples/co2-cyclic
   examples/machine-learning
