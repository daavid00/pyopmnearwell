Table-only generation
=====================

Omit ``flow`` to generate property tables without running a simulation.
Simulation-only variables are ignored with warnings. Relevant values include
``model``, ``template``, ``krw``, ``krn``, ``pcap``, ``safu``, ``poroperm``,
and ``popevals``.

Depending on the supplied values, this workflow writes ``TABLES.INC``,
``PERMFACT.INC``, and ``PCFACT.INC``.
