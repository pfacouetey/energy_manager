import pytest
import numpy as np

from energy_manager.src.utils.set_edf_prices import set_edf_prices

@pytest.fixture()
def expected_subscriptions():
    return ["Base", "Heures Creuses - Heures Pleines"]

@pytest.fixture()
def expected_columns():
    return ["subscription", "kwh_price_normal_hour", "kwh_price_peak_hour"]

def test_get_edf_price(expected_subscriptions, expected_columns):
    """
    Test that the function set_edf_prices returns a DataFrame with the expected columns.
    """
    actual_df_edf_prices = set_edf_prices()
    actual_columns = list(actual_df_edf_prices.columns)

    # Check if the DataFrame actual_edf_price has the expected columns
    assert actual_columns == expected_columns, (
        f"Expected {expected_columns}, but got {actual_columns}"
    )

    # Check if the DataFrame actual_edf_price has the expected souscription_types
    actual_subscriptions = list(actual_df_edf_prices["subscription"])
    assert actual_subscriptions == expected_subscriptions, (
        f"Expected {expected_subscriptions}, but got {actual_subscriptions}"
    )

    # Check if the DataFrame actual_edf_prices has the expected prices values
    # Check if the prices are positive
    assert np.all(actual_df_edf_prices["kwh_price_normal_hour"].values > 0), "Expected positive kwh_price_normal_hour values"
    assert np.all(actual_df_edf_prices["kwh_price_peak_hour"].values > 0), "Expected positive kwh_price_peak_hour values"
    # Subscription type "Base"
    np.testing.assert_equal(
        actual_df_edf_prices.loc[
            actual_df_edf_prices["subscription"] == "Base", "kwh_price_normal_hour"].values,
        actual_df_edf_prices.loc[
            actual_df_edf_prices["subscription"] == "Base", "kwh_price_peak_hour"].values,
        "Expected to have the same price for Base subscription"
    )
    # Subscription type "Heures Creuses - Heures Pleines"
    assert \
        actual_df_edf_prices.loc[
            actual_df_edf_prices["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_normal_hour"].values[
            0] < actual_df_edf_prices.loc[
            actual_df_edf_prices["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_peak_hour"].values[
            0], "Expected to have normal hour price less than peak hour price for Heures Creuses - Heures Pleines"