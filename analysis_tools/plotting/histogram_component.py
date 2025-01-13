from typing import Optional
import numpy as np

__all__ = [
    "HistogramComponent",
]


class HistogramComponent:
    def __init__(
        self,
        data: np.ndarray,
        label: str,
        weights: Optional[np.ndarray] = None,
        color: Optional[str] = None,
        related_component: Optional["HistogramComponent"] = None,
        line_style: str = "-",
    ) -> None:
        self._data = data
        self._label = label
        self._weights = weights
        self._color = color
        self._related_component = related_component
        self._line_style = line_style

    def get_bin_count(self) -> np.ndarray:
        pass

    @property
    def data(self) -> np.ndarray:
        return self._data

    @property
    def label(self) -> str:
        return self._label

    @property
    def weights(self) -> Optional[np.ndarray]:
        return self._weights

    @property
    def color(self) -> Optional[str]:
        return self._color

    @property
    def related_component(self) -> Optional["HistogramComponent"]:
        return self._related_component

    @property
    def line_style(self) -> str:
        return self._line_style
