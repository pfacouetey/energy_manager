import pytest
import numpy as np

from src_copy.energy_manager.utils.set_edf_prices import set_edf_prices

@pytest.fixture()
def expected_subscriptions():
    return ["Base", "Heures Creuses - Heures Pleines"]

@pytest.fixture()
def expected_columns():
    return ["subscription", "kwh_price_normal_hour", "kwh_price_peak_hour"]

def test_get_edf_price(
        expected_subscriptions,
        expected_columns,
):
    """
    Tests the EDF price dataset for correctness including column names, subscription details, and price validation.

    This function validates the integrity of the data returned from the `set_edf_prices` function. It checks the
    columns of the resulting DataFrame, the content of the subscription column, and the kwh price values for
    both normal and peak hours. It also ensures specific relationships between these price values
    based on the subscription type.

    Args:
        expected_subscriptions (list): The expected subscription names for the EDF dataset.
        expected_columns (list): The expected column names of the resulting DataFrame to be validated.
    """
    actual_edf_prices_df = set_edf_prices()
    actual_columns = list(actual_edf_prices_df.columns)

    assert actual_columns == expected_columns, (
        f"Expected {expected_columns}, but got {actual_columns}"
    )

    actual_subscriptions = list(actual_edf_prices_df["subscription"])
    assert actual_subscriptions == expected_subscriptions, (
        f"Expected {expected_subscriptions}, but got {actual_subscriptions}"
    )

    assert np.all(actual_edf_prices_df["kwh_price_normal_hour"].values > 0), "Expected positive kwh_price_normal_hour values"
    assert np.all(actual_edf_prices_df["kwh_price_peak_hour"].values > 0), "Expected positive kwh_price_peak_hour values"
    np.testing.assert_equal(
        actual_edf_prices_df.loc[
            actual_edf_prices_df["subscription"] == "Base", "kwh_price_normal_hour"].values,
        actual_edf_prices_df.loc[
            actual_edf_prices_df["subscription"] == "Base", "kwh_price_peak_hour"].values,
        "Expected to have the same price for Base subscription"
    )
    assert \
        actual_edf_prices_df.loc[
            actual_edf_prices_df["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_normal_hour"].values[
            0] < actual_edf_prices_df.loc[
            actual_edf_prices_df["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_peak_hour"].values[
            0], "Expected to have normal hour price less than peak hour price for Heures Creuses - Heures Pleines"
