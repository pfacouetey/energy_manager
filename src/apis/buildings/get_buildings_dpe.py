import requests
import pandas as pd
from typing import Optional

from energy_manager.src.apis.buildings.get_department import get_department


def get_buildings_dpe(city_name: str) -> Optional[pd.DataFrame]:
    """
    Fetches buildings DPE data for a given city.

    Args:
        city_name (str): Name of the city.

    Returns:
        Optional[pd.DataFrame]: DataFrame with buildings DPE data, or None if the fetch fails.
    """
    base_url = ("https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
                "base-des-diagnostics-de-performance-energetique-dpe-des-batiments-residentiels-p/records")
    department_name = get_department(city_name=city_name)
    if department_name:
        params = {
            "select": "classe_energie,"
                      " tr002_type_batiment_id,"
                      " min(surface_habitable) as min_surface_habitable,"
                      " max(surface_habitable) as max_surface_habitable",
            "where": f"annee_construction is not null and "
                     f"annee_construction >= date'2000' and "
                     f"classe_energie is not null and "
                     f"surface_habitable is not null and "
                     f"(tr002_type_batiment_id = \"Appartement\" or "
                     f"tr002_type_batiment_id = \"Maison\" or "
                     f"tr002_type_batiment_id = \"Logements collectifs\") and "
                     f"nom_dep = \"{department_name}\" and "
                     f"(classe_energie = \"A\" or "
                     f"classe_energie = \"B\" or "
                     f"classe_energie = \"C\" or "
                     f"classe_energie = \"D\" or "
                     f"classe_energie = \"E\" or "
                     f"classe_energie = \"F\" or "
                     f"classe_energie = \"G\")",
            "group_by": "classe_energie, tr002_type_batiment_id"
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            if data["results"]:
                new_data = pd.DataFrame(data["results"])

                new_data.rename(
                    columns={
                        "classe_energie": "dpe_class", "tr002_type_batiment_id": "building_type",
                        "min_surface_habitable": "min_surface_in_square_meters",
                        "max_surface_habitable": "max_surface_in_square_meters",
                    }, inplace=True)
                new_data[["min_surface_in_square_meters", "max_surface_in_square_meters"]] = (
                    new_data[["min_surface_in_square_meters", "max_surface_in_square_meters"]]).astype(float)
                new_data["building_type"] = new_data["building_type"].astype(str)
                new_data["dpe_class"] = pd.Categorical(
                    new_data["dpe_class"], categories=["A", "B", "C", "D", "E", "F", "G"], ordered=True)

                return new_data

            else:
                print(f"No infos on buildings energy consumption found for the city {city_name}.")
                return None

        else:
            print(f"Error fetching data: {response.status_code}")
            return None

    else:
        print(f"No department found for city {city_name}.")
        return None
