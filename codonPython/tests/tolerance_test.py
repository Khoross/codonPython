from codonPython.tolerance import check_tolerance
import numpy as np
import pandas as pd
# import pandas.util.testing as pdt
import pytest


testdata = [
    np.array([1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242]),
    np.array([1, 2, 3, 4, 5, 5.5, 6, 6.5, 7]),
]


@pytest.mark.parametrize("t, y, to_exclude, poly_features, alpha, expected", [
    (
        *testdata,
        2,
        [1, 2],
        0.05,
        pd.DataFrame({
            'yhat_u': [
                8.11380197739608,
                9.051653693670929,
                7.127135023632205,
                7.735627110021585,
            ],
            'yobs': [6.5, 7.0, 6.5, 7.0],
            'yhat': [
                7.214285714285714,
                8.071428571428573,
                6.500000000000002,
                6.821428571428574,
            ],
            'yhat_l': [
                6.31476945117535,
                7.091203449186216,
                5.872864976367799,
                5.907230032835563,
            ],
            'polynomial': [1, 1, 2, 2]
        })
    ),
    (
        *testdata,
        2,
        [3],
        0.05,
        pd.DataFrame({
            'yhat_u': [
                6.753927165005773,
                7.214574732953706,
            ],
            'yobs': [6.5, 7.0],
            'yhat': [
                6.0000000000000036,
                5.571428571428576,
            ],
            'yhat_l': [
                5.2460728349942345,
                3.928282409903445,
            ],
            'polynomial': [3, 3]
        })
    ),
])
def test_tolerance_checking_BAU(t, y, to_exclude, poly_features, alpha, expected):
    obtained = check_tolerance(
        t,
        y,
        to_exclude=to_exclude,
        poly_features=poly_features,
        alpha=alpha,
    )
    assert expected.equals(obtained)


@pytest.mark.parametrize("t, y, to_exclude, poly_features, alpha", [
    (
        *testdata,
        2,
        "flamingo",  # This should be a list
        0.05,
    ),
    (
        *testdata,
        2,
        [2],
        "flamingo",  # Needs to be int
    ),
    (
        *testdata,
        2,
        [2],
        42,  # Needs to be between 0 and 1
    ),
    (
        *testdata,
        "flamingo",  # Needs to be int
        [2],
        0.05,
    ),
])
def test_ValueErrors(t, y, to_exclude, poly_features, alpha):
    with pytest.raises(ValueError):
        check_tolerance(t, y, to_exclude=to_exclude,
                        poly_features=poly_features, alpha=alpha)


@pytest.mark.parametrize("t, y, to_exclude, poly_features, alpha", [
    (
        *testdata,
        2,
        [42],  # Elements in the list should be between 0 and 4
        0.05,
    ),
    (
        *testdata,
        42,  # Can't have to_exclude making your sample size smaller than 4
        [2],
        0.05,
    ),
    (
        np.array([1234, 1235, 1236, 1237, 1238, 1239,
                  1240, 1241, np.nan]),  # Missing t value
        np.array([1, 2, 3, 4, 5, 5.5, 6, 6.5, 7]),
        2,
        [2],
        0.05,
    ),
    (
        np.array([1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242]),
        np.array([1, 2, 3, 4, 5, 5.5, 6, 6.5, np.nan]),  # Missing y value
        2,
        [2],
        0.05,
    )
])
def test_AssertionErrors(t, y, to_exclude, poly_features, alpha):
    with pytest.raises(AssertionError):
        check_tolerance(t, y, to_exclude=to_exclude,
                        poly_features=poly_features, alpha=alpha)
