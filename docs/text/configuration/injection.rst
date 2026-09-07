Injection, wells, and TUNING
============================

Injection records
-----------------

Most models accept four or five entries per ``inj`` row; ``h2store`` accepts
four, five, or six. The common fields are duration, report interval, phase
identifier (0 wetting or 1 non-wetting), and rate. H2 storage may add a positive
BHP limit. A final non-empty string defines TUNING records.

Cyclic example
--------------

The documented ``co2.toml`` injects CO2 for seven days, water for seven days,
and CO2 again for seven days, using 0.1-day output spacing and model-specific
TUNING strings.

TUNING compatibility
--------------------

After release 2025.04, the maximum solver time step and TUNING items belong at
the end of each injection record. If TUNING values are present but ``flow`` does
not enable TUNING, pyopmnearwell emits a warning.
