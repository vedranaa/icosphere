import pytest

import icosphere


@pytest.mark.parametrize("nu", [1, 2, 3, 5, 10])
def test_icosphere(nu):
    sv, sf = icosphere.icosphere(nu)
    # Just a smoke test for now...
    assert sv.shape
    assert sf.shape
