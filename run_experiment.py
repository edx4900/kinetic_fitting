import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from eyring_plot import fit_eyring_plot
from kinetic_model import kinetic_model
from sig_figs import format_value_and_error


def curve_fit_plot(ax, df, label, exp_type, solvent=None):
    # Extract concentration and rate data from the DataFrame
    concentration = df['concentration'].to_numpy()
    rate = df['rate'].to_numpy()

    # Set bounds for the curve fitting
    bounds = ([0, 0], [np.inf, np.inf])

    # Perform curve fitting and obtain parameters and covariance
    popt, pcov = curve_fit(kinetic_model, concentration, rate, bounds=bounds)
    ax.scatter(concentration, rate)
    conc_values = np.linspace(min(concentration), max(concentration), 500)
    plt.plot(conc_values, kinetic_model(conc_values, *popt), label=label)

    # Calculate the error in the fitted parameters
    perr = np.sqrt(np.diag(pcov))

    return popt, perr


def run_experiment(data, substrate, plotter, post_plot=None, data_collector=None, ylabel='Rate', exp_type='substrate_dependence'):
    # Gather unique files from the dataset
    files = set(f for environment_data in data.values() for f in environment_data.keys())
    mod_env = ''

    # Iterate through each file
    for i, file in enumerate(sorted(files), start=1):
        fig, ax = plt.subplots()

        # Iterate through different conditions (e.g., pH, temperature)
        for environment in sorted(data.keys()):
            if file in data[environment]:
                # Determine the label for this condition based on experiment type
                if exp_type == 'ph_dependence':
                    mod_env = f'pH {environment}'
                elif exp_type == 'temp_dependence':
                    mod_env = f'{environment} ℃'
                else:
                    mod_env = environment

                # Fit data and plot
                popt, perr = curve_fit_plot(ax, data[environment][file], mod_env, exp_type)
                print(f"{file[:6]} - run {i}: {mod_env}: k2 = {popt[0]} ± {perr[0]} - Kd = {popt[1]} ± {perr[1]}")

                if data_collector:
                    data_collector(popt[0], perr[0], popt[1], perr[1], environment)

        ax.set_title(f'Date: {file[:6]} - run {i}')
        ax.set_xlabel(f'[{substrate}]')
        ax.set_ylabel(ylabel)
        ax.legend()
        plt.show()

    if post_plot:
        post_plot()

    consolidate_results(data, substrate, exp_type)


def run_substrate_dependence(data, substrate):
    run_experiment(data, substrate, lambda file: f'run {file}')


def run_ph_dependence(data, substrate):
    run_experiment(data, substrate, lambda file: f'pH {file}', exp_type='ph_dependence')


def run_temp_dependence(data, substrate):
    k2_values, T_C, Kd_values = [], [], []

    def data_collector(k2, k2_error, kd, kd_error, temp):
        k2_values.append(k2)
        T_C.append(temp)
        Kd_values.append(kd)

    def post_plot():
        fit_eyring_plot(T_C, k2_values)

    run_experiment(data, substrate, lambda file: f'{file} ℃', post_plot, data_collector, exp_type='temp_dependence')


def run_sKIE(data, substrate):
    run_experiment(data, substrate, lambda file: f'{file}', exp_type="sKIE")


def consolidate_results(data, substrate, exp_type='substrate_dependence'):
    # Get a set of all files in the dataset
    files = set(f for environment_data in data.values() for f in environment_data.keys())

    # Initialize variables for solvent KIE calculation
    k2_h2o, k2_d2o = None, None
    err_h2o, err_d2o = None, None

    # Create a new figure and axes for consolidated plot
    fig_all, ax_all = plt.subplots()

    # Iterate through different experimental conditions (e.g., pH, temperature)
    for key in sorted(data.keys()):
        concentration_all = []
        rate_all = []
        mod_key = ''

        # Determine the label for this condition based on experiment type
        if exp_type == 'ph_dependence':
            mod_key = f'pH {key}'
        elif exp_type == 'temp_dependence':
            mod_key = f'{key} ℃'
        else:
            mod_key = key

        # Aggregate concentration and rate data across all files for this condition
        for file in sorted(files):
            if file in data[key]:
                df = data[key][file]
                concentration_all += df['concentration'].tolist()
                rate_all += df['rate'].tolist()

        # Set labels and plot consolidated data
        ax_all.set_title('Combined Runs')
        ax_all.set_xlabel(f'[{substrate}]')
        ax_all.set_ylabel('Rate')
        popt, perr = curve_fit_plot(ax_all,
                                    pd.DataFrame({'concentration': concentration_all, 'rate': rate_all}),
                                    label=mod_key, exp_type=exp_type)

        # Display k2 and Kd values for substrate dependence
        if exp_type == "substrate_dependence":
            plt.text(0.95, 0.1, f"k2 = {format_value_and_error(popt[0], perr[0])}\n"
                                f"Kd = {format_value_and_error(popt[1], perr[1])}",
                     transform=plt.gca().transAxes, ha='right', va='center')

        # Calculate and display solvent KIE for sKIE experiments
        if exp_type == "sKIE":
            if mod_key == 'H2O':
                k2_h2o, err_h2o = popt[0], perr[0]
            else:
                k2_d2o, err_d2o = popt[0], perr[0]

        # Print consolidated results for the current condition
        print(f"\nConsolidated results for {mod_key}:")
        print(f"k2 = {format_value_and_error(popt[0], perr[0])}")
        print(f"Kd = {format_value_and_error(popt[1], perr[1])}")

        # Calculate and print solvent KIE if both H2O and D2O data are available
        if k2_h2o is not None and k2_d2o is not None:
            div_result = k2_h2o / k2_d2o
            rA = err_h2o / k2_h2o
            rB = err_d2o / k2_d2o
            error_prop = rA + rB
            print(f'\nsolvent KIE = {div_result:.2f} ± {error_prop:.2f}')

    # Display legend and show the consolidated plot if multiple files are present
    if len(files) > 1:
        plt.legend()
        plt.show()