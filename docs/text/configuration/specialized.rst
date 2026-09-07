Salt precipitation and biofilm
==============================

Salt precipitation
------------------

The ``saltprec`` model requires ``saltprops``, ``poroperm``, and ``popevals``.
``saltprops`` contains three non-negative values, with the second not below the
first. ``popevals`` stores unique name-value pairs by layer. The validated
``poroperm`` expression generates ``PERMFACT.INC`` and optional ``PCFACT.INC``.
See ``examples/saltprec.toml``.

Biofilm
-------

The ``biofilm`` template requires ``biof`` records with nine non-negative
entries and porosity-permeability evaluation data. See
``examples/h2biofilm.toml``.

Machine-learning dependency
---------------------------

TensorFlow is not required for normal deck generation or simulation. It is used
only by the ML near-well workflows and is currently installed separately for
supported Python versions.
