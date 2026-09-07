# pylint: skip-file
# type: ignore
"""Provide MinMax scaler layers for tensorflow.keras.

Warning: Tensorflow 2.17 and Keras 3.0 introduce many pylint errors, hence we disable
linting completely. It is possible that the module is not functional at the moment.
"""

from collections.abc import Sequence

import keras
import numpy as np
import tensorflow as tf
from numpy.typing import ArrayLike


class ScalerLayer(keras.layers.Layer):
    """MixIn to provide functionality for the Scaler Layer."""

    data_min: tf.Tensor
    data_max: tf.Tensor
    min: tf.Tensor
    scalar: tf.Tensor

    def __init__(
        self,
        data_min: float | ArrayLike | None = None,
        data_max: float | ArrayLike | None = None,
        feature_range: Sequence[float] | np.ndarray | tf.Tensor = (0, 1),
        **kwargs,  # pylint: disable=W0613
    ) -> None:
        """init  .

        Parameters
        ----------
        data_min : float | ArrayLike | None, optional
            Value used by the operation.
        data_max : float | ArrayLike | None, optional
            Value used by the operation.
        feature_range : Sequence[float] | np.ndarray | tf.Tensor, optional
            Value used by the operation.
        **kwargs : Any
            Additional options forwarded to the underlying operation.
        """
        super().__init__(**kwargs)
        if isinstance(feature_range, tuple):
            # One feature range for all features
            if feature_range[0] >= feature_range[1]:
                raise ValueError("Feature range must be strictly increasing.")
            self.feature_range_: tf.Tensor = tf.convert_to_tensor(
                feature_range, dtype=tf.float32
            )
        elif isinstance(feature_range, (list, np.ndarray)):
            for fr in feature_range:
                if fr[0] >= fr[1]:
                    raise ValueError("Feature range must be strictly increasing.")
            self.feature_range_: tf.Tensor = tf.convert_to_tensor(
                feature_range, dtype=tf.float32
            )

        elif isinstance(feature_range, dict):
            # feature_range is a dict when it comes from config loading
            self.feature_range_: tf.Tensor = tf.convert_to_tensor(
                feature_range["config"]["value"], dtype=feature_range["config"]["dtype"]
            )

        self.data_min_ = data_min
        self.data_max_ = data_max
        self._is_adapted: bool = False

        if data_min is not None and data_max is not None:
            self.data_min_ = tf.convert_to_tensor(data_min, dtype=tf.float32)
            self.data_max_ = tf.convert_to_tensor(data_max, dtype=tf.float32)
            self._adapt()

    def build(self, input_shape: tuple[int, ...]) -> None:
        """Initialize scaling bounds when the layer is built.

        not been initialized yet.

        Parameters
        ----------
        input_shape : tuple[int, ...]
            Shape of input tensors presented to the layer.
        """
        if not self._is_adapted:
            is_adapted = True
            if self.data_min_ is None and self.data_max_ is None:
                is_adapted = False
            # ``data_min`` and ``data_max`` have the same shape as one input tensor.
            self.data_min_ = tf.zeros(input_shape[1:])
            self.data_max_ = tf.ones(input_shape[1:])
            self._adapt()
            if not is_adapted:
                self._is_adapted = False

    def get_weights(self) -> list[ArrayLike]:
        """Return parameters of the scaling.

        Returns:
            list[ArrayLike]: List with three elements in the following order:
            ``self.data_min_``, ``self.data_max_``, ``self.feature_range_``
        """
        return [self.data_min_, self.data_max_, self.feature_range_]

    def set_weights(self, weights: list[ArrayLike]) -> None:
        """Set parameters of the scaling.

        Args:
            weights (list[ArrayLike]): List with three elements in the following order:
            ``data_min``, ``data_max``, ``feature_range``

        Raises:
            ValueError: If ``feature_range[0] >= feature_range[1]``.
        """
        self.feature_range_ = tf.convert_to_tensor(weights[2], dtype=tf.float32)
        if self.feature_range_[0] >= self.feature_range_[1]:
            raise ValueError("Feature range must be strictly increasing.")
        self.data_min_ = tf.convert_to_tensor(weights[0], dtype=tf.float32)
        self.data_max_ = tf.convert_to_tensor(weights[1], dtype=tf.float32)

    def adapt(self, data: ArrayLike) -> None:
        """Fit scaling bounds independently for each input feature.

        each input feature.

        Parameters
        ----------
        data : ArrayLike
            Values used to fit the scaling extrema.
        """
        data = tf.convert_to_tensor(data, dtype=tf.float32)
        self.data_min_ = tf.math.reduce_min(data, axis=0)
        self.data_max_ = tf.math.reduce_max(data, axis=0)
        self._adapt()

    def _adapt(self) -> None:
        """Derive scaling offsets and ranges from the configured extrema."""
        if tf.math.reduce_any(self.data_min_ > self.data_max_):
            raise RuntimeError(
                f"""self.data_min_ {self.data_min_} cannot be larger than self.data_max_
                {self.data_max_} for any element."""
            )
        self.scalar = tf.where(
            self.data_max_ > self.data_min_,
            self.data_max_ - self.data_min_,
            tf.ones_like(self.data_min_),
        )
        self.min = tf.where(
            self.data_max_ > self.data_min_,
            self.data_min_,
            tf.zeros_like(self.data_min_),
        )
        self._is_adapted = True

    @property
    def is_adapted(self):
        """Return whether the scaling parameters have been initialized.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        return self._is_adapted

    @property
    def feature_range(self):
        """Return the target interval for each scaled feature.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        return self.feature_range_

    @property
    def data_min(self):
        """Return the observed minimum for each feature.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        return self.data_min_

    @property
    def data_max(self):
        """Return the observed maximum for each feature.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        return self.data_max_


class MinMaxScalerLayer(
    ScalerLayer, tf.keras.layers.Layer
):  # pylint: disable=W0223,R0901
    """Scales the input according to MinMaxScaling.

    See
    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
    for an explanation of the transform.
    """

    def __init__(
        self,
        data_min: float | ArrayLike | None = None,
        data_max: float | ArrayLike | None = None,
        feature_range: Sequence[float] | np.ndarray | tf.Tensor = (0, 1),
        **kwargs,  # pylint: disable=W0613
    ) -> None:
        """init  .

        Parameters
        ----------
        data_min : float | ArrayLike | None, optional
            Value used by the operation.
        data_max : float | ArrayLike | None, optional
            Value used by the operation.
        feature_range : Sequence[float] | np.ndarray | tf.Tensor, optional
            Value used by the operation.
        **kwargs : Any
            Additional options forwarded to the underlying operation.
        """
        super().__init__(data_min, data_max, feature_range, **kwargs)
        self.name: str = "MinMaxScalerLayer"

        if data_min is not None and data_max is not None:
            self._adapt()

    # Ignore pylint complaining about a missing docstring. Also ignore
    # "variadics removed ...".
    def call(self, inputs: tf.Tensor) -> tf.Tensor:  # pylint: disable=C0116, W0221
        """Apply the layer transformation to an input tensor.

        Parameters
        ----------
        inputs : tf.Tensor
            Tensor values transformed by the layer.

        Returns
        -------
        tf.Tensor
            Result produced by the operation.
        """
        if not super().is_adapted:
            raise RuntimeError(
                """The layer has not been adapted correctly. Call ``adapt`` before using
                the layer or set the ``data_min`` and ``data_max`` values manually.
                """
            )

        # Ensure the dtype is correct.
        inputs = tf.convert_to_tensor(inputs, dtype=tf.float32)

        feature_ranges = tf.convert_to_tensor(self.feature_range_, dtype=tf.float32)
        # If only one feature range is given for multiple features --> broadcast
        if len(feature_ranges.shape) == 1 and len(inputs.shape) > 1:
            feature_ranges = tf.expand_dims(feature_ranges, axis=0)
            feature_ranges = tf.tile(feature_ranges, [tf.shape(inputs)[1], 1])
            self.feature_range_ = feature_ranges

        scaled_data = (inputs - self.min) / self.scalar
        return (
            scaled_data * (self.feature_range_[:, 1] - self.feature_range_[:, 0])
        ) + self.feature_range_[:, 0]

    def compute_output_shape(self, input_shape):
        """Return the unchanged output shape of the elementwise transformation.

        Parameters
        ----------
        input_shape : Any
            Shape of input tensors presented to the layer.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        return input_shape  # The output shape is the same as the input shape

    def get_config(self):
        """Return a serializable Keras layer configuration.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        config = super().get_config()
        config.update(
            {
                "feature_range": self.feature_range_,
                "data_min": (
                    self.data_min_.numpy().tolist()
                    if self.data_min_ is not None
                    else None
                ),
                "data_max": (
                    self.data_max_.numpy().tolist()
                    if self.data_max_ is not None
                    else None
                ),
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        """Reconstruct a scaler layer from serialized configuration.

        Parameters
        ----------
        config : Any
            Serialized Keras layer configuration.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        data_min = config.pop("data_min", None)
        data_max = config.pop("data_max", None)
        feature_range = config.pop("feature_range", (0, 1))

        # Convert the list to a tensor if not None
        data_min = tf.convert_to_tensor(data_min) if data_min is not None else None
        data_max = tf.convert_to_tensor(data_max) if data_max is not None else None
        return cls(
            data_min=data_min, data_max=data_max, feature_range=feature_range, **config
        )


class MinMaxUnScalerLayer(ScalerLayer, tf.keras.layers.Layer):
    """Unscales the input by applying the inverse transform of ``MinMaxScalerLayer``.

    See
    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
    for an explanation of the transformation.
    """

    def __init__(
        self,
        data_min: float | ArrayLike | None = None,
        data_max: float | ArrayLike | None = None,
        feature_range: Sequence[float] | np.ndarray | tf.Tensor = (0, 1),
        **kwargs,  # pylint: disable=W0613
    ) -> None:
        """init  .

        Parameters
        ----------
        data_min : float | ArrayLike | None, optional
            Value used by the operation.
        data_max : float | ArrayLike | None, optional
            Value used by the operation.
        feature_range : Sequence[float] | np.ndarray | tf.Tensor, optional
            Value used by the operation.
        **kwargs : Any
            Additional options forwarded to the underlying operation.
        """
        super().__init__(data_min, data_max, feature_range, **kwargs)
        self._name: str = "MinMaxUnScalerLayer"
        if data_min is not None and data_max is not None:
            self._adapt()

    def call(
        self, inputs: tf.Tensor
    ) -> tf.Tensor:  # pylint: disable=missing-function-docstring
        """Apply the layer transformation to an input tensor.

        Parameters
        ----------
        inputs : tf.Tensor
            Tensor values transformed by the layer.

        Returns
        -------
        tf.Tensor
            Result produced by the operation.
        """
        if not super().is_adapted:
            raise RuntimeError(
                """The layer has not been adapted correctly. Call ``adapt`` before using
                the layer or set the ``data_min`` and ``data_max`` values manually."""
            )
        # Ensure the dtype is correct.
        feature_ranges = tf.convert_to_tensor(self.feature_range_, dtype=tf.float32)
        inputs = tf.convert_to_tensor(inputs, dtype=tf.float32)

        # If only one feature is given for multiple features --> broadcast
        if len(feature_ranges.shape) == 1 and len(inputs.shape) > 1:
            feature_ranges = tf.expand_dims(feature_ranges, axis=0)
            feature_ranges = tf.tile(feature_ranges, [tf.shape(inputs)[1], 1])
            self.feature_range_ = feature_ranges

        unscaled_data = (inputs - self.feature_range_[:, 0]) / (
            self.feature_range_[:, 1] - self.feature_range_[:, 0]
        )
        return unscaled_data * self.scalar + self.min

    def compute_output_shape(self, input_shape):
        """Return the unchanged output shape of the elementwise transformation.

        Parameters
        ----------
        input_shape : Any
            Shape of input tensors presented to the layer.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        return input_shape  # The output shape is the same as the input shape

    def get_config(self):
        """Return a serializable Keras layer configuration.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        config = super().get_config()
        config.update(
            {
                "feature_range": self.feature_range_,
                "data_min": (
                    self.data_min_.numpy().tolist()
                    if self.data_min_ is not None
                    else None
                ),
                "data_max": (
                    self.data_max_.numpy().tolist()
                    if self.data_max_ is not None
                    else None
                ),
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        """Reconstruct a scaler layer from serialized configuration.

        Parameters
        ----------
        config : Any
            Serialized Keras layer configuration.

        Returns
        -------
        Any
            Result produced by the operation.
        """
        data_min = config.pop("data_min", None)
        data_max = config.pop("data_max", None)
        feature_range = config.pop("feature_range", (0, 1))

        # Convert the list to a tensor if not None
        data_min = tf.convert_to_tensor(data_min) if data_min is not None else None
        data_max = tf.convert_to_tensor(data_max) if data_max is not None else None
        return cls(
            data_min=data_min, data_max=data_max, feature_range=feature_range, **config
        )
