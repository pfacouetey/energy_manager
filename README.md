# energy_manager

A tool to optimize your house energy consumption!

## Installation

```bash
$ pip install energy_manager
```

## Usage

`energy_manager` is a tool designed specifically for French consumers who currently use or plan to use EDF as their energy provider. 
This document outlines the eligibility criteria, pricing options, time classification, and data sources used in the application.

### Eligibility Criteria

To be eligible for the `energy_manager`, the following conditions must be met:

- **Building Age**: Only buildings constructed in the year 2000 or later are considered.
- **Energy Performance**: Buildings must have a DPE (Diagnostic de Performance Énergétique) rating between A and F.
- **Building Type**: The program applies exclusively to the following building types:
  - `Appartement`
  - `Maison`
  - `Logement Collectif`

### Pricing Options

The calculations within `energy_manager` are based on two EDF pricing options:

- **Option Base ;**
- **Option Heures Creuses - Heures Pleines .**

### Time Classification
To classify which hours of the day are considered Heure Creuse or Heure Pleine, we refer to four proposals provided by ENEDIS to EDF clients. 
Please note that the availability of these proposals may vary depending on your city or region.

### Weather Data
The weather information used in our calculations is sourced from the [Open Weather API](https://openweathermap.org/).

### Energy Cost Estimation

To estimate the energy consumption for heating or cooling a house, the user must provide three essential parameters.

#### Mandatory Parameters

- **City Name (`USER_CITY_NAME`)**: The name of the city where the house is located.
- **Expected Temperature (`USER_TEMPERATURE`)**: The desired indoor temperature the user wants to maintain.
- **DPE Usage (`USER_DPE_USAGE`)**: A multiplication factor for the house's DPE (Diagnostic de Performance Énergétique).

#### Optional Parameters

- **Insulation Factor (`USER_INSULATION_FACTOR`)**: This refers to the insulation properties of the building materials used in the house, which help reduce heat loss or gain. If not provided, it defaults to 1.

#### Package Capabilities

The package has access to:

- Types, surface areas, and `DPE_VALUE` of buildings present in the specified `CITY`.
- Current temperature (`TEMPERATURE(h_x)`) at a given hour (`h_x`) and corresponding energy price (`ENERGY_PRICE(h_x)`) for an entire day.

Based on the provided parameters, the package can offer a rough estimate of energy costs in euros per square meter for buildings in the same region as the user's.
These energy costs are estimated for a whole day based on one hour time step (12AM-1AM, 1AM-2AM, ..., 10PM-11PM, 11PM-12AM).

The energy cost at a given time `(h_x)` (for example `h_x = 1AM-2AM`), for a type of building, is defined by:
```
Estimated Cost = ( |USER_TEMPERATURE - TEMPERATURE(h_x)| * USER_DPE_USAGE * DPE_VALUE * ENERGY_PRICE(h_x) ) / USER_INSULATION_FACTOR
```

What this formula shows is that, per square meter and for an insulation factor of 1 : 
- The user believes he's currently using or will use `USER_USAGE*DPE_VALUE` as energy to elevate/decrease of his house surface temperature of 1 Celsius degree for 1 hour long.

## Contributing

Interested in contributing? Check out the contributing guidelines. 
Please note that this project is released with a Code of Conduct. 
By contributing to this project, you agree to abide by its terms.

## License
`energy_manager` was created by Prince Foli Acouetey. It is licensed under the terms of the MIT license.

## Credits
`energy_manager` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
