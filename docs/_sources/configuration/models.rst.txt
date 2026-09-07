Models and templates
====================

Physical models
---------------

``model`` accepts ``co2store``, ``co2eor``, ``foam``, ``h2store``, or
``saltprec``. ``template`` names a Mako file under the selected model directory.

Model-specific requirements
---------------------------

``co2store``, ``h2store``, and ``saltprec`` require initial phase, saturation
expressions, saturation records, temperature, and boundary pore-volume control.
``co2eor`` and ``foam`` require injection and production BHP limits.
``saltprec`` requires salt properties and porosity-permeability tables. The
``biofilm`` template requires biofilm parameters and porosity-permeability data.

Flow command
------------

``flow`` contains the executable, optional MPI launcher, and simulator flags,
excluding ``--output-dir``. Include ``--enable-tuning=true`` when injection
records define TUNING values.
