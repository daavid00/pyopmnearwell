pyopmnearwell
=============

.. rst-class:: lead

   A flexible framework for generating and running near-well OPM Flow models.

**pyopmnearwell** creates model-specific decks and property tables for CO2,
hydrogen, enhanced-oil-recovery, foam, salt-precipitation, and related near-well
studies.

.. grid:: 1 2 2 4
   :gutter: 3
   :margin: 4 0 4 0

   .. grid-item-card:: :octicon:`rocket;1.2em` Get started
      :link: introduction
      :link-type: doc

      Understand the models, templates, grids, and workflows.

   .. grid-item-card:: :octicon:`download;1.2em` Install
      :link: installation
      :link-type: doc

      Install pyopmnearwell, OPM Flow, and visualization tools.

   .. grid-item-card:: :octicon:`gear;1.2em` Configure a model
      :link: configuration_file
      :link-type: doc

      Define geometry, rock, saturation, and injection settings.

   .. grid-item-card:: :octicon:`book;1.2em` Explore examples
      :link: examples
      :link-type: doc

      Run water, cyclic CO2, machine-learning, and publication workflows.

Quick installation
------------------

.. code-block:: console

   pip install git+https://github.com/cssr-tools/pyopmnearwell.git

Quick start
-----------

.. code-block:: console

   pyopmnearwell -i examples/h2o.toml -o hello_world
   pyopmnearwell -i examples/co2.toml -o co2
   pyopmnearwell --help

What can pyopmnearwell do?
--------------------------

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Generate near-well grids

      Create radial, cake, core, Cartesian, tensor, coordinate, and corner-point grids.

   .. grid-item-card:: Configure physical models

      Generate CO2 storage, CO2 EOR, foam, hydrogen storage, and salt-precipitation decks.

   .. grid-item-card:: Write model tables

      Generate saturation, geology, boundary multiplier, and porosity-permeability include files.

   .. grid-item-card:: Run reproducible studies

      Execute OPM Flow workflows and generate datasets for scientific and machine-learning studies.

.. toctree::
   :hidden:
   :maxdepth: 2

   introduction
   installation
   configuration_file
   examples
   command-line
   api
   output_folder
   contributing
   related
