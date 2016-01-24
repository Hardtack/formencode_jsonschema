def compare_schema(expected, actual):
    expected = expected.copy()
    actual = actual.copy()
    expected_required = expected.pop('required', ())
    actual_required = actual.pop('required', ())
    assert set(expected_required) == set(actual_required)
    assert expected == actual
