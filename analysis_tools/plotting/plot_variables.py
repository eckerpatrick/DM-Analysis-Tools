from typing import NamedTuple, Tuple, Optional, List, Union


__all__ = [
    "PlotVariable",
    "HistVariable",
    "BinningVariable",
]


class PlotVariable(NamedTuple):
    df_label: str
    label: str
    unit: Optional[str] = None
    scope: Optional[Tuple[float, float]] = None
    x_scale_log: bool = False
    y_scale_log: bool = False


class HistVariable:
    def __init__(
        self,
        df_label: str,
        label: str,
        unit: Optional[str] = None,
        bins: int = 10,
        scope: Optional[Tuple[float, float]] = None,
        x_scale_log: bool = False,
    ) -> None:
        self._df_label = df_label
        self._label = label
        self._unit = unit
        self._bins = bins
        self._scope = scope
        self._x_scale_log = x_scale_log

    @property
    def x_label(self):
        return f"{self.label} ({self.unit})" if self.unit else self.label

    @property
    def df_label(self) -> str:
        return self._df_label

    @property
    def label(self) -> str:
        return self._label

    @property
    def unit(self) -> Optional[str]:
        return self._unit

    @property
    def bins(self) -> int:
        return self._bins

    @property
    def scope(self) -> Optional[Tuple[float, float]]:
        return self._scope

    @property
    def x_scale_log(self) -> bool:
        return self._x_scale_log


class BinningVariable:
    def __init__(
        self,
        df_label: str,
        label: str,
        binning: Union[int, Tuple[float, ...]],
        scope: Tuple[float, float] = None,
        unit: Optional[str] = None,
        bin_mids: bool = False,
    ) -> None:
        self._df_label = df_label
        self._label = label
        self._scope = scope
        self._binning = binning
        self._unit = unit
        self._bin_mids = bin_mids

    def get_bin_edges(self) -> Tuple[Tuple[float, float], ...]:
        bin_edges = []  # type: List[Tuple[float, float]]
        if isinstance(self.binning, tuple):
            if self.bin_mids is False:
                for i in range(len(self.binning) - 1):
                    assert self.binning[i] < self.binning[i + 1], (self.binning[i], self.binning[i + 1])
                    bin_edges.append((self.binning[i], self.binning[i + 1]))
                assert len(bin_edges) == len(self.binning) - 1
            else:
                raise ValueError
        else:
            assert self.scope is not None
            assert isinstance(self.binning, int)
            lower_bound, upper_bound = self.scope
            step = (upper_bound - lower_bound) / self.bins
            for i in range(self.bins):
                low = i * step + lower_bound
                up = (i + 1) * step + lower_bound
                bin_edges.append((low, up))

            assert len(bin_edges) == self.bins, (len(bin_edges), self.bins)
        return tuple(bin_edges)

    def get_upper_limits(self) -> Tuple[float, ...]:
        return tuple([x for _, x in self.get_bin_edges()])

    def get_bin_mids(self) -> Tuple[float, ...]:
        if isinstance(self.binning, int):
            assert self.scope is not None
            low, up = self.scope
            step = (up - low) / self.bins
            bin_mids = [low + (i + 1 / 2) * step for i in range(self.bins)]
            return tuple(bin_mids)
        else:
            if self.bin_mids is False:
                bin_mids = [(up - lw) / 2 + lw for lw, up in self.get_bin_edges()]
                return tuple(bin_mids)
            else:
                assert isinstance(self.binning, tuple)
                return self.binning

    def get_label_for_bin(self, bin_edges: Tuple[float, float]) -> str:
        lower_limit, upper_limit = bin_edges
        if self.unit:
            return rf"{lower_limit} {self.unit} $\leq$ {self.label} < {upper_limit} {self.unit}"
        else:
            return rf"{lower_limit} $\leq$ {self.label} < {upper_limit}"

    @staticmethod
    def from_hist_variable(hist_variable: HistVariable) -> "BinningVariable":
        return BinningVariable(
            df_label=hist_variable.df_label,
            label=hist_variable.label,
            binning=hist_variable.bins,
            scope=hist_variable.scope,
            unit=hist_variable.unit,
        )

    @property
    def bins(self) -> int:
        if isinstance(self.binning, int):
            bins = self.binning
            assert isinstance(bins, int)
            return bins
        else:
            assert isinstance(self.binning, tuple)
            if self.bin_mids is False:
                return len(self.binning) - 1
            else:
                return len(self.binning)

    @property
    def x_label(self):
        return f"{self.label} ({self.unit})" if self.unit else self.label

    @property
    def df_label(self) -> str:
        return self._df_label

    @property
    def label(self) -> str:
        return self._label

    @property
    def scope(self) -> Optional[Tuple[float, float]]:
        return self._scope

    def set_scope(self, scope: Tuple[float, float]) -> None:
        self._scope = scope

    @property
    def binning(self) -> Union[int, Tuple[float, ...]]:
        return self._binning

    @property
    def unit(self) -> Optional[str]:
        return self._unit

    @property
    def bin_mids(self) -> bool:
        return self._bin_mids
