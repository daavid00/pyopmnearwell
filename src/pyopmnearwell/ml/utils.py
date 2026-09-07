"""Utilility functions for the ensemble and ML capabilities.

Note: ``ml.ensemble`` makes use of ``np.random.default_rng``, which ignores the global
seed of ``numpy``. Make sure to set them locally for full determinism.
"""

import keras
import tensorflow as tf


def enable_determinism(seed: int | None = None):
    """Set global random seeds and enable deterministic TensorFlow operations.

    ``keras.utils.set_random_seed`` configures the Python, NumPy, and TensorFlow
    seeds. Local ``numpy.random.Generator`` instances are independent and must be
    seeded when they are created.

    Parameters
    ----------
    seed : int | None, optional
        Seed applied to the supported global random-number generators.
    """
    # ``tf.keras.utils.set_random_seed`` sets the python, numpy, and tensorflow seed
    # simultaneously.
    keras.utils.set_random_seed(seed=seed)
    tf.config.experimental.enable_op_determinism()
