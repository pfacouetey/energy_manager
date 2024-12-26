import pytest

from src.energy_manager.utils.set_dpe_mappings import set_dpe_mappings


@pytest.fixture()
def expected_dpe_classes():
    return ["F", "A", "D", "B", "C", "E"]

@pytest.fixture()
def expected_dpe_classes_order(expected_dpe_classes):
    return sorted(expected_dpe_classes)

@pytest.fixture()
def expected_dpe_values_order():
    return [70.0, 110.0, 180.0, 250.0, 330.0, 420.0]

def test_get_dpe_mappings(
        expected_dpe_classes,
        expected_dpe_values_order,
        expected_dpe_classes_order,
):
    """
    Tests the functionality of `set_dpe_mappings()` by verifying the mapping's classes,
    ordering, and value correctness based on the provided expected data.

    Args:
        expected_dpe_classes (list[str]): A list of expected DPE classes that should
            match the keys of the actual DPE mappings.
        expected_dpe_values_order (list[float]): A list of expected DPE values in the
            specified order. The actual DPE mappings' values are converted to floats
            and compared against this list.
        expected_dpe_classes_order (list[str]): A list of expected DPE classes in the
            specified order. The actual DPE classes are validated to maintain this
            ordering.

    Raises:
        AssertionError: If the actual DPE mappings' values are not strings, if the
            keys do not match the expected DPE classes, if the ordering of the classes
            or values is incorrect, or if the numerical values of consecutive mapping
            entries violate ascending order.
    """
    actual_dpe_mappings = set_dpe_mappings()
    actual_dpe_classes = list(actual_dpe_mappings.keys())
    actual_dpe_classes_order = list(actual_dpe_mappings.keys())

    assert all(isinstance(value, str) for value in actual_dpe_mappings.values()), (
        f"Expected all values to be strings, but got {actual_dpe_mappings.values()}"
    )

    assert set(actual_dpe_mappings.keys()) == set(expected_dpe_classes), (
        f"Expected {expected_dpe_classes}, but got {actual_dpe_classes}")

    assert actual_dpe_classes_order == expected_dpe_classes_order, "DPE classes are not in ascending order"

    actual_dpe_values_order = [float(value) for value in list(actual_dpe_mappings.values())]
    assert actual_dpe_values_order == expected_dpe_values_order, f"Expected {expected_dpe_values_order}, but got {actual_dpe_values_order}."

    for i, item in enumerate(actual_dpe_classes):
        if i + 1 < len(actual_dpe_classes):
            assert int(actual_dpe_mappings[item]) < int(actual_dpe_mappings[actual_dpe_classes[i + 1]]), \
                f"Value for {item} is not less than {actual_dpe_classes[i + 1]}"
