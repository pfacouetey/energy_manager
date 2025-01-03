# energy_manager
A tool to optimize your house energy consumption!

## Table of Contents
1. [Overview]()
2. [Installation and Setup]()
3. [Technologies Used]()
4. [Usage]()
5. [Future Improvements]()
6. [License]()
7. [Contributing]()
8. [Credits]()

## Overview
 Energy consumption is a vital consideration in modern buildings. 
 The `energy_manager` package is a tool specifically designed for French consumers who currently use or plan to use EDF as their energy provider. 
 This tool provides users with a comprehensive overview of how they can optimize their energy consumption.

## Technologies Used
- Python (3.12.8)
- Key Libraries:
    - **pandas/numpy**: Data handling and numerical computations.
    - **seaborn/matplotlib**: For visualizing results.

## Installation and Setup
To install `energy_manager`, you can simply run the command:
```bash
  pip install energy_manager
```

## Usage
To gain a better understanding of how to use this package, please refer to the `example.ipynb` notebook located in the `docs folder` or consult this [link](https://energy-manager.readthedocs.io/en/latest/).

Additionally, we provide information on the eligibility criteria, pricing options, time classifications, and data sources utilized in `energy_manager`.

### Eligibility Criteria
To be eligible for the `energy_manager`, the following conditions must be met:

- _Building Age_: Only buildings constructed in the year 2000 or later are considered.
- _Energy Performance_: Buildings must have a DPE (Diagnostic de Performance Énergétique) rating between A and F.
- _Building Type_: The program applies exclusively to building types such as `Appartement`, `Maison`, `Logement Collectif`.

### Pricing Options
The calculations within `energy_manager` are based on two EDF pricing options:
- _Option Base_ ;
- _Option Heures Creuses - Heures Pleines_ .

### Time Classification
To classify which hours of the day are considered `Heure Creuse` or `Heure Pleine`, we refer to four proposals provided by ENEDIS to EDF clients. 
Please note that the availability of these proposals may vary depending on your city or region.

### Weather Data
The weather information used in our calculations is sourced from the [Open Weather API](https://openweathermap.org/).

### Energy Cost Estimation
To estimate the energy consumption for heating or cooling a house, the user must provide four essential parameters.

#### Mandatory Parameters
- `city_name` The name of the city where the house is located.
- `temperature`: The desired indoor temperature (in °C) the user wants to maintain.
- `dpe_usage`: A multiplication factor to correct his house's DPE (Diagnostic de Performance Énergétique) based on season.
- `openweathermap_api_key`: This key will be used by `energy_manger` to get all required information on the user's city coordinates and its weather.

To get a valid `openweathermap_api_key`, refer to this link :  [`One Call API 3.0`](https://home.openweathermap.org/subscriptions/unauth_subscribe/onecall_30/base).
It's a `Subscription Pay As You Call` which will only makes you pay when you get over a daily limit of 1000 API calls if you're subscribing as an individual.

#### Optional Parameters
- `insulation_factor`: This refers to the insulation properties of the building materials used in the house, which help reduce heat loss or gain. 
If not provided, it defaults to 1.

#### Package Capabilities
The package has access to:
- Types, surface areas, and `dpe_value` of buildings present in the specified `user_city_name`.
- Current temperature (`temperature(h_x)`) at a given hour (`h_x`) and corresponding energy price (`energy_price(h_x)`) for an entire day.

Based on the provided parameters, the package can offer a rough estimate of energy costs in euros per square meter for buildings in the same region as the user's.
These energy costs are estimated for a whole day based on one hour time step (12AM-1AM, 1AM-2AM, ..., 10PM-11PM, 11PM-12AM).

The energy cost at a given time `(h_x)` (for example `h_x = 1AM-2AM`), for a type of building, is defined by:
```
Energy_Cost(h_x) = ( |user_temperature - temperature(h_x)| * user_dpe_usage * dpe_value * energy_price(h_x) ) / user_insulation_factor
```

Based on this formula, per square meter and for an insulation factor of 1, the user will use `user_dpe_usage*dpe_value` as energy to elevate/decrease of his house surface temperature of 1 Celsius degree for 1 hour long.

## Future Improvements
- Formulate a strategy to enhance the accuracy of current rough estimates of energy consumption.
- Extend energy estimation methodologies to include other energy providers, facilitating a broader comparison of available energy options.

## License
`energy_manager` is registered under the terms of the MIT license. For any further details, consult the LICENSE file.

## Contributing
Interested in contributing? Check out the contributing guidelines. 
Please note that this project is released with a Code of Conduct. 
By contributing to this project, you agree to abide by its terms.

## Credits
`energy_manager` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and [`py-pkgs-cookiecutter`](https://github.com/py-pkgs/py-pkgs-cookiecutter).
