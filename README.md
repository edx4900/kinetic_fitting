# Kinetic Fitting for Biochemical Reactions

This repository contains a collection Python scripts designed to fit experimental biochemical data to a kinetic model. The code reads data from a directory of Excel files, each containing concentration and rate data from multiple experiments of the same type. The result is a visualization of kinetic fitting parameters.

This codebase is useful for biochemists, molecular biologists or anyone interested in depicting kinetic behavior of biochemical reactions.

## Table of Contents

- [Data Organization](#data-organization)
- [Naming Conventions](#naming-conventions)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Usage](#usage)

## Data Organization

### Excel Files

Make sure to structure your data in Excel files following these guidelines:

- **Sheet Setup**: Create a separate sheet within the Excel file for each condition under which the experiment is performed. These may refer to variations in parameters such as "pH", "temperature", or "solvent". Name these sheets to reflect their specific conditions. In this way, each sheet of the workbook corresponds to a distinct set of experimental conditions.

- **Column Arrangement**: Each sheet should contain two columns - "concentration" and "rate." These columns represent the substrate concentration and the observed rate values of your experiment.

For example, if you conducted experiments at varying temperatures, your Excel workbook might look something like this:

`Sheet: "T = 25 C"`
```
"concentration": [0.1, 0.2, 0.3, 0.4, 0.5]
"rate": [0.05, 0.04, 0.07, 0.07, 0.08]
```
`Sheet: "T = 30 C"`
```
"concentration": [0.1, 0.2, 0.3, 0.4, 0.5]
"rate": [0.06, 0.08, 0.10, 0.11, 0.12]
```

## Naming Conventions

### Directory

Your directory naming structure should use the following convention: `date_experiment_substrate`. Make sure to separate the three parts (date, experiment, and substrate) with underscores (_).

For example, the directory can be named as "20220131_pH_4-bromophenol".

#### Experiment Types: 

- **Substrate Dependence**: 
    - Directory: `date_sub_substrate`
    - Determines rate and dissociation constants.

- **pH Dependence**: Assesses substrate impact at variable pH levels.
    - Directory: `date_pH_substrate`
    - Provides rate and dissociation constants for each pH.

- **Temperature Dependence**: Explores substrate influence under various temperatures.
    - Directory: `date_temp_substrate`
    - Extracts activation parameters (ΔH‡ and ΔS‡) from Eyring plot analysis and evaluates kinetic parameters at each temperature point.

- **Solvent Kinetic Isotope Effect (sKIE)**: Studies substrate response in H2O and D2O.
    - Directory: `date_sKIE_substrate`
    - Outputs sKIE value and related kinetic parameters for each solvent type.

### Excel Files

The naming structure of your Excel files should begin with 'YYMMDD' denoting the date, followed by any descriptive information. For example, "220131_temperature_data.xlsx".

The code is set up to expect this date in the file name. It helps keep your data organized and sorted easily. If you want to use a different naming style, you'll just need to adjust the code to match.

## Getting Started 

The instructions below will guide you to run a copy of this project on your local machine.

### Prerequisites

This project requires Python3 and a couple of Python libraries.

To install the required packages, use this command:

```shell
pip install pandas openpyxl numpy matplotlib scipy
```

### Usage

After successfully cloning this repository and switching into the project's root directory, run the project as a module using this command:

```shell
python3 -m kinetic_fitting <directory_path>
```
Replace `<directory_path>` with the path to the directory that contains your Excel data files.