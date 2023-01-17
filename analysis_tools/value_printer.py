from typing import Optional
import numpy as np

__all__ = [
    "significant_digit_index",
    "get_rounded_to_significant_digit",
]


def significant_digit_index(x: float):
    if x >= 1:
        index = int(np.log10(x))
        digit = int(x / 10**index)
        if digit < 3:
            return -index + 1
        return -index
    else:
        a = np.array([int(d) for d in np.format_float_positional(x) if d != "."])
        index = np.argmax(a > 0)
        if a[index] < 3:
            return index + 1
        return index


# todo: Check what happens with negative numbers -> are they treated correctly
def get_rounded_to_significant_digit(
    x: float,
    error: Optional[float] = None,
    sig_digit_index: Optional[int] = None,
) -> str:
    if not error:
        if x >= 1:
            digits_before_decimal = int(np.log10(x)) + 1
            x = x / (10 ** (digits_before_decimal - 1))
            exponent = digits_before_decimal - 1
        else:
            factor = significant_digit_index(x=x)
            x = x * 10 ** (factor - 1)
            exponent = -(factor - 1)
    else:
        if error >= 1:
            digits_before_decimal = int(np.log10(error)) + 1
            x = x / (10 ** (digits_before_decimal - 1))
            error = error / (10 ** (digits_before_decimal - 1))
            exponent = digits_before_decimal - 1
        else:
            factor = significant_digit_index(x=error)
            x = x * 10 ** (factor - 1)
            error = error * 10 ** (factor - 1)
            exponent = -(factor - 1)

    if sig_digit_index is not None:
        pass
    else:
        if error:
            sig_digit_index = significant_digit_index(x=error)
        else:
            sig_digit_index = significant_digit_index(x=x)

    trim = "-" if sig_digit_index == 0 else "k"
    x_str = np.format_float_positional(
        round(x, sig_digit_index),
        unique=False,
        precision=abs(sig_digit_index),
        trim=trim,
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

    # todo: always round up the uncertainty
    error_str = np.format_float_positional(
        round(error, sig_digit_index),
        unique=False,
        precision=abs(sig_digit_index),
        trim=trim,
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
