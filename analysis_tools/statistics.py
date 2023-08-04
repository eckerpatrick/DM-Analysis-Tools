from typing import Union, Tuple, Optional

# import gammapy.stats as gstats
# import numpy as np
# import scipy.stats
# import scipy.special
import ROOT as root

__all__ = [
    "bayes_divide",
    # "get_fc_upper_limit",
]


def bayes_divide(
    a: Union[float, int],
    b: Union[float, int],
    cl: float = 0.683,
) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    hall = root.TH1D("hall", "hall", 1, 0, 1)
    hsel = root.TH1D("hsel", "hsel", 1, 0, 1)

    if b > a:
        return None, None, None

    if a == 0:
        return 0, None, None

    hall.SetBinContent(1, a)
    hsel.SetBinContent(1, b)

    g = root.TGraphAsymmErrors()
    g.Divide(hsel, hall, "cl=%s b(1,1) mode" % (str(cl)))

    return b / a, g.GetErrorYlow(0), g.GetErrorYhigh(0)


# def get_fc_upper_limit(
#    n_background: float,
#    n_observed: float,
#    cl: float = 0.9,
# ) -> float:
#    x_bins = np.arange(0, 50)
#    mu_bins = np.linspace(0, 15, int(15 / 0.005) + 1, endpoint=True)
#    matrix = [scipy.stats.poisson(mu + n_background).pmf(x_bins) for mu in mu_bins]
#
#    acceptance_intervals = gstats.fc_construct_acceptance_intervals_pdfs(matrix, cl)
#    lower_limit_num, upper_limit_num, _ = gstats.fc_get_limits(mu_bins, x_bins, acceptance_intervals)
#
#    upper_limit = gstats.fc_find_limit(n_observed, upper_limit_num, mu_bins)
#    return upper_limit
