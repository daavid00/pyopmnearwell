Rock and saturation properties
==============================

Rock records
------------

Each physical layer uses ``[Kxy, Kz, porosity, thickness, z_cells]``. Only the
final boundary-rock record may use ``[Kxy, Kz, porosity]``. Permeabilities are
non-negative, porosity lies in [0, 1], thickness is positive, and cell counts
are positive integers.

Saturation expressions
----------------------

``krw``, ``krn``, and ``pcap`` are restricted Python expressions that must
reference ``sw``. Approved positional NumPy functions include ``np.maximum``,
``np.minimum``, ``np.clip``, ``np.where``, ``np.exp``, ``np.log``, and related
safe numerical functions.

Saturation records
------------------

Every ``safu`` row has 11 entries: ``swi``, ``sni``, wetting and non-wetting
end points, entry pressure, three exponents, capillary threshold, low-saturation
control, and number of points. Endpoint saturations lie in [0, 1] and sum to at
most one. At least two table points are required.

Hysteresis and boundary behavior
--------------------------------

``ehystr`` configures EHYSTR. ``pvmult`` controls boundary pore volume: positive
values apply a multiplier, zero may use producers, and -1 disables it.
