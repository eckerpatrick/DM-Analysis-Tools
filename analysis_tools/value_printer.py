from typing import Optional
import numpy as np

__all__ = [
    "significant_digit_index",
    "get_rounded_to_significant_digit",
]


def significant_digit_index(x: float) -> int:
    if x >= 1:
        index = int(np.log10(x))
        digit = int(x / 10**index)
        if digit < 3:
            return -index + 1
        return -index
    else:
        a = np.array([int(d) for d in np.format_float_positional(x) if d != "."])
        index = int(np.argmax(a > 0))
        if a[index] < 3:
            return index + 1
        return index


def get_rounded_to_significant_digit(
    x: float,
    error: Optional[float] = None,
    sig_digit_index: Optional[int] = None,
) -> str:
    if error and error < 0:
        print("Warning: Setting error to abs(error) because you gave a negative error!")
        error = abs(error)

    if not sig_digit_index:
        if not error:
            sig_digit_index = significant_digit_index(x=abs(x))
        else:
            sig_digit_index = significant_digit_index(x=error)

    exponent = -sig_digit_index
    x = round(x, sig_digit_index)
    x = x / (10.0**exponent)

    x_str = np.format_float_positional(
        x,
        unique=False,
        precision=0,
        trim="-",
    )
    if not error:
        if exponent != 0:
            final_str = r"${a} \times 10^{c}$".format(
                a=x_str,
                c="{" + str(exponent) + "}",
            )
        else:
            final_str = x_str
        return final_str

    error += float(5 * 10.0 ** (-sig_digit_index - 1))
    error = round(error, sig_digit_index)
    error = error / (10.0**exponent)
    error_str = np.format_float_positional(
        error,
        unique=False,
        precision=0,
        trim="-",
    )

    if exponent != 0:
        final_str = r"$({a} \pm {b}) \times 10^{c}$".format(
            a=x_str,
            b=error_str,
            c="{" + str(exponent) + "}",
        )
    else:
        final_str = r"${a} \pm {b}$".format(
            a=x_str,
            b=error_str,
        )
    return final_str
