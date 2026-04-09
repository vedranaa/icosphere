import pytest

import icosphere


@pytest.mark.parametrize("nu", [1, 2, 3, 5, 10])
def test_icosphere(nu):
    vertices, faces = icosphere.icosphere(nu)
    # Smoke test: ensure outputs are not empty.
    assert vertices.shape
    assert faces.shape
