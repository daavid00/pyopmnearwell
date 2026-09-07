Grids and geometry
==================

Supported grids
---------------

``grid`` accepts ``cake``, ``cartesian``, ``cartesian2d``, ``cave``,
``coord2d``, ``coord3d``, ``core``, ``cpg3d``, ``radial``, ``tensor2d``, or
``tensor3d``.

Main dimensions
---------------

``xdim`` is a positive length. ``diameter`` is the well diameter. ``adim`` is
the angular aperture for cake and radial grids, inlet/outlet length for core,
or width for supported 2D grids. ``xcn`` contains counts for uniform/tensor
grids or strictly increasing coordinates for coordinate grids. ``xfac`` controls
exponential near-well refinement; zero gives equidistant spacing.

Surface and optional geometry
-----------------------------

``zxy`` is a reservoir-surface expression. ``perforations`` contains activation,
count, and length. ``removecells`` removes near-well cells where applicable.

.. figure:: ../figs/gridding.png
   :alt: Radial, cake, Cartesian 2D, and Cartesian 3D grids

.. figure:: ../figs/core.png
   :alt: Cylindrical core model geometry
