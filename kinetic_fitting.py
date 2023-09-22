import os
import sys
from run_experiment import run_ph_dependence, run_substrate_dependence, run_temp_dependence, run_sKIE
from load_data import load_data


def main():
    # Check if directory is given as argument
    if len(sys.argv) < 2:
        print("Usage: python kinetic_fitting.py <directory_path>")
        return

    # Get the directory path from arguments
    directory_path = sys.argv[1]

    # Separate directory name to obtain the experiment type and substrate
    directory_name = os.path.basename(directory_path)
    splits = directory_name.split('_')

    if len(splits) != 3:
        print("Invalid directory name. It should be in the form date_experiment_substrate")
        return

    date, experiment_type, substrate = splits
    data = load_data(directory_path, experiment_type, substrate)

    # print(f"Date: {date}")
    print(f"Experiment Type: {experiment_type}")
    print(f"Substrate: {substrate}")

    # Map of experiment type to scripts
    experiment_scripts = {
        "pH": run_ph_dependence,
        "sKIE": run_sKIE,
        "sub": run_substrate_dependence,
        "temp": run_temp_dependence,
    }

    # Run the corresponding function based on experiment type
    if experiment_type in experiment_scripts:
        func = experiment_scripts[experiment_type]
        func(data, substrate)
    else:
        print("Invalid experiment type")

if __name__ == "__main__":
    main()