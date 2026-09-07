Configuration reference
=======================

A TOML file selects a physical model, template, grid, properties, and schedule.
Validation is model-aware, warns about unknown or ineffective settings, and can
also support table-only generation when ``flow`` is omitted.

.. toctree::
   :maxdepth: 1

   configuration/models
   configuration/grids
   configuration/properties
   configuration/injection
   configuration/specialized
   configuration/table-only
   configuration/complete
