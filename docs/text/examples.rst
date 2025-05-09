********
Examples
********

Water injection
---------------
In this example we consider the configuration file 'h2o.toml' available in the 
examples folder (`link to the file <https://github.com/cssr-tools/pyopmnearwell/blob/main/examples/h2o.toml>`_), where
the co2store model is used and only water is injected in a radial grid.

If the generated files are to be saved in a folder called 'h2o_radial', then this is achieved by the following command:

.. code-block:: bash

    pyopmnearwell -i h2o.toml -o h2o_radial

We change the grid to a 3D catesian grid:

.. code-block:: python
    :linenos:
    :lineno-start: 7

    grid = "cartesian" #Grid type: cake, radial, core, cartesian2d, coord2d, tensor2d, cartesian, cpg3d, coord3d, or tensor3d
    adim = 100 #Grid cake/radial: theta [degrees]; core: input/output pipe length [m]; cartesian2d, coord2d, tensor2d: width[m]

and increase the injection rate 6 times (this to be comparable since the radial grid has an angle of 60).

.. code-block:: python
    :linenos:
    :lineno-start: 32

    inj = [[1e-1,1e-1,5e-2,0,360000]]

We run again the configuration file and save it in a different folder:

.. code-block:: bash

    pyopmnearwell -i h2o.toml -o h2o_cartesian

To compare the results in the radial and cartesian folder, then it is enough to write in the terminal:

.. code-block:: bash

    pyopmnearwell -c compare

The following figure compares the pressure profile for both simulations (pressure_1D_single_layer_xnormal.png inside the compare folder):

.. figure:: figs/pressure_1D.png


CO2 cyclic injection
--------------------

In this example we consider the configuration file described in the
:doc:`configuration file<./configuration_file>` section, which is available in the 
examples folder as 'co2.toml'.

If the generated files are to be saved in a folder called 'co2', then this is achieved by the following command:

.. code-block:: bash

    pyopmnearwell -i co2.toml -o co2

The execution time was c.a. 20 seconds and the following is an animation using
ResInsight to visualize the gas saturation:

.. figure:: figs/saturation.gif

    Simulation results of the gas saturation.

The following are some of the plots created by the **pyopmnearwell** executable:

.. figure:: figs/permeability_2D.png
.. figure:: figs/w_rate.png
.. figure:: figs/nearwell_saturation.png
    
    Permeability (top), CO2 injection schedule (middle), and saturation values over time on the cells along the well location
    at three different locations (bottom).

CCUS (machine learning)
-----------------------
See `this folder <https://github.com/cssr-tools/pyopmnearwell/tree/main/examples/cemracs2023/ml_example_co2eor>`_ for an example of
how to use **pyopmnearwell** to generate data for different input parameters (e.g., injection rates) and read the data (e.g., 
production volumes). An additional example can be found in the `data_generation <https://github.com/cssr-tools/pyopmnearwell/tree/main/examples/data_generation>`_ folder. 
These examples could be used as a starting point for the ones interested in ML.

Publications
------------
For the simulation results published in `this paper <https://onepetro.org/SPEBERG/proceedings/24BERG/1-24BERG/D011S012R010/544194>`_ 
about the impact of intermittency on salt precipitation during CO2 injection, see/run 
`these configuration files <https://github.com/cssr-tools/pyopmnearwell/blob/main/publications>`_.

For a study where **pyopmnearwell** is used to generated a machine-learned near-well model, `click here <https://github.com/cssr-tools/ML_near_well>`_. 