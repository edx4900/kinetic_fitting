import math

def sig_figs(error_value):
    return abs(math.floor(math.log10(error_value)))

def format_value_and_error(value, error_val):
    sf = sig_figs(error_val)
    return f"{value:.{sf}f} ± {error_val:.{sf}f}"