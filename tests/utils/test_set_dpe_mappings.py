import pytest

from energy_manager.src.energy_manager.utils.set_dpe_mappings import set_dpe_mappings


@pytest.fixture()
def expected_dpe_classes():
    return ["A", "B", "C", "D", "E", "F"]

@pytest.fixture()
def expected_dpe_classes_order(expected_dpe_classes):
    return expected_dpe_classes

@pytest.fixture()
def expected_dpe_values_order():
    return [70.0, 110.0, 180.0, 250.0, 330.0, 420.0]

def test_get_dpe_mappings(expected_dpe_classes, expected_dpe_classes_order, expected_dpe_values_order):
    """
    Test that the function set_dpe_mappings returns a dictionary with the expected DPE classes.
    """
    actual_dpe_mappings = set_dpe_mappings()
    actual_dpe_classes = list(actual_dpe_mappings.keys())
    actual_dpe_classes_order = list(actual_dpe_mappings.keys())

    # Check if the dictionary actual_dpe_mappings values are strings
    assert all(isinstance(value, str) for value in actual_dpe_mappings.values()), (
        f"Expected all values to be strings, but got {actual_dpe_mappings.values()}"
    )

    # Check if the dictionary actual_dpe_mappings contains the expected DPE classes
    assert list(actual_dpe_mappings.keys()) == expected_dpe_classes, (
        f"Expected {expected_dpe_classes}, but got {actual_dpe_classes}")

    # Check if the dictionary keys are in ascending order
    assert actual_dpe_classes_order == expected_dpe_classes_order, "DPE classes are not in ascending order"

    # Check if the dictionary values are as in expected_dpe_values_order
    actual_dpe_values_order = [float(value) for value in list(actual_dpe_mappings.values())]
    assert actual_dpe_values_order == expected_dpe_values_order, f"Expected {expected_dpe_values_order}, but got {actual_dpe_values_order}."

    # Additional check: verify each pair of actual_dpe_mappings is in correct order
    for i, item in enumerate(actual_dpe_classes):
        if i + 1 < len(actual_dpe_classes):
            assert int(actual_dpe_mappings[item]) < int(actual_dpe_mappings[actual_dpe_classes[i + 1]]), \
                f"Value for {item} is not less than {actual_dpe_classes[i + 1]}"