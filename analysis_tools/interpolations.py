from typing import Tuple, Callable, List

import numpy as np
from scipy.interpolate import interp1d

__all__ = [
    "logarithmic_interpolation",
    "find_intersections_between_interpolations",
]


def logarithmic_interpolation(
    x: np.ndarray,
    y: np.ndarray,
) -> Callable:
    logx = np.log10(x)
    logy = np.log10(y)
    lin_interp = interp1d(logx, logy, kind="linear")
    log_interp = lambda zz: np.power(10.0, lin_interp(np.log10(zz)))
    return log_interp


def find_intersections_between_interpolations(
    points: np.ndarray,
    interpolations: Tuple[Callable, Callable],
    accuracy: int = 1000,
) -> List[float]:
    intersections = []
    for i in range(len(points) - 1):
        lower, upper = points[i], points[i + 1]
        check_points = np.linspace(lower, upper, accuracy)
        inter_1, inter_2 = interpolations
        diff = inter_1(check_points) - inter_2(check_points)

        if all(v > 0 for v in diff) or all(v < 0 for v in diff):
            continue
        else:
            signs = np.sign(diff)
            sign_0 = signs[0]

            index = np.argmax(signs != sign_0)
            # Check that there are no further intersections in that range
            assert all(s == signs[index] for s in signs[index + 1 : -1])
            intersection_x = check_points[index]
            print(f"Intersection found at x = {intersection_x}!")
            intersections.append(intersection_x)
    return intersections
