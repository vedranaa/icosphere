import icosphere
import unittest


class TestIcosphere(unittest.TestCase):

    def test_smoke(self):
        for nu in [1, 2, 3, 5, 10]:
            vertices, faces = icosphere.icosphere(nu)
            # Smoke test: ensure outputs are not empty.
            self.assertTrue(vertices.shape)
            self.assertTrue(faces.shape)


if __name__ == "__main__":
    unittest.main()
