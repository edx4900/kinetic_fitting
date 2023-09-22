from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
from sig_figs import format_value_and_error

# universal gas constant
R = 8.3145  # J/(mol*K)
kb = 1.380658E-23  # J/K
planck = 6.6260755E-34  # J s
# conversion factor from J to cal
j_to_cal = 0.239005736
# conversion factor from cal to kcal
cal_to_kcal = 1e-3


def to_kelvin(temp_c):
    """Convert a temperature in °C to Kelvin"""
    return temp_c + 273.15


def fit_eyring_plot(T_C, k2_values):
    T_K = [to_kelvin(t) for t in T_C]  # Convert to Kelvin

    # Prepare the data for the Eyring plot
    x_values = [1 / T for T in T_K]  # Inverse temperatures
    y_values = [np.log(k2 / T) for k2, T in zip(k2_values, T_K)]

    # Perform the linear regression
    slope, intercept, _, _, _ = linregress(x_values, y_values)

    # calculate Delta H and Delta S
    delta_H = -R * slope  # in Joules
    delta_S = R * (intercept - np.log(kb / planck))  # in Joules/K
    delta_H *= j_to_cal * cal_to_kcal  # Convert to kcal/mol
    delta_S *= j_to_cal  # Convert to cal/mol/K

    # Estimating error in the linear regression:
    # Fit a polynomial and calculate the covariance
    degree = 1
    p, cov = np.polyfit(x_values, y_values, degree, cov=True)
    # Extract variances of polynomial coefficients from the covariance matrix
    var_slope, var_intercept = np.diagonal(cov)

    # Calculate standard deviations as square roots of variances
    std_slope = np.sqrt(var_slope)
    std_intercept = np.sqrt(var_intercept)

    # Calculate error in Delta H and Delta S
    delta_H_err = abs(-R * std_slope * j_to_cal * cal_to_kcal)  # Error in Delta H
    delta_S_err = abs(R * std_intercept * j_to_cal)  # Error in Delta S

    # Plot the data and the linear regression model
    plt.scatter(x_values, y_values, label="k2")
    plt.plot(x_values, [slope * x + intercept for x in x_values], 'r', label="Linear fit")
    plt.xlabel("Inverse temperature (1/K)")
    plt.ylabel("-ln(k/T)")
    plt.legend()
    plt.title("Eyring plot")

    print('\nΔH‡: ' + str(delta_H) + ' ± ' + str(delta_H_err) + ' kcal/mol')
    print('ΔS‡: ' + str(delta_S) + ' ± ' + str(delta_S_err) + ' cal/ (mol*K)')

    # Print out the fits on the plot
    plt.text(0.05, 0.2, 'Fit parameters:', transform=plt.gca().transAxes, ha='left', va='center')
    plt.text(0.05, 0.15, f'ΔH‡ = {format_value_and_error(delta_H, delta_H_err)} kcal/mol',
             transform=plt.gca().transAxes, ha='left', va='center')
    plt.text(0.05, 0.1, f'ΔS‡ = {format_value_and_error(delta_S, delta_S_err)} cal/mol/K',
             transform=plt.gca().transAxes, ha='left', va='center')
    plt.show()